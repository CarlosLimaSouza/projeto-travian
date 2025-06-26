import random
from config import MINTIME, MAXTIME, TEST_MODE
import asyncio
from logger import log
from construcoes_config import valida_upgrade,converte_gid_para_nome
from browser_utils import get_browser
import gc

async def upgrade_construcoes(page):
    log('Verificando construções...')
    await page.click('#navigation a.buildingView')
    # log(await page.content())
    await page.waitForSelector('#villageContent', timeout=40000)
    lista_construcoes = await page.evaluate('''
        () => {
            const container = document.getElementById('villageContent');
            if (!container) return false;
            const links = container.querySelectorAll('.buildingSlot');
            return Array.from(links)
                .map(link => {
                    const a = link.querySelector('a');
                    return (a && a.classList.contains('good')) ? {
                        id: link.getAttribute('data-aid'),
                        gid: link.getAttribute('data-gid'),
                        level: a.getAttribute('data-level'),
                        href: a.href
                    } : null;
                })
                .filter(item => item && item.level !== null && item.gid !== "0");
        }
    ''')
    if not lista_construcoes:
        log('Nenhuma construção disponível para upgrade.')
        return
    # log(f'Construções disponíveis para upgrade: {lista_construcoes}')


    # valida os upgrades possíveis
    construcoes_validas= [c for c in lista_construcoes if valida_upgrade(c['gid'], c['level'])]
    if not construcoes_validas:
        log('Nenhuma construção válida para upgrade.')
        return
    # log(f'Construções válidas para upgrade: {construcoes_validas}')

    construcao_clicada = False
    for construcao in construcoes_validas:
        try:
            log(f"URL da contrução: {construcao['href']}")
            try:
                # await page.close()
                # browser = await get_browser()
                # page = await browser.newPage()
                # gc.collect()
                await page.goto(construcao['href'], waitUntil='networkidle0')
                construcao_clicada = True
            except Exception as e:
                log(f"Unexpected error: {e}")
            log(f'Construção {converte_gid_para_nome(construcao["gid"])} clicada para upgrade..o nível atual é {construcao["level"]}.')
            break  # Sai do loop após clicar na primeira construção válida
        except Exception as e:
            log(f'Erro ao clicar na construção ID:{construcao["id"]}/campo_{converte_gid_para_nome(construcao["gid"])}: {e}')

    if not construcao_clicada:
        log('Nenhuma construção válida encontrada para upgrade.')
        return

    if construcao_clicada:
        # Espera o botão de upgrade aparecer
        try:
            await page.waitForSelector('.upgradeButtonsContainer', timeout=30000)
            upgrade_url = await page.evaluate('''
                () => {
                    const button = document.querySelector('.upgradeButtonsContainer .section1 button.build');
                    if (!button) return null;

                    const onclick = button.getAttribute('onclick');
                    if (!onclick) return null;

                    const match = onclick.match(/window\\.location\\.href = '([^']+)'/);
                    return match ? match[1] : null;
                }
            ''')
            if TEST_MODE:
                log('[TESTE] Botão de upgrade de construção seria clicado agora!')
            else:
                # log(f"URL do botao clicado: {upgrade_url}")
                # await page.goto(upgrade_url, waitUntil='networkidle0')
                await page.click('.upgradeButtonsContainer .section1 button.build')
                log('Botão de upgrade de construção clicado!')
        except Exception as e:
            log(f'Erro ao tentar clicar no botão de upgrade: {e}')
    else:
        log('Nenhum espaço de construção disponível para upgrade.')

    await asyncio.sleep(random.randint(MINTIME, MAXTIME))