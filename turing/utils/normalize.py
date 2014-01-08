
import re


_WHITESPACE_REGEXP = re.compile('\s+')


def normalize(string, ignore=(), caseless=True, spaceless=True):
    """Normalizes given string according to given spec.

    By default string is turned to lower case and all whitespace is removed.
    Additional characters can be removed by giving them in `ignore` list.
    """
    if spaceless:
        string = _WHITESPACE_REGEXP.sub('', string)
    if caseless:
        string = string.lower()
        ignore = [i.lower() for i in ignore]
    for ign in ignore:
        if ign in string:  # performance optimization
            string = string.replace(ign, '')
    return string


def make_normalizer(**options):
    def concrete_normalizer(string):
        return normalize(string, **options)

    return concrete_normalizer
