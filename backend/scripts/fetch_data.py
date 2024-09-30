import os
import logging
import pandas as pd
import yfinance as yf
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models import SolanaPrice, Base
from app.database import DATABASE_URL
from datetime import datetime

# Configurar logging
log_path = os.path.join(os.path.dirname(__file__), '../logs/api.log')
logging.basicConfig(
    filename=log_path,
    level=logging.INFO,
    format='%(asctime)s %(levelname)s:%(message)s'
)

def fetch_data():
    try:
        logging.info("Iniciando a coleta de dados da Solana.")
        sol = yf.Ticker("SOL-USD")
        hist = sol.history(period="5y")
        hist.reset_index(inplace=True)
        hist = hist[['Date', 'Open', 'High', 'Low', 'Close', 'Volume']]
        hist.rename(columns={'Date': 'date', 'Open': 'open', 'High': 'high',
                            'Low': 'low', 'Close': 'close', 'Volume': 'volume'}, inplace=True)
        
        # Conectar ao banco de dados
        engine = create_engine(DATABASE_URL)
        SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
        session = SessionLocal()
        
        # Criar tabelas se não existirem
        Base.metadata.create_all(bind=engine)
        
        # Inserir dados no banco
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
        session.close()
        logging.info("Coleta e inserção de dados concluídas com sucesso.")
    except Exception as e:
        logging.error(f"Erro ao coletar dados: {e}")

if __name__ == "__main__":
    fetch_data()
