from flask import Flask, jsonify
from flask_cors import CORS
import yfinance as yf
import pandas as pd
import joblib
from datetime import datetime, timedelta

app = Flask(__name__)
CORS(app)

# Carregar o modelo treinado
model = joblib.load('solana_model.joblib')

def get_solana_data(days=5):
    end_date = datetime.now()
    start_date = end_date - timedelta(days=days)
    solana = yf.Ticker("SOL-USD")
    df = solana.history(start=start_date, end=end_date)
    return df

def prepare_data(df):
    df['Returns'] = df['Close'].pct_change()
    df['SMA5'] = df['Close'].rolling(window=5).mean()
    df['SMA20'] = df['Close'].rolling(window=20).mean()
    df['RSI'] = calculate_rsi(df['Close'], window=14)
    return df.dropna()

def calculate_rsi(data, window=14):
    delta = data.diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=window).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=window).mean()
    rs = gain / loss
    return 100 - (100 / (1 + rs))

@app.route('/predict', methods=['GET'])
def predict():
    df = get_solana_data()
    prepared_data = prepare_data(df)
    
    if prepared_data.empty:
        return jsonify({"error": "Não foi possível obter dados suficientes para fazer uma previsão"}), 400
    
    latest_data = prepared_data.iloc[-1]
    X = latest_data[['Returns', 'SMA5', 'SMA20', 'RSI']].values.reshape(1, -1)
    prediction = model.predict(X)[0]
    probability = model.predict_proba(X)[0]
    
    historical_prices = df['Close'].tolist()
    historical_dates = [date.strftime('%Y-%m-%d') for date in df.index]
    
    result = {
        "prediction": "Comprar" if prediction == 1 else "Vender",
        "confidence": float(probability.max()),
        "current_price": float(latest_data['Close']),
        "last_update": latest_data.name.isoformat(),
        "historical_data": {
            "dates": historical_dates,
            "prices": historical_prices
        }
    }
    
    return jsonify(result)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)