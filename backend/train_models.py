import os
import pandas as pd
import yfinance as yf
from sklearn.linear_model import LinearRegression
import joblib
from utils import calculate_RSI, calculate_MACD

# Definir os símbolos dos criptoativos
symbols = {
    'BNB': 'BNB-USD',
    'Solana': 'SOL-USD',
    'Ethereum': 'ETH-USD',
    'Bitcoin': 'BTC-USD',
    'Dogecoin': 'DOGE-USD'
}

# Definir as features utilizadas
features = ['Close', 'MA10', 'MA50', 'MA100', 'Daily Return', 'Volatility', 'RSI', 'MACD']

# Garantir que a pasta 'models' exista
if not os.path.exists('models'):
    os.makedirs('models')

for asset_name, ticker in symbols.items():
    print(f'Treinando modelo para {asset_name}...')
    
    # Baixar dados históricos (últimos 500 dias para ter mais dados)
    data = yf.download(tickers=ticker, period='500d')
    
    if data.empty:
        print(f'Não foi possível baixar dados para {asset_name}.')
        continue
    
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
    
    # Definir X e y
    X = df[features]
    y = df['Close'].shift(-1).dropna()  # Prever o próximo fechamento
    X = X[:-1]  # Remover a última linha que não tem y correspondente
    
    # Treinar o modelo
    model = LinearRegression()
    model.fit(X, y)
    
    # Salvar o modelo
    model_filename = f'models/{asset_name}_model.pkl'
    joblib.dump(model, model_filename)
    print(f'Modelo para {asset_name} salvo como {model_filename}.\n')
