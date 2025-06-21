import asyncio
from browser_utils import get_browser
from login import do_login
from lobby import go_to_lobby
from gameworld import select_gameworld
from recursos import upgrade_recursos
from construcoes import upgrade_construcoes
from logger import log
from config import LOOK_RESOURCE, LOOK_BUILDING,APP_ENABLE
from aldeias import get_villages
import gc

async def main():
    browser = await get_browser()
    page = await browser.newPage()
    await page.goto('https://www.travian.com/')

    if APP_ENABLE:
        log("Aplicativo está habilitado. Iniciando o processo...") 
    else:
        log("Aplicativo está desabilitado. Encerrando o processo.")
        await browser.close()
        return

    # logado = await go_to_lobby(page)
    # if not logado:
    await do_login(page)

    await select_gameworld(page)
    gc.collect()
    aldeias = await get_villages(page)
    if not aldeias:
        log('Nenhuma aldeia encontrada. Encerrando o processo.')
        return
    log(f'aldeias encontradas: {aldeias}')
    
    for aldeia in aldeias:
        gc.collect()
        log(f'Processando aldeia: {aldeia["nome"]} (ID: {aldeia["id"]})')
        await page.close()
        page = await browser.newPage()  # Cria uma nova página
        await page.goto(aldeia['href'], waitUntil='networkidle0')
        if LOOK_RESOURCE:
            await upgrade_recursos(page)    
        if LOOK_BUILDING: 
            await upgrade_construcoes(page)

    await browser.close()  # Fecha o navegador ao final

asyncio.run(main())
