# Based off of the original version by James Tauber. Cleaned up and refactored.

_BETACODE_MAP = {
    '*A':     '\u0391',
    '*B':     '\u0392',
    '*G':     '\u0393',
    '*D':     '\u0394',
    '*E':     '\u0395',
    '*Z':     '\u0396',
    '*H':     '\u0397',
    '*Q':     '\u0398',
    '*I':     '\u0399',
    '*K':     '\u039A',
    '*L':     '\u039B',
    '*M':     '\u039C',
    '*N':     '\u039D',
    '*C':     '\u039E',
    '*O':     '\u039F',
    '*P':     '\u03A0',
    '*R':     '\u03A1',
    '*S':     '\u03A3',
    '*T':     '\u03A4',
    '*U':     '\u03A5',
    '*F':     '\u03A6',
    '*X':     '\u03A7',
    '*Y':     '\u03A8',
    '*W':     '\u03A9',

    'A':      '\u03B1',
    'B':      '\u03B2',
    'G':      '\u03B3',
    'D':      '\u03B4',
    'E':      '\u03B5',
    'Z':      '\u03B6',
    'H':      '\u03B7',
    'Q':      '\u03B8',
    'I':      '\u03B9',
    'K':      '\u03BA',
    'L':      '\u03BB',
    'M':      '\u03BC',
    'N':      '\u03BD',
    'C':      '\u03BE',
    'O':      '\u03BF',
    'P':      '\u03C0',
    'R':      '\u03C1',

    'S\n':    '\u03C2',
    'S,':     '\u03C2,',
    'S.':     '\u03C2.',
    'S:':     '\u03C2:',
    'S;':     '\u03C2;',
    'S]':     '\u03C2]',
    'S@':     '\u03C2@',
    'S_':     '\u03C2_',
    'S':      '\u03C3',

    'T':      '\u03C4',
    'U':      '\u03C5',
    'F':      '\u03C6',
    'X':      '\u03C7',
    'Y':      '\u03C8',
    'W':      '\u03C9',

    'I+':     '\u03CA',
    'U+':     '\u03CB',

    'A)':     '\u1F00',
    'A(':     '\u1F01',
    'A)\\':   '\u1F02',
    'A(\\':   '\u1F03',
    'A)/':    '\u1F04',
    'A(/':    '\u1F05',
    'E)':     '\u1F10',
    'E(':     '\u1F11',
    'E)\\':   '\u1F12',
    'E(\\':   '\u1F13',
    'E)/':    '\u1F14',
    'E(/':    '\u1F15',
    'H)':     '\u1F20',
    'H(':     '\u1F21',
    'H)\\':   '\u1F22',
    'H(\\':   '\u1F23',
    'H)/':    '\u1F24',
    'H(/':    '\u1F25',
    'I)':     '\u1F30',
    'I(':     '\u1F31',
    'I)\\':   '\u1F32',
    'I(\\':   '\u1F33',
    'I)/':    '\u1F34',
    'I(/':    '\u1F35',
    'O)':     '\u1F40',
    'O(':     '\u1F41',
    'O)\\':   '\u1F42',
    'O(\\':   '\u1F43',
    'O)/':    '\u1F44',
    'O(/':    '\u1F45',
    'U)':     '\u1F50',
    'U(':     '\u1F51',
    'U)\\':   '\u1F52',
    'U(\\':   '\u1F53',
    'U)/':    '\u1F54',
    'U(/':    '\u1F55',
    'W)':     '\u1F60',
    'W(':     '\u1F61',
    'W)\\':   '\u1F62',
    'W(\\':   '\u1F63',
    'W)/':    '\u1F64',
    'W(/':    '\u1F65',

    'A)=':    '\u1F06',
    'A(=':    '\u1F07',
    'H)=':    '\u1F26',
    'H(=':    '\u1F27',
    'I)=':    '\u1F36',
    'I(=':    '\u1F37',
    'U)=':    '\u1F56',
    'U(=':    '\u1F57',
    'W)=':    '\u1F66',
    'W(=':    '\u1F67',

    '*A)':    '\u1F08',
    '*)A':    '\u1F08',
    '*A(':    '\u1F09',
    '*(A':    '\u1F09',

    '*(\A':   '\u1F0B',
    '*A)/':   '\u1F0C',
    '*)/A':   '\u1F0C',
    '*A(/':   '\u1F0F',
    '*(/A':   '\u1F0F',
    '*E)':    '\u1F18',
    '*)E':    '\u1F18',
    '*E(':    '\u1F19',
    '*(E':    '\u1F19',

    '*(\E':   '\u1F1B',
    '*E)/':   '\u1F1C',
    '*)/E':   '\u1F1C',
    '*E(/':   '\u1F1D',
    '*(/E':   '\u1F1D',

    '*H)':    '\u1F28',
    '*)H':    '\u1F28',
    '*H(':    '\u1F29',
    '*(H':    '\u1F29',
    '*H)\\':  '\u1F2A',
    ')\\*H':  '\u1F2A',
    '*)\\H':  '\u1F2A',

    '*H)/':   '\u1F2C',
    '*)/H':   '\u1F2C',

    '*)=H':   '\u1F2E',
    '(/*H':   '\u1F2F',
    '*(/H':   '\u1F2F',
    '*I)':    '\u1F38',
    '*)I':    '\u1F38',
    '*I(':    '\u1F39',
    '*(I':    '\u1F39',

    '*I)/':   '\u1F3C',
    '*)/I':   '\u1F3C',

    '*I(/':   '\u1F3F',
    '*(/I':   '\u1F3F',

    '*O)':    '\u1F48',
    '*)O':    '\u1F48',
    '*O(':    '\u1F49',
    '*(O':    '\u1F49',

    '*(\O':   '\u1F4B',
    '*O)/':   '\u1F4C',
    '*)/O':   '\u1F4C',
    '*O(/':   '\u1F4F',
    '*(/O':   '\u1F4F',

    '*U(':    '\u1F59',
    '*(U':    '\u1F59',

    '*(/U':   '\u1F5D',

    '*(=U':   '\u1F5F',
    
    '*W)':    '\u1F68',
    '*W(':    '\u1F69',
    '*(W':    '\u1F69',

    '*W)/':   '\u1F6C',
    '*)/W':   '\u1F6C',
    '*W(/':   '\u1F6F',
    '*(/W':   '\u1F6F',

    '*A)=':   '\u1F0E',
    '*)=A':   '\u1F0E',
    '*A(=':   '\u1F0F',
    '*W)=':   '\u1F6E',
    '*)=W':   '\u1F6E',
    '*W(=':   '\u1F6F',
    '*(=W':   '\u1F6F',

    'A\\':    '\u1F70',
    'A/':     '\u1F71',
    'E\\':    '\u1F72',
    'E/':     '\u1F73',
    'H\\':    '\u1F74',
    'H/':     '\u1F75',
    'I\\':    '\u1F76',
    'I/':     '\u1F77',
    'O\\':    '\u1F78',
    'O/':     '\u1F79',
    'U\\':    '\u1F7A',
    'U/':     '\u1F7B',
    'W\\':    '\u1F7C',
    'W/':     '\u1F7D',

    'A)/|':   '\u1F84',
    'A(/|':   '\u1F85',
    'H)|':    '\u1F90',
    'H(|':    '\u1F91',
    'H)/|':   '\u1F94',
    'H)=|':   '\u1F96',
    'H(=|':   '\u1F97',
    'W)|':    '\u1FA0',
    'W(=|':   '\u1FA7',

    'A=':     '\u1FB6',
    'H=':     '\u1FC6',
    'I=':     '\u1FD6',
    'U=':     '\u1FE6',
    'W=':     '\u1FF6',

    'I\\+':   '\u1FD2',
    'I/+':    '\u1FD3',
    'I+/':    '\u1FD3',
    'U\\+':   '\u1FE2',
    'U/+':    '\u1FE3',

    'A|':     '\u1FB3',
    'A/|':    '\u1FB4',
    'H|':     '\u1FC3',
    'H/|':    '\u1FC4',
    'W|':     '\u1FF3',
    'W|/':    '\u1FF4',
    'W/|':    '\u1FF4',

    'A=|':    '\u1FB7',
    'H=|':    '\u1FC7',
    'W=|':    '\u1FF7',

    'R(':     '\u1FE4',
    '*R(':    '\u1FEC',
    '*(R':    '\u1FEC'
}


class Trie:
    """
    A simple trie class.
    """

    def __init__(self):
        """
        Create the Trie with an empty root.
        """
        self.root = [None, {}]

    def add(self, key, value):
        """
        Add an iterable key to the trie with an associated value.

        Args:
        key: The key to store in the Trie.
        value: The associated value to the key.
        """
        curr_node = self.root
        for ch in key:
            curr_node = curr_node[1].setdefault(ch, [None, {}])
        curr_node[0] = value

    def find(self, key):
        """
        Finds the given key in the Trie.

        Args:
        key: The key to search for in the trie.

        Returns:
        The associated value with the key if the key exists in the tree and None
        otherwise.
        """
        curr_node = self.root

        for ch in key:
            try:
                curr_node = curr_node[1][ch]
            except KeyError:
                return None

        return curr_node[0]

    def find_prefix(self, key):
        """
        Finds a maximal prefix of the key in the trie if possible.

        Args:
        key: The key whose prefix will be searched for in the Trie.

        Returns:
        An ordered pair where the first value is the value found in the Trie
        from a prefix in the key and the second value is the remainder of the
        key.
        """
        curr_node = self.root
        remainder = key

        for ch in key:
            try:
                curr_node = curr_node[1][ch]
            except KeyError:
                return (curr_node[0], remainder)
            remainder = remainder[1:]

        return (curr_node[0], remainder)


def create_conversion_tree():
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
    t = create_conversion_tree()

    total = ''
    idx = 0

    while idx < len(text):
        value, left = t.find_prefix(text[idx:])

        if value is None:
            total += text[idx]
            idx += 1
        else:
            total += value
            idx += len(text) - idx - len(left)

    return total + text[idx:]


beta = 'th=s tou= filoso/fou'.upper()
uni = beta_to_uni(beta)
print(uni)
