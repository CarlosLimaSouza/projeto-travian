import asyncio
import random
from logger import log
from config import IS_DEVELOPMENT_MODE
from browser_utils import get_browser, close_browser_safely
from login import do_login
from gameworld import select_gameworld
from aldeias import get_villages
from recursos import upgrade_recursos
from construcoes import upgrade_construcoes
from database import init_db, get_db_connection, populate_default_rules

from fastapi import FastAPI, BackgroundTasks, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates # Importa o renderizador
from fastapi.staticfiles import StaticFiles   # Importa o servidor de arquivos estáticos

# --- Configuração do FastAPI ---
app = FastAPI()
# Diz ao FastAPI para servir os arquivos da pasta 'static' na URL '/static'
app.mount("/static", StaticFiles(directory="static"), name="static")

# Configura o Jinja2 para procurar por templates na pasta 'templates'
templates = Jinja2Templates(directory="templates")

bot_lock = asyncio.Lock()

@app.on_event("startup")
def on_startup():
    init_db()
    populate_default_rules()

# --- Funções de Lógica do Bot (em segundo plano) ---

async def sync_villages_with_game():
    if bot_lock.locked():
        log("Sincronização de aldeias tentada, mas o bot já está em execução.")
        return
    
    async with bot_lock:
        log("Iniciando processo de sincronização de aldeias...")
        browser = None
        try:
            browser = await get_browser()
            page = await browser.newPage()
            await page.goto('https://www.travian.com/', {'waitUntil': 'networkidle0'})
            await do_login(page)
            await select_gameworld(page)
            
            lista_aldeias_do_jogo = await get_villages(page)
            if not lista_aldeias_do_jogo:
                log("Nenhuma aldeia encontrada durante a sincronização.")
                return

            log(f"Encontradas {len(lista_aldeias_do_jogo)} aldeias. Tentando salvar no banco de dados...")
            conn = get_db_connection()
            try:
                # Usa INSERT OR IGNORE para adicionar apenas aldeias novas, sem dar erro se já existirem
                conn.executemany(
                    'INSERT OR IGNORE INTO villages (id, nome, href) VALUES (?, ?, ?)',
                    [(v['id'], v['nome'], v['href']) for v in lista_aldeias_do_jogo]
                )
                log("Dados inseridos na transação. Tentando commitar...")
                conn.commit() # Este é o comando crucial para salvar permanentemente.
                log("Commit realizado com sucesso! Os dados agora devem estar no arquivo.")
            except Exception as db_error:
                log(f"!!! ERRO AO SALVAR NO BANCO DE DADOS: {db_error} !!!")
                conn.rollback() # Desfaz a transação em caso de erro
            finally:
                conn.close()
                log("Conexão com o banco de dados fechada.")

        except Exception as e:
            log(f"Erro durante a sincronização de aldeias: {e}")
        finally:
            if browser:
                await close_browser_safely(browser)

# ... (O resto do arquivo main.py pode permanecer exatamente como a versão completa que enviei anteriormente) ...
# A função run_bot_session e todos os endpoints da API já estão corretos.
async def run_bot_session():
    log("Iniciando uma nova sessão do bot baseada nas configurações do DB...")
    conn = get_db_connection()
    aldeias_para_processar = conn.execute(
        'SELECT * FROM villages WHERE is_active = 1 ORDER BY priority DESC'
    ).fetchall()
    conn.close()
    if not aldeias_para_processar:
        log("Sessão encerrada: Nenhuma aldeia ativa para processar.")
        return
    browser = None
    try:
        browser = await get_browser()
        page = await browser.newPage()

        await page.goto('https://www.travian.com/', {'waitUntil': 'networkidle0', 'timeout': 90000})
        await do_login(page)
        await select_gameworld(page)
        log(f"Sessão iniciada. {len(aldeias_para_processar)} aldeias a serem processadas.")
        for aldeia in aldeias_para_processar:
            try:
                await page.setRequestInterception(True)
        
                async def intercept(request):
                    if request.resourceType in ['image','font', 'media']:
                        await request.abort()
                    else:
                        await request.continue_()

                page.on('request', lambda req: asyncio.ensure_future(intercept(req)))
                # -----------------------------------------------------------
                log(f"Processando aldeia: {aldeia['nome']} (ID: {aldeia['id']})")
                await page.goto(aldeia['href'], {'waitUntil': 'networkidle0'})
            except Exception as e:
                log(f"Erro fatal ao abrir a aldeia: {e}")

            try:
                await upgrade_recursos(page)
            except Exception as e:
                log(f"Erro fatal no upgrade_recursos: {e}")
            try:
                await upgrade_construcoes(page)
            except Exception as e:
                log(f"Erro fatal no upgrade_construcoes: {e}")
            log(f"Processamento da aldeia '{aldeia['nome']}' finalizado. Pausando...")
            await asyncio.sleep(random.randint(10, 20)) 
        log("Ciclo completo de todas as aldeias ativas finalizado.")
    except Exception as e:
        log(f"Erro fatal na sessão principal do bot: {e}")
    finally:
        if browser:
            await close_browser_safely(browser)

@app.get("/", response_class=HTMLResponse)
async def config_page(request: Request):
    message = request.query_params.get('message')
    conn = get_db_connection()
    villages = conn.execute('SELECT * FROM villages ORDER BY nome').fetchall()
    building_rules = conn.execute('SELECT * FROM building_rules ORDER BY nome').fetchall()
    resource_rules = conn.execute('SELECT * FROM resource_rules ORDER BY nome').fetchall()
    conn.close()
    
    return templates.TemplateResponse(
        "config.html", 
        {
            "request": request, 
            "villages": villages,
            "building_rules": building_rules,
            "resource_rules": resource_rules
        }
    )


@app.get("/sync-villages")
async def sync_villages_endpoint(background_tasks: BackgroundTasks):
    background_tasks.add_task(sync_villages_with_game)
    return RedirectResponse(url="/?message=sync_started", status_code=303)

@app.post("/update-villages")
async def update_villages_config(request: Request):
    form_data = await request.form()
    conn = get_db_connection()
    villages = conn.execute('SELECT id FROM villages').fetchall()
    for v in villages:
        v_id = v['id']
        is_active = 1 if f'active_{v_id}' in form_data else 0
        priority = int(form_data.get(f'priority_{v_id}', 0))
        conn.execute('UPDATE villages SET is_active = ?, priority = ? WHERE id = ?', (is_active, priority, v_id))
    conn.commit()
    conn.close()
    return RedirectResponse(url="/", status_code=303)

@app.post("/update-resources")
async def update_resources_config(request: Request):
    form_data = await request.form()
    conn = get_db_connection()
    rules = conn.execute('SELECT gid FROM resource_rules').fetchall()
    for r in rules:
        gid = r['gid']
        max_level = int(form_data.get(f'level_{gid}', 0))
        conn.execute('UPDATE resource_rules SET max_level = ? WHERE gid = ?', (max_level, gid))
    conn.commit()
    conn.close()
    return RedirectResponse(url="/", status_code=303)

@app.post("/update-buildings")
async def update_buildings_config(request: Request):
    form_data = await request.form()
    conn = get_db_connection()
    rules = conn.execute('SELECT gid FROM building_rules').fetchall()
    for b in rules:
        gid = b['gid']
        max_level = int(form_data.get(f'level_{gid}', 0))
        conn.execute('UPDATE building_rules SET max_level = ? WHERE gid = ?', (max_level, gid))
    conn.commit()
    conn.close()
    return RedirectResponse(url="/", status_code=303)

@app.get("/run")
async def run_bot_endpoint(background_tasks: BackgroundTasks):
    if bot_lock.locked():
        return HTMLResponse("<h1>O bot já está em execução.</h1>", status_code=409)
    async with bot_lock:
        background_tasks.add_task(run_bot_session)
    return RedirectResponse(url="/", status_code=303)