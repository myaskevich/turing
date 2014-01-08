
import os
import sys
import traceback

from turing.runtime.machine import Turing


_state_registry = set(
    "Does not end with zero",
)


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
    turing.start(out_stream)


if __name__ == '__main__':
    try:
        main(sys.args)
        sys.exit(0)
    except Exception:
        traceback.print_exc()
        sys.exit(1)
