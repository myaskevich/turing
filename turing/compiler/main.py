
import optparse
import sys
import traceback

from os.path import join, dirname, isfile

from jinja2 import Template
from parsimonious.exceptions import ParseError

from turing.syntax import parse, TuringSyntaxError


TEMPLATE_PATH = join(dirname(__file__), 'templates', 'template.txt')


def make_parser():
    usage = "Usage: turingc FILE [OPTIONS]"
    parser = optparse.OptionParser(usage=usage)

    parser.add_option("-o",
                      dest="output", default="a.turc",
                      help='Place the output into FILE')

    parser.add_option("-d", '--debug', action='store_true',
                      dest="debug", default=False,
                      help='Activate debug mode')

    return parser


def puts(*msg):
    print "turingc:",
    for m in msg:
        print m,
    print


def fail(*msg):
    puts(*msg)
    sys.exit(1)


def main(argv=sys.argv):
    parser = make_parser()
    options, arguments = parser.parse_args(argv[1:])

    if not arguments:
        parser.print_usage()
        fail("fatal error: no input files")

    input_file = arguments.pop(0)

    if isfile(input_file):
        source = open(input_file, 'rb').read()
    else:
        puts("no such file or directory")
        fail("fatal error: no input files")

    compile_source(source, options.output)


def compile_source(source, output):
    try:
        node = parse(source)

    except (ParseError, TuringSyntaxError), e:
        line, column = e.line(), e.column()

        source_lines = source.split("\n")
        bad_line = source_lines[line]

        puts(bad_line)
        puts("^".rjust(column))

        fail("syntax error: invalid syntax at line %d, column %d" % (line, column))

    except Exception, e:
        traceback.print_exc()
        fail("Unexpected compilation error")

    template_str = open(TEMPLATE_PATH, 'rb').read()
    Template(template_str).stream(states=node).dump(output)


if __name__ == '__main__':
    main()
    sys.exit(0)
