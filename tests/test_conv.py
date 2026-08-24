"""
Tests for betacode.conv: beta_to_uni and uni_to_beta.

Each Case names an equivalence between a canonical betacode string and its
unicode counterpart. By default a case is checked in every direction the
library supports:
  - beta_to_uni(beta, strict=True) == uni
  - beta_to_uni(variant, strict=False) == uni, for every diacritic-order
    variant of beta (see "Order fuzzing" below)
  - uni_to_beta(uni) == beta

Not every case is symmetric though, so a case can opt out of checking one
direction -- see the Case flags documented alongside it in cases.py.

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

import itertools
import unicodedata

import pytest

import betacode
from betacode import _map
from .cases import CONV_CASES, Case

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


@pytest.mark.parametrize("case", CONV_CASES, ids=[case.id for case in CONV_CASES])
def test_conv_equivalence(case: Case, order_fuzz_enabled: bool) -> None:
    """Check the directions of case's beta/uni equivalence that its flags allow."""
    assert not (case.skip_to_uni and case.skip_to_beta), "a case cannot skip both directions"

    uni_normalized = unicodedata.normalize("NFC", case.uni)
    beta_normalized = unicodedata.normalize("NFC", case.beta)

    if not case.skip_to_uni:
        strict = unicodedata.normalize("NFC", betacode.beta_to_uni(case.beta, strict=True))
        assert strict == uni_normalized

        variants = _reorderings(case.beta) if case.fuzz and order_fuzz_enabled else [case.beta]
        for variant in variants:
            non_strict = unicodedata.normalize("NFC", betacode.beta_to_uni(variant, strict=False))
            assert non_strict == uni_normalized, f"beta_to_uni({variant!r}, strict=False)"

    if not case.skip_to_beta:
        reverse = unicodedata.normalize("NFC", betacode.uni_to_beta(case.uni))
        assert reverse == beta_normalized
