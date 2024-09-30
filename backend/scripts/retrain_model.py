import os
import sys
import pandas as pd
import numpy as np
import yfinance as yf
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models import SolanaPrice, Base
from app.database import DATABASE_URL
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, accuracy_score
import joblib
import matplotlib.pyplot as plt
import seaborn as sns

# Configurar logging se necessário

# Conectar ao banco de dados
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base.metadata.create_all(bind=engine)
session = SessionLocal()

# Obter dados históricos
sol = yf.Ticker("SOL-USD")
hist = sol.history(period="5y")
hist.reset_index(inplace=True)
hist = hist[['Date', 'Open', 'High', 'Low', 'Close', 'Volume']]
hist.rename(columns={'Date': 'date', 'Open': 'open', 'High': 'high',
                    'Low': 'low', 'Close': 'close', 'Volume': 'volume'}, inplace=True)

# Inserir dados no banco de dados
for _, row in hist.iterrows():
    existing = session.query(SolanaPrice).filter(SolanaPrice.date == row['date']).first()
    if not existing:
        price = SolanaPrice(
            date=row['date'],
            open=row['open'],
            high=row['high'],
            low=row['low'],
            close=row['close'],
            volume=row['volume']
        )
        session.add(price)
session.commit()

# Carregar dados do banco
data = session.query(SolanaPrice).order_by(SolanaPrice.date).all()
session.close()

df = pd.DataFrame([{
    'date': record.date,
    'open': record.open,
    'high': record.high,
    'low': record.low,
    'close': record.close,
    'volume': record.volume
} for record in data])

# Engenharia de Features
df['price_change'] = df['close'].pct_change()
df['moving_avg_5'] = df['close'].rolling(window=5).mean()
df['moving_avg_10'] = df['close'].rolling(window=10).mean()
df['volatility'] = df['close'].rolling(window=10).std()
df['target'] = np.where(df['price_change'].shift(-1) > 0, 1, 0)  # 1: Comprar, 0: Vender
df.dropna(inplace=True)

# Preparação dos Dados
features = ['open', 'high', 'low', 'close', 'volume', 'moving_avg_5', 'moving_avg_10', 'volatility']
X = df[features]
y = df['target']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Treinamento do Modelo
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Avaliação
y_pred = model.predict(X_test)
print("Acurácia:", accuracy_score(y_test, y_pred))
print(classification_report(y_test, y_pred))

# Salvar o Modelo
joblib.dump(model, 'models/solana_rf_model.joblib')

# (Opcional) Visualização das Previsões
df['prediction'] = model.predict(X)

plt.figure(figsize=(14,7))
sns.lineplot(x='date', y='close', data=df, label='Preço de Fechamento')
sns.scatterplot(x='date', y='close', hue='prediction', palette='coolwarm', label='Sinal de Compra/Venda', alpha=0.5)
plt.title('Previsões de Compra/Venda para Solana')
plt.xlabel('Data')
plt.ylabel('Preço (USD)')
plt.legend()
plt.show()
