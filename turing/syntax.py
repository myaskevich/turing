
import sys

from parsimonious import Grammar
from parsimonious.nodes import NodeVisitor

from turing.utils.normalize import make_normalizer


norm_state = make_normalizer(ignore=('_', '-', '.', ',', ':', ';'))


rules = """\
    program = state*
    _ = ~"\s*"

    state_modifier = "initial" / "final"
    state_name = ~"[ a-zA-Z0-9_]+"
    state_code = statement*
    state = _ state_modifier* _ "state" _ state_name _ "{" _ state_code _ "}" _

    number = _ ~"[0-9]{1}" _
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


class TuringSyntaxVisitor(NodeVisitor):
    def generic_visit(self, node, child):
        pass

    def visit_program(self, node, child):
        sys.stderr.write(str(node) + "\n")
        return child


    def visit_state_modifier(self, node, child):
        return child

    def visit_state_code(self, node, child):
        return child

    def visit_state_name(self, node, child):
        return norm_state(node.text)

    def visit_state(self, node, child):
        return node


    def visit_number(self, node, child):
        _, number, _ = node
        return number.text.strip()

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

        return node

    def visit_no_move(self, node, child):
        return node

    def visit_write(self, node, child):
        _, _, _, what_node, _ = node
        what = self.machine.eval(what_node)
        return node

    def visit_erase(self, node, child):
        return node

    def visit_assume(self, node, child):
        _, _, _, state_node, _ = node
        return node


def parse(src):
    root = Grammar(rules)["program"].parse(src)
    return TuringSyntaxVisitor().visit(root)
