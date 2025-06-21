#!/bin/bash

# Inicia o cron em background
service cron start

# Roda seu app Python em background (se necessário)
python main.py &

# Mantém o container vivo
tail -f /dev/null