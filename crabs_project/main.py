from framework import wsgi
from crabs_project import settings
from crabs_project.urls import router

app = wsgi.App(settings, routes=router)
