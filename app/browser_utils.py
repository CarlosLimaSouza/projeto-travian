import os
import sys
import psutil
from pyppeteer import launch, connect
from config import IS_HEADLESS_MODE_ENABLED
from logger import log

# Define o caminho do executável do Chrome/Chromium dependendo do SO
if sys.platform.startswith("win"):
    CHROME_PATH = "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe"
else:
    CHROME_PATH = "/usr/bin/chromium"

async def get_browser():
    """
    Obtém uma instância do navegador.
    Se a variável de ambiente BROWSERLESS_CONNECTION_URL estiver definida,
    conecta-se a um serviço remoto. Caso contrário, lança um navegador local.
    """
    browser_url = os.getenv('BROWSERLESS_CONNECTION_URL')

    if browser_url:
        # --- MODO REMOTO (PRODUÇÃO / RAILWAY) ---
        log(f"Variável BROWSERLESS_CONNECTION_URL encontrada. Conectando ao serviço remoto...")
        try:
            return await connect(
                browserWSEndpoint=browser_url,
                timeout=120000  # Timeout de 2 minutos para a conexão de rede
            )
        except Exception as e:
            log(f"[ERRO FATAL] Falha ao conectar ao serviço Browserless em {browser_url}: {e}")
            raise
    else:
        # --- MODO LOCAL (DESENVOLVIMENTO) ---
        log("Nenhuma variável BROWSERLESS_CONNECTION_URL encontrada. Lançando navegador localmente...")
        args = [
            '--no-sandbox',
            '--disable-dev-shm-usage',
            '--disable-gpu',
            '--disable-setuid-sandbox',
            '--window-size=1280,768',
            '--no-zygote',
            '--disable-extensions',
            '--disable-software-rasterizer',
            '--disable-background-networking',
            '--disable-background-timer-throttling',
            '--disable-backgrounding-occluded-windows',
            '--disable-breakpad',
            '--disable-client-side-phishing-detection',
            '--disable-component-update',
            '--disable-default-apps',
            '--disable-domain-reliability',
            '--disable-features=AudioServiceOutOfProcess',
            '--disable-hang-monitor',
            '--disable-ipc-flooding-protection',
            '--disable-notifications',
            '--disable-popup-blocking',
            '--disable-print-preview',
            '--disable-prompt-on-repost',
            '--disable-renderer-backgrounding',
            '--disable-sync',
            '--metrics-recording-only',
            '--mute-audio',
            '--no-first-run',
            '--safebrowsing-disable-auto-update',
            '--enable-automation',
            '--password-store=basic',
            '--use-mock-keychain',
            '--memory-pressure-off',
        ]
        return await launch(
            headless=IS_HEADLESS_MODE_ENABLED,
            executablePath=CHROME_PATH,
            args=args
        )

async def close_browser_safely(browser):
    """
    Fecha a conexão ou o navegador de forma segura.
    Diferencia entre uma instância local (que precisa ser morta com psutil)
    e uma conexão remota (que só precisa ser fechada).
    """
    if not browser:
        return

    # Um navegador lançado localmente tem o atributo 'process'.
    # Um navegador conectado remotamente não tem.
    is_local_browser = hasattr(browser, 'process') and browser.process

    if is_local_browser:
        # --- LÓGICA PARA NAVEGADOR LOCAL ---
        pid = browser.process.pid
        log(f"Fechando navegador local com psutil (PID: {pid})...")
        try:
            parent_process = psutil.Process(pid)
            for child in parent_process.children(recursive=True):
                child.kill()
            parent_process.kill()
        except psutil.NoSuchProcess:
            log(f"Processo {pid} não encontrado (provavelmente já foi fechado).")
        except Exception as e:
            log(f"Erro ao matar processo com psutil: {e}")
    else:
        # --- LÓGICA PARA NAVEGADOR REMOTO ---
        log("Fechando conexão com o navegador remoto...")

    try:
        # Para ambos os casos, tentamos chamar o close() para limpar a conexão
        await browser.close()
        log("Conexão/Navegador fechado com sucesso.")
    except Exception as e:
        log(f"Erro durante o browser.close() final (pode ser ignorado se o processo já foi morto): {e}")