
import traceback

from turing.compiler.main import main


def turingc(*args):
    main(["main.py"] + list(args))


def assert_turingc_ok(*args):
    try:
        turingc(*args)
    except SystemExit, e:
        assert e.code == 0
    except:
        raise


def assert_turingc_fails(*args):
    try:
        turingc(*args)
    except SystemExit, e:
        assert e.code == 1
    except:
        raise

    assert False


# def test_file_argument():
#     assert_turingc_fails()


def test_examples():
    assert_turingc_ok("examples/ends_with_zero.turing")
