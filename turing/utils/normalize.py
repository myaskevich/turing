
import re


_WHITESPACE_REGEXP = re.compile('\s+')


def normalize(string, ignore='', caseless=True, spaceless=True):
    if spaceless:
        string = _WHITESPACE_REGEXP.sub('', string)
    if caseless:
        string = string.lower()
    if ignore:
        string = re.sub(ignore, '', string)
    return string


def make_normalizer(**options):
    def concrete_normalizer(string):
        return normalize(string, **options)

    return concrete_normalizer


def get_state_name_norm():
    return make_normalizer(ignore='[^a-zA-Z0-9_]')
