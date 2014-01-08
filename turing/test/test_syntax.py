
import sys

from turing.syntax import parse

def test_state():
    assert parse(""" initial state do not make me sad { move left } """)
