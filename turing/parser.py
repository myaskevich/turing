
from parsimonious import Grammar
from parsimonious.nodes import NodeVisitor

from turing.utils.normalize import make_normalizer


norm_state = make_normalizer(ignore=('_', '-', '.', ',', ':', ';'))

grammar1 = """\
    program = statement*
    _ = ~"\s*"

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

grammar = """
    program = state*
    _ = ~"\s*"

    state_pos_indicator = "initial" / "final"
    state_name = ~"[a-zA-Z0-9_-.,:;!?"]+"
    state = _ state_pos_indicator* _ "state" _ state_name _ "{" state_code "}"
"""


class TuringSyntaxVisitor(NodeVisitor):
    def generic_visit(self, node, child):
        pass

    def visit_state_pos_indicator(self, node, child):
        pass

    def visit_state_name(self, node, child):
        return norm_state(node.text)
