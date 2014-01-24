
class BaseContext(object):
    def __init__(self, node):
        self._node = node


class StateContext(BaseContext):
    @property
    def name(self):
        pass

    @property
    def class_name(self):
        pass

    @property
    def modifiers(self):
        pass

    @property
    def code(self):
        pass


class TuringContext(BaseContext):
    @property
    def states(self):
        for state_node in self._node:
            yield StateContext(state_node)
