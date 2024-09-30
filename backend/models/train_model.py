import pandas as pd
import numpy as np
import yfinance as yf
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
import joblib

def get_solana_data(period="1y"):
    solana = yf.Ticker("SOL-USD")
    df = solana.history(period=period)
    return df

def calculate_rsi(data, window=14):
    delta = data.diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=window).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=window).mean()
    rs = gain / loss
    return 100 - (100 / (1 + rs))

def prepare_data(df):
    df['Returns'] = df['Close'].pct_change()
    df['Target'] = np.where(df['Returns'].shift(-1) > 0, 1, 0)
    df['SMA5'] = df['Close'].rolling(window=5).mean()
    df['SMA20'] = df['Close'].rolling(window=20).mean()
    df['RSI'] = calculate_rsi(df['Close'])
    return df.dropna()

def train_model():
    # Obter dados
    df = get_solana_data()
    
    # Preparar dados
    df = prepare_data(df)
    
    # Separar features e target
    X = df[['Returns', 'SMA5', 'SMA20', 'RSI']]
    y = df['Target']
    
    # Dividir em conjunto de treino e teste
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # Treinar o modelo
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)
    
    # Avaliar o modelo
    y_pred = model.predict(X_test)
    print(f"Acurácia: {accuracy_score(y_test, y_pred)}")
    print(classification_report(y_test, y_pred))
    
    # Salvar o modelo
    joblib.dump(model, 'solana_model.joblib')
    print("Modelo treinado e salvo como 'solana_model.joblib'")

if __name__ == "__main__":
    train_model()