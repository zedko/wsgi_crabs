def add_custom_header(request):
    request['header'] = "CUSTOM_HEADER_VALUE"


middleware_list = [
    add_custom_header,
]