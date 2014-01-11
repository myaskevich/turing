

class State(object):
    def resolve(self, machine):
        raise NotImplementedError


class InitialState(object):
    pass


class FinalState(object):
    pass


class DoesNotEndWithZero_State(InitialState):
    def resolve(self, machine):
        if machine.head == '0':
            machine.assume(get_state("ends_with_zero"))

        else:
            machine.assume(get_state("does_not_end_with_zero"))

        machine.move(Direction.RIGHT)


class EndsWithZero_State(FinalState):
    def resolve(self, machine):
        if machine.head == '0':
            machine.assume(get_state("ends_with_zero"))

        else:
            machine.assume(get_state("does_not_end_with_zero"))

        machine.do(Action.NONE)

        machine.move(Direction.RIGHT)
