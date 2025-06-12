from pyppeteer import launch
from config import USER_DATA_DIR, IS_HEADLESS_MODE_ENABLED
import sys

if sys.platform.startswith("win"):
    CHROME_PATH = "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe"
else:
    CHROME_PATH = "/usr/bin/chromium"

async def get_browser():
    return await launch(
        headless=IS_HEADLESS_MODE_ENABLED,
        executablePath=CHROME_PATH,
        userDataDir=USER_DATA_DIR,
        args=[
            '--no-sandbox',
            '--disable-dev-shm-usage',
            '--disable-gpu',
            '--disable-setuid-sandbox'
        ]
    )