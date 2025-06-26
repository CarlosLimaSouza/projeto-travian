from database import get_db_connection

def valida_upgrade(gid, nivel):
    """
    Valida se um recurso pode ser atualizado com base nas regras do banco de dados.
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
    # Busca a regra para o GID específico na tabela de recursos
    rule = conn.execute('SELECT max_level FROM resource_rules WHERE gid = ?', (gid,)).fetchone()
    conn.close()

    if rule:
        # Se encontrou uma regra, verifica se o nível atual é menor que o máximo permitido
        max_level = rule['max_level']
        return nivel < max_level

    # Se não houver regra, não permite o upgrade
    return False

def converte_gid_para_nome(gid):
    """Converte o GID de um recurso para seu nome."""
    gid_map = {
        1: "Madeira",
        2: "Barro",
        3: "Ferro",
        4: "Cereal"
    }
    return gid_map.get(int(gid), "Recurso Desconhecido")