import random
import asyncio
from config import MINTIME, MAXTIME, TEST_MODE
from logger import log

async def upgrade_recursos(page):
    log('Verificando recursos...')
    await page.click('#navigation a.resourceView')
    await page.waitForSelector('#resourceFieldContainer', timeout=10000)
    recurso_clicado = await page.evaluate('''
        () => {
            const container = document.getElementById('resourceFieldContainer');
            if (!container) return false;
            const links = container.querySelectorAll('a.good');
            if (links.length > 0) {
                links[0].click();
                return true;
            }
            return false;
        }
    ''')
    log(f'Campo de recurso clicado: {recurso_clicado}')

    if recurso_clicado:
        # Espera o botão de upgrade aparecer
        await page.waitForSelector('.upgradeButtonsContainer .section1 button.build', timeout=5000)
        if TEST_MODE:
            log('[TESTE] Botão de upgrade de recurso seria clicado agora!')
        else:
            await page.click('.upgradeButtonsContainer .section1 button.build')
            log('Botão de upgrade de recurso clicado!')
    else:
        log('Nenhum campo de recurso disponível para upgrade.')

    await asyncio.sleep(random.randint(MINTIME, MAXTIME))