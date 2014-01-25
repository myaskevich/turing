
from nose.tools import ok_

from turing.syntax import parse


def test_state():
    ok_(parse(open("examples/ends_with_zero.turing").read()))
