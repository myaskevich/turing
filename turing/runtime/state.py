
from turing.utils.normalize import get_state_name_norm

norm = get_state_name_norm()


class BaseState(object):
    def _initialize(self, machine):
        pass

    def _resolve(self, machine):
        raise NotImplementedError

    def _finalize(self, machine):
        pass

    def execute(self, machine):
        self._initialize(machine)
        try:
            self._resolve(machine)
        finally:
            self._finalize(machine)

    def getid(self):
        return norm(self.name)

    def __str__(self):
        return self.name

    def __repr__(self):
        return "'" + str(self.name) + "'"


class InitialMixin(object):
    def is_initial(self):
        return True


class FinalMixin(object):
    def is_final(self):
        return True


class UserState(BaseState):
    pass


class StateRegister(object):
    def __init__(self):
        self._current = None
        self._register = {}

    def get_initial(self):
        for state in self._register.values():
            try:
                if state.is_initial():
                    return state
            except AttributeError:
                pass
        return None

    def get_finals(self):
        finals = []

        for state in self._register.values():
            try:
                if state.is_final():
                    finals.append(state)
            except AttributeError:
                pass

        return tuple(finals)

    @property
    def current(self):
        return self._current

    def set_current(self, state):
        if isinstance(state, BaseState):
            self._current = self._register[state.getid()]
        else:
            self._current = self._register[norm(state)]

    def add_state(self, state):
        self._register[state.getid()] = state

    def get_state(self, name):
        return self._register[state.getid()]

    def __str__(self):
        return str(self._register)
