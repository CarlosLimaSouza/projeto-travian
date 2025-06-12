from config import EMAIL, PASSWORD
from logger import log

async def do_login(page):
    # Se o botão de login não existe, provavelmente já está logado
    login_btn = await page.querySelector('button.login')
    if not login_btn:
        log('Já está logado, não precisa fazer login.')
        return False

    # Aceita cookies se necessário
    await page.evaluate('''
        () => {
            const host = document.querySelector('#cmpwrapper');
            if (!host) return false;
            const shadow = host.shadowRoot;
            if (!shadow) return false;
            const btn = shadow.querySelector('#cmpbntnotxt');
            if (btn) btn.click();
            return true;
        }
    ''')
    await page.click('button.login')
    await page.waitForSelector('input[name="name"]')
    await page.type('input[name="name"]', EMAIL)
    await page.type('input[name="password"]', PASSWORD)
    await page.click('button.green.buttonFramed.withText.withLoadingIndicator[type="submit"]')
    await page.waitForNavigation()
    log('Logged in')
    return True