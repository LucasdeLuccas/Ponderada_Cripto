from flask import Flask, request, jsonify, Response, stream_with_context
import joblib
import pandas as pd
import yfinance as yf
from utils import calculate_RSI, calculate_MACD
from flask_cors import CORS
from datetime import datetime, timedelta
import os
import logging
from logging.handlers import RotatingFileHandler
import time

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})  # Para desenvolvimento; restrinja em produção

# Configurar Logging
if not os.path.exists('logs'):
    os.mkdir('logs')
file_handler = RotatingFileHandler('logs/app.log', maxBytes=10*1024*1024, backupCount=5)
file_handler.setFormatter(logging.Formatter(
    '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
))
file_handler.setLevel(logging.INFO)
app.logger.addHandler(file_handler)

app.logger.setLevel(logging.INFO)
app.logger.info('CryptoPredictor startup')

# Definir os símbolos dos criptoativos
symbols = {
    'BNB': 'BNB-USD',
    'Solana': 'SOL-USD',
    'Ethereum': 'ETH-USD',
    'Bitcoin': 'BTC-USD',
    'Dogecoin': 'DOGE-USD'
}

# Carregar modelos
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
models = {}
for asset in symbols.keys():
    model_path = os.path.join(BASE_DIR, 'models', f'{asset}_model.pkl')
    try:
        models[asset] = joblib.load(model_path)
        app.logger.info(f"Modelo para {asset} carregado com sucesso.")
    except FileNotFoundError:
        app.logger.error(f"Modelo para {asset} não encontrado em {model_path}.")

# Definir as features utilizadas
features = ['Close', 'MA10', 'MA50', 'MA100', 'Daily Return', 'Volatility', 'RSI', 'MACD']

@app.route('/predict', methods=['GET'])
def predict():
    asset = request.args.get('asset')
    date_str = request.args.get('date')  # Recebe a data no formato 'YYYY-MM-DD'

    app.logger.info(f"Recebida requisição de previsão: asset={asset}, date={date_str}")

    if not asset or asset not in models:
        app.logger.warning("Asset não suportado ou não fornecido.")
        return jsonify({'error': 'Asset não suportado ou não fornecido.'}), 400

    # Validar e converter a data
    try:
        date = datetime.strptime(date_str, '%Y-%m-%d')
    except (ValueError, TypeError):
        app.logger.warning("Data inválida ou não fornecida.")
        return jsonify({'error': 'Data inválida ou não fornecida. Use o formato YYYY-MM-DD.'}), 400

    # Definir o período para baixar dados (500 dias antes da data selecionada)
    start_date = date - timedelta(days=500)
    end_date = date

    # Baixar dados históricos
    try:
        data = yf.download(tickers=symbols[asset], start=start_date.strftime('%Y-%m-%d'), end=end_date.strftime('%Y-%m-%d'))
        app.logger.info(f"Dados baixados para {asset} de {start_date.date()} até {end_date.date()}.")
    except Exception as e:
        app.logger.error(f"Erro ao baixar dados: {e}")
        return jsonify({'error': 'Erro ao baixar dados históricos.'}), 500

    if data.empty:
        app.logger.warning("Nenhum dado disponível para o asset e data fornecidos.")
        return jsonify({'error': 'Nenhum dado disponível para o asset e data fornecidos.'}), 400

    # Pré-processamento
    df = data.copy()
    df['MA10'] = df['Close'].rolling(window=10).mean()
    df['MA50'] = df['Close'].rolling(window=50).mean()
    df['MA100'] = df['Close'].rolling(window=100).mean()
    df['Daily Return'] = df['Close'].pct_change()
    df['Volatility'] = df['Close'].rolling(window=10).std()
    df['RSI'] = calculate_RSI(df['Close'])
    df['MACD'], df['MACD Signal'] = calculate_MACD(df['Close'])
    df.dropna(inplace=True)

    # Garantir que a data selecionada está no índice
    available_dates = df.index.strftime('%Y-%m-%d').tolist()
    if date_str not in available_dates:
        # Usar a data mais próxima anterior disponível
        df_filtered = df[df.index <= date]
        if df_filtered.empty:
            app.logger.warning("Nenhum dado disponível para a data selecionada.")
            return jsonify({'error': 'Nenhum dado disponível para a data selecionada.'}), 400
        selected_row = df_filtered.iloc[-1]
        selected_date = df_filtered.index[-1].strftime('%Y-%m-%d')
    else:
        selected_row = df.loc[date_str]
        selected_date = date_str

    # Preparar os dados para previsão
    X = selected_row[features].values.reshape(1, -1)

    # Fazer a previsão
    try:
        model = models[asset]
        prediction = model.predict(X)[0]
        app.logger.info(f"Previsão feita para {asset} em {selected_date}: {prediction}")
    except Exception as e:
        app.logger.error(f"Erro na previsão: {e}")
        return jsonify({'error': 'Erro ao fazer a previsão.'}), 500

    # Gerar sinal
    current_price = selected_row['Close']
    signal = 'Buy' if prediction > current_price else 'Sell'
    app.logger.info(f"Sinal gerado: {signal}")

    # Preparar dados para o gráfico (últimos 30 dias até a data selecionada)
    graph_df = df.loc[:selected_date].tail(30)
    graph_data = {
        'dates': graph_df.index.strftime('%Y-%m-%d').tolist(),
        'prices': graph_df['Close'].tolist(),
        'asset': asset,
    }

    response = {
        'asset': asset,
        'date': selected_date,
        'prediction': prediction,
        'current_price': current_price,
        'signal': signal,
        'features': selected_row[features].to_dict(),
        'graphData': graph_data,
    }

    app.logger.info("Resposta de previsão enviada ao frontend.")
    return jsonify(response)

@app.route('/logs', methods=['GET'])
def stream_logs():
    def generate():
        with open('logs/app.log', 'r') as f:
            # Move o cursor para o final do arquivo
            f.seek(0, os.SEEK_END)
            while True:
                line = f.readline()
                if not line:
                    time.sleep(0.5)
                    continue
                yield f"data: {line}\n\n"
    return Response(stream_with_context(generate()), mimetype='text/event-stream')

@app.route('/', methods=['GET'])
def home():
    return jsonify({'message': 'CryptoPredictor Backend está funcionando! Use o endpoint /predict.'}), 200

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')