
import sys

from turing.syntax import parse

def test_state():
    for state in parse("""
    initial state do not make me sad { move left } 
    initial state do not make me sad { move left } 
"""):
        sys.stderr.write(state.text + '\n')
