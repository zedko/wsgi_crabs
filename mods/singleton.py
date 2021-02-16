def singleton_decorator(cls):
    storage = {}

    def inner(*args, **kwargs):
        if cls not in storage:
            storage[cls] = cls(*args, *kwargs)
        return storage[cls]

    return inner
