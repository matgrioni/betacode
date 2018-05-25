import itertools
import unicodedata

import pygtrie

from . import _map

# Special characters that need their own references to rewrite with
_FINAL_LC_SIGMA = '\u03c2'
_MEDIAL_LC_SIGMA = '\u03c3'

# Punctuation marks in the betacode map
_BETA_PUNCTUATION = frozenset('\':-_')
_BETA_APOSTROPHE = '\u2019'


def _create_unicode_map():
    """
    Create the inverse map from unicode to betacode.

    Returns:
    The hash map to convert unicode characters to the beta code representation.
    """
    unicode_map = {}

    for beta, uni in _map.BETACODE_MAP.items():
        # Include decomposed equivalent where necessary.
        norm = unicodedata.normalize('NFC', uni)
        unicode_map[norm] = beta
        unicode_map[uni] = beta

    # Add the final sigmas.
    final_sigma_norm = unicodedata.normalize('NFC', _FINAL_LC_SIGMA)
    unicode_map[final_sigma_norm] = 's'
    unicode_map[_FINAL_LC_SIGMA] = 's'

    return unicode_map

_UNICODE_MAP = _create_unicode_map()


def _create_conversion_trie(strict):
    """
    Create the trie for betacode conversion.

    Args:
    text: The beta code text to convert. All of this text must be betacode.
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
                t[perm_str.lower()] = uni
                t[perm_str.upper()] = uni

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

def _penultimate_sigma_word_final(text):
    return len(text) > 1 and text[-2] == _MEDIAL_LC_SIGMA and \
        not text[-1].isalnum() and text[-1] != _BETA_APOSTROPHE


_BETA_CONVERSION_TRIES = {}
def beta_to_uni(text, strict=False):
    """
    Converts the given text from betacode to unicode.

    Args:
    text: The beta code text to convert. All of this text must be betacode.
    strict: Flag to allow for flexible diacritic order on input.

    Returns:
    The converted text.
    """
    # Check if the requested configuration for conversion already has a trie
    # stored otherwise convert it.
    param_key = (strict,)
    try:
       t = _BETA_CONVERSION_TRIES[param_key]
    except KeyError:
        t = _create_conversion_trie(*param_key)
        _BETA_CONVERSION_TRIES[param_key] = t

    transform = []
    idx = 0
    possible_word_boundary = False

    while idx < len(text):
        if possible_word_boundary and _penultimate_sigma_word_final(transform):
            transform[-2] = _FINAL_LC_SIGMA

        step = t.longest_prefix(text[idx:idx + _MAX_BETA_TOKEN_LEN])

        if step:
            possible_word_boundary = text[idx] in _BETA_PUNCTUATION

            key, value = step
            transform.append(value)
            idx += len(key)
        else:
            possible_word_boundary = True

            transform.append(text[idx])
            idx += 1

    # Check one last time in case there is some whitespace or punctuation at the
    # end and check if the last character is a sigma.
    if possible_word_boundary and _penultimate_sigma_word_final(transform):
        transform[-2] = _FINAL_LC_SIGMA
    elif len(transform) > 0 and transform[-1] == _MEDIAL_LC_SIGMA:
        transform[-1] = _FINAL_LC_SIGMA

    converted = ''.join(transform)
    return converted

def uni_to_beta(text):
    """
    Convert unicode text to a betacode equivalent.

    This method can handle tónos or oxeîa characters in the input.

    Args:
    text: The text to convert to betacode. This text does not have to all be
        Greek polytonic text, and only Greek characters will be converted. Note
        that in this case, you cannot convert to beta and then back to unicode.

    Returns:
    The betacode equivalent of the inputted text where applicable.
    """
    u = _UNICODE_MAP

    transform = []

    for ch in text:
        try:
            conv = u[ch]
        except KeyError:
            conv = ch

        transform.append(conv)

    converted = ''.join(transform)
    return converted
