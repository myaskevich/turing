
NULL = ''
EXPAND_CHAR = '.'


class TapeError(Exception):
    pass


class TapeIsOverException(TapeError):
    pass


class Tape(object):
    def __init__(self, source=""):
        self._tape = list(source)
        self._head = 0

    def get(self):
        try:
            return self._tape[self._head]
        except IndexError:
            raise TapeError("Couldn't read tape at pos %d" % self._head)

    def put(self, item):
        try:
            self._tape[self._head] = item
        except IndexError:
            raise TapeError("Couldn't write to an empty tape")

    def left(self):
        raise TapeError("Tape can't be moved back (left)")

    def right(self):
        if self._head == len(self._tape) - 1 or len(self._tape) == 0:
            raise TapeIsOverException

        self._head += 1

    def __eq__(self, other):
        this = ''.join(self._tape).strip(EXPAND_CHAR)
        other = ''.join(tuple(other)).strip(EXPAND_CHAR)
        return this == other

    def __str__(self):
        return ''.join(self._tape).strip(EXPAND_CHAR)

    def __add__(self, other):
        other = ''.join(tuple(other)).strip(EXPAND_CHAR)
        return Tape(str(self) + other)

    def __radd__(self, other):
        other = ''.join(tuple(other)).strip(EXPAND_CHAR)
        return Tape(other + str(self))


class NullableTape(Tape):
    def get(self):
        try:
            return self._tape[self._head]
        except IndexError:
            return NULL


class ExtendableTape(Tape):
    def put(self, item):
        if not self._tape:
            self.left()

        super(ExtendableTape, self).put(item)

    def left(self):
        if self._head == 0:
            self._tape.insert(0, EXPAND_CHAR)
        else:
            self._head -= 1

    def right(self):
        if self._head == len(self._tape) - 1:
            self._tape.append(EXPAND_CHAR)

        super(ExtendableTape, self).right()
