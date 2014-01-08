
from turing.const import Direction, Action


class Turing(object):
    def __init__(self, tape):
        self._tape = tape
        self._state = state

    def move(self, direction):
        if direction == Direction.LEFT:
            self._tape.left()
            print self._tape.get()

        elif direction == Direction.RIGHT:
            self._tape.right()
            print self._tape.get()

        elif direction == Direction.NONE:
            print self._tape.get()

        else:
            assert 0   # sanity check

    def do(self, action, *args):
        if action == Action.WRITE:
            assert len(args) == 1
            self._tape.put(args[0])
            print 'put', args[0]

        elif action == Action.ERASE:
            self._tape.put(NULL)
            print 'erase'

        elif action == Action.NONE:
            print 'do nothing'

        else:
            assert 0  # sanity check

    def assume(self, state):
        self._state = state
