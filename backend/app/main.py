from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routes import predict, log
from .database import engine, Base

# Criar tabelas no banco de dados
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="API de Previsão de Solana",
    description="API para prever sinais de compra ou venda para a criptomoeda Solana.",
    version="1.0.0"
)

# Configurar CORS
origins = [
    "http://localhost",
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(predict.router)
app.include_router(log.router)

@app.get("/")
def read_root():
    return {"message": "API de Previsão de Solana está funcionando!"}
