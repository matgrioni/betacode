import itertools
import unicodedata

import pygtrie

# Special characters that need their own references to rewrite with
_FINAL_LC_SIGMA = '\u03c2'
_MEDIAL_LC_SIGMA = '\u03c3'

# Punctuation marks in the betacode map
_BETA_PUNCTUATION = frozenset('\':-_')

_BETACODE_MAP = {
    # No marks
    'a':       '\u03b1',
    'b':       '\u03b2',
    'g':       '\u03b3',
    'd':       '\u03b4',
    'e':       '\u03b5',
    'z':       '\u03b6',
    'h':       '\u03b7',
    'q':       '\u03b8',
    'i':       '\u03b9',
    'k':       '\u03ba',
    'l':       '\u03bb',
    'm':       '\u03bc',
    'n':       '\u03bd',
    'c':       '\u03be',
    'o':       '\u03bf',
    'p':       '\u03c0',
    'r':       '\u03c1',
    's':       '\u03c3',
    's1':      '\u03c3',
    's2':      '\u03c2',
    's3':      '\u03f2',
    't':       '\u03c4',
    'u':       '\u03c5',
    'f':       '\u03c6',
    'x':       '\u03c7',
    'y':       '\u03c8',
    'w':       '\u03c9',
    '*a':      '\u0391',
    '*b':      '\u0392',
    '*g':      '\u0393',
    '*d':      '\u0394',
    '*e':      '\u0395',
    '*z':      '\u0396',
    '*h':      '\u0397',
    '*q':      '\u0398',
    '*i':      '\u0399',
    '*k':      '\u039a',
    '*l':      '\u039b',
    '*m':      '\u039c',
    '*n':      '\u039d',
    '*c':      '\u039e',
    '*o':      '\u039f',
    '*p':      '\u03a0',
    '*r':      '\u03a1',
    '*s':      '\u03a3',
    '*s3':     '\u03f9',
    '*t':      '\u03a4',
    '*u':      '\u03a5',
    '*f':      '\u03a6',
    '*x':      '\u03a7',
    '*y':      '\u03a8',
    '*w':      '\u03a9',

    # Smooth breathing
    'a)':      '\u1f00',
    'e)':      '\u1f10',
    'h)':      '\u1f20',
    'i)':      '\u1f30',
    'o)':      '\u1f40',
    'u)':      '\u1f50',
    'w)':      '\u1f60',
    'r)':      '\u1fe4',
    '*)a':     '\u1f08',
    '*)e':     '\u1f18',
    '*)h':     '\u1f28',
    '*)i':     '\u1f38',
    '*)o':     '\u1f48',
    '*)w':     '\u1f68',

    # Rough breathing
    'a(':      '\u1f01',
    'e(':      '\u1f11',
    'h(':      '\u1f21',
    'i(':      '\u1f31',
    'o(':      '\u1f41',
    'u(':      '\u1f51',
    'w(':      '\u1f61',
    'r(':      '\u1fe5',
    '*(a':     '\u1f09',
    '*(e':     '\u1f19',
    '*(h':     '\u1f29',
    '*(i':     '\u1f39',
    '*(o':     '\u1f49',
    '*(u':     '\u1f59',
    '*(w':     '\u1f69',
    '*(r':     '\u1fec',

    # Acute accent and grave accent
    'a\\':     '\u1f70',
    'a/':      '\u1f71',
    'e\\':     '\u1f72',
    'e/':      '\u1f73',
    'h\\':     '\u1f74',
    'h/':      '\u1f75',
    'i\\':     '\u1f76',
    'i/':      '\u1f77',
    'o\\':     '\u1f78',
    'o/':      '\u1f79',
    'u\\':     '\u1f7a',
    'u/':      '\u1f7b',
    'w\\':     '\u1f7c',
    'w/':      '\u1f7d',
    '*\\a':    '\u1fba',
    '*/a':     '\u1fbb',
    '*\\e':    '\u1fce',
    '*/e':     '\u1fc9',
    '*\\h':    '\u1fca',
    '*/h':     '\u1fcb',
    '*\\i':    '\u1fda',
    '*/i':     '\u1fdb',
    '*\\o':    '\u1ff8',
    '*/o':     '\u1ff9',
    '*\\u':    '\u1fea',
    '*/u':     '\u1feb',
    '*\\w':    '\u1ffa',
    '*/w':     '\u1ffb',

    # Smooth breathing and acute accent
    'a)/':     '\u1f04',
    'e)/':     '\u1f14',
    'h)/':     '\u1f24',
    'i)/':     '\u1f34',
    'o)/':     '\u1f44',
    'u)/':     '\u1f54',
    'w)/':     '\u1f64',
    '*)/a':    '\u1f0c',
    '*)/e':    '\u1f1c',
    '*)/h':    '\u1f2c',
    '*)/i':    '\u1f3c',
    '*)/o':    '\u1f4c',
    '*)/u':    '\u1f5c',
    '*)/w':    '\u1f6c',

    # Smooth breathing and grave accent
    'a)\\':    '\u1f02',
    'e)\\':    '\u1f12',
    'h)\\':    '\u1f22',
    'i)\\':    '\u1f32',
    'o)\\':    '\u1f42',
    'u)\\':    '\u1f52',
    'w)\\':    '\u1f62',
    '*)\\a':   '\u1f0a',
    '*)\\e':   '\u1f1a',
    '*)\\h':   '\u1f2a',
    '*)\\i':   '\u1f3a',
    '*)\\o':   '\u1f4a',
    '*)\\u':   '\u1f5a',
    '*)\\w':   '\u1f6a',

    # Rough breathing and acute accent
    'a(/':     '\u1f05',
    'e(/':     '\u1f15',
    'h(/':     '\u1f25',
    'i(/':     '\u1f35',
    'o(/':     '\u1f45',
    'u(/':     '\u1f55',
    'w(/':     '\u1f65',
    '*(/a':    '\u1f0d',
    '*(/e':    '\u1f1d',
    '*(/h':    '\u1f2d',
    '*(/i':    '\u1f3d',
    '*(/o':    '\u1f4d',
    '*(/u':    '\u1f5d',
    '*(/w':    '\u1f6d',

    # Rough breathing and grave accent
    'a(\\':    '\u1f03',
    'e(\\':    '\u1f13',
    'h(\\':    '\u1f23',
    'i(\\':    '\u1f33',
    'o(\\':    '\u1f43',
    'u(\\':    '\u1f53',
    'w(\\':    '\u1f63',
    '*(\\a':   '\u1f0b',
    '*(\\e':   '\u1f1b',
    '*(\\h':   '\u1f2b',
    '*(\\i':   '\u1f3b',
    '*(\\o':   '\u1f4b',
    '*(\\u':   '\u1f5b',
    '*(\\w':   '\u1f6b',

    # Perispomeni
    'a=':     '\u1fb6',
    'h=':     '\u1fc6',
    'i=':     '\u1fd6',
    'u=':     '\u1fe6',
    'w=':     '\u1ff6',

    # Smooth breathing and perispomeni
    'a)=':    '\u1f06',
    'h)=':    '\u1f26',
    'i)=':    '\u1f36',
    'u)=':    '\u1f56',
    'w)=':    '\u1f66',
    '*)=a':   '\u1f0e',
    '*)=h':   '\u1f2e',
    '*)=i':   '\u1f3e',
    '*)=w':   '\u1f6e',

    # Rough breathing and perispomeni
    'a(=':    '\u1f07',
    'h(=':    '\u1f27',
    'i(=':    '\u1f37',
    'u(=':    '\u1f57',
    'w(=':    '\u1f67',
    '*(=a':   '\u1f0f',
    '*(=h':   '\u1f2f',
    '*(=i':   '\u1f3f',
    '*(=u':   '\u1f5f',
    '*(=w':   '\u1f6f',

    # Perispomeni and ypogegrammeni
    'a=|':    '\u1fb7',
    'h=|':    '\u1fc7',
    'w=|':    '\u1ff7',

    # Ypogegrammeni
    'a|':     '\u1fb3',
    'h|':     '\u1fc3',
    'w|':     '\u1ff3',
    '*a|':    '\u1fbc',
    '*h|':    '\u1fcc',
    '*w|':    '\u1ffc',

    # Acute accent and ypogegrammeni
    'a/|':    '\u1fb4',
    'h/|':    '\u1fc4',
    'w/|':    '\u1ff4',

    # Smooth breathing and ypogegrammeni
    'a)|':    '\u1f80',
    'h)|':    '\u1f90',
    'w)|':    '\u1fa0',
    '*)a|':   '\u1f88',
    '*)h|':   '\u1f98',
    '*)w|':   '\u1fa8',

    # Rough breathing and ypogegrammeni
    'a(|':    '\u1f81',
    'h(|':    '\u1f91',
    'w(|':    '\u1fa1',
    '*(a|':   '\u1f89',
    '*(h|':   '\u1f99',
    '*(w|':   '\u1fa9',

    # Smooth breathing, acute accent, and ypogegrammeni
    'a)\|':   '\u1f82',
    'h)\|':   '\u1f92',
    'w)\|':   '\u1fa2',
    '*)\\a|': '\u1f8a',
    '*)\h|':  '\u1f9a',
    '*)\w|':  '\u1faa',

    # Rough breathing, grave accent, and ypogegrammeni
    'a(\|':   '\u1f83',
    'h)\|':   '\u1f93',
    'w)\|':   '\u1fa3',
    '*(\\a|': '\u1f8b',
    '*)\h|':  '\u1f9b',
    '*)\w|':  '\u1fab',

    # Smooth breathing, accute accent, and ypogegrammeni
    'a)/|':   '\u1f84',
    'h)/|':   '\u1f94',
    'w)/|':   '\u1fa4',
    '*)/a|':  '\u1f8c',
    '*)/h|':  '\u1f9c',
    '*)/w|':  '\u1fac',

    # Rough breating, acute accent, and ypogegrammeni
    'a(/|':   '\u1f85',
    'h(/|':   '\u1f95',
    'w(/|':   '\u1fa5',
    '*(/a|':  '\u1f8d',
    '*(/h|':  '\u1f9d',
    '*(/w|':  '\u1fad',

    # Smooth breathing, ypogegrammeni, and perispomeni
    'a)=|':   '\u1f86',
    'h)=|':   '\u1f96',
    'w)=|':   '\u1fa6',
    '*)=a|':  '\u1f8e',
    '*)=h|':  '\u1f9e',
    '*)=w|':  '\u1fae',

    # Rough breathing, ypogegrammeni, and perispomeni
    'a(=|':   '\u1f87',
    'h(=|':   '\u1f97',
    'w(=|':   '\u1fa7',
    '*(=a|':  '\u1f8f',
    '*(=h|':  '\u1f9f',
    '*(=w|':  '\u1faf',

    # Diaeresis
    'i+':     '\u03ca',
    '*+i':    '\u03aa',
    'i\\+':   '\u1fd2',
    'i/+':    '\u1fd3',
    'i+/':    '\u1fd3',
    'i=+':    '\u1fd7',
    'u+':     '\u03cb',
    '*+u':    '\u03ab',
    'u\\+':   '\u1fe2',
    'u/+':    '\u1fe3',
    'u=+':    '\u1fe7',

    # Macron
    'a&':     '\u1fb0',
    'i&':     '\u1fd0',
    'u&':     '\u1fe0',

    # Breve
    'a\'':    '\u1fb1',
    'i\'':    '\u1fd1',
    'u\'':    '\u1fe1',

    # Basic punctuation
    ':':      '\u00b7',
    '\'':     '\u2019',
    '-':      '\u2010',
    '_':      '\u2014'
}


def _create_unicode_map():
    """
    Create the inverse map from unicode to betacode.

    Returns:
    The hash map to convert unicode characters to the beta code representation.
    """
    unicode_map = {}

    for beta, uni in _BETACODE_MAP.items():
        # Include decomposed equivalent where necessary.
        norm = unicodedata.normalize('NFD', uni)
        unicode_map[norm] = beta
        unicode_map[uni] = beta

    # Add the final sigmas.
    final_sigma_norm = unicodedata.normalize('NFC', _FINAL_LC_SIGMA)
    unicode_map[final_sigma_norm] = 's'
    unicode_map[_FINAL_LC_SIGMA] = 's'

    return unicode_map

_UNICODE_MAP = _create_unicode_map()

def _create_conversion_trie():
    """
    Create the trie for betacode conversion.

    Returns:
    The trie for conversion.
    """
    t = pygtrie.CharTrie()

    for beta, uni in _BETACODE_MAP.items():
        # The order of accents is very strict and weak. Allow for many orders of
        # accents between asterisk and letter or after letter. This does not
        # introduce ambiguity since each betacode token only has one letter and
        # either starts with a asterisk or a letter.
        diacritics = beta[1:]

        perms = itertools.permutations(diacritics)
        for perm in perms:
            perm_str = beta[0] + ''.join(perm)

            t[perm_str.upper()] = uni
            t[perm_str.lower()] = uni

    return t

_CONVERSION_TRIE = _create_conversion_trie()


def _find_max_beta_token_len():
    """
    Finds the maximum length of a single betacode token.

    Returns:
    The length of the longest key in the betacode map, which corresponds to the
    longest single betacode token.
    """
    max_beta_len = -1
    for beta, uni in _BETACODE_MAP.items():
        if len(beta) > max_beta_len:
            max_beta_len = len(beta)

    return max_beta_len

_MAX_BETA_TOKEN_LEN = _find_max_beta_token_len()


def beta_to_uni(text):
    """
    Converts the given text from betacode to unicode.

    Args:
    text: The beta code text to convert. All of this text must be betacode.

    Returns:
    The converted text.
    """
    t = _CONVERSION_TRIE

    transform = []
    idx = 0

    possible_word_boundary = False
    while idx < len(text):
        if possible_word_boundary and len(transform) > 1 and \
            transform[-2] == _MEDIAL_LC_SIGMA and not transform[-1].isalnum():
            transform[-2] = _FINAL_LC_SIGMA

        step = t.longest_prefix(text[idx:idx + _MAX_BETA_TOKEN_LEN])

        if step:
            key, value = step
            possible_word_boundary = text[idx] in _BETA_PUNCTUATION

            transform.append(value)
            idx += len(key)
        else:
            possible_word_boundary = True

            transform.append(text[idx])
            idx += 1

    # Check one last time in case there is some whitespace or punctuation at the
    # end and check if the last character is a sigma.
    if possible_word_boundary and len(transform) > 1 and \
        transform[-2] == _MEDIAL_LC_SIGMA and not transform[-1].isalnum():
        transform[-2] = _FINAL_LC_SIGMA
    elif len(transform) > 0 and transform[-1] == _MEDIAL_LC_SIGMA:
        transform[-1] = _FINAL_LC_SIGMA

    converted = ''.join(transform)
    return converted

def uni_to_beta(text):
    """
    Convert unicode text to a betacode equivalent.

    Args:
    text: The text to convert to betacode. This text does not have to all be
          Greek polytonic text, and only Greek characters will be converted.
          Note that in this case, you cannot convert to beta and then back to
          unicode.

    Returns:
    The betacode equivalent of the inputted text where applicable.
    """
    transform = []

    last_lookup_failed = False
    for ch in text:
        try:
            last_lookup_failed = True
            conv = _UNICODE_MAP[ch]
        except KeyError:
            last_lookup_failed = True
            conv = ch

        transform.append(conv)

    converted = ''.join(transform)
    return converted
