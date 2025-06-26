import sqlite3
from logger import log
import os
from config import IS_DEVELOPMENT_MODE

# Lógica de caminho do banco de dados (sem alterações)
if IS_DEVELOPMENT_MODE:
    DATABASE_DIR = "data"
    os.makedirs(DATABASE_DIR, exist_ok=True)
else:
    DATABASE_DIR = "/data"
DATABASE_FILE = os.path.join(DATABASE_DIR, "bot_config.sqlite3")

def get_db_connection():
    """Cria uma conexão com o banco de dados."""
    conn = sqlite3.connect(DATABASE_FILE)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """Inicializa o banco de dados e cria as tabelas se não existirem."""
    log("Verificando e inicializando tabelas do banco de dados...")
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS villages (
            id TEXT PRIMARY KEY, nome TEXT NOT NULL, href TEXT NOT NULL,
            is_active BOOLEAN NOT NULL DEFAULT 1, priority INTEGER DEFAULT 0
        )''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS building_rules (
            gid INTEGER PRIMARY KEY, nome TEXT NOT NULL, max_level INTEGER NOT NULL
        )''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS resource_rules (
            gid INTEGER PRIMARY KEY, nome TEXT NOT NULL, max_level INTEGER NOT NULL
        )''')
        
    conn.commit()
    conn.close()
    log("Tabelas do banco de dados prontas.")


def populate_default_rules():
    """Insere as regras padrão de construção e recursos se as tabelas estiverem vazias."""
    log("Verificando se as regras padrão precisam ser populadas...")
    conn = get_db_connection()
    
    # --- VERIFICA E POPULA AS CONSTRUÇÕES ---
    count = conn.execute('SELECT COUNT(*) FROM building_rules').fetchone()[0]
    if count == 0:
        log("Tabela 'building_rules' está vazia. Populando com dados padrão...")
        
        # <<< LISTA COMPLETA DE CONSTRUÇÕES AQUI >>>
        building_data = [
            (5, "Serraria", 5),
            (6, "Alvenaria", 5),
            (7, "Fundição", 5),
            (8, "Moinho", 5),
            (9, "Padaria", 1),
            (10, "Armazém", 20),
            (11, "Celeiro", 20),
            (12, "Ferreiro (Legado)", 1),
            (13, "Casa de Ferragens", 10),
            (14, "Praça dos Torneios", 1),
            (15, "Edifício Principal", 20),
            (16, "Ponto de Reunião Militar", 10),
            (17, "Mercado", 20),
            (18, "Embaixada", 1),
            (19, "Quartel", 12),
            (20, "Cavalaria", 10),
            (21, "Oficina", 10),
            (22, "Academia", 10),
            (23, "Esconderijo", 10),
            (24, "Prefeitura", 1),
            (25, "Residência", 10),
            (26, "Palácio", 1),
            (27, "Tesouraria", 1),
            (28, "Companhia do Comércio", 1),
            (29, "Grande Quartel", 1),
            (30, "Grande Cavalaria", 1),
            (31, "Muro de Pedra", 10),
            (32, "Muro de Barro", 10),
            (33, "Estacada", 1),
            (34, "Pedreiro", 1),
            (35, "Cervejaria", 1),
            (36, "Caçador", 1),
            (37, "Mansão do Herói", 10),
        ]
        conn.executemany('INSERT INTO building_rules (gid, nome, max_level) VALUES (?, ?, ?)', building_data)
        log(f"{len(building_data)} regras de construção inseridas.")

    # --- VERIFICA E POPULA OS RECURSOS ---
    count = conn.execute('SELECT COUNT(*) FROM resource_rules').fetchone()[0]
    if count == 0:
        log("Tabela 'resource_rules' está vazia. Populando com dados padrão...")
        resource_data = [
            (1, "Madeira", 10),
            (2, "Barro", 10),
            (3, "Ferro", 10),
            (4, "Cereal", 7)
        ]
        conn.executemany('INSERT INTO resource_rules (gid, nome, max_level) VALUES (?, ?, ?)', resource_data)
        log(f"{len(resource_data)} regras de recursos inseridas.")
        
    conn.commit()
    conn.close()