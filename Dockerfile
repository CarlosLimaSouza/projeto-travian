# Usa uma imagem base Python slim e estável
FROM python:3.13-slim

# Define variáveis de ambiente que podem ser usadas durante o build
ENV PYTHONUNBUFFERED=1 \
    PYPPETEER_CHROMIUM_REVISION="" \
    PYPPETEER_EXECUTABLE_PATH="/usr/bin/chromium"

# Instala as dependências do sistema para o Chromium
RUN apt-get update && \
    apt-get install -y chromium fonts-liberation libnss3 libatk-bridge2.0-0 libgtk-3-0 libxss1 libasound2 libgbm1 libxshmfence1 && \
    rm -rf /var/lib/apt/lists/*

# Define o diretório de trabalho dentro do container
WORKDIR /app

# --- A MUDANÇA CRUCIAL ESTÁ AQUI ---
# Copia o CONTEÚDO da sua pasta local 'app' para o WORKDIR do container (/app)
COPY app/ .

# Instala as dependências Python a partir do requirements.txt que agora está em /app/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Expõe a porta que a aplicação vai usar internamente
EXPOSE 8080

# Define o comando para iniciar a aplicação
# Agora, podemos usar "main:app" porque main.py está diretamente em /app
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]