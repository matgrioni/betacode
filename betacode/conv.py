import itertools
import unicodedata

import pygtrie

from . import _map

# Special characters that need their own references to rewrite with
_FINAL_LC_SIGMA = '\u03c2'
_MEDIAL_LC_SIGMA = '\u03c3'

# Punctuation marks in the betacode map
_BETA_PUNCTUATION = frozenset('\':-_')

# Individual letter marks. Add s1, s2, and s3 separately from other one betacode
# characters.
_BETA_LETTERS = set('abgdezhqiklmncoprstufxyw')
_BETA_LETTERS.add(('s1',))
_BETA_LETTERS.add(('s2',))
_BETA_LETTERS.add(('s3',))
_BETA_LETTERS = frozenset(_BETA_LETTERS)


def _create_unicode_map(combining):
    """
    Create the inverse map from unicode to betacode.

    Args:
    combining: Flag for how to treat combining codepoints. If set, then they are
        converted into the appropriate betacode form. Otherwise, they are not
        converted at all.

    Returns:
    The hash map to convert unicode characters to the beta code representation.
    """
    unicode_map = {}

    for beta, uni in _map.BETACODE_MAP.items():
        # Include decomposed equivalent where necessary.
        norm = unicodedata.normalize('NFD', uni)
        unicode_map[norm] = beta
        unicode_map[uni] = beta

    # Add the final sigmas.
    final_sigma_norm = unicodedata.normalize('NFD', _FINAL_LC_SIGMA)
    unicode_map[final_sigma_norm] = 's'
    unicode_map[_FINAL_LC_SIGMA] = 's'

    if combining:
        for beta, uni in _map.BETA_COMBINING_MAP.items():
            unicode_map[uni] = beta

    return unicode_map


def _create_conversion_trie(case, combining, strict):
    """
    Create the trie for betacode conversion.

    Args:
    text: The beta code text to convert. All of this text must be betacode.
    case: Case sensitivity, so that if set, only upper case betacode will be
        converted.
    combining: Flag to allow for combining characters in unicode output so that
        any combination of diacritics and letters are allowed. Non-combining
        forms will always be preferred.
    strict: Flag to allow for flexible diacritic order on input.

    Returns:
    The trie for conversion.
    """
    t = pygtrie.CharTrie()

    for beta, uni in _map.BETACODE_MAP.items():
        if strict:
            t[beta] = uni
        else:
            # The order of accents is very strict and weak. Allow for many orders of
            # accents between asterisk and letter or after letter. This does not
            # introduce ambiguity since each betacode token only has one letter and
            # either starts with a asterisk or a letter.
            diacritics = beta[1:]

            perms = itertools.permutations(diacritics)
            for perm in perms:
                perm_str = beta[0] + ''.join(perm)

                t[perm_str.upper()] = uni

                if not case:
                    t[perm_str.lower()] = uni

    if combining:
        for beta, uni in _map.BETA_COMBINING_MAP.items():
            t[beta] = uni

    return t


def _find_max_beta_token_len():
    """
    Finds the maximum length of a single betacode token.

    Returns:
    The length of the longest key in the betacode map, which corresponds to the
    longest single betacode token.
    """
    max_beta_len = -1
    for beta, uni in _map.BETACODE_MAP.items():
        if len(beta) > max_beta_len:
            max_beta_len = len(beta)

    return max_beta_len

_MAX_BETA_TOKEN_LEN = _find_max_beta_token_len()


_BETA_CONVERSION_TRIES = {}
def beta_to_uni(text, case=False, combining=False, strict=False):
    """
    Converts the given text from betacode to unicode.

    Args:
    text: The beta code text to convert. All of this text must be betacode.
    case: Case sensitivity, so that if set, only upper case betacode will be
        converted.
    combining: Flag to allow for combining characters in unicode output so that
        any combination of diacritics and letters are allowed. Non-combining
        forms will always be preferred.
    strict: Flag to allow for flexible diacritic order on input.

    Returns:
    The converted text.
    """
    # Check if the requested configuration for conversion already has a trie
    # stored otherwise convert it.
    param_key = (case, combining, strict)
    try:
       t = _BETA_CONVERSION_TRIES[param_key]
    except KeyError:
        t = _create_conversion_trie(*param_key)
        _BETA_CONVERSION_TRIES[param_key] = t

    transform = []
    idx = 0
    possible_word_boundary = False
    in_middle_beta = False
    current_middle_transform = ['']

    while idx < len(text):
        # TODO: Check if this logic works with many combining characters.
        if possible_word_boundary and len(transform) > 1 and \
            transform[-2] == _MEDIAL_LC_SIGMA and not transform[-1].isalnum():
            transform[-2] = _FINAL_LC_SIGMA

        step = t.longest_prefix(text[idx:idx + _MAX_BETA_TOKEN_LEN])

        if step:
            if not in_middle_beta:
                possible_word_boundary = text[idx] in _BETA_PUNCTUATION
                key, value = step

                # To work with combining characters we have to properly combine when
                # there is a capital letter and the combining characters can be in
                # front of the letter and have to be moved to behind. In this case,
                # the prefix makes an actual match but the rest might not.
                if combining and key[0] == '*':
                    next_transform = ['']
                    for letter in key[1:]:
                        if letter in _BETA_LETTERS:
                            next_transform[0] = t['*' + letter]
                        else:
                            next_transform.append(t[letter])
                    transform.extend(new_transform)
                else:
                    transform.append(value)

                idx += len(key)
            else:
                # If we have encoutered a combining betacode character with an
                # unrecognized prefix, then keep track of its characters.
                key, value = step
                if key in _BETA_LETTERS:
                    current_middle_transform[0] = t['*' + key]
                    transform.extend(current_middle_transform)

                    in_middle_beta = False
                    current_middle_transform.clear()
                else:
                    current_middle_transform.append(value)

        else:
            possible_word_boundary = True

            # If the beginning of a combining capital betacode character is not
            # recognized then keep track of it as we go.
            if combining and text[idx] == '*':
                in_middle_beta = True
            else:
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

_UNI_CONVERSION_TRIES = {}
def uni_to_beta(text, combining=True):
    """
    Convert unicode text to a betacode equivalent.

    This method can handle tónos or oxeîa characters in the input.

    Args:
    text: The text to convert to betacode. This text does not have to all be
        Greek polytonic text, and only Greek characters will be converted. Note
        that in this case, you cannot convert to beta and then back to unicode.
    combining: Flag that is set to encode combining codepoints into the betacode
        equivalent.

    Returns:
    The betacode equivalent of the inputted text where applicable.
    """
    param_key = (combining,)
    try:
        u = _UNI_CONVERSION_TRIES[param_key]
    except KeyError:
        u = _create_unicode_map(*param_key)
        _UNI_CONVERSION_TRIES[param_key] = u

    transform = []

    for ch in text:
        try:
            conv = u[ch]
        except KeyError:
            conv = ch

        transform.append(conv)

    converted = ''.join(transform)
    return converted
