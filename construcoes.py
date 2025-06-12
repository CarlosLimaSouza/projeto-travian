import random
from config import MINTIME, MAXTIME, TEST_MODE
import asyncio
from logger import log

async def upgrade_construcoes(page):
    log('Verificando construções...')
    await page.click('#navigation a.buildingView')
    await page.waitForSelector('#villageContent', timeout=10000)
    construcao_clicada = await page.evaluate('''
        () => {
            const container = document.getElementById('villageContent');
            if (!container) return false;
            const slots = container.querySelectorAll('.buildingSlot');
            for (const slot of slots) {
                const link = slot.querySelector('a.good');
                if (link) {
                    link.click();
                    return true;
                }
            }
            return false;
        }
    ''')
    log(f'Espaço de construção clicado: {construcao_clicada}')

    if construcao_clicada:
        # Espera o botão de upgrade aparecer
        try:
            await page.waitForSelector('.upgradeButtonsContainer .section1 button.build', timeout=5000)
            if TEST_MODE:
                log('[TESTE] Botão de upgrade de construção seria clicado agora!')
            else:
                await page.click('.upgradeButtonsContainer .section1 button.build')
                log('Botão de upgrade de construção clicado!')
        except Exception as e:
            log(f'Erro ao tentar clicar no botão de upgrade: {e}')
    else:
        log('Nenhum espaço de construção disponível para upgrade.')

    await asyncio.sleep(random.randint(MINTIME, MAXTIME))