# Usa uma imagem base Python slim
FROM python:3.13-slim

# Instala as dependências do sistema para o Chromium
RUN apt-get update && \
    apt-get install -y chromium fonts-liberation libnss3 libatk-bridge2.0-0 libgtk-3-0 libxss1 libasound2 libgbm1 libxshmfence1 && \
    rm -rf /var/lib/apt/lists/*

# Configura as variáveis de ambiente para o Pyppeteer encontrar o Chromium instalado pelo sistema
ENV PYPPETEER_CHROMIUM_REVISION="" \
    PYPPETEER_EXECUTABLE_PATH="/usr/bin/chromium"

# Define o diretório de trabalho dentro do container
WORKDIR /app

# Copia os arquivos do projeto para o diretório de trabalho
# COPY . . é mais idiomático aqui, pois copia para o WORKDIR atual (/app)
COPY . .

# Instala as dependências Python a partir do requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Expõe a porta que o Railway irá mapear
EXPOSE 8000

# Define o comando para iniciar a aplicação
# Usa o formato exec e a variável de ambiente HYPERCORN_BIND
CMD ["hypercorn", "main:app"]