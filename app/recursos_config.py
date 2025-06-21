# gid que definem os recursos
madeira = 1
barro = 2
ferro = 3
cereal = 4

# niveis maximos dos recursos (sem limite == 99)
madeira_maximo= 10
barro_maximo = 10
ferro_maximo = 9
cereal_maximo = 8
 
def valida_upgrade(slot, nivel):   
    # verifica se nivel é um número inteiro
    if not isinstance(nivel, int):
        nivel = 0 
    slot = int(slot)
    nivel = int(nivel)
    # deve chegar no slot algo como "1" ou "2" ou "3" ou "4"
    if slot == madeira:
        if madeira_maximo > nivel:
            return True
    elif slot == barro:
        if barro_maximo > nivel:
            return True
    elif slot == ferro:
        if ferro_maximo > nivel:
            return True
    elif slot == cereal:
        if cereal_maximo > nivel:
            return True
    return False  # Se não for nenhum dos recursos ou já estiver no máximo

def converte_gid_para_nome(gid):
    gid = int(gid) 
    if gid == madeira:
        return "Madeira"
    elif gid == barro:
        return "Barro"
    elif gid == ferro:
        return "Ferro"
    elif gid == cereal:
        return "Cereal"
    else:
        return "Recurso Desconhecido"  # Caso o gid não corresponda a nenhum recurso conhecido