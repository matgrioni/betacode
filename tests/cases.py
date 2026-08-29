"""
Beta/unicode equivalence cases for betacode.conv tests.

Each Case names an equivalence between a canonical betacode string and its
unicode counterpart. By default a case is checked in every direction the
library supports:
  - beta_to_uni(beta, strict=True) == uni
  - beta_to_uni(variant, strict=False) == uni, for every diacritic-order
    variant of beta (see test_conv.py for how variants are generated)
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
    skip generating its diacritic-order variants.

This module is excluded from codespell in `make lint`: the betacode strings
here are dense in short, accented tokens that regularly collide with
codespell's dictionary.
"""

from dataclasses import dataclass


@dataclass(frozen=True)
class Case:
    """A single beta/uni equivalence to check, with flags for asymmetric cases."""

    id: str
    beta: str
    uni: str
    skip_to_uni: bool = False
    skip_to_beta: bool = False
    fuzz: bool = True


CONV_CASES = [
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
    Case("hyphenated_compound", "a)/lloi-de\\", "ἄλλοι‐δὲ"),
]
