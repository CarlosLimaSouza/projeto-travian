## Índice

- [Guia de Configuração da VM para rodar o Bot Travian](#rodando-numa-vps-ou-vm)
- [Rodando Localmente com Ambiente Virtual (venv)](#rodando-localmente-com-ambiente-virtual-venv)


## Guia de Configuração da VM para rodar o Bot Travian

1. Atualize o sistema
```sh
sudo apt update && sudo apt upgrade -y
```

2. Instale o Docker e dependências
```sh
sudo apt install -y docker.io
sudo systemctl enable --now docker

sudo apt install -y nano cron
sudo systemctl enable --now cron

sudo apt install -y docker-compose-plugin
# Ou, para versões antigas:
# sudo apt install -y docker-compose
```

3. Adicione seu usuário ao grupo docker
```sh
sudo usermod -aG docker $USER
# Depois, faça logout e login novamente! (exit ou desligue e ligue a VM)
```

4. Faça login no Docker Hub (se necessário)
```sh
docker login
```

5. Baixe a imagem do container
```sh
docker pull carlinls/bot-travian:latest
```

6. Crie o .env
- Crie um arquivo `.env` com os caminhos desejados:
  ```sh
  cat > .env <<EOF
  TRAVIAN_EMAIL=seu_email@exemplo.com
  TRAVIAN_PASSWORD=sua_senha_segura
  TRAVIAN_GAMEWORLD=International 8
  TRAVIAN_MINTIME=10
  TRAVIAN_MAXTIME=20
  TRAVIAN_TEST_MODE=True
  TRAVIAN_HEADLESS=True
  TRAVIAN_LOOK_RESOURCE=True
  TRAVIAN_LOOK_BUILDING=False
  EOF
  ```
- Edite o conteúdo do `.env` se necessário:
  ```sh
  nano .env
  ```

7. Use Docker Compose
- Crie um arquivo `docker-compose.yml`:
  ```sh
  cat > docker-compose.yml <<EOF
  services:
    bot-travian:
      image: carlinls/bot-travian:latest
      env_file:
        - .env
      volumes:
        - ./travian_bot.log:/app/travian_bot.log
      restart: "no"
  EOF
  ```
- Para rodar:
  ```sh
  docker compose run --rm bot-travian
  ```

8. Configure o cron para execução automática
- Edite o crontab:
  ```sh
  crontab -e
  ```
- Adicione a linha (exemplo para rodar a cada 10 minutos):
  ```sh
  TZ=America/Sao_Paulo
    */10 * * * * /usr/bin/docker compose run --rm bot-travian >> /home/SEU_USUARIO_VM/app.log 2>&1
  
    */10 * * * * echo "Cron rodou em: $(date)" >> /home/SEU_USUARIO_VM/cron_teste.log
  ```

---
**Observações:**
- Sempre verifique permissões das pastas e arquivos.
- O caminho dos volumes deve ser ajustado conforme a estrutura da VM.
- Se mudar o nome do usuário, ajuste os caminhos.

---



## Rodando Localmente com Ambiente Virtual (venv)

1. **Crie o ambiente virtual:**
   ```sh
   python -m venv venv
   ```

2. **Ative o ambiente virtual:**
   - No Windows:
     ```sh
     .\venv\Scripts\activate
     ```
   - No Linux/Mac:
     ```sh
     source venv/bin/activate
     ```

3. **Instale as dependências:**
   ```sh
   pip install --upgrade pip
   pip install -r requirements.txt
   ```

4. **Configure suas variáveis de ambiente:**
   - Edite o arquivo `app/config_dev.py` para suas configurações locais

5. **Execute o projeto:**
   ```sh
   cd app
   python main.py
   ```
**Observações:**
- Não esqueça de ativar o ambiente virtual sempre que for rodar o projeto localmente!
