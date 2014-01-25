#!/usr/bin/env python

import os
import optparse
import sys
import traceback

from turing.runtime.state import UserState, InitialMixin, FinalMixin, \
    StateRegister
from turing.runtime.machine import Turing, TerminateException
from turing.tape import TapeError, TapeIsOverException, Tape
from turing.const import Move, Action


_states = set()
{% for state in states %}
{{ state }}
{% endfor %}

def make_state_table():
    table = StateRegister()

    for state in _states:
        table.add_state(state)

    return table


def make_parser():
    usage = "Usage: %s INPUT" % __file__
    parser = optparse.OptionParser(usage=usage)

    parser.add_option("-t", "--trace", action='store_true',
                      dest="trace", default=False,
                      help="Run program in trace mode")

    return parser


def puts(*msg):
    print "turing:",
    for m in msg:
        print m,
    print


def fail(code, *msg):
    puts(*msg)
    sys.exit(code)


def main(argv=sys.argv):
    parser = make_parser()
    options, arguments = parser.parse_args(argv[1:])

    if not arguments:
        parser.print_usage()
        fail(1, "fatal error: no input files")

    source = arguments.pop(0)

    run_machine(source, trace=options.trace)


def run_machine(source, trace=False):

    if isinstance(source, Tape):
        raw = source
    elif os.path.isfile(source):
        with open(source, 'rb') as file:
            raw = file.read()
    else:
        raw = source

    turing = Turing(raw)
    start_tape = str(raw)

    state_register = make_state_table()
    initial = state_register.get_initial()
    finals = state_register.get_finals()

    turing.set_state_register(state_register)
    state_register.set_current(initial.getid())

    try:
        puts("started at", "'" + str(initial) + "'")
        turing.start(trace=trace)

    except (TapeIsOverException, TerminateException), e:
        if turing._register.current in finals:
            puts("terminated at", "'" + str(turing._register.current) + "'")
        else:
            fail(1, "failed at", "'" + str(turing._register.current) + "'")

    except TapeError, e:
        fail(2, "tape error:", e)

    finally:
        end_tape = str(turing._tape)

        puts("<-", start_tape)
        puts("->", end_tape)


if __name__ == '__main__':
    main()
    sys.exit(0)
