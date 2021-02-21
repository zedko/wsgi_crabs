from time import time


def work_time(func):
    def inner(*args, **kwargs):
        current_time = time()
        result = func(*args, **kwargs)
        print(f'FUNC {func.__module__}.{func.__name__} TIME SPENT ---> {time() - current_time}')
        return result
    return inner
