# gid que definem os recursos
serraria = 5
alvenaria = 6
fundicao = 7
moinho = 8
padaria = 9
armazem = 10
celeiro = 11
# ferreiro = 12 #legado
casa_de_ferragens = 13
praca_dos_torneios = 14
edificio_principal = 15
ponto_de_reuniao_militar = 16
mercado = 17
embaixada = 18
quartel = 19
cavalaria = 20
oficina = 21
academia = 22
esconderijo = 23
prefeitura = 24
residencia = 25
palacio = 26
tesouraria = 27
companhia_do_comercio = 28
grande_quartel = 29
grande_cavalaria = 30
muro_de_pedra = 31
muro_de_barro = 32
estacada = 33
pedreiro = 34
cervejaria = 35
caçador = 36
mansao_do_heroi = 37


# niveis maximos das contruções (sem limite == 99)
serraria_maximo = 1
alvenaria_maximo = 1
fundicao_maximo = 1
moinho_maximo = 1
padaria_maximo = 1
armazem_maximo = 12
celeiro_maximo = 1
# ferreiro_maximo = 1
casa_de_ferragens_maximo = 10
praca_dos_torneios_maximo = 1
edificio_principal_maximo = 20
ponto_de_reuniao_militar_maximo = 10
mercado_maximo = 12
embaixada_maximo = 1
quartel_maximo = 12
cavalaria_maximo = 7
oficina_maximo = 1
academia_maximo = 1
esconderijo_maximo = 1
prefeitura_maximo = 1
residencia_maximo = 1
palacio_maximo = 1
tesouraria_maximo = 1
companhia_do_comercio_maximo = 1
grande_quartel_maximo = 1
grande_cavalaria_maximo = 1
muro_de_pedra_maximo = 10
muro_de_barro_maximo = 10
estacada_maximo = 1
pedreiro_maximo = 1
cervejaria_maximo = 1
caçador_maximo = 1
mansao_do_heroi_maximo = 1
 
def valida_upgrade(gid, nivel): 
    if nivel is None:
        print(f"[ERRO] Nivel está None para gid={gid}")
        return False
    try:
        nivel = int(nivel)
    except Exception as e:
        print(f"[ERRO] Nivel inválido para gid={gid}: {nivel} ({e})")
        return False   
    gid = int(gid)
    # nivel = int(nivel)

    if gid == serraria:
        return nivel < serraria_maximo
    elif gid == alvenaria:
        return nivel < alvenaria_maximo
    elif gid == fundicao:
        return nivel < fundicao_maximo
    elif gid == moinho:
        return nivel < moinho_maximo
    elif gid == padaria:
        return nivel < padaria_maximo
    elif gid == armazem:
        return nivel < armazem_maximo
    elif gid == celeiro:
        return nivel < celeiro_maximo
    elif gid == ferreiro:
        return nivel < ferreiro_maximo
    elif gid == casa_de_ferragens:
        return nivel < casa_de_ferragens_maximo
    elif gid == praca_dos_torneios:
        return nivel < praca_dos_torneios_maximo
    elif gid == edificio_principal:
        return nivel < edificio_principal_maximo
    elif gid == ponto_de_reuniao_militar:
        return nivel < ponto_de_reuniao_militar_maximo
    elif gid == mercado:
        return nivel < mercado_maximo
    elif gid == embaixada:
        return nivel < embaixada_maximo
    elif gid == quartel:
        return nivel < quartel_maximo
    elif gid == cavalaria:
        return nivel < cavalaria_maximo
    elif gid == oficina:
        return nivel < oficina_maximo
    elif gid == academia:
        return nivel < academia_maximo
    elif gid == esconderijo:
        return nivel < esconderijo_maximo
    elif gid == prefeitura:
        return nivel < prefeitura_maximo
    elif gid == residencia:
        return nivel < residencia_maximo
    elif gid == palacio:
        return nivel < palacio_maximo
    elif gid == tesouraria:
        return nivel < tesouraria_maximo
    elif gid == companhia_do_comercio:
        return nivel < companhia_do_comercio_maximo
    elif gid == grande_quartel:
        return nivel < grande_quartel_maximo
    elif gid == grande_cavalaria:
        return nivel < grande_cavalaria_maximo
    elif gid == muro_de_pedra:
        return nivel < muro_de_pedra_maximo
    elif gid == muro_de_barro:
        return nivel < muro_de_barro_maximo
    elif gid == estacada:
        return nivel < estacada_maximo
    elif gid == pedreiro:
        return nivel < pedreiro_maximo
    elif gid == cervejaria:
        return nivel < cervejaria_maximo
    elif gid == caçador:
        return nivel < caçador_maximo
    elif gid == mansao_do_heroi:
        return nivel < mansao_do_heroi_maximo

    return False


def converte_gid_para_nome(gid):
    gid = int(gid)
    if gid == serraria:
        return "serraria"
    elif gid == alvenaria:
        return "alvenaria"
    elif gid == fundicao:
        return "fundicao"
    elif gid == moinho:
        return "moinho"
    elif gid == padaria:
        return "padaria"
    elif gid == armazem:
        return "armazem"
    elif gid == celeiro:
        return "celeiro"
    elif gid == ferreiro:
        return "ferreiro"
    elif gid == casa_de_ferragens:
        return "casa_de_ferragens"
    elif gid == praca_dos_torneios:
        return "praca_dos_torneios"
    elif gid == edificio_principal:
        return "edificio_principal"
    elif gid == ponto_de_reuniao_militar:
        return "ponto_de_reuniao_militar"
    elif gid == mercado:
        return "mercado"
    elif gid == embaixada:
        return "embaixada"
    elif gid == quartel:
        return "quartel"
    elif gid == cavalaria:
        return "cavalaria"
    elif gid == oficina:
        return "oficina"
    elif gid == academia:
        return "academia"
    elif gid == esconderijo:
        return "esconderijo"
    elif gid == prefeitura:
        return "prefeitura"
    elif gid == residencia:
        return "residencia"
    elif gid == palacio:
        return "palacio"
    elif gid == tesouraria:
        return "tesouraria"
    elif gid == companhia_do_comercio:
        return "companhia_do_comercio"
    elif gid == grande_quartel:
        return "grande_quartel"
    elif gid == grande_cavalaria:
        return "grande_cavalaria"
    elif gid == muro_de_pedra:
        return "muro_de_pedra"
    elif gid == muro_de_barro:
        return "muro_de_barro"
    elif gid == estacada:
        return "estacada"
    elif gid == pedreiro:
        return "pedreiro"
    elif gid == cervejaria:
        return "cervejaria"
    elif gid == caçador:
        return "caçador"
    elif gid == mansao_do_heroi:
        return "mansao_do_heroi"
    else:
        return "Construção desconhecida"
