from logger import log

async def get_villages(page):
    log('Listando todas as aldeias...')

    await page.waitForSelector('div.iconAndNameWrapper', timeout=40000)

    # Obtém a lista de aldeias
    lista_aldeias = await page.evaluate('''
        () => {
            const container = document.querySelector('div.villageList');
            if (!container) return [];
            const links = container.querySelectorAll('div.dropContainer');
            return Array.from(links).map(link => {
                const detalhes = link.querySelector('div.listEntry');
                return {
                    id: detalhes?.getAttribute('data-did'),
                    nome: detalhes?.querySelector('div.iconAndNameWrapper')?.querySelector('span.name')?.textContent.trim(),
                    href: detalhes?.querySelector('a')?.href
                };
            });
        }
    ''')

    if not lista_aldeias:
        log('Nenhuma aldeia encontrada.')
        return

    return lista_aldeias

    
    # Return mock data
    # return [
    #     {
    #         "id": "24109",
    #         "nome": "carlin 1",
    #         "href": "https://ts8.x1.international.travian.com/dorf1.php?newdid=24109&"
    #     },
    #     {
    #         "id": "34852",
    #         "nome": "carlin 2",
    #         "href": "https://ts8.x1.international.travian.com/dorf1.php?newdid=34852&"
    #     },
    #     {
    #         "id": "36944",
    #         "nome": "carlin 3",
    #         "href": "https://ts8.x1.international.travian.com/dorf1.php?newdid=36944&"
    #     }
    # ]