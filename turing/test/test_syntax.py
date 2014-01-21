
import sys

from turing.syntax import parse

def test_state():
    parse("""
        initial state do not make me sad { move left } 
        initial state do not make me sad { move left } 
    """)
