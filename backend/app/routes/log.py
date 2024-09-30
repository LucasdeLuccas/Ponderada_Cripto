from fastapi import APIRouter
from pydantic import BaseModel
import logging
from typing import List
import os

router = APIRouter(
    prefix="/log",
    tags=["Log"]
)

class LogEntry(BaseModel):
    action: str
    date: str
    prediction: str
    timestamp: str

@router.post("/", response_model=dict)
def log_action(entry: LogEntry):
    logging.info(f"Action: {entry.action}, Date: {entry.date}, Prediction: {entry.prediction}")
    return {"status": "logado"}

@router.get("/s/", response_model=dict)
def get_logs():
    log_file_path = os.path.join(os.path.dirname(__file__), '../../logs/api.log')
    if not os.path.exists(log_file_path):
        return {"logs": []}
    
    with open(log_file_path, 'r') as f:
        lines = f.readlines()

    logs = []
    for line in lines:
        try:
            parts = line.strip().split(' ', 3)
            timestamp = ' '.join(parts[:2])
            message = parts[3]
            # Exemplo de mensagem: "Action: predict, Date: 2023-08-01, Prediction: Comprar"
            if "Action: predict" in message:
                msg_parts = message.split(', ')
                action = msg_parts[0].split(': ')[1]
                date = msg_parts[1].split(': ')[1]
                prediction = msg_parts[2].split(': ')[1]
                logs.append({
                    "timestamp": timestamp,
                    "action": action,
                    "date": date,
                    "prediction": prediction
                })
        except IndexError:
            continue  # Ignorar linhas que não seguem o formato esperado

    return {"logs": logs}
