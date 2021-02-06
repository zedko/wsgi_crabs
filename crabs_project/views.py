from jinja2 import Environment, PackageLoader, select_autoescape
env = Environment(
    loader=PackageLoader('crabs_project', 'templates'),
    autoescape=select_autoescape(['html', 'xml'])
)


def index(request):
    template = env.get_template('index.html')
    content = {
        'name': 'Crabs',
        'text': 'Blah blah'
    }
    print(request['query_string'])
    content_text = template.render(content)
    status_code = '200 OK'
    return content_text, status_code


def non_index(request):
    content_text = 'Go back to welcoming page'
    status_code = '200 OK'
    return content_text, status_code


def form(request):
    template = env.get_template('form.html')
    content = {

    }
    content_text = template.render(content)
    status_code = '200 OK'
    if request['method'] == 'POST':
        print("QUERY STRING: ", request['body'])
    return content_text, status_code
