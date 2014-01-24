
from turing.runtime.example import main


def turing(src):
    return main(['main.py', src])


def assert_turing(src, expected):
    out = turing(src)
    assert out == expected, src + " -/> " + expected + ", got " + out


def test_runtime():
    assert_turing('', '')
    assert_turing('00000000000000', 'xxxxxxxxxxxxxx')
    assert_turing('00010111011011', 'xxx1x111x11x11')
