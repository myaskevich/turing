
NULL = '.'

class Tape(object):
    def __init__(self, source=""):
        self._tape = list(source)
        self._head = 0

    def get(self):
        return self._tape[self._head]

    def put(self, item):
        if not self._tape:
            self.left()

        self._tape[self._head] = item

    def left(self):
        if self._head == 0:
            self._tape.insert(0, NULL)
        else:
            self._head -= 1

    def right(self):
        if self._head == len(self._tape) - 1:
            self._tape.append(NULL)

        self._head += 1

    def __eq__(self, other):
        this = ''.join(self._tape).strip(NULL)
        other = ''.join(tuple(other)).strip(NULL)
        return this == other

    def __str__(self):
        return ''.join(self._tape).strip(NULL)

    def __add__(self, other):
        other = ''.join(tuple(other)).strip(NULL)
        return Tape(str(self) + other)

    def __radd__(self, other):
        other = ''.join(tuple(other)).strip(NULL)
        return Tape(other + str(self))
