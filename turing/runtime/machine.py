
from turing.const import Direction, Action
from turing.tape import TapeIsOverException


class Turing(object):
    def __init__(self, tape, init_state):
        self._tape = tape
        self._state = init_state

    @property
    def head(self):
        return self._tape.get()

    def move(self, direction):
        # if direction == Direction.LEFT:
        #     self._tape.left()
        #     print self._tape.get()

        if direction == Direction.RIGHT:
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

    def start(self, out_stream):
        try:
            self._state.resolve(self)
        except TapeIsOverException:
            # Just terminate
