
class BaseState(object):
    def exec(self, machine):
        self._initialize(machine)
        self._resolve(machine)
        self._finalize(machine)


class InitialMixin(object):
    def is_initial(self):
        return True


class FinalMixin(object):
    def is_final(self):
        return True


class UserState(BaseState):
    pass
