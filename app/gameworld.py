from config import GAMEWORLD
from logger import log

async def select_gameworld(page):
    log(f'Selecionando o gameworld: {GAMEWORLD}')
    try:
        await page.waitForSelector('.yourGameworlds', timeout=40000)
        log('[DEBUG] .yourGameworlds encontrado')
        worlds = await page.querySelectorAll('.yourGameworlds .gameworld')
        log(f'[DEBUG] Mundos encontrados: {len(worlds)}')
        for world in worlds:
            # Busca o nome do gameworld
            name = await page.evaluate('(el) => el.querySelector(".gameworldName")?.innerText || ""', world)
            log(f'[DEBUG] Mundo: {name}')
            if GAMEWORLD.lower() in name.lower():
                # Clica no botão "Play now" dentro do gameworld correto
                play_btn = await world.querySelector('button.playNow')
                if play_btn:
                    await play_btn.click()
                    await page.waitForNavigation()
                    log(f'Entrou no gameworld: {GAMEWORLD}')
                    return True
                else:
                    log('[DEBUG] Botão "Play now" não encontrado nesse mundo.')
        log(f'Gameworld "{GAMEWORLD}" não encontrado.')
        return False
    except Exception as e:
        log(f'[DEBUG] Erro ao selecionar gameworld: {e}')
        url = page.url
        if "dorf" in url:
            log('[DEBUG] Já está dentro de um gameworld.')
            return True
        else:
            log('[DEBUG] Não foi possível encontrar a lista de mundos.')
            return False