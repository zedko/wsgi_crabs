import jsonpickle


class JsonSerializer:
    def __init__(self, data):
        self.data = data

    def serialize(self) -> str:
        self._include_exclude()
        return jsonpickle.dumps(self.data, unpicklable=False)

    # TODO add include / exclude keys ability.
    def _include_exclude(self):
        pass


if __name__ == '__main__':
    from crabs_project.models import KitchenCourse, AppData
    real_data = AppData()
    real_data.set_test_data()

    test_dict = {
        "key": "value",
        "key2": "value2"
    }

    test_class = KitchenCourse('test course 1', price=95.5, desc="A simple kitchen course")

    test_string = "test"

    a = JsonSerializer(test_dict)
    b = JsonSerializer(test_class)
    c = JsonSerializer(test_string)
    x = JsonSerializer(real_data.courses)

    print('dict: ', a.serialize())
    print('course: ', b.serialize())
    print('string', c.serialize())
    print('real data: ', x.serialize())

