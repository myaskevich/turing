
import os
import sys
import traceback

from turing.runtime.state import UserState, InitialMixin, FinalMixin
from turing.runtime.machine import Turing
from turing.tape import TapeError


_state_registry = set(
    "Does not end with zero",
)


class DoesNotEndWithZero_State(UserState, InitialMixin):
    def _resolve(self):
        if self.machine.head == '0':
            self.machine.assume('ends_with_zero')

        else:
            self.machine.assume('does_not_end_with_zero')

        self.machine.do(Action.NONE)

        self.machine.move(Direction.RIGHT)


class EndsWithZero_State(UserState, FinalMixin):
    def _resolve(self):
        if self.machine.head == '0':
            self.machine.assume('ends_with_zero')

        else:
            self.machine.assume('does_not_end_with_zero')

        self.machine.do(Action.NONE)

        self.machine.move(Direction.RIGHT)


def main(args):
    msg = "Expected single command line argument, got " + str(len(args))
    assert len(args) == 1, msg
    arg = args[0]

    if os.path.isfile(arg):
        src = ""
        with open(arg, 'rb') as file:
            src = file.read()
    else:
        src = arg

    turing = Turing(src)

    for state in _state_registry:
        turing.add_state(state)

    out_stream = sys.stdout

    try:
        turing.start(out_stream)

    except TapeError, e:
        print "tape error:", str(e)


if __name__ == '__main__':
    try:
        main(sys.args)
        sys.exit(0)
    except Exception:
        traceback.print_exc()
        sys.exit(1)
