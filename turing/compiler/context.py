
import re


def class_name_norm(name):
    class_name = re.sub("\s+", ' ', name.text)
    class_name = re.sub(' ', '_', class_name)
    class_name = re.sub('[^a-zA-Z0-9 _]', '', class_name)

    return class_name


class BaseContext(object):
    def __init__(self, node):
        self._node = node


class StateContext(BaseContext):
    @property
    def name(self):
        _, _, _, _, _, name, _, _, _, _, _, _, _ = self._node

        return name.text

    @property
    def class_name(self):
        _, _, _, _, _, name, _, _, _, _, _, _, _ = self._node

        return class_name_norm(name)

    @property
    def modifiers(self):
        _, modifier, _, _, _, _, _, _, _, _, _, _, _ = self._node

        modifiers = "UserState"

        if modifier.text == "initial":
            modifiers += ", InitialMixin"

        if modifier.text == 'final':
            modifiers += ', FinalMixin'

        return modifiers

    @property
    def code(self):
        _, _, _, _, _, _, _, _, _, code, _, _, _ = self._node

        return code.text


class TuringContext(BaseContext):
    @property
    def states(self):
        for state_node in self._node:
            yield StateContext(state_node)
