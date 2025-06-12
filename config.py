import os

EMAIL = os.getenv('TRAVIAN_EMAIL', 'email@teste.com')
PASSWORD = os.getenv('TRAVIAN_PASSWORD', 'senha123')
GAMEWORLD = os.getenv('TRAVIAN_GAMEWORLD', 'International 8')
MINTIME = int(os.getenv('TRAVIAN_MINTIME', 10))
MAXTIME = int(os.getenv('TRAVIAN_MAXTIME', 20))

USER_DATA_DIR = os.path.join(os.path.dirname(__file__), "chrome_profile")

TEST_MODE = os.getenv('TRAVIAN_TEST_MODE', 'True').lower() == 'true'
IS_HEADLESS_MODE_ENABLED = os.getenv('TRAVIAN_HEADLESS', 'True').lower() == 'true'
LOOK_RESOURCE = os.getenv('TRAVIAN_LOOK_RESOURCE', 'True').lower() == 'true'
LOOK_BUILDING = os.getenv('TRAVIAN_LOOK_BUILDING', 'True').lower() == 'true'