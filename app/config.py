import os

# --- AQUI ESTÁ A MUDANÇA PRINCIPAL ---
# Determine o modo UMA VEZ e exporte a variável.
# Outros módulos poderão importar `IS_DEVELOPMENT_MODE`.
IS_DEVELOPMENT_MODE = os.getenv('MODO_DESENVOLVIMENTO', 'True').lower() == 'true'


# Tenta importar config_dev.py se estiver em modo desenvolvimento
if IS_DEVELOPMENT_MODE:
    try:
        from config_dev import (
            EMAIL_DEV, PASSWORD_DEV, TEST_MODE_DEV, APP_ENABLE_DEV,
            IS_HEADLESS_MODE_ENABLED_DEV, MINTIME_DEV, MAXTIME_DEV,
            LOOK_RESOURCE_DEV, LOOK_BUILDING_DEV, GAMEWORLD_DEV
        )
        # Configurações de desenvolvimento
        APP_ENABLE = APP_ENABLE_DEV
        TEST_MODE = TEST_MODE_DEV
        IS_HEADLESS_MODE_ENABLED = IS_HEADLESS_MODE_ENABLED_DEV
        EMAIL = EMAIL_DEV
        PASSWORD = PASSWORD_DEV
        GAMEWORLD = GAMEWORLD_DEV
        MINTIME = MINTIME_DEV
        MAXTIME = MAXTIME_DEV
        LOOK_RESOURCE = LOOK_RESOURCE_DEV
        LOOK_BUILDING = LOOK_BUILDING_DEV
    except ImportError:
        # Se não encontrar o config_dev.py, usa as variáveis de ambiente com defaults de dev
        APP_ENABLE = os.getenv('APP_ENABLE', 'True').lower() == 'true'
        TEST_MODE = os.getenv('TRAVIAN_TEST_MODE', 'True').lower() == 'true'
        IS_HEADLESS_MODE_ENABLED = os.getenv('TRAVIAN_HEADLESS', 'True').lower() == 'true'
        EMAIL = os.getenv('TRAVIAN_EMAIL', 'teste@email.com.br')
        PASSWORD = os.getenv('TRAVIAN_PASSWORD', 'senha123')
        GAMEWORLD = os.getenv('TRAVIAN_GAMEWORLD', 'International 8')
        MINTIME = int(os.getenv('TRAVIAN_MINTIME', 10))
        MAXTIME = int(os.getenv('TRAVIAN_MAXTIME', 20))
        LOOK_RESOURCE = os.getenv('TRAVIAN_LOOK_RESOURCE', 'True').lower() == 'true'
        LOOK_BUILDING = os.getenv('TRAVIAN_LOOK_BUILDING', 'True').lower() == 'true'
else:
    # Configurações de produção, pegando variáveis de ambiente
    APP_ENABLE = os.getenv('APP_ENABLE', 'True').lower() == 'true'
    TEST_MODE = os.getenv('TRAVIAN_TEST_MODE', 'False').lower() == 'false' # Default em prod deve ser False
    IS_HEADLESS_MODE_ENABLED = os.getenv('TRAVIAN_HEADLESS', 'True').lower() == 'true'
    EMAIL = os.getenv('TRAVIAN_EMAIL') # Em prod, não deve haver default para credenciais
    PASSWORD = os.getenv('TRAVIAN_PASSWORD')
    GAMEWORLD = os.getenv('TRAVIAN_GAMEWORLD')
    MINTIME = int(os.getenv('TRAVIAN_MINTIME', 60)) # Tempos maiores em prod
    MAXTIME = int(os.getenv('TRAVIAN_MAXTIME', 120))
    LOOK_RESOURCE = os.getenv('TRAVIAN_LOOK_RESOURCE', 'True').lower() == 'true'
    LOOK_BUILDING = os.getenv('TRAVIAN_LOOK_BUILDING', 'True').lower() == 'true'