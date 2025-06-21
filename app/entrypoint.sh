#!/bin/bash

# Inicia o cron em background
service cron start

# Roda seu app Python (ou qualquer outro comando)
python main.py

# Mantém o container vivo
tail -f /dev/null