# Usar uma imagem base oficial do Python
FROM python:3.10-slim

# Definir variáveis de ambiente
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Definir o diretório de trabalho no contêiner
WORKDIR /app

# Instalar dependências do sistema
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copiar o arquivo de requisitos para o diretório de trabalho
COPY requirements.txt .

# Instalar dependências Python
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Copiar todo o código do backend para o diretório de trabalho
COPY . .

# Expor a porta que o Flask usará
EXPOSE 5000

# Definir a variável de ambiente para o Flask
ENV FLASK_APP=app.py

# Comando para iniciar o Flask
CMD ["flask", "run", "--host=0.0.0.0"]
