from pyppeteer import launch
from config import IS_HEADLESS_MODE_ENABLED
import sys

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
            '--window-size=375,667',
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