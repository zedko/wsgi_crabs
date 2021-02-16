from copy import deepcopy


class PrototypeMixin:
    def copy(self):
        return deepcopy(self)
