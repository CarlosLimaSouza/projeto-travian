# Guia de Configuração da VM para rodar o Bot Travian

## 1. Atualize o sistema
```sh
sudo apt update && sudo apt upgrade -y
```

## 2. Instale o Docker
```sh
sudo apt install -y docker.io
sudo systemctl enable --now docker

sudo apt install nano
sudo apt install -y cron
sudo systemctl enable --now cron


sudo apt install -y docker-compose-plugin
# Ou, para versões antigas:
# sudo apt install -y docker-compose
```

## 3. Adicione seu usuário ao grupo docker
```sh
sudo usermod -aG docker $USER
# Depois, faça logout e login novamente! (exit ou desliga e liga a VM)
```

## 4. Faça login no Docker Hub (se necessário)
```sh
docker login
```

## 5. Baixe a imagem do container
```sh
docker pull carlinls/bot-travian:latest
# cria e da permissão da pasta q armazena a sessão do login e sera usada como volume
sudo rm -rf ./sessao
mkdir ./sessao
chmod 777 ./sessao
```
## 7. Use Docker Compose
- Crie um arquivo `.env` com os caminhos desejados:
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

-edite o conteudo do env:
  nano .env

- Crie um arquivo `docker-compose.yml`:
    cat > docker-compose.yml <<EOF
    version: '3'
    services:
      bot-travian:
        image: carlinls/bot-travian:latest
        env_file:
          - .env
        volumes:
          - ./sessao:/app/chrome_profile
        restart: "no"
    EOF
- Para rodar:
  ```sh
docker compose run --rm bot-travian
  ```
```

## 8. Configure o cron para execução automática
- Edite o crontab:
  ```sh
  crontab -e
  ```
- Adicione a linha (exemplo para rodar a cada 10 minutos):
  ```sh
  TZ=America/Sao_Paulo
  */10 * * * * /usr/bin/docker compose run --rm bot-travian >> /home/carlinls/app.log 2>&1

  */10 * * * * echo "Cron rodou em: $(date)" >> /home/carlinls/cron_teste.log
  ```
---

**Observações:**
- Sempre verifique permissões das pastas e arquivos.
- O caminho dos volumes deve ser ajustado conforme a estrutura da VM.
- Se mudar o nome do usuário, ajuste os caminhos.

---