
from turing.tape import Tape, NULL


def test_get():
    tape = Tape("0101010110101")

    tape         ; assert tape.get() == '0'
    tape         ; assert tape.get() == '0'
    tape.left()  ; assert tape.get() == NULL
    tape.left()  ; assert tape.get() == NULL
    tape.right() ; assert tape.get() == NULL
    tape.right() ; assert tape.get() == '0'
    tape.right() ; assert tape.get() == '1'
    tape.right() ; assert tape.get() == '0'
    tape.right() ; assert tape.get() == '1'
    tape.right() ; assert tape.get() == '0'
    tape.left()  ; assert tape.get() == '1'
    tape.right() ; assert tape.get() == '0'
    tape.right() ; assert tape.get() == '1'
    tape.right() ; assert tape.get() == '0'
    tape.right() ; assert tape.get() == '1'
    tape.right() ; assert tape.get() == '1'
    tape.right() ; assert tape.get() == '0'
    tape.right() ; assert tape.get() == '1'
    tape.right() ; assert tape.get() == '0'
    tape.right() ; assert tape.get() == '1'
    tape.right() ; assert tape.get() == NULL
    tape.right() ; assert tape.get() == NULL
    tape.right() ; assert tape.get() == NULL
    tape.left()  ; assert tape.get() == NULL
    tape.left()  ; assert tape.get() == NULL
    tape.left()  ; assert tape.get() == '1'
    tape         ; assert tape.get() == '1'
    tape         ; assert tape.get() == '1'


def test_put():
    tape = Tape()

    for j in range(10):
        for i in range(10):
            tape.put(str(i))
            tape.right()

        for k in range(9):
            tape.left()

    result = "0000000000123456789"
    assert tape == result, "'" + tape + "' != '" + result + "'"


    tape = Tape()

    for j in reversed(range(10)):
        for i in reversed(range(10)):
            tape.put(str(i))
            tape.left()

        for k in reversed(range(9)):
            tape.right()

    result = "0123456789999999999"

    assert tape == result, "'" + tape + "' != '" + result + "'"
