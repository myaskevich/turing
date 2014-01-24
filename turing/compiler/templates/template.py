#!/usr/bin/env python

import os
import sys
import traceback

from turing.runtime.state import UserState, InitialMixin, FinalMixin, \
    StateRegister
from turing.runtime.machine import Turing, TerminateException
from turing.tape import TapeError, TapeIsOverException, Tape
from turing.const import Move, Action


_states = set()
{% for state in context.states %}

class {{ state.class_name }}({{ state.modifiers }}):
    name = "{{ state.name }}"

    def _resolve(self, machine):
        {{ state.code|indent }}

_states.add({{ state.class_name }}())
{% endfor %}

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
            sys.stderr.write("terminated at '" + str(turing._register.current) + "'\n")
        else:
            sys.stderr.write("didn't terminate at either " + str(finals) + ". got " + str(turing._register.current) + "\n")
            ret = 1

    except TapeError, e:
        print "tape error:", str(e)
        ret = 2

    except TerminateException, e:
        if turing._register.current in finals:
            sys.stderr.write('terminated at ' + str(turing._register.current) + "\n")
        else:
            sys.stderr.write("didn't terminate at either " + str(finals) + ". got '" + str(turing._register.current) + "'\n")
            ret = 1

    finally:
        out_tape = str(turing._tape)

    return ret


if __name__ == '__main__':
    try:
        sys.exit(main(sys.args))
    except Exception:
        traceback.print_exc()
        sys.exit(1)

