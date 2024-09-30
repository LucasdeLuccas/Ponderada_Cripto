# Solana Predictor - Ponderada_Cripto

![Solana Logo](frontend/public/images/solana.png)


## ❌ Por Que Não Utilizamos DataLake?

Optamos por não utilizar uma solução de DataLake neste projeto devido à complexidade adicional e ao escopo atual da aplicação. Nosso foco principal é fornecer previsões consistentes e armazenar logs de forma eficiente utilizando o PostgreSQL, que atende perfeitamente às necessidades de persistência de dados do projeto. A implementação de um DataLake exigiria uma arquitetura mais robusta e especializada para gerenciamento e análise de grandes volumes de dados, o que, no momento, não se alinha com os objetivos imediatos da aplicação.

## 🐳 Como Utilizamos Docker

O **Docker** foi essencial para garantir a consistência e a facilidade de implantação da aplicação em diferentes ambientes. Utilizamos o **Docker Compose** para orquestrar múltiplos containers, cada um responsável por um serviço específico:

- **solana-backend**: Serviço backend desenvolvido com FastAPI, responsável pela lógica de previsão e interação com o banco de dados.
- **solana-db**: Banco de dados PostgreSQL para armazenar logs e dados relevantes.
- **solana-frontend**: Interface frontend desenvolvida com React, fornecendo uma experiência de usuário intuitiva.

Essa abordagem permite que todas as dependências e configurações sejam encapsuladas nos containers, facilitando a escalabilidade e manutenção do sistema.


## 📈 Visão Geral

O **Solana Predictor** é uma aplicação web interativa que permite aos usuários obter recomendações sobre quando **Comprar**, **Vender** ou **Manter** suas posições em Solana (SOL). Através de uma interface, os usuários podem selecionar uma data e receber uma recomendação personalizada baseada em uma lógica determinística, garantindo consistência nas previsões para a mesma data.

## 🚀 Funcionalidades

- **Previsão de Ações**: Gere recomendações de "Comprar", "Vender" ou "Manter" para Solana (SOL) com base na data selecionada.
- **Logs de Previsões**: Registre e visualize todas as previsões realizadas, mantendo um histórico detalhado das ações recomendadas.
- **Interface Intuitiva**: Utilize uma interface moderna e responsiva desenvolvida com React e React Bootstrap.
- **Consistência nas Previsões**: Garantia de que a mesma data sempre retornará a mesma ação, proporcionando confiabilidade ao usuário.
- **Exportação de Logs**: Opção para exportar o histórico de previsões em formato CSV para análises futuras.

## 🛠 Tecnologias Utilizadas

- **Frontend**: React, React Bootstrap
- **Backend**: FastAPI
- **Banco de Dados**: PostgreSQL
- **Orquestração de Containers**: Docker, Docker Compose
- **API Externa**: CoinGecko (para obtenção de dados históricos de Solana)


## 📚 Guia de Instalação

### 📝 Pré-requisitos

Antes de iniciar, certifique-se de ter os seguintes softwares instalados em sua máquina:

- [Docker](https://www.docker.com/get-started) (inclui Docker Compose)
- [Git](https://git-scm.com/downloads)

### 🔧 Passo a Passo

1. **Clonar o Repositório**

   Abra o terminal e execute:

   ```bash
   git clone https://github.com/LucasdeLuccas/Ponderada_Cripto.git
   cd Ponderada-Cripto/docker
   ```

2. **Inicializar os Containers com Docker Compose**

   No diretório `docker/`, execute:

   ```bash
   docker-compose up --build -d
   ```

   **Explicação dos Comandos:**

   - `up`: Cria e inicia os containers definidos no `docker-compose.yml`.
   - `--build`: Reconstrói as imagens dos serviços antes de iniciar os containers.
   - `-d`: Executa os containers em segundo plano (modo "detached").

3. **Verificar se os Containers Estão Rodando**

   Execute:

   ```bash
   docker-compose ps
   ```

   **Saída Esperada:**

   ```
   NAME              IMAGE             COMMAND                  SERVICE    CREATED          STATUS          PORTS
   solana-backend    docker-backend    "uvicorn app.main:ap…"   backend    X seconds ago    Up X seconds    0.0.0.0:8000->8000/tcp
   solana-db         postgres:14       "docker-entrypoint.s…"   postgres   X seconds ago    Up X seconds    0.0.0.0:5432->5432/tcp
   solana-frontend   docker-frontend   "/docker-entrypoint.…"   frontend   X seconds ago    Up X seconds    0.0.0.0:80->80/tcp
   ```

4. **Acessar a Aplicação**

   -Abra o navegador e vá para [http://localhost](http://localhost).

5. **Explicação dos Comandos:**

   - `up`: Cria e inicia os containers definidos no `docker-compose.yml`.
   - `--build`: Reconstrói as imagens dos serviços antes de iniciar os containers.
   - `-d`: Executa os containers em segundo plano (modo "detached").  

## 📊 Estrutura do Projeto

```
solana-predictor/
├── backend/
│   ├── app/
│   │   ├── main.py
│   │   ├── models.py
│   │   ├── database.py
│   │   └── routes/
│   │       ├── predict.py
│   │       └── log.py
│   ├── scripts/
│   │   ├── populate_solana_prices.py
│   │   └── retrain_model.py
│   ├── Dockerfile
│   └── requirements.txt
├── frontend/
│   ├── public/
│   │   ├── index.html
│   │   └── images/
│   │       └── solana.png
│   ├── src/
│   │   ├── components/
│   │   │   ├── PredictionButton.js
│   └── pages/
│   │       ├── PredictionPage.js
│   │       └── LogsPage.js
│   ├── Dockerfile
│   ├── package.json
│   └── package-lock.json
├── docker/
│   └── docker-compose.yml
└── README.md
```

## 📦 Estrutura de Arquivos Importante

- **backend/**: Contém todo o código relacionado ao backend, incluindo APIs, modelos de dados e scripts para manipulação de dados.
- **frontend/**: Contém o código da interface de usuário desenvolvida com React.
- **docker/**: Inclui o arquivo `docker-compose.yml` que orquestra os containers Docker.
- **README.md**: Documentação do projeto.

## 🧩 Componentes Principais

### **Frontend**

- **React**: Biblioteca JavaScript para construir a interface de usuário.
- **React Bootstrap**: Framework de estilos para garantir uma interface responsiva e moderna.
- **PredictionButton**: Componente responsável por gerar previsões baseadas na data selecionada.
- **LogsPage**: Página que exibe o histórico de previsões realizadas pelo usuário.

### **Backend**

- **FastAPI**: Framework web rápido para construir APIs eficientes.
- **PostgreSQL**: Banco de dados relacional para armazenar logs e dados históricos.
- **Scripts**: Scripts Python para popular o banco de dados com dados históricos e re-treinar modelos de previsão.




 

 
