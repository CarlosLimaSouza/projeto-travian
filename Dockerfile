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

# Copia o CONTEÚDO da sua pasta local 'app' para o WORKDIR do container (/app)
COPY app/ .

# Instala as dependências Python a partir do requirements.txt que agora está em /app/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Expõe a porta que a aplicação vai usar internamente.
# Nota: O Railway ignora este valor e usa o que está em $PORT, mas é uma boa prática.
EXPOSE 8080

# --- MUDANÇA PRINCIPAL AQUI ---
# Comando Antigo:
# CMD uvicorn main:app --host 0.0.0.0 --port $PORT

# Comando NOVO e CORRIGIDO:
# Adiciona --proxy-headers para que o Uvicorn confie nos cabeçalhos do proxy do Railway (X-Forwarded-Proto, etc.)
# Adiciona --forwarded-allow-ips='*' para aceitar esses cabeçalhos de qualquer IP de proxy (necessário no Railway).
CMD uvicorn main:app --host 0.0.0.0 --port $PORT --proxy-headers --forwarded-allow-ips='*'