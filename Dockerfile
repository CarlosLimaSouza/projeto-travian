# Usa uma imagem base Python slim e estável
FROM python:3.13-slim

# Define variáveis de ambiente que podem ser usadas durante o build
# PYTHONUNBUFFERED garante que os logs apareçam em tempo real
ENV PYTHONUNBUFFERED=1 \
    PYPPETEER_CHROMIUM_REVISION="" \
    PYPPETEER_EXECUTABLE_PATH="/usr/bin/chromium"

# Instala as dependências do sistema para o Chromium
RUN apt-get update && \
    apt-get install -y chromium fonts-liberation libnss3 libatk-bridge2.0-0 libgtk-3-0 libxss1 libasound2 libgbm1 libxshmfence1 && \
    rm -rf /var/lib/apt/lists/*

# Define o diretório de trabalho dentro do container
WORKDIR /

# Copia primeiro o arquivo de requisitos para aproveitar o cache do Docker
COPY requirements.txt .

# Instala as dependências Python
RUN pip install --no-cache-dir -r requirements.txt

# Copia o resto dos arquivos do projeto para o diretório de trabalho
# O ponto de origem '.' é a raiz do seu projeto
# O ponto de destino '.' é o WORKDIR atual (/app)
COPY . .

# Expõe a porta que a aplicação vai usar internamente
EXPOSE 8080

# Define o comando para iniciar a aplicação
# - "uvicorn": O executável
# - "app.main:app": O caminho do módulo (PACOTE.ARQUIVO:OBJETO)
# - "--host", "0.0.0.0": Escuta em todas as interfaces de rede
# - "--port", "8080": Usa a porta 8080
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080"]