from sqlalchemy.orm import Session
from . import models
from datetime import date  # Certifique-se de que está importado

def get_price_by_date(db: Session, price_date: date):
    return db.query(models.SolanaPrice).filter(models.SolanaPrice.date == price_date).first()
