
def transition(direction=None, action=None, state=None, args=()):
    def alter(machine):
        if direction is not None:
            machine.move(direction)

        if action is not None:
            machine.do(action, *args)

        if state is not None:
            machine.assume(state)

    return alter


def move_closure(direction):
    return transition(direction=direction)


def do_closure(action, *args):
    return transition(action=action, args=args)


def assume_closure(state):
    return transition(state=state)
