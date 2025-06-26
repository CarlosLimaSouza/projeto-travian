from pyppeteer import launch
from config import IS_HEADLESS_MODE_ENABLED
import sys
import psutil
from logger import log

if sys.platform.startswith("win"):
    CHROME_PATH = "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe"
else:
    CHROME_PATH = "/usr/bin/chromium"

async def get_browser():
    return await launch(
        headless=IS_HEADLESS_MODE_ENABLED,
        executablePath=CHROME_PATH,
        args=[
            '--no-sandbox',
            '--disable-dev-shm-usage',
            '--disable-gpu',
            '--disable-setuid-sandbox',
            '--window-size=1280,768',
            '--disable-gpu',
            '--no-zygote',
            '--disable-extensions',
            '--disable-software-rasterizer',
            '--disable-background-networking',
            '--disable-background-timer-throttling',
            '--disable-backgrounding-occluded-windows',
            '--disable-breakpad',
            '--disable-client-side-phishing-detection',
            '--disable-component-update',
            '--disable-default-apps', #testado até aqui
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
            '--memory-pressure-off',  # Opcional, mas pode ajudar
        ]
    )
async def close_browser_safely(browser):
    """Fecha o navegador de forma segura, garantindo que o processo seja encerrado."""
    if not browser:
        return

    try:
        # Pega o PID (Process ID) do processo principal do Chrome
        pid = browser.process.pid
        log(f"Tentando fechar o navegador e o processo PID: {pid}")

        # Usa psutil para encontrar e matar o processo e todos os seus filhos
        parent_process = psutil.Process(pid)
        for child in parent_process.children(recursive=True):
            log(f"Matando processo filho: {child.pid}")
            child.kill()
        log(f"Matando processo pai: {parent_process.pid}")
        parent_process.kill()
    except psutil.NoSuchProcess:
        log("Processo do navegador não encontrado (provavelmente já foi fechado).")
    except Exception as e:
        log(f"Erro ao tentar matar o processo do navegador com psutil: {e}")

    try:
        # Agora, chame o close() original, que deve funcionar
        # pois o processo que segurava os arquivos já foi encerrado.
        await browser.close()
        log("Navegador fechado com sucesso.")
    except Exception as e:
        # Se mesmo assim der erro, apenas registre, pois o principal (matar o processo) foi feito.
        log(f"Erro durante o browser.close() final (pode ser ignorado se o processo foi morto): {e}")