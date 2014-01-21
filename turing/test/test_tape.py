import unittest

from nose.tools import raises

from turing.tape import Tape, NullableTape, ExtendableTape, \
    EXPAND_CHAR, NULL, TapeError


class TapeTestCase(unittest.TestCase):

    @raises(TapeError)
    def test_get_fails_on_empty_tape(self):
        tape = Tape('')
        tape.get()

    @raises(TapeError)
    def test_get_fails_when_head_is_out_of_left_bound(self):
        tape = Tape('123')
        tape.get()
        tape.left()
        tape.get()

    @raises(TapeError)
    def test_get_fails_when_head_is_out_of_right_bound(self):
        tape = Tape('123')
        tape.get()
        tape.right()
        tape.get()
        tape.right()
        tape.get()
        tape.right()

    @raises(TapeError)
    def test_put_fails_on_empty_tape(self):
        tape = Tape('')
        tape.put('a')


class NullableTapeTestCase(unittest.TestCase):
    def test_get_on_empty_tape(self):
        assert NULL == NullableTape('').get()


class ExtandableTapeTestCase(unittest.TestCase):

    def test_get(self):
        tape = ExtendableTape("0101010110101")

        tape         ; assert tape.get() == '0'
        tape         ; assert tape.get() == '0'
        tape.left()  ; assert tape.get() == EXPAND_CHAR
        tape.left()  ; assert tape.get() == EXPAND_CHAR
        tape.right() ; assert tape.get() == EXPAND_CHAR
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
        tape.right() ; assert tape.get() == EXPAND_CHAR
        tape.right() ; assert tape.get() == EXPAND_CHAR
        tape.right() ; assert tape.get() == EXPAND_CHAR
        tape.left()  ; assert tape.get() == EXPAND_CHAR
        tape.left()  ; assert tape.get() == EXPAND_CHAR
        tape.left()  ; assert tape.get() == '1'
        tape         ; assert tape.get() == '1'
        tape         ; assert tape.get() == '1'


    def test_put(self):
        tape = ExtendableTape()

        for j in range(10):
            for i in range(10):
                tape.put(str(i))
                tape.right()

            for k in range(9):
                tape.left()

        result = "0000000000123456789"
        assert tape == result, "'" + tape + "' != '" + result + "'"


        tape = ExtendableTape()

        for j in reversed(range(10)):
            for i in reversed(range(10)):
                tape.put(str(i))
                tape.left()

            for k in reversed(range(9)):
                tape.right()

        result = "0123456789999999999"

        assert tape == result, "'" + tape + "' != '" + result + "'"
