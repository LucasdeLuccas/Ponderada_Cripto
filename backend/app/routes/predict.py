from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import crud, models, schemas
from app.database import SessionLocal, engine
import joblib
from datetime import datetime
import base64
import matplotlib.pyplot as plt
import io

router = APIRouter()

# Carregar o modelo treinado
model = joblib.load('models/solana_rf_model.joblib')

# Dependência para obter a sessão do banco de dados
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/predict/", response_model=schemas.PredictionResponse)
def create_prediction(prediction_request: schemas.PredictionRequest, db: Session = Depends(get_db)):
    try:
        # Converter a string da data para objeto datetime
        purchase_date = datetime.strptime(prediction_request.date, "%Y-%m-%d").date()

        # Obter os dados do banco para a data selecionada
        solana_price = crud.get_price_by_date(db, price_date=purchase_date)
        if not solana_price:
            raise HTTPException(status_code=404, detail="Data não encontrada no banco de dados.")

        # Preparar os dados para o modelo (exemplo: usar preços anteriores)
        # Isso depende de como o seu modelo foi treinado
        # Supondo que você tenha uma função para preparar os dados
        input_features = prepare_features(db, purchase_date)

        # Fazer a previsão
        prediction = model.predict([input_features])[0]

        # Interpretar a previsão
        if prediction == 1:
            recommendation = "Comprar"
        elif prediction == -1:
            recommendation = "Vender"
        else:
            recommendation = "Manter"

        # Gerar o gráfico de previsão
        fig, ax = plt.subplots()
        ax.plot([solana_price.date, solana_price.date], [solana_price.close, solana_price.close * 1.1], label='Previsão de Alta')
        ax.plot([solana_price.date, solana_price.date], [solana_price.close, solana_price.close * 0.9], label='Previsão de Queda')
        ax.set_xlabel('Data')
        ax.set_ylabel('Preço de Fechamento')
        ax.set_title('Previsão de Preço da Solana')
        ax.legend()

        # Converter o gráfico para base64
        buf = io.BytesIO()
        plt.savefig(buf, format='png')
        buf.seek(0)
        image_base64 = base64.b64encode(buf.read()).decode('utf-8')
        plt.close(fig)

        return schemas.PredictionResponse(
            date=str(purchase_date),
            prediction=recommendation,
            plot=image_base64
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

def prepare_features(db: Session, purchase_date: datetime.date):
    
    prices = db.query(models.SolanaPrice).filter(models.SolanaPrice.date <= purchase_date).order_by(models.SolanaPrice.date.desc()).limit(10).all()
    if len(prices) < 10:
        raise HTTPException(status_code=400, detail="Dados insuficientes para a data selecionada.")
    feature = [price.close for price in prices]
    return feature

model = joblib.load('models/solana_rf_model.joblib')

