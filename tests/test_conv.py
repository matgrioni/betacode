"""
Tests for betacode.conv: beta_to_uni and uni_to_beta.

Each Case names an equivalence between a canonical betacode string and its
unicode counterpart. By default a case is checked in every direction the
library supports:
  - beta_to_uni(beta, strict=True) == uni
  - beta_to_uni(variant, strict=False) == uni, for every diacritic-order
    variant of beta (see "Order fuzzing" below)
  - uni_to_beta(uni) == beta

Not every case is symmetric though, so a case can opt out of some of the above:
  - skip_to_beta: `uni` is reachable from `beta`, but converting `uni` back does
    not reproduce this exact `beta`. This is usually because multiple
    betacode spellings collapse to the same unicode character, e.g. bare "s"
    for a medial sigma vs. the explicit "s1", or "s2" vs. a contextually
    inferred final sigma. Only the beta_to_uni direction is checked.
  - skip_to_uni: `beta` cannot be produced by converting `uni` back. This is
    usually because `uni` contains characters, such as plain ASCII or Latin
    text, that beta_to_uni would itself try to transliterate. Only
    uni_to_beta is checked.
  - fuzz: set to False to check only the canonical ordering of `beta`, and
    skip generating its diacritic-order variants (see below).

Order fuzzing
--------------
`beta` is assumed to already be in canonical order. Every betacode token
(a run of characters starting with an asterisk or a letter, e.g. "a)/" or
"*)\\h|") accepts its diacritics -- and, for capitals, its base letter -- in
any order when parsed non-strictly. Rather than hand-writing a handful of
scrambled inputs, `_reorderings` derives every valid reordering of `beta`
directly and each is checked against `uni` under beta_to_uni(strict=False).
This can be disabled for the whole run with `pytest --no-order-fuzz`, which
falls back to checking only the canonical ordering.
"""

import dataclasses
import itertools
import unicodedata

import pytest

import betacode
from betacode import _map

_MAX_TOKEN_LEN = max(len(key) for key in _map.BETACODE_MAP)


def _tokenize(beta: str) -> list[str]:
    """
    Split a canonical betacode string into its component tokens.

    Each returned piece is either a full entry from BETACODE_MAP (e.g. "a)/",
    "*)\\h|") or a single character that isn't part of any token, such as
    whitespace or punctuation.
    """
    tokens = []
    idx = 0
    while idx < len(beta):
        for length in range(min(_MAX_TOKEN_LEN, len(beta) - idx), 0, -1):
            candidate = beta[idx : idx + length]
            if candidate in _map.BETACODE_MAP:
                tokens.append(candidate)
                idx += length
                break
        else:
            tokens.append(beta[idx])
            idx += 1

    return tokens


def _token_reorderings(token: str) -> list[str]:
    """All ways to reorder a single betacode token's diacritics."""
    if token not in _map.BETACODE_MAP:
        return [token]

    anchor = token[0]
    if len(token) > 1:
        assert anchor == "*" or anchor.isalpha(), f"malformed betacode token: {token!r}"

    reorderings = {anchor + "".join(perm) for perm in itertools.permutations(token[1:])}
    return sorted(reorderings)


def _reorderings(beta: str) -> list[str]:
    """All diacritic-order variants of a canonical betacode string."""
    choices = [_token_reorderings(token) for token in _tokenize(beta)]
    return ["".join(combo) for combo in itertools.product(*choices)]


@dataclasses.dataclass(frozen=True)
class Case:
    """A single beta/uni equivalence to check, with flags for asymmetric cases."""

    id: str
    beta: str
    uni: str
    skip_to_uni: bool = False
    skip_to_beta: bool = False
    fuzz: bool = True


CASES = [
    Case("empty", "", ""),
    Case("simple_conv_no_diacritics", "ab", "αβ"),
    Case("simple_conv", "tou=", "τοῦ"),
    Case("final_sigma", "th=s", "τῆς"),
    Case("numeric_sigma_id", "th=s2", "τῆς", skip_to_beta=True),
    Case("keep_non_final_sigma_numeric", "th=s3 tou=", "τῆϲ τοῦ"),
    Case("final_sigma_word", "th=s tou=", "τῆς τοῦ"),
    Case("final_sigma_whitespace", "th=s\ttou=", "τῆς\tτοῦ"),
    Case("final_sigma_punctuation", "th=s; tou=", "τῆς; τοῦ"),
    Case("final_sigma_apostrophe", "th=s' tou=", "τῆσ’ τοῦ", skip_to_beta=True),
    Case(
        "multi_word_medial_sigma",
        "analabo/ntes de\\ kaq' e(/kaston",
        "αναλαβόντες δὲ καθ’ ἕκαστον",
        skip_to_beta=True,
    ),
    Case(
        "punctuation_semicolon",
        "e)/oiken h)\\ dida/skonti; nh\\",
        "ἔοικεν ἢ διδάσκοντι; νὴ",
        skip_to_beta=True,
    ),
    Case("punctuation_colon", "dh=lon: oi(/ te", "δῆλον· οἵ τε"),
    Case("many_accents", "*)/eforos kai\\ a)/lloi", "Ἔφορος καὶ ἄλλοι"),
    Case(
        "multiple_elisions",
        "e)n d' e)\\pes' w)keanw=|",
        "ἐν δ’ ἒπεσ’ ὠκεανῷ",
        skip_to_beta=True,
    ),
    Case("iota_subscript_and_diaeresis_grave", "a)=| i\\+", "ᾆ ῒ"),
    Case("cap_breathing_grave_iota_subscript", "*)\\h|", "ᾚ"),
    Case(
        "colon_ascii_punctuation_passthrough",
        "plei/ous: e)/ti de\\ oi( meta\\",
        "πλείους: ἔτι δὲ οἱ μετὰ",
        skip_to_uni=True,
    ),
    Case(
        "non_greek_passthrough",
        "Many python packages cannot convert this: e)/ti de\\ oi(",
        "Many python packages cannot convert this: ἔτι δὲ οἱ",
        skip_to_uni=True,
    ),
]


@pytest.mark.parametrize("case", CASES, ids=[case.id for case in CASES])
def test_conv_equivalence(case: Case, order_fuzz_enabled: bool) -> None:
    """Check the directions of case's beta/uni equivalence that its flags allow."""
    assert not (
        case.skip_to_uni and case.skip_to_beta
    ), "a case cannot skip both directions"

    uni_normalized = unicodedata.normalize("NFC", case.uni)
    beta_normalized = unicodedata.normalize("NFC", case.beta)

    if not case.skip_to_uni:
        strict = unicodedata.normalize("NFC", betacode.beta_to_uni(case.beta, strict=True))
        assert strict == uni_normalized

        variants = _reorderings(case.beta) if case.fuzz and order_fuzz_enabled else [case.beta]
        for variant in variants:
            non_strict = unicodedata.normalize(
                "NFC", betacode.beta_to_uni(variant, strict=False)
            )
            assert non_strict == uni_normalized, f"beta_to_uni({variant!r}, strict=False)"

    if not case.skip_to_beta:
        reverse = unicodedata.normalize("NFC", betacode.uni_to_beta(case.uni))
        assert reverse == beta_normalized
