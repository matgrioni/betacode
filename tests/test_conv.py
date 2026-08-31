"""
Test engine that validates the Case list defined in cases.py.

For each Case, validates the desired directions of conversion and other
validation options such as fuzzing. Actual cases are authored in cases.py
which contains all validation cases.
"""

import itertools
import unicodedata

import pytest

import betacode
from betacode import _map
from .cases import CONV_CASES, Case

_MAX_TOKEN_LEN = max(len(key) for key in _map.BETACODE_MAP)


def _tokenize(beta: str) -> list[str]:
    """Split a canonical betacode string into its component tokens.

    Each returned piece is either a full entry from BETACODE_MAP (e.g. "a)/",
    "*)\\h|") or a single character that isn't part of any token, such as
    whitespace or punctuation.

    Args:
        beta: The betacode string to split, assumed to already be in
            canonical diacritic order.

    Returns:
        The component tokens/characters, in order.
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
    """All ways to reorder a single betacode token's diacritics.

    Args:
        token: A single betacode token in canonical order. If it isn't
            actually a token in BETACODE_MAP, it's returned unchanged.

    Returns:
        Every valid reordering of token's diacritics, sorted.
    """
    if token not in _map.BETACODE_MAP:
        return [token]

    anchor = token[0]
    if len(token) > 1:
        assert anchor == "*" or anchor.isalpha(), f"malformed betacode token: {token!r}"

    reorderings = {anchor + "".join(perm) for perm in itertools.permutations(token[1:])}
    return sorted(reorderings)


def _reorderings(beta: str) -> list[str]:
    """All diacritic-order variants of a canonical betacode string.

    Args:
        beta: The betacode string to generate variants of, assumed to
            already be in canonical order.

    Returns:
        Every combination of diacritic-order variants across beta's tokens.
    """
    choices = [_token_reorderings(token) for token in _tokenize(beta)]
    return ["".join(combo) for combo in itertools.product(*choices)]


@pytest.mark.parametrize("case", CONV_CASES, ids=[case.id for case in CONV_CASES])
def test_conv_equivalence(case: Case, order_fuzz_enabled: bool) -> None:
    """Check the directions and modes of case's beta/uni equivalence its options allow.

    Args:
        case: The equivalence to check, and which directions/modes to check
            it in.
        order_fuzz_enabled: Whether to fuzz diacritic order for the
            non-strict beta_to_uni check (see --no-order-fuzz).
    """
    assert not (case.to_uni.skip and case.to_beta.skip), "a case cannot skip both directions"

    uni_normalized = unicodedata.normalize("NFC", case.uni)
    beta_normalized = unicodedata.normalize("NFC", case.beta)

    if not case.to_uni.skip:
        if not case.to_uni.skip_strict:
            strict = unicodedata.normalize("NFC", betacode.beta_to_uni(case.beta, strict=True))
            assert strict == uni_normalized

        if not case.to_uni.skip_non_strict:
            fuzz = not case.to_uni.skip_fuzz and order_fuzz_enabled
            variants = _reorderings(case.beta) if fuzz else [case.beta]
            for variant in variants:
                non_strict = unicodedata.normalize(
                    "NFC", betacode.beta_to_uni(variant, strict=False)
                )
                assert non_strict == uni_normalized, f"beta_to_uni({variant!r}, strict=False)"

    if not case.to_beta.skip:
        reverse = unicodedata.normalize("NFC", betacode.uni_to_beta(case.uni))
        assert reverse == beta_normalized
