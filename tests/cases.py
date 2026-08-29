"""
Beta/unicode equivalence cases for betacode.conv tests.

Each Case names an equivalence between a canonical betacode string and its
unicode counterpart, and is checked (by test_conv.py) in up to three ways:
  - beta_to_uni(beta, strict=True) == uni
  - beta_to_uni(variant, strict=False) == uni, for every diacritic-order
    variant of beta (see test_conv.py for how variants are generated)
  - uni_to_beta(uni) == beta

Not every case is symmetric, so each of those checks can be skipped. This is
controlled by two small per-direction option structs on Case:
  - to_uni: ToUniOptions
      - skip: skip both the strict and non-strict beta_to_uni checks
        entirely. Usually because `uni` contains characters, such as plain
        ASCII or Latin text, that beta_to_uni would itself try to
        transliterate.
      - skip_strict / skip_non_strict: skip just one of the two beta_to_uni
        modes, for a case where strict and non-strict parsing of the same
        `beta` are expected to disagree (see the ToUni wrapper below).
      - skip_fuzz: skip generating diacritic-order variants of `beta` for the
        non-strict check, checking only its canonical ordering.
  - to_beta: ToBetaOptions
      - skip: skip the uni_to_beta check. Usually because multiple betacode
        spellings collapse to the same unicode character, e.g. bare "s" for a
        medial sigma vs. the explicit "s1", so only one of them can be the
        one uni_to_beta actually reproduces.

Most cases don't need to construct these structs directly -- the wrapper
functions below cover the common scenarios and read as what each case is
actually demonstrating:
  - Full: nothing is skipped; beta and uni fully agree in both directions.
  - ToUni: only beta_to_uni is checked; uni_to_beta would not reproduce this
    particular `beta` spelling. Both the strict and non-strict checks run by
    default; pass skip_strict or skip_non_strict for a `beta` spelling where
    the two modes are expected to disagree (e.g. diacritics deliberately out
    of order, or ASCII case that only non-strict folds).
  - ToBeta: only uni_to_beta is checked; beta_to_uni would not reproduce this
    particular `uni` text. Takes `uni` before `beta`, since a ToBeta case is
    naturally described starting from the unicode text.

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
    """A case where only beta_to_uni is checked; the reverse uni_to_beta(uni)
    would not reproduce this exact beta spelling. By default both the strict
    and non-strict checks run; pass skip_strict or skip_non_strict for a
    `beta` spelling where the two modes are expected to disagree (e.g.
    diacritics deliberately out of order, or ASCII case that only non-strict
    folds)."""
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
    """A case where only uni_to_beta is checked; beta_to_uni(beta) would not
    reproduce this exact uni text (e.g. it contains characters beta_to_uni
    would itself try to transliterate)."""
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
    # beta_to_uni only ever matches ASCII betacode tokens, so unicode already
    # present in the input (e.g. from mixed-source text) is inert to it. The
    # reverse doesn't hold: uni_to_beta would rewrite the embedded "αβ" back to
    # ASCII, so the uni_to_beta direction is skipped here.
    ToUni("embedded_unicode_passthrough", "lo/gos αβ", "λόγος αβ"),
    # Non-strict mode is order-flexible (see test_conv.py's "Order fuzzing"), but
    # strict mode is not: it still greedily matches whatever valid,
    # canonically-ordered prefix it can find (here, the acute accent alone) and
    # leaves the rest as literal, untranslated text, rather than rejecting the
    # whole token.
    ToUni("strict_partial_match_on_scrambled_order", "a/)", "ά)", skip_non_strict=True),
    ToUni("non_strict_full_match_on_scrambled_order", "a/)", "ἄ", skip_strict=True),
    # Capital Greek letters are always written with a leading "*"; strict mode
    # treats a bare, un-starred capital ASCII letter as literal text rather than
    # folding its case. Non-strict mode does fold it, but only as a side effect
    # of how its trie is built (every diacritic permutation is stored in both
    # ASCII cases) -- not a deliberate "ignore-case" feature -- so it's worth
    # pinning down explicitly.
    ToUni("strict_bare_letter_is_case_sensitive", "A", "A", skip_non_strict=True),
    ToUni("non_strict_bare_letter_folds_case", "A", "α", skip_strict=True),
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


def _generate_map_cases() -> list[Case]:
    """One Case per betacode._map.BETACODE_MAP entry.

    Complements CURATED_CASES above: with ~270 entries in the map, most
    individual tokens (bare "w", "z", the macron/breve marks, most of the
    capital breathing+accent+iota-subscript combinations, ...) never appear in
    any of those curated phrases.
    """
    generated = []

    for beta, uni in _map.BETACODE_MAP.items():
        normalized_uni = unicodedata.normalize("NFC", uni)
        # Need the actual reverse map uni_to_beta uses to know which spelling
        # wins the race described below, not just re-derive its logic here.
        is_canonical_reverse = (
            conv._UNICODE_MAP.get(normalized_uni) == beta  # pylint: disable=protected-access
        )
        case_id = f"map_{beta}"

        if uni == "σ":
            # A medial sigma token ("s"/"s1") converted entirely on its own is
            # indistinguishable from a one-letter word, so beta_to_uni's
            # word-boundary heuristic (conv._penultimate_sigma_word_final)
            # turns it into a final sigma instead of the medial sigma the map
            # itself defines. Skip the beta_to_uni checks for these until that
            # ambiguity is addressed (planned as a separate change). "s" also
            # loses the uni_to_beta canonical-spelling race to "s1" (see
            # is_canonical_reverse below), leaving nothing left to check for
            # it, so it's excluded entirely rather than generating a case that
            # skips both directions.
            if is_canonical_reverse:
                generated.append(ToBeta(case_id, uni, beta))
            continue

        if is_canonical_reverse:
            generated.append(Full(case_id, beta, uni))
        else:
            # Multiple betacode spellings collapse to the same unicode
            # character (e.g. "s2" vs. a contextually inferred final sigma);
            # only the map's last-inserted spelling for that character is what
            # uni_to_beta actually reproduces, so this beta loses that race.
            generated.append(ToUni(case_id, beta, uni))

    return generated


CONV_CASES = CURATED_CASES + _generate_map_cases()
