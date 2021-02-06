import crabs_project
import os

ROOT_DIR = os.path.join('../', os.path.abspath(os.curdir))
STATIC_FILES_DIR = os.path.join(ROOT_DIR, 'staticfiles')
STATIC_URL = '/static/'  # all urls that starts with STATIC_URL will be considered as request for static file
ROUTES = crabs_project.urls.router
MIDDLEWARE = crabs_project.middleware.middleware_list
