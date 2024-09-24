from flask import Flask, request, jsonify
import joblib
import pandas as pd
import yfinance as yf
from utils import calculate_RSI, calculate_MACD
from flask_cors import CORS
from datetime import datetime, timedelta
import os

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})  

# Obter o caminho absoluto do diretório atual
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

symbols = {
    'BNB': 'BNB-USD',
    'Solana': 'SOL-USD',
    'Ethereum': 'ETH-USD',
    'Bitcoin': 'BTC-USD',
    'Dogecoin': 'DOGE-USD'
}

# Carregar modelos com caminhos absolutos
models = {}
try:
    models['Bitcoin'] = joblib.load(os.path.join(BASE_DIR, 'models/Bitcoin_model.pkl'))
    models['Ethereum'] = joblib.load(os.path.join(BASE_DIR, 'models/Ethereum_model.pkl'))
    models['BNB'] = joblib.load(os.path.join(BASE_DIR, 'models/BNB_model.pkl'))
    models['Solana'] = joblib.load(os.path.join(BASE_DIR, 'models/Solana_model.pkl'))
    models['Dogecoin'] = joblib.load(os.path.join(BASE_DIR, 'models/Dogecoin_model.pkl'))
    print("Modelos carregados com sucesso.")
except FileNotFoundError as e:
    print(f"Erro ao carregar modelo: {e}")
    exit(1)

# Definir as features utilizadas
features = ['Close', 'MA10', 'MA50', 'MA100', 'Daily Return', 'Volatility', 'RSI', 'MACD']

@app.route('/', methods=['GET'])
def home():
    return jsonify({'message': 'CryptoPredictor Backend está funcionando! Use o endpoint /predict.'}), 200

@app.route('/predict', methods=['GET'])
def predict():
    asset = request.args.get('asset')  # Exemplo: 'Bitcoin'
    date = request.args.get('date')    # Data no formato 'YYYY-MM-DD' (opcional)

    print(f"Recebido asset: {asset}, date: {date}")

    if asset not in models:
        print(f"Asset não suportado: {asset}")
        return jsonify({'error': 'Asset not supported'}), 400

    # Usar a data atual se nenhuma data for fornecida
    if not date:
        date = datetime.utcnow().strftime('%Y-%m-%d')
        print(f"Data não fornecida. Usando data atual: {date}")

    # Calcular datas de início e fim
    end_date = datetime.today()
    start_date = end_date - timedelta(days=500)
    start_str = start_date.strftime('%Y-%m-%d')
    end_str = end_date.strftime('%Y-%m-%d')
    print(f"Baixando dados para {asset} de {start_str} até {end_str}")

    # Obter dados históricos (últimos 500 dias)
    data = yf.download(tickers=symbols[asset], start=start_str, end=end_str)
    if data.empty:
        print(f'Nenhum dado disponível para {asset}.')
        return jsonify({'error': 'No data available for the asset'}), 400

    # Garantir que a data esteja no índice dos dados
    available_dates = data.index.strftime('%Y-%m-%d').tolist()
    print(f"Datas disponíveis (últimas 5): {available_dates[-5:]}")  # Mostrar as últimas 5 datas
    if date not in available_dates:
        # Usar a data mais recente disponível
        date = available_dates[-1]
        print(f"Data solicitada não disponível. Usando data mais recente: {date}")

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

    print(f"Pré-processamento concluído. Dados disponíveis para {date}.")

    # Selecionar a data específica
    try:
        X = df.loc[date, features]
        print(f"Features selecionadas para {date}: {X.to_dict()}")
    except KeyError:
        print(f'Data não disponível após o processamento: {date}')
        return jsonify({'error': 'Data not available after processing'}), 400

    # Converter para DataFrame se necessário
    if isinstance(X, pd.Series):
        X = X.to_frame().T

    # Fazer a previsão
    model = models[asset]
    prediction = model.predict(X)[0]
    print(f"Previsão: {prediction}")

    # Gerar sinal
    current_price = X['Close'].values[0]
    signal = 1 if prediction > current_price else -1
    print(f"Preço atual: {current_price}, Sinal: {'Buy' if signal == 1 else 'Sell'}")

    response = {
        'asset': asset,
        'date': date,
        'prediction': prediction,
        'current_price': current_price,
        'signal': 'Buy' if signal == 1 else 'Sell',
        'features': X.to_dict(orient='records')[0],
        'graphData': {
            'dates': df.index.strftime('%Y-%m-%d').tolist(),
            'prices': df['Close'].tolist(),
            'asset': asset,
        },
    }

    return jsonify(response)

if __name__ == '__main__':
    app.run(debug=True)
