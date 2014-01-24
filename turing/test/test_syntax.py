
import sys

from turing.syntax import parse

def test_state():
    print parse(open("examples/ends_with_zero.turing").read())
