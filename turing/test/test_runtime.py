
from turing.runtime.example import main
from turing.tape import NullableTape


def turing(src):
    return main(['main.py', src])


def assert_turing_ok(src, expected):
    tape = NullableTape(src)
    ret = turing(tape)
    out = str(tape)

    assert ret == 0, "machine didn't terminate"
    assert out == expected, src + " -/> " + expected + ", got " + out


def assert_turing_ko(src, expected):
    tape = NullableTape(src)
    ret = turing(tape)
    out = str(tape)

    assert ret == 1, "machine terminate when it shouldn't have"
    assert out == expected, src + " -/> " + expected + ", got " + out


def test_runtime():
    assert_turing_ko('', '')
    assert_turing_ok('00000000000000', 'xxxxxxxxxxxxxx')
    assert_turing_ko('00010111011011', 'xxx10111011011')
