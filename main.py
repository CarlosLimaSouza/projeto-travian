import asyncio
from browser_utils import get_browser
from login import do_login
from lobby import go_to_lobby
from gameworld import select_gameworld
from recursos import upgrade_recursos
from construcoes import upgrade_construcoes
from logger import log
from config import LOOK_RESOURCE, LOOK_BUILDING

async def main():
    browser = await get_browser()
    page = await browser.newPage()
    await page.goto('https://www.travian.com/')

    logged_in = await do_login(page)
    if not logged_in:
        await go_to_lobby(page)

    await select_gameworld(page)

    # Apenas UM ciclo!
    if LOOK_RESOURCE:
        await upgrade_recursos(page)    
    if LOOK_BUILDING: 
        await upgrade_construcoes(page)

    await browser.close()  # Fecha o navegador ao final

asyncio.run(main())
