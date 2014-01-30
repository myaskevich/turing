
from parsimonious import Grammar
from parsimonious.exceptions import ParseError
from parsimonious.nodes import NodeVisitor, VisitationError

from turing.utils.normalize import get_state_name_norm


norm_state = get_state_name_norm()


class TuringSyntaxError(VisitationError):
    def __init__(self, text, pos):
        self.text = text
        self.pos = pos

    def line(self):
        pos = self.pos

        for i, line in enumerate(self.text.split("\n")):
            if pos <= len(line):
                return i
            else:
                pos -= len(line) + 1

        return 0

    def column(self):
        pos = self.pos

        for i, line in enumerate(self.text.split("\n")):
            if pos <= len(line):
                return pos + 1
            else:
                pos -= len(line) + 1

        return 0


rules = """
    program = state*
    _ = ~"\s*"

    initial_state_modifier = "initial"
    final_state_modifier = "final"
    state_modifier = initial_state_modifier / final_state_modifier
    state_name = ~"[ a-zA-Z0-9_]+"
    state_code = statement*
    state = _ state_modifier* _ state_modifier* _ "state" _ state_name _ "{" _ state_code _ "}" _

    literal = ~"[a-zA-Z0-9]{1}"
    self = _ "self" _
    head = _ "head" _
    ref = self / head

    junk_direction = ~".*"
    direction = "right" / "left" / junk_direction
    move = _ "move" _ direction _
    no_move = _ "no" _ "move" _
    movement = move / no_move

    write = _ "do"* _ "write" _ literal _
    erase = _ "do"* _ "erase" _
    no_action = _ "do" _ "nothing" _
    action = write / erase / no_action

    state_name = ~"[a-zA-Z0-9 ,.]+"u
    state_ref = self / state_name
    assume = _ "assume" _ state_ref _

    eq = "is"
    eq_neq = eq
    condition = _ head _ eq_neq _ literal _
    if_branch = _ "if" _ condition _ "then" _ state_code _
    elif_branch = _ "else" _ "if" _ condition _ "then" _ state_code _
    elif_branches = elif_branch*
    else_branch = _ "else" _ state_code _
    if_block = _ if_branch _ elif_branches _ else_branch? _ "endif" _

    statement = movement / action / assume / if_block
"""


def indent(level=0):
    def wrapper(visit_to_wrap):
        def indent_visit(self, *args):
            text = visit_to_wrap(self, *args)
            indent_text = ""
            for line in text.split("\n"):
                indent_text += (' ' * 4 * level) + line + "\n"

            return indent_text[:-1]

        return indent_visit

    return wrapper


class TuringSyntaxVisitor(NodeVisitor):
    def generic_visit(self, node, child):
        return child

    def visit_program(self, node, child):
        return child


    def visit_initial_state_modifier(self, node, child):
        return "InitialMixin"

    def visit_final_state_modifier(self, node, child):
        return "FinalMixin"

    def visit_state_modifier(self, node, child):
        return child[0]

    @indent(level=2)
    def visit_state_code(self, node, child):
        return "\n".join(child)

    def visit_state_name(self, node, child):
        return node.text.strip()

    def visit_state(self, node, child):
        _, modifier1, _, modifier2, _, _, _, name, _, _, _, code, _, _, _ = child
        
        class_name = norm_state(name)

        modifiers = ["UserState"]
        if modifier1:
            modifiers.append(modifier1[0])
        if modifier2:
            modifiers.append(modifier2[0])

        return """
class _%(class_name)s(%(modifiers)s):
    name = '%(name)s'

    def _resolve(self, machine):
%(code)s
        pass  # handle empty state as well

_states.add(_%(class_name)s()) """ % {
        'class_name': class_name,
        'name': name,
        'modifiers': ', '.join(modifiers),
        'code': code,
    }

    def visit_number(self, node, child):
        _, number, _ = node

        return "'" + number.text.strip() + "'"

    def visit_char(self, node, child):
        _, char, _ = node
        return "'" + char.text + "'"

    def visit_literal(self, node, child):
        literal = node.text.strip("'\"")
        return "'" + literal + "'"

    def visit_statement(self, node, child):
        return child[0]

    def visit_movement(self, node, child):
        return child[0]

    def visit_move(self, node, child):
        _, _, _, direction, _ = node

        move = 'machine.move(%s)'

        if direction.text == 'left':
            there = "Move.LEFT"

        elif direction.text == 'right':
            there = "Move.RIGHT"

        else:
            assert 0

        return move % there

    def visit_no_move(self, node, child):
        return 'machine.move(Move.NONE)'

    def visit_action(self, node, child):
        return child[0]

    def visit_write(self, node, child):
        _, _, _, _, _, what, _ = node
        
        return "machine.do(Action.WRITE, '%s')" % what.text

    def visit_erase(self, node, child):
        return "machine.do(Action.ERASE)"

    def visit_no_action(self, node, child):
        return "machine.do(Action.NONE)"

    def visit_assume(self, node, child):
        _, _, _, state_ref, _ = node

        return "machine.assume('%s')" % state_ref.text

    def visit_self(self, node, child):
        return 'self'

    def visit_head(self, node, child):
        return 'machine.head'

    def visit_eq(self, node, child):
        return '=='

    def visit_eq_neq(self, node, child):
        return child[0]

    def visit_condition(self, node, child):
        _, head, _, eq_neq, _, literal, _ = child

        return head + ' ' + eq_neq + ' ' + literal

    def visit_if_branch(self, node, child):
        _, _, _, condition, _, _, _, code, _ = child

        return """\
if %(condition)s:
%(code)s""" % {'condition': condition, 'code': code}

    def visit_elif_branch(self, node, child):
        _, _, _, _, _, condition, _, _, _, code, _ = child

        return """
elif %(condition)s:
%(code)s""" % {'condition': condition, 'code': code}

    def visit_elif_branches(self, node, child):
        return ''.join(child)

    def visit_else_branch(self, node, child):
        _, _, _, code, _ = child

        return """
else:
%(code)s""" % {'code': code}

    def visit_if_block(self, node, child):
        _, if_branch, _, elif_branches, _, else_branch, _, _, _ = child

        return "%(if_branch)s%(elif_branches)s%(else_branch)s" % {
            'if_branch': if_branch,
            'elif_branches': elif_branches,
            'else_branch': else_branch[0] if else_branch else "",
        }



    

    def visit_junk_direction(self, node, child):
        raise TuringSyntaxError(node.full_text, node.start)


def parse(src):
    root = Grammar(rules)["program"].parse(src)
    return TuringSyntaxVisitor().visit(root)
