from database import get_db_connection

def valida_upgrade(gid, nivel):
    """
    Valida se uma construção pode ser atualizada com base nas regras do banco de dados.
    """
    if nivel is None:
        return False
    try:
        # Garante que estamos comparando números
        nivel = int(nivel)
        gid = int(gid)
    except (ValueError, TypeError):
        return False

    conn = get_db_connection()
    # Busca a regra para o GID específico na tabela de construções
    rule = conn.execute('SELECT max_level FROM building_rules WHERE gid = ?', (gid,)).fetchone()
    conn.close()

    if rule:
        # Se encontrou uma regra, verifica se o nível atual é menor que o máximo permitido
        max_level = rule['max_level']
        return nivel < max_level
    
    # Se não houver regra para esse GID, não permite o upgrade por segurança
    return False

def converte_gid_para_nome(gid):
    """
    Converte o GID de uma construção para seu nome.
    Esta função poderia ser otimizada para buscar do DB, mas por enquanto, manter assim é simples.
    """
    gid_map = {
        5: "Serraria", 6: "Alvenaria", 7: "Fundição", 8: "Moinho", 9: "Padaria",
        10: "Armazém", 11: "Celeiro", 12: "Ferreiro (Legado)", 13: "Casa de Ferragens",
        14: "Praça dos Torneios", 15: "Edifício Principal", 16: "Ponto de Reunião Militar",
        17: "Mercado", 18: "Embaixada", 19: "Quartel", 20: "Cavalaria", 21: "Oficina",
        22: "Academia", 23: "Esconderijo", 24: "Prefeitura", 25: "Residência", 26: "Palácio",
        27: "Tesouraria", 28: "Companhia do Comércio", 29: "Grande Quartel", 30: "Grande Cavalaria",
        31: "Muro de Pedra", 32: "Muro de Barro", 33: "Estacada", 34: "Pedreiro",
        35: "Cervejaria", 36: "Caçador", 37: "Mansão do Herói"
    }
    return gid_map.get(int(gid), "Construção Desconhecida")