from parsimonious import Grammar
from parsimonious.nodes import NodeVisitor

from turing.action import move_closure, do_closure, assume_closure


rules = """\
    program = statement*
    _ = ~"\s*"

    number = _ ~"[0-9]+" _
    char = _ ~"[a-zA-Z ]{1}"u _
    literal = number / char

    direction = "right" / "left"
    move = _ "move" _ direction _
    no_move = _ "no" _ "move" _
    movement = move / no_move

    write = _ "write" _ literal _
    erase = _ "erase" _
    action = write / erase

    state_name = ~"[a-zA-Z0-9 ]+"u
    assume = _ "assume" _ state_name _

    statement = movement / action / assume / literal
"""


class Turing(object):

    def parse(self, source):
        return Grammar(rules)['program'].parse(source)

    def eval(self, source):
        node = self.parse(source) if isinstance(source, basestring) else source
        return ProgramVisitor(self).visit(node)

    def move(self, direction):
        if direction == Direction.RIGHT:
            print "moving right"
        elif direction == Direction.LEFT:
            print "moving left"
        elif direction == Direction.NONE:
            print "no movement"

    def do(self, action, *args):
        if action == Action.WRITE:
            print "writing", args
        elif action == Action.ERASE:
            print "erasing"

    def assume(self, state):
        print 'assuming', state, 'state'


class Action:
    WRITE = 1
    ERASE = 2


class Direction:
    RIGHT = 1
    LEFT = 2
    NONE = 3


class ProgramVisitor(NodeVisitor):
    def __init__(self, machine):
        self.machine = machine

    def generic_visit(self, node, child):
        pass

    def visit_program(self, node, child):
        return child

    def visit_number(self, node, child):
        _, number, _ = node
        return int(number.text)

    def visit_quote(self, node, child):
        return child

    def visit_char(self, node, child):
        _, char, _ = node
        return char.text

    def visit_literal(self, node, child):
        return child[0]

    def visit_statement(self, node, child):
        return child[0]

    def visit_move(self, node, child):
        _, _, _, direction, _ = node

        if direction.text == "left":
            code = Direction.LEFT
        elif direction.text == "right":
            code = Direction.RIGHT
        else:
            assert 0   # sanity check

        move_closure(code)(self.machine)

    def visit_no_move(self, node, child):
        move_closure(Direction.NONE)(self.machine)

    def visit_write(self, node, child):
        _, _, _, what_node, _ = node
        what = self.machine.eval(what_node)
        do_closure(Action.WRITE, what)(self.machine)

    def visit_erase(self, node, child):
        do_closure(Action.ERASE)(self.machine)

    def visit_assume(self, node, child):
        _, _, _, state_node, _ = node
        assume_closure(state_node.text.strip())(self.machine)
