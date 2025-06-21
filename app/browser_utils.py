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
            '--no-zygote'
        ]
    )