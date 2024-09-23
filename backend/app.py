from flask import Flask, request, jsonify
import joblib
import pandas as pd
import yfinance as yf
from utils import calculate_RSI, calculate_MACD
from flask_cors import CORS
from datetime import datetime, timedelta

app = Flask(__name__)
CORS(app)

# Definir os símbolos dos criptoativos
symbols = {
    'BNB': 'BNB-USD',
    'Solana': 'SOL-USD',
    'Ethereum': 'ETH-USD',
    'Bitcoin': 'BTC-USD',
    'Dogecoin': 'DOGE-USD'
}

# Carregar modelos
models = {
    'Bitcoin': joblib.load('models/BTC_model.pkl'),
    'Ethereum': joblib.load('models/ETH_model.pkl'),
    'BNB': joblib.load('models/BNB_model.pkl'),
    'Solana': joblib.load('models/Solana_model.pkl'),
    'Dogecoin': joblib.load('models/Dogecoin_model.pkl')
}

# Definir as features utilizadas
features = ['Close', 'MA10', 'MA50', 'MA100', 'Daily Return', 'Volatility', 'RSI', 'MACD']

@app.route('/predict', methods=['GET'])
def predict():
    asset = request.args.get('asset')  # Exemplo: 'Bitcoin'
    date = request.args.get('date')    # Data no formato 'YYYY-MM-DD' (opcional)

    if asset not in models:
        return jsonify({'error': 'Asset not supported'}), 400

    # Usar a data atual se nenhuma data for fornecida
    if not date:
        date = datetime.utcnow().strftime('%Y-%m-%d')

    # Obter dados históricos (últimos 200 dias)
    data = yf.download(tickers=symbols[asset], period='200d')
    if data.empty:
        return jsonify({'error': 'No data available for the asset'}), 400

    # Garantir que a data esteja no índice dos dados
    available_dates = data.index.strftime('%Y-%m-%d').tolist()
    if date not in available_dates:
        # Usar a data mais recente disponível
        date = available_dates[-1]

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

    # Selecionar a data específica
    try:
        X = df.loc[date, features]
    except KeyError:
        return jsonify({'error': 'Data not available after processing'}), 400

    # Converter para DataFrame se necessário
    if isinstance(X, pd.Series):
        X = X.to_frame().T

    # Fazer a previsão
    model = models[asset]
    prediction = model.predict(X)[0]

    # Gerar sinal
    current_price = X['Close'].values[0]
    signal = 1 if prediction > current_price else -1

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
