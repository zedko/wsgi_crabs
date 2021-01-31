from crabs_project.urls import router
from crabs_project.middleware import middleware_list
from os import path, getcwd

# TODO move all settings to project scoped file
STATIC_FILES_DIR = '/staticfiles/'
STATIC_URL = '/static/'


class App:
    def __init__(self, routes: dict, middleware: list):
        self.router = routes
        self.middleware = middleware

    def __call__(self, environ, start_response):
        print('=' * 10)
        for (key, value) in environ.items():
            print(key, value)
        print('+' * 10)

        url_path: str = environ['PATH_INFO']
        content_type: str = "text/html"

        request = {}
        for ware in self.middleware:
            ware(request)

        # make sure that both URL (in environ['PATH_info'] and in routes dict) have slashes as last symbol
        if self.fix_url_slash(url_path) in (self.fix_url_slash(key) for key in router.keys()):
            data, status = self.router[url_path](request)

        elif url_path.startswith(STATIC_URL):
            # TODO add dictionary with content-types (suggest look at files extensions. E.g. .css -> Content-type: text/css
            content_type = "text/css"
            file_path = url_path[len(STATIC_URL):]
            data, status = self.get_static(STATIC_FILES_DIR, file_path)
        else:
            data, status = response_404(request)

        start_response(status, [
            ("Content-Type", content_type),
            ("Content-Length", str(len(data))),
            ("CUSTOM_HEADER", request.get("header"))  # добавляем значение из middleware
        ])

        binary_data = data.encode(encoding='utf-8')
        return [binary_data]

    @staticmethod
    def fix_url_slash(path: str):
        """
        Adds slash at the end of path
        """
        if path[-1] != '/':
            path += '/'
        return path

    @staticmethod
    def get_static(static_dir, file_path):
        # TODO define root dir in settings
        path_to_file = path.join('staticfiles', file_path)
        print(path_to_file, getcwd())
        with open(path_to_file, 'r') as f:
            file_content = f.read().replace('\n', '')
        status_code = '200 OK'
        return file_content, status_code



def response_404(request):
    content_text = 'Gunicorn cannot find the page you looking for'
    status_code = '404 NOT FOUNDED'
    return content_text, status_code


app = App(router, middleware_list)
