from framework.render import render


class BaseView:
    template = 'index.html'
    status_code = '200 OK'
    content_text = ''
    request = {}

    def get_context(self) -> dict:
        return {}

    def render(self, jinja_loader_params, static_url: str):
        template = self.__class__.template
        context: dict = self.get_context()
        self.content_text = render(template, jinja_loader_params, static_url, **context)
        return self.content_text, self.status_code

    def __call__(self, request):
        self.request = request
        return self.render(('crabs_project', 'templates'), '/static/')
