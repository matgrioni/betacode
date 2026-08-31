"""
Defines the Case list that test_conv.py validates.

Each Case pairs a betacode string with its unicode equivalent, checked in
both directions (beta_to_uni strict/non-strict, and uni_to_beta). Any
direction or mode can be skipped via Case.to_uni/to_beta, but prefer building
cases with the Full/ToUni/ToBeta constructors below over setting those
options by hand -- see their docstrings for what each represents.

This module is excluded from codespell in `make lint`: the betacode strings
here are dense in short, accented tokens that regularly collide with
codespell's dictionary.
"""

import unicodedata
from dataclasses import dataclass, field

from betacode import _map, conv


@dataclass(frozen=True)
class ToUniOptions:
    """Options for the beta_to_uni direction of a Case."""

    skip: bool = False
    skip_strict: bool = False
    skip_non_strict: bool = False
    skip_fuzz: bool = False


@dataclass(frozen=True)
class ToBetaOptions:
    """Options for the uni_to_beta direction of a Case."""

    skip: bool = False


@dataclass(frozen=True)
class Case:
    """A single beta/uni equivalence to check, with per-direction options."""

    id: str
    beta: str
    uni: str
    to_uni: ToUniOptions = field(default_factory=ToUniOptions)
    to_beta: ToBetaOptions = field(default_factory=ToBetaOptions)


# pylint: disable=invalid-name


def Full(case_id: str, beta: str, uni: str) -> Case:
    """A case checked in every direction and mode.

    Use when beta and uni fully agree everywhere: strict and non-strict
    beta_to_uni, and uni_to_beta.

    Args:
        case_id: Unique identifier for the case.
        beta: The canonical betacode spelling.
        uni: Its unicode equivalent.

    Returns:
        A Case with no validations skipped and full bidirectional conversion
        validation.
    """
    return Case(case_id, beta, uni, to_uni=ToUniOptions(), to_beta=ToBetaOptions())


def ToUni(  # pylint: disable=too-many-arguments
    case_id: str,
    beta: str,
    uni: str,
    *,
    skip_fuzz: bool = False,
    skip_strict: bool = False,
    skip_non_strict: bool = False,
) -> Case:
    """A case checked only in the beta_to_uni direction.

    Use when uni_to_beta(uni) would not reproduce this exact beta spelling.
    Both the strict and non-strict checks run by default; skip one of them
    when the two modes are expected to disagree on this beta.

    Args:
        case_id: Unique identifier for the case.
        beta: The betacode spelling to convert.
        uni: The expected unicode equivalent.
        skip_fuzz: Skip diacritic-order variants of beta in the non-strict
            check, checking only its canonical ordering.
        skip_strict: Skip the strict beta_to_uni check.
        skip_non_strict: Skip the non-strict beta_to_uni check.

    Returns:
        A Case with uni_to_beta skipped.
    """
    return Case(
        case_id,
        beta,
        uni,
        to_uni=ToUniOptions(
            skip_fuzz=skip_fuzz, skip_strict=skip_strict, skip_non_strict=skip_non_strict
        ),
        to_beta=ToBetaOptions(skip=True),
    )


def ToBeta(case_id: str, uni: str, beta: str) -> Case:
    """A case checked only in the uni_to_beta direction.

    Use when beta_to_uni(beta) would not reproduce this exact uni text (e.g.
    it contains characters beta_to_uni would itself try to transliterate).

    Args:
        case_id: Unique identifier for the case.
        uni: The unicode text to convert.
        beta: The expected betacode equivalent.

    Returns:
        A Case with beta_to_uni skipped.
    """
    return Case(case_id, beta, uni, to_uni=ToUniOptions(skip=True), to_beta=ToBetaOptions())


# pylint: enable=invalid-name


CURATED_CASES = [
    Full("empty", "", ""),
    Full("simple_conv_no_diacritics", "ab", "αβ"),
    Full("simple_conv", "tou=", "τοῦ"),
    Full("final_sigma", "th=s", "τῆς"),
    Full("keep_non_final_sigma_numeric", "th=s3 tou=", "τῆϲ τοῦ"),
    Full("final_sigma_word", "th=s tou=", "τῆς τοῦ"),
    Full("final_sigma_whitespace", "th=s\ttou=", "τῆς\tτοῦ"),
    Full("final_sigma_punctuation", "th=s; tou=", "τῆς; τοῦ"),
    Full("punctuation_colon", "dh=lon: oi(/ te", "δῆλον· οἵ τε"),
    Full("many_accents", "*)/eforos kai\\ a)/lloi", "Ἔφορος καὶ ἄλλοι"),
    Full("iota_subscript_and_diaeresis_grave", "a)=| i\\+", "ᾆ ῒ"),
    Full("cap_breathing_grave_iota_subscript", "*)\\h|", "ᾚ"),
    Full("hyphenated_compound", "a)/lloi-de\\", "ἄλλοι‐δὲ"),
    ToUni("numeric_sigma_id", "th=s2", "τῆς"),
    ToUni("final_sigma_apostrophe", "th=s' tou=", "τῆσ’ τοῦ"),
    ToUni(
        "multi_word_medial_sigma",
        "analabo/ntes de\\ kaq' e(/kaston",
        "αναλαβόντες δὲ καθ’ ἕκαστον",
    ),
    ToUni(
        "punctuation_semicolon",
        "e)/oiken h)\\ dida/skonti; nh\\",
        "ἔοικεν ἢ διδάσκοντι; νὴ",
    ),
    ToUni(
        "multiple_elisions",
        "e)n d' e)\\pes' w)keanw=|",
        "ἐν δ’ ἒπεσ’ ὠκεανῷ",
    ),
    # Unicode already in the input passes through beta_to_uni untouched;
    # uni_to_beta would convert it back though, so skip that direction.
    ToUni("embedded_unicode_passthrough", "lo/gos αβ", "λόγος αβ"),
    # Strict mode only matches canonical order; non-strict accepts any order.
    ToUni("strict_partial_match_on_scrambled_order", "a/)", "ά)", skip_non_strict=True),
    ToUni("non_strict_full_match_on_scrambled_order", "a/)", "ἄ", skip_strict=True),
    ToBeta(
        "colon_ascii_punctuation_passthrough",
        "πλείους: ἔτι δὲ οἱ μετὰ",
        "plei/ous: e)/ti de\\ oi( meta\\",
    ),
    ToBeta(
        "non_greek_passthrough",
        "Many python packages cannot convert this: ἔτι δὲ οἱ",
        "Many python packages cannot convert this: e)/ti de\\ oi(",
    ),
    ToBeta("non_latin_unicode_passthrough", "Hello, Привет 123!", "Hello, Привет 123!"),
]

# Cases pinning down odd behavior in the current implementation rather than
# intended design -- kept separate so they're easy to find and revisit.
KNOWN_QUIRK_CASES = [
    ToUni("strict_bare_letter_is_case_sensitive", "A", "A", skip_non_strict=True),
    ToUni("non_strict_bare_letter_folds_case", "A", "α", skip_strict=True),
]


def _generate_map_cases() -> list[Case]:
    """Build a Case for each betacode._map.BETACODE_MAP entry.

    Covers tokens no curated case exercises.

    Returns:
        One Case per map entry, skipping "s" entirely (see the comment
        below).
    """
    generated = []

    for beta, uni in _map.BETACODE_MAP.items():
        normalized_uni = unicodedata.normalize("NFC", uni)
        is_canonical_reverse = (
            conv._UNICODE_MAP.get(normalized_uni) == beta  # pylint: disable=protected-access
        )
        case_id = f"map_{beta}"

        if uni == "σ":
            # "s"/"s1" alone trip beta_to_uni's word-boundary final-sigma
            # heuristic (to be addressed separately); skip beta_to_uni for
            # both, and drop "s" entirely since it also loses the
            # uni_to_beta spelling race to "s1", leaving nothing to check.
            if is_canonical_reverse:
                generated.append(ToBeta(case_id, uni, beta))
            continue

        if is_canonical_reverse:
            generated.append(Full(case_id, beta, uni))
        else:
            # A different beta spelling is uni_to_beta's canonical choice
            # for this uni (e.g. "s2" vs. a contextually inferred final
            # sigma), so this one loses that race.
            generated.append(ToUni(case_id, beta, uni))

    return generated


CONV_CASES = CURATED_CASES + _generate_map_cases() + KNOWN_QUIRK_CASES
