# Imagem base do Python
FROM python:3.10-slim

# Define diretório de trabalho dentro do container
WORKDIR /app

# Copia todos os arquivos da pasta local para dentro do container
COPY . .

# Atualiza o pip e instala as dependências
RUN pip install --upgrade pip \
    && pip install -r requirements.txt

# Comando padrão ao iniciar o container
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8002"]
