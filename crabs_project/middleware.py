def add_custom_header(request):
    request['header'] = 'test_header_value'


middleware_list = [
    add_custom_header,
]
