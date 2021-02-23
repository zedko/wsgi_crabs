import crabs_project.settings as settings
from framework.wsgi import App
from framework.render import render
from crabs_project.models import AppData, Student, Chef
from framework.wsgi_cbv import BaseView
from framework.serialize import JsonSerializer
from mods.loggar import Loggar
from mods.work_time import work_time


log = Loggar()
# TODO fix save and load pickled data
app_data = AppData()
app_data.set_test_data()

static_url = settings.STATIC_URL
jinja_loader_params = ('crabs_project', 'templates')


class IndexPage(BaseView):
    template = 'index.html'

    def get_context(self) -> dict:
        content = app_data.get_context_data('courses', 'professions', 'users')
        content['user'] = app_data.get_active_user()
        print("REQUEST_DATA: -----> ", self.request)
        print("CONTENT: -----> ", content)
        return content

# @work_time
# def index(request):
#     content = app_data.get_context_data('courses', 'professions', 'users')
#     content['user'] = app_data.get_active_user()
#     content_text = render('index.html', loader_params=jinja_loader_params, static_url=static_url, **content)
#     status_code = '200 OK'
#     log.info(f'{request["url"]}, {status_code}')
#     return content_text, status_code


def non_index(request):
    content_text = 'Go back to welcoming page'
    status_code = '200 OK'
    return content_text, status_code


def participate(request):
    content = app_data.get_context_data('courses', 'professions', 'users')
    content['user'] = app_data.get_active_user()
    content_text = render('participate.html', loader_params=jinja_loader_params, static_url=static_url, **content)
    status_code = '200 OK'
    if request['method'] == 'POST':
        print("QUERY STRING: ", request['body'])
    return content_text, status_code


def courses(request):
    # TODO make buying courses awailible in all functions
    print(request)
    if request['method'] == 'GET':
        try:
            course_title = request['query_string']['course']
            course = app_data.get_course(course_title)
            user = app_data.get_active_user()
            if isinstance(user, Student):
                user.buy_course(course)
            if isinstance(user, Chef):
                user.authorize_for_course(course)
        except TypeError:
            pass
    if request['method'] == 'POST':
        course_data = request['body']
        app_data.add_course(**course_data)
    content = app_data.get_context_data('courses', 'users')
    content['user'] = app_data.get_active_user()
    content_text = render('courses.html', loader_params=jinja_loader_params, static_url=static_url, **content)
    status_code = '200 OK'
    return content_text, status_code


def professions(request):
    content = app_data.get_context_data('professions', 'users')
    content['user'] = app_data.get_active_user()

    content_text = render('professions.html', loader_params=jinja_loader_params, static_url=static_url, **content)
    status_code = '200 OK'
    return content_text, status_code


@work_time
def api_courses(request):
    json_ = JsonSerializer(app_data.courses).serialize()
    content_text = json_
    status_code = '200 OK'
    return content_text, status_code


@App.add_route('/test/')
def buy_course(request):
    for __, _ in request.items():
        print(__, _)
    if request['method'] == 'POST':
        print('ALRIGHT')
    status_code = '200 OK'
    content_text = "It worked"
    return content_text, status_code


