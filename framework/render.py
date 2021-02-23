from jinja2 import Environment, PackageLoader, select_autoescape


# TODO find out how to fix the need of passing loader_params and static_url
def render(template_name: str, loader_params=('crabs_project', 'templates'), static_url: str='/static/', **kwargs):
    """
    :param template_name provide a template name as str like 'index.html'
    :param loader_params provide a package tuple ('package_name', 'template_folder_name')
    :param static_url provide a static url as str like '/static/'
    """
    env = Environment(
        loader=PackageLoader(*loader_params),
        autoescape=select_autoescape(['html', 'xml'])
    )
    env.globals['static'] = static_url

    template = env.get_template(template_name)
    return template.render(**kwargs)
