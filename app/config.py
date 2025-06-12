import os
from config_dev import MODO_DESENVOLVIMENTO,EMAIL_DEV, PASSWORD_DEV,TEST_MODE_DEV,APP_ENABLE_DEV,IS_HEADLESS_MODE_ENABLED_DEV,MINTIME_DEV,MAXTIME_DEV,LOOK_RESOURCE_DEV,LOOK_BUILDING_DEV,GAMEWORLD_DEV
# Importando as variáveis de ambiente do arquivo config_dev.py

if MODO_DESENVOLVIMENTO:
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
else:
    # Configurações do aplicativo pegando variáveis de ambiente
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