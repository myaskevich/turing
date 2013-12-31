import mock

from pytest import raises

from turing import Turing, Direction, Action
from turing.action import transition


def test_number():
    assert Turing().eval('123') == [123]
    assert Turing().eval(' 123 ') == [123]
    assert Turing().eval('1 123 ') == [1, 123]
    assert Turing().eval(' 123 2') == [123, 2]

def test_char():
    assert Turing().eval("a") == ['a']
    with raises(AssertionError):
        assert Turing().eval("abc") == ['a']
    assert Turing().eval("Z") == ['Z']

def test_move():
    turing = Turing()
    machine = mock.Mock(wraps=turing)

    machine.eval("move left")
    machine.move.assert_called_with(Direction.LEFT)

    machine.eval("move right")
    machine.move.assert_called_with(Direction.RIGHT)

    machine.eval("no move")
    machine.move.assert_called_with(Direction.NONE)

def test_write():
    turing = Turing()
    machine = mock.Mock(wraps=turing)

    machine.eval("write 1")
    machine.do.assert_called_with(Action.WRITE, 1)

    machine.eval("write a")
    machine.do.assert_called_with(Action.WRITE, 'a')

def test_erase():
    turing = Turing()
    machine = mock.Mock(wraps=turing)

    machine.eval("erase")
    machine.do.assert_called_with(Action.ERASE)

def test_assume():
    turing = Turing()
    machine = mock.Mock(wraps=turing)

    machine.eval("assume state 1")
    machine.assume.assert_called_with("state 1")
