from pydantic import BaseModel
from typing import Optional

class PredictionRequest(BaseModel):
    date: str  # Formato 'YYYY-MM-DD'

class PredictionResponse(BaseModel):
    date: str
    prediction: str
    plot: str  # Gráfico em base64
