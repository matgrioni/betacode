"""
Tests for betacode.conv: beta_to_uni and uni_to_beta.

Each Case names an equivalence between a betacode string and its unicode
counterpart. By default a case is checked in every direction the library
supports:
  - beta_to_uni(beta, strict=False) == uni
  - beta_to_uni(beta, strict=True) == uni
  - uni_to_beta(uni) == beta

Not every case is symmetric though, so a case can opt out of some of the above:
  - out_of_order: `beta` has its diacritics in a non-canonical order. Only
    beta_to_uni(beta, strict=False) is checked. strict rejects reordering, and
    uni_to_beta always emits the canonical ordering, so neither of those would
    reproduce this particular `beta`.
  - skip_to_beta: `uni` is reachable from `beta`, but converting `uni` back does
    not reproduce this exact `beta`. This is usually because multiple
    betacode spellings collapse to the same unicode character, e.g. bare "s"
    for a medial sigma vs. the explicit "s1", or "s2" vs. a contextually
    inferred final sigma. Only the beta_to_uni direction is checked.
  - skip_to_uni: `beta` cannot be produced by converting `uni` back. This is
    usually because `uni` contains characters, such as plain ASCII or Latin
    text, that beta_to_uni would itself try to transliterate. Only
    uni_to_beta is checked.
"""

import dataclasses
import unicodedata

import pytest

import betacode.conv


@dataclasses.dataclass(frozen=True)
class Case:
    """A single beta/uni equivalence to check, with flags for asymmetric cases."""

    id: str
    beta: str
    uni: str
    out_of_order: bool = False
    skip_to_uni: bool = False
    skip_to_beta: bool = False


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
    Case(
        "out_of_order",
        "e/)oiken h\\) dida/skonti; nh\\ a=|)i+\\",
        "ἔοικεν ἢ διδάσκοντι; νὴ ᾆῒ",
        out_of_order=True,
    ),
    Case(
        "cap_out_of_order",
        "*)/eforos ka*)/ei\\ a/)lloi",
        "Ἔφορος καἜὶ ἄλλοι",
        out_of_order=True,
    ),
    Case(
        "cap_out_of_order_with_iota",
        "*)/eforos ka*)/ei\\ a/)lloi *)h\\|",
        "Ἔφορος καἜὶ ἄλλοι ᾚ",
        out_of_order=True,
    ),
    Case(
        "cap_out_of_order_asterisk_position",
        "*)e/foros ka*e)/i\\ a/)lloi *)\\h|",
        "Ἔφορος καἜὶ ἄλλοι ᾚ",
        out_of_order=True,
    ),
    Case(
        "out_of_order_iota_subscript_perispomeni",
        "e)n d' e)\\pes' w)keanw|=",
        "ἐν δ’ ἒπεσ’ ὠκεανῷ",
        out_of_order=True,
    ),
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
def test_conv_equivalence(case: Case) -> None:
    """Check the directions of case's beta/uni equivalence that its flags allow."""
    assert not (
        case.skip_to_uni and case.skip_to_beta
    ), "a case cannot skip both directions"

    uni_normalized = unicodedata.normalize("NFC", case.uni)
    beta_normalized = unicodedata.normalize("NFC", case.beta)

    if not case.skip_to_uni:
        non_strict = unicodedata.normalize(
            "NFC", betacode.conv.beta_to_uni(case.beta, strict=False)
        )
        assert non_strict == uni_normalized

        if not case.out_of_order:
            strict = unicodedata.normalize(
                "NFC", betacode.conv.beta_to_uni(case.beta, strict=True)
            )
            assert strict == uni_normalized

    if not case.out_of_order and not case.skip_to_beta:
        reverse = unicodedata.normalize("NFC", betacode.conv.uni_to_beta(case.uni))
        assert reverse == beta_normalized
