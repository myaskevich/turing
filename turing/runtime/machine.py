
import sys

from turing.const import Move, Action
from turing.tape import TapeIsOverException, NullableTape, Tape


class TerminateException(Exception):
    pass


MAX_STATE_LOOP = 1000000L


class Turing(object):
    def __init__(self, src, out=sys.stdout):
        if isinstance(src, Tape):
            self._tape = src
        else:
            self._tape = NullableTape(src)
        self._states = None
        self._outstream = out

    def set_states(self, table):
        self._states = table

    @property
    def head(self):
        return self._tape.get()

    def move(self, direction):
        # if direction == Move.LEFT:
        #     self._tape.left()
        #     print self._tape.get()

        if direction == Move.RIGHT:
            self._tape.right()

        elif direction == Move.NONE:
            pass

        else:
            assert 0   # sanity check

    def do(self, action, *args):
        if action == Action.WRITE:
            assert len(args) == 1
            self._tape.put(args[0])

        elif action == Action.ERASE:
            self._tape.put(NULL)

        elif action == Action.NONE:
            pass

        else:
            assert 0  # sanity check

    def assume(self, state_name):
        self._states.set_current(state_name)

    def start(self):
        watch_state = None
        watch_state_iter = 0

        while True:
            current = self._states.current
            current.execute(self)

            if current == watch_state:
                assert watch_state_iter < MAX_STATE_LOOP, "MAX_STATE_LOOP exceeded"
                watch_state_iter += 1
            else:
                watch_state = current
                watch_state_iter = 0
