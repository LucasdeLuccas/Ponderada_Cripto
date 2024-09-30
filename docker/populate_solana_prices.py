import requests
import datetime
from sqlalchemy import create_engine, Column, Date, Numeric, BigInteger
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

# Configurações do Banco de Dados
DATABASE_URL = f"postgresql://{os.getenv('DATABASE_USER')}:{os.getenv('DATABASE_PASSWORD')}@{os.getenv('DATABASE_HOST')}/{os.getenv('DATABASE_NAME')}"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Definição do Modelo
class SolanaPrice(Base):
    __tablename__ = "solana_price"
    date = Column(Date, primary_key=True, index=True)
    open = Column(Numeric)
    high = Column(Numeric)
    low = Column(Numeric)
    close = Column(Numeric)
    volume = Column(BigInteger)

def fetch_historical_data(start_date, end_date):
    """
    Busca dados históricos da Solana (SOL) usando a API da CoinGecko.
    """
    url = f"https://api.coingecko.com/api/v3/coins/solana/market_chart/range"
    # Convertendo datas para timestamps UNIX
    start_timestamp = int(datetime.datetime.strptime(start_date, "%Y-%m-%d").timestamp())
    end_timestamp = int(datetime.datetime.strptime(end_date, "%Y-%m-%d").timestamp())
    params = {
        'vs_currency': 'usd',
        'from': start_timestamp,
        'to': end_timestamp
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Erro ao buscar dados: {response.status_code} - {response.text}")

def process_data(data):
    """
    Processa os dados recebidos da API para extrair informações diárias.
    """
    prices = data.get('prices', [])
    volumes = data.get('total_volumes', [])

    processed_data = {}
    for price in prices:
        date = datetime.datetime.fromtimestamp(price[0]/1000).date()
        processed_data.setdefault(date, {'open': price[1], 'high': price[1], 'low': price[1], 'close': price[1]})

    for price in prices:
        date = datetime.datetime.fromtimestamp(price[0]/1000).date()
        processed_data[date]['close'] = price[1]
        if price[1] > processed_data[date]['high']:
            processed_data[date]['high'] = price[1]
        if price[1] < processed_data[date]['low']:
            processed_data[date]['low'] = price[1]

    for volume in volumes:
        date = datetime.datetime.fromtimestamp(volume[0]/1000).date()
        if date in processed_data:
            processed_data[date]['volume'] = int(volume[1])
        else:
            processed_data[date] = {'open': volume[1], 'high': volume[1], 'low': volume[1], 'close': volume[1], 'volume': int(volume[1])}

    return processed_data

def insert_data(session, data):
    """
    Insere os dados processados no banco de dados.
    """
    for date, values in data.items():
        # Verifica se o registro já existe
        existing = session.query(SolanaPrice).filter(SolanaPrice.date == date).first()
        if not existing:
            solana_price = SolanaPrice(
                date=date,
                open=values.get('open'),
                high=values.get('high'),
                low=values.get('low'),
                close=values.get('close'),
                volume=values.get('volume', 0)
            )
            session.add(solana_price)
    session.commit()

def main():
    # Definir o intervalo de datas
    today = datetime.date.today()
    start_date = datetime.date(2020, 1, 1)  # Data inicial, ajuste conforme necessário
    end_date = today

    print(f"Buscando dados de {start_date} até {end_date}...")

    try:
        raw_data = fetch_historical_data(start_date.strftime("%Y-%m-%d"), end_date.strftime("%Y-%m-%d"))
        processed_data = process_data(raw_data)
        session = SessionLocal()
        insert_data(session, processed_data)
        print("Dados inseridos com sucesso!")
    except Exception as e:
        print(f"Erro: {e}")

if __name__ == "__main__":
    main()

