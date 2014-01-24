
import os
import sys
import traceback

from turing.runtime.state import UserState, InitialMixin, FinalMixin, \
    StateRegister
from turing.runtime.machine import Turing, TerminateException
from turing.tape import TapeError, TapeIsOverException, Tape
from turing.const import Move, Action


_states = set()


class DoesNotEndWithZero_State(UserState, InitialMixin, FinalMixin):
    name = "does not end with zero"

    def _resolve(self, machine):
        if machine.head == '0' :
            machine.assume('endswithzero')
            machine.do(Action.WRITE, 'x')

        else:
            machine.assume(self)

        machine.move(Move.RIGHT)

_states.add(DoesNotEndWithZero_State())


class EndsWithZero_State(UserState, FinalMixin):
    name = "ends with zero"

    def _resolve(self, machine):
        if machine.head == '0' :
            machine.assume(self)
            machine.do(Action.WRITE, 'x')

        else:
            machine.assume('doesnotendwithzero')

        machine.move(Move.RIGHT)

_states.add(EndsWithZero_State())


def make_state_table():
    table = StateRegister()

    for state in _states:
        table.add_state(state)

    return table


def main(args):
    msg = "Expected single command line argument, got " + str(len(args))
    assert len(args) == 2, msg
    arg = args[1]

    if isinstance(arg, Tape):
        src = arg
    elif os.path.isfile(arg):
        src = ""
        with open(arg, 'rb') as file:
            src = file.read()
    else:
        src = arg

    turing = Turing(src)
    sys.stderr.write("-> " + str(turing._tape) + "\n")

    state_register = make_state_table()
    initial = state_register.get_initial()
    finals = state_register.get_finals()

    turing.set_state_register(state_register)
    state_register.set_current(initial.getid())

    ret = 0

    try:
        turing.start()

    except TapeIsOverException, e:
        # print e
        if turing._register.current in finals:
            sys.stderr.write('terminated at ' + str(turing._register.current) + "\n")
        else:
            sys.stderr.write("didn't terminate at either " + str(finals) + ". got " + str(turing._register.current) + "\n")
            ret = 1

    except TapeError, e:
        print "tape error:", str(e)
        ret = 2

    except TerminateException, e:
        pass

    finally:
        out_tape = str(turing._tape)
        sys.stderr.write("<- " + out_tape + "\n")

    return ret


if __name__ == '__main__':
    try:
        sys.exit(main(sys.args))
    except Exception:
        traceback.print_exc()
        sys.exit(1)
