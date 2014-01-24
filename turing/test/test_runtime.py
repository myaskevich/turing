
from turing.runtime.example import main
from turing.tape import NullableTape


def turing(src):
    return main(['main.py', src])


def assert_turing(src, expected):
    tape = NullableTape(src)
    ret = turing(tape)
    out = str(tape)

    assert ret == 0, "machine didn't terminate"
    assert out == expected, src + " -/> " + expected + ", got " + out


def test_runtime():
    assert_turing('', '')
    assert_turing('00000000000000', 'xxxxxxxxxxxxxx')
    assert_turing('00010111011011', 'xxx1x111x11x11')
