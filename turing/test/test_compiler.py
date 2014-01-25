
import os

from os.path import join, splitext

from turing.compiler.main import main, compile_source


def turingc_cmd(*args):
    main(["main.py"] + list(args))


def turingc(source):
    compile_source(source, os.devnull)


def assert_turingc_ok(source):
    try:
        turingc(source)
    except SystemExit, e:
        assert e.code == 0, "turingc returned %d" % e.code
    except:
        raise


def assert_turingc_fails(source):
    try:
        turingc(source)
    except SystemExit, e:
        assert e.code == 1, "turingc returned %d" % e.code
    except:
        raise
    else:
        assert 0, "turingc didn't fail"


def assert_turingc_cmd_ok(*args):
    try:
        turingc_cmd(*args)
    except SystemExit, e:
        assert e.code == 0, "turingc returned %d" % e.code
    except:
        raise


def assert_turingc_cmd_fails(*args):
    try:
        turingc_cmd(*args)
    except SystemExit, e:
        assert e.code == 1, "turingc returned %d" % e.code
    except:
        raise
    else:
        assert 0


def test_file_argument():
    assert_turingc_cmd_fails()
    assert_turingc_cmd_fails('not a file')


def test_compile_examples():
    for filename in os.listdir("examples"):
        output = splitext(filename)[0] + '.turc'
        assert_turingc_cmd_ok(join("examples", filename), '-o', output)


def test_empty_state():
    assert_turingc_ok(" state empty { do nothing } ")
    assert_turingc_ok(" state empty { } ")


def test_error_reporting():
    assert_turingc_ok("""\
state jog {
    if head is 1 then
        assume head is 1
    else if head is 2 then
        assume head is 2
    else
        assume head is not 1 or 2
    endif

    do nothing
}
state walk {
    do write 1
}
""")
