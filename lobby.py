from logger import log

async def go_to_lobby(page):
    log('Redirecionando para o lobby...')
    await page.goto('https://lobby.legends.travian.com/account')
    url_atual = page.url
    log(f"URL atual após goto: {url_atual}")

    try:
        await page.waitForSelector('.content', timeout=30000)
        log("Seletor .content encontrado!")
    except Exception as e:
        log(f"Erro ao esperar seletor .content: {e}")
        # Tenta checar manualmente se o seletor existe
        content = await page.querySelector('.content')
        if content:
            log("Seletor .content existe, mas não carregou a tempo.")
        else:
            log("Seletor .content realmente não está presente na página.")