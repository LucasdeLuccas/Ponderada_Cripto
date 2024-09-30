from sqlalchemy import Column, Integer, Float, Date
from .database import Base

class SolanaPrice(Base):
    __tablename__ = 'solana_prices'
    id = Column(Integer, primary_key=True, index=True)
    date = Column(Date, unique=True, index=True)
    open = Column(Float)
    high = Column(Float)
    low = Column(Float)
    close = Column(Float)
    volume = Column(Float)
