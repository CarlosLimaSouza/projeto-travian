FROM python:3.13-slim

RUN apt-get update && \
    apt-get install -y chromium fonts-liberation libnss3 libatk-bridge2.0-0 libgtk-3-0 libxss1 libasound2 libgbm1 libxshmfence1 && \
    rm -rf /var/lib/apt/lists/*

ENV PYPPETEER_CHROMIUM_REVISION="" \
    PYPPETEER_EXECUTABLE_PATH="/usr/bin/chromium"

WORKDIR /app
COPY . /app

# Adiciona permissão de execução ao nosso script de inicialização
RUN chmod +x ./start.sh

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8080

# Usa o nosso script de inicialização para iniciar a aplicação
CMD ["./start.sh"]