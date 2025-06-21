from logger import log

async def go_to_lobby(page):
    log("Acessando a página do lobby...")
    try:
        await page.waitForSelector('.content', timeout=40000)
        log("Seletor .content encontrado!")
        return True
    except Exception as e:
        log(f"Erro ao esperar seletor .content: {e}")
        # Tenta checar manualmente se o seletor existe
        content = await page.querySelector('.content')
        if content:
            log("Seletor .content existe, mas não carregou a tempo.")
        else:
            log("Seletor .content realmente não está presente na página.")
            return False