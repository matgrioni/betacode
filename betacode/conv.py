from betaconv.trie import Trie

_FINAL_LC_SIGMA = '\u03c2'
_MEDIAL_LC_SIGMA = '\u03c3'

_BETACODE_MAP = {
    '*a':     '\u0391',
    '*b':     '\u0392',
    '*g':     '\u0393',
    '*d':     '\u0394',
    '*e':     '\u0395',
    '*z':     '\u0396',
    '*h':     '\u0397',
    '*q':     '\u0398',
    '*i':     '\u0399',
    '*k':     '\u039a',
    '*l':     '\u039b',
    '*m':     '\u039c',
    '*n':     '\u039d',
    '*c':     '\u039e',
    '*o':     '\u039f',
    '*p':     '\u03a0',
    '*r':     '\u03a1',
    '*s':     '\u03a3',
    '*t':     '\u03a4',
    '*u':     '\u03a5',
    '*f':     '\u03a6',
    '*x':     '\u03a7',
    '*y':     '\u03a8',
    '*w':     '\u03a9',

    'a':      '\u03b1',
    'b':      '\u03b2',
    'g':      '\u03b3',
    'd':      '\u03b4',
    'e':      '\u03b5',
    'z':      '\u03b6',
    'h':      '\u03b7',
    'q':      '\u03b8',
    'i':      '\u03b9',
    'k':      '\u03ba',
    'l':      '\u03bb',
    'm':      '\u03bc',
    'n':      '\u03bd',
    'c':      '\u03be',
    'o':      '\u03bf',
    'p':      '\u03c0',
    'r':      '\u03c1',

    's':      '\u03c3',

    't':      '\u03c4',
    'u':      '\u03c5',
    'f':      '\u03c6',
    'x':      '\u03c7',
    'y':      '\u03c8',
    'w':      '\u03c9',

    'i+':     '\u03ca',
    'u+':     '\u03cb',

    'a)':     '\u1f00',
    'a(':     '\u1f01',
    'a)\\':   '\u1f02',
    'a(\\':   '\u1f03',
    'a)/':    '\u1f04',
    'a(/':    '\u1f05',
    'e)':     '\u1f10',
    'e(':     '\u1f11',
    'e)\\':   '\u1f12',
    'e(\\':   '\u1f13',
    'e)/':    '\u1f14',
    'e(/':    '\u1f15',
    'h)':     '\u1f20',
    'h(':     '\u1f21',
    'h)\\':   '\u1f22',
    'h(\\':   '\u1f23',
    'h)/':    '\u1f24',
    'h(/':    '\u1f25',
    'i)':     '\u1f30',
    'i(':     '\u1f31',
    'i)\\':   '\u1f32',
    'i(\\':   '\u1f33',
    'i)/':    '\u1f34',
    'i(/':    '\u1f35',
    'o)':     '\u1f40',
    'o(':     '\u1f41',
    'o)\\':   '\u1f42',
    'o(\\':   '\u1f43',
    'o)/':    '\u1f44',
    'o(/':    '\u1f45',
    'u)':     '\u1f50',
    'u(':     '\u1f51',
    'u)\\':   '\u1f52',
    'u(\\':   '\u1f53',
    'u)/':    '\u1f54',
    'u(/':    '\u1f55',
    'w)':     '\u1f60',
    'w(':     '\u1f61',
    'w)\\':   '\u1f62',
    'w(\\':   '\u1f63',
    'w)/':    '\u1f64',
    'w(/':    '\u1f65',

    'a)=':    '\u1f06',
    'a(=':    '\u1f07',
    'h)=':    '\u1f26',
    'h(=':    '\u1f27',
    'i)=':    '\u1f36',
    'i(=':    '\u1f37',
    'u)=':    '\u1f56',
    'u(=':    '\u1f57',
    'w)=':    '\u1f66',
    'w(=':    '\u1f67',

    '*a)':    '\u1f08',
    '*)a':    '\u1f08',
    '*a(':    '\u1f09',
    '*(a':    '\u1f09',

    'a)':     '\u1f00',
    ')a':     '\u1f00',
    'a(':     '\u1f01',
    '(a':     '\u1f01',

    '*(\\a':  '\u1f0b',
    '*a)/':   '\u1f0c',
    '*)/a':   '\u1f0c',
    '*a(/':   '\u1f0f',
    '*(/a':   '\u1f0f',
    '*e)':    '\u1f18',
    '*)e':    '\u1f18',
    '*e(':    '\u1f19',
    '*(e':    '\u1f19',

    '*(\e':   '\u1f1b',
    '*e)/':   '\u1f1c',
    '*)/e':   '\u1f1c',
    '*e(/':   '\u1f1d',
    '*(/e':   '\u1f1d',

    '*h)':    '\u1f28',
    '*)h':    '\u1f28',
    '*h(':    '\u1f29',
    '*(h':    '\u1f29',
    '*h)\\':  '\u1f2a',
    ')\\*h':  '\u1f2a',
    '*)\\h':  '\u1f2a',

    '*h)/':   '\u1f2c',
    '*)/h':   '\u1f2c',

    '*)=h':   '\u1f2e',
    '(/*h':   '\u1f2f',
    '*(/h':   '\u1f2f',
    '*i)':    '\u1f38',
    '*)i':    '\u1f38',
    '*i(':    '\u1f39',
    '*(i':    '\u1f39',

    '*i)/':   '\u1f3c',
    '*)/i':   '\u1f3c',

    '*i(/':   '\u1f3f',
    '*(/i':   '\u1f3f',

    '*o)':    '\u1f48',
    '*)o':    '\u1f48',
    '*o(':    '\u1f49',
    '*(o':    '\u1f49',

    '*(\o':   '\u1f4b',
    '*o)/':   '\u1f4c',
    '*)/o':   '\u1f4c',
    '*o(/':   '\u1f4f',
    '*(/o':   '\u1f4f',

    '*u(':    '\u1f59',
    '*(u':    '\u1f59',

    '*(/u':   '\u1f5d',

    '*(=u':   '\u1f5f',
    
    '*w)':    '\u1f68',
    '*w(':    '\u1f69',
    '*(w':    '\u1f69',

    '*w)/':   '\u1f6c',
    '*)/w':   '\u1f6c',
    '*w(/':   '\u1f6f',
    '*(/w':   '\u1f6f',

    '*a)=':   '\u1f0e',
    '*)=a':   '\u1f0e',
    '*a(=':   '\u1f0f',
    '*w)=':   '\u1f6e',
    '*)=w':   '\u1f6e',
    '*w(=':   '\u1f6f',
    '*(=w':   '\u1f6f',

    'a\\':    '\u1f70',
    'a/':     '\u1f71',
    'e\\':    '\u1f72',
    'e/':     '\u1f73',
    'h\\':    '\u1f74',
    'h/':     '\u1f75',
    'i\\':    '\u1f76',
    'i/':     '\u1f77',
    'o\\':    '\u1f78',
    'o/':     '\u1f79',
    'u\\':    '\u1f7a',
    'u/':     '\u1f7b',
    'w\\':    '\u1f7c',
    'w/':     '\u1f7d',

    'a)/|':   '\u1f84',
    'a(/|':   '\u1f85',
    'h)|':    '\u1f90',
    'h(|':    '\u1f91',
    'h)/|':   '\u1f94',
    'h)=|':   '\u1f96',
    'h(=|':   '\u1f97',
    'w)|':    '\u1fa0',
    'w(=|':   '\u1fa7',

    'a=':     '\u1fb6',
    'h=':     '\u1fc6',
    'i=':     '\u1fd6',
    'u=':     '\u1fe6',
    'w=':     '\u1ff6',

    'i\\+':   '\u1fd2',
    'i/+':    '\u1fd3',
    'i+/':    '\u1fd3',
    'u\\+':   '\u1fe2',
    'u/+':    '\u1fe3',

    'a|':     '\u1fb3',
    'a/|':    '\u1fb4',
    'h|':     '\u1fc3',
    'h/|':    '\u1fc4',
    'w|':     '\u1ff3',
    'w|/':    '\u1ff4',
    'w/|':    '\u1ff4',

    'a=|':    '\u1fb7',
    'h=|':    '\u1fc7',
    'w=|':    '\u1ff7',

    'r(':     '\u1fe4',
    '*r(':    '\u1fec',
    '*(r':    '\u1fec',
}

def _create_unicode_map():
    """
    Create the inverse map from unicode to betacode.

    Returns:
    The hash map to convert unicode characters to the beta code representation.
    """
    unicode_map = {}

    for beta, uni in _BETACODE_MAP.items():
        unicode_map[uni] = beta

    # Add the final sigmas.
    unicode_map[_FINAL_LC_SIGMA] = 's'

    return unicode_map

_UNICODE_MAP = _create_unicode_map()


def _create_conversion_trie():
    """
    Create the trie for betacode conversion.

    Returns:
    The trie.
    """
    t = Trie()

    for beta, uni in _BETACODE_MAP.items():
        t.add(beta, uni)

    return t


def beta_to_uni(text):
    """
    Converts the given text from betacode to unicode.

    Args:
    text: The beta code text to convert.

    Returns:
    The converted text.
    """
    t = _create_conversion_trie()

    transform = []
    idx = 0

    last_lookup_fail = False
    while idx < len(text):
        if last_lookup_fail and len(transform) > 1 and \
            transform[-2] == _MEDIAL_LC_SIGMA and not transform[-1].isalnum():
            transform[-2] = _FINAL_LC_SIGMA

        value, left = t.find_prefix(text[idx:])

        if value is None:
            last_lookup_fail = True

            transform.append(text[idx])
            idx += 1
        else:
            last_lookup_fail = False

            transform.append(value)
            idx += len(text) - idx - len(left)

    # Check one last time in case there is some whitespace or punctuation at the
    # end and check if the last character is a sigma.
    if last_lookup_fail and len(transform) > 1 and \
        transform[-2] == _MEDIAL_LC_SIGMA and not transform[-1].isalnum():
        transform[-2] = _FINAL_LC_SIGMA
    elif transform[-1] == _MEDIAL_LC_SIGMA:
        transform[-1] = _FINAL_LC_SIGMA

    converted = ''.join(transform)
    return converted

def uni_to_beta(text):
    """
    Convert unicode text to a betacode equivalent.

    Args:
    text: The text to convert to betacode. This text does not have to all be
          Greek polytonic text, and only Greek characters will be converted.

    Returns:
    The betacode equivalent of the inputted text.
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
