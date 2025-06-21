FROM python:3.13-slim

RUN apt-get update && \
    apt-get install -y chromium chromium-driver fonts-liberation libnss3 libatk-bridge2.0-0 libgtk-3-0 libxss1 libasound2 libgbm1 libxshmfence1 && \
    rm -rf /var/lib/apt/lists/*

ENV PYPPETEER_CHROMIUM_REVISION="" \
    PYPPETEER_EXECUTABLE_PATH="/usr/bin/chromium"

WORKDIR /app
COPY ./app/ /app/
COPY requirements.txt /app/

RUN pip install --no-cache-dir -r requirements.txt

RUN mkdir -p /profile

# instale o cron
RUN apt-get update && apt-get install -y cron

# Copie o crontab para o local padrão do sistema
COPY app/etc/crontab /etc/crontab

# Dê permissão de execução
RUN chmod 0644 /etc/crontab

#entrypoint para o container
COPY app/entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

#entrypoint como comando principal
# CMD ["/usr/sbin/cron", "-f"]
CMD ["/entrypoint.sh"]
# CMD ["python", "main.py"]