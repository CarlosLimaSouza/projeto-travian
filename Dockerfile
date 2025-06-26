FROM python:3.13-slim

RUN apt-get update && \
    apt-get install -y chromium chromium-driver fonts-liberation libnss3 libatk-bridge2.0-0 libgtk-3-0 libxss1 libasound2 libgbm1 libxshmfence1 && \
    rm -rf /var/lib/apt/lists/*

ENV PYPPETEER_CHROMIUM_REVISION="" \
    PYPPETEER_EXECUTABLE_PATH="/usr/bin/chromium"

WORKDIR /app  
COPY . /app   

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8000

CMD ["sh", "-c", "hypercorn main:app --bind 0.0.0.0:${PORT:-8000}"]
