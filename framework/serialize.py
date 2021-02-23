import json


class JsonSerializer:
    def __init__(self, data):
        self.data = data

    def serialize(self) -> str:
        data = self._collect_dict()
        return json.dumps(data)

    def _collect_dict(self):
        data = self.data
        try:
            data = data.__dict__
        except AttributeError:
            if not isinstance(data, dict):
                raise TypeError(f'Cannot serialize {type(data)}. Provide an instance of class or dict')
        print(type(data), data)
        return data

    # TODO add include / exclude keys ability.
    def _include_exclude(self):
        pass


if __name__ == '__main__':
    from crabs_project.models import KitchenCourse


    test_dict = {
        "key": "value",
        "key2": "value2"
    }

    test_class = KitchenCourse('test course 1', price=95.5, desc="A simple kitchen course")

    test_string = "test"

    a = JsonSerializer(test_dict)
    b = JsonSerializer(test_class)
    c = JsonSerializer(test_string)

    print('dict: ', a.serialize())
    print('course: ', b.serialize())
    print('string', c.serialize())

