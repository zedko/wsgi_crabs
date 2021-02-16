import crabs_project.middleware
import os
from mods.loggar import Loggar

ROOT_DIR = os.path.join('../', os.path.abspath(os.getcwd()))
STATIC_FILES_DIR = os.path.join(ROOT_DIR, 'staticfiles')
STATIC_URL = '/static/'  # all urls that starts with STATIC_URL will be considered as request for static file
MIDDLEWARE = crabs_project.middleware.middleware_list

# global logger setup
LOGGER = Loggar()
LOGGER.set_file(os.path.join(ROOT_DIR, 'log.log'))
LOGGER.set_level('info')
