import mock

from nose.tools import raises

from turing.core import Translator, Direction, Action
from turing.action import transition


def test_number():
    assert Translator().eval('3') == ['3']
    assert Translator().eval(' 2 ') == ['2']

def test_char():
    assert Translator().eval("a") == ['a']
    assert Translator().eval("Z") == ['Z']

@raises(AssertionError)
def test_string():
    assert Translator().eval("abc") == ['a']

def _test_move():
    turing = Translator()
    machine = mock.Mock(wraps=turing)

    machine.eval("move left")
    machine.move.assert_called_with(Direction.LEFT)

    machine.eval("move right")
    machine.move.assert_called_with(Direction.RIGHT)

    machine.eval("no move")
    machine.move.assert_called_with(Direction.NONE)

def _test_write():
    turing = Translator()
    machine = mock.Mock(wraps=turing)

    machine.eval("write 1")
    machine.do.assert_called_with(Action.WRITE, 1)

    machine.eval("write a")
    machine.do.assert_called_with(Action.WRITE, 'a')

def _test_erase():
    turing = Translator()
    machine = mock.Mock(wraps=turing)

    machine.eval("erase")
    machine.do.assert_called_with(Action.ERASE)

def _test_assume():
    turing = Translator()
    machine = mock.Mock(wraps=turing)

    machine.eval("assume state 1")
    machine.assume.assert_called_with("state 1")
