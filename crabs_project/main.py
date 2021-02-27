from framework import wsgi
from crabs_project import settings
from crabs_project.urls import router

wsgi.App.settings = settings
app = wsgi.App(routes=router)
