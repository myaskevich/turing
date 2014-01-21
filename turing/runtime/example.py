
import os
import sys
import traceback

from turing.runtime.state import UserState, InitialMixin, FinalMixin, \
    StateTable
from turing.runtime.machine import Turing, TerminateException
from turing.tape import TapeError
from turing.const import Move, Action


_states = set()


class DoesNotEndWithZero_State(UserState, InitialMixin, FinalMixin):
    name = "does not end with zero"

    def _resolve(self, machine):
        if machine.head == '0' :
            machine.assume('endswithzero')

        else:
            machine.assume('doesnotendwithzero')

        machine.do(Action.NONE)

        machine.move(Move.RIGHT)

_states.add(DoesNotEndWithZero_State())


class EndsWithZero_State(UserState, FinalMixin):
    name = "ends with zero"

    def _resolve(self, machine):
        if machine.head == '0':
            machine.assume('endswithzero')

        else:
            machine.assume('doesnotendwithzero')

        machine.do(Action.WRITE, 'x')

        machine.move(Move.RIGHT)

_states.add(EndsWithZero_State())


def make_state_table():
    table = StateTable()

    for state in _states:
        table.add_state(state)

    return table


def main(args):
    msg = "Expected single command line argument, got " + str(len(args))
    assert len(args) == 2, msg
    arg = args[1]

    if os.path.isfile(arg):
        src = ""
        with open(arg, 'rb') as file:
            src = file.read()
    else:
        src = arg

    turing = Turing(src)
    sys.stderr.write("-> " + str(turing._tape) + "\n")

    state_table = make_state_table()
    state_table.set_current(state_table.get_initial().getid())

    turing.set_states(state_table)

    try:
        turing.start()

    except TapeError, e:
        print "tape error:", str(e)

    except TerminateException:
        print "terminated"

    finally:
        out_tape = str(turing._tape)
        sys.stderr.write("<- " + out_tape + "\n")

    return out_tape


if __name__ == '__main__':
    try:
        main(sys.args)
        sys.exit(0)
    except Exception:
        traceback.print_exc()
        sys.exit(1)
