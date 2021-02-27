import crabs_project.middleware
import os
from pathlib import Path
from mods.loggar import Loggar

DEBUG = False

ROOT_DIR = Path(__file__).resolve().parent.parent
STATIC_FILES_DIR = os.path.join(ROOT_DIR, 'staticfiles')
STATIC_URL = '/static/'  # all urls that starts with STATIC_URL will be considered as request for static file
MIDDLEWARE = crabs_project.middleware.middleware_list

# global logger setup
LOGGER = Loggar()
LOGGER.set_file(os.path.join(ROOT_DIR, 'log.log'))
LOGGER.set_level('info')

SQLITE_DB_NAME = 'db.sqlite'
DATABASE_CONNECT = os.path.join(ROOT_DIR, SQLITE_DB_NAME)
