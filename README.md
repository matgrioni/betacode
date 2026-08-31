[![CI](https://github.com/matgrioni/betacode/actions/workflows/ci.yml/badge.svg?branch=master)](https://github.com/matgrioni/betacode/actions/workflows/ci.yml)

## betacode

Convert betacode to unicode and vice-versa. The mapping is based on the Greek sections of the [TLG Beta Code Manual](http://www.tlg.uci.edu/encoding/BCM.pdf); only Greek is handled (see [Status and limitations](#status-and-limitations)).

## Motivation

I was working on a classics research project and had to use the Perseus catalog to extract some Greek text. Much to my surprise, the only download available was a betacode version — an encoding over 30 years old, rather than modern unicode. There was no pip package I could reach for, so I wrote my own.

At the time I had very little background in classics, and not much more experience programming, so this reflects a lot of early learning rather than careful design. Read [Status and limitations](#status-and-limitations) before relying on it for anything serious.

## Install

```
pip install betacode
```

## Usage

Input can be upper or lower case. The official TLG definition uses only uppercase, but many resources, such as the Perseus catalog, are lowercase, so both are accepted. Diacritic order does not need to follow the canonical order from the TLG manual unless `strict` is set (see below); output always uses the canonical order.

### Betacode to unicode

```python
import betacode

beta = 'analabo/ntes de\ kaq\' e(/kaston'
betacode.beta_to_uni(beta) # αναλαβόντες δὲ καθ᾽ ἕκαστον
```

Polytonic accent marks (oxeîa) are used rather than monotonic ones (tónos). Both are de jure equivalent in Greek, but betacode was designed to encode classical works, so the polytonic diacritics are the better fit. The oxeîa form can be converted to the monotonic form with a search and replace, or via unicode normalization, since oxeîa has a canonical decomposition to tónos.

Conversion can be made stricter with the `strict` flag:

```python
betacode.beta_to_uni(text, strict=True)
```

When set, only the canonical order of diacritics defined by the TLG manual is accepted. Otherwise, diacritics may appear in any order, as long as capital letters begin with `*` and lowercase letters begin with the letter itself rather than a diacritic.

### Unicode to betacode

```python
import betacode

uni = 'αναλαβόντες δὲ καθ᾽ ἕκαστον'
betacode.uni_to_beta(uni) # analabo/ntes de\ kaq\' e(/kaston
```

Input text may use either polytonic (oxeîa) or monotonic (tónos) accent marks.

## Command line usage

Installing the package also installs a `betacode` command with two subcommands, `to-unicode` and `to-beta`. Each accepts one of `-t`/`--text` for raw text on the command line, `-f`/`--file` for a file to convert, or `-i`/`--interactive` for a continuous, REPL-like session.

Convert raw text given directly on the command line:

```
betacode to-unicode --text "lo/gos"
# λόγος
```

```
betacode to-beta --text "λόγος"
# lo/gos
```

Add `--strict` to `to-unicode` to only accept the canonical diacritic order:

```
betacode to-unicode --strict --text "lo/gos"
```

Convert the contents of a file, writing the result to stdout:

```
betacode to-unicode --file input.txt > output.txt
```

Start a continuous session, where each line entered is converted and printed until you exit with `Ctrl-D`:

```
$ betacode to-unicode --interactive
Entering continuous mode. Press Ctrl-D (or Ctrl-Z on Windows) to exit.
>> lo/gos
λόγος
>> kalo/s
καλός
>>
```

## Status and limitations

This library only ever covers the Greek portions of betacode. Betacode as a format encodes several ancient languages, and individual works sometimes mix more than one language in the same source; none of that is handled here, only Greek.

Betacode-to-unicode conversion has been attempted by a number of projects with various complications. Perseus Digital Library [describes some of the transformation work and complications](https://github.com/PerseusDL/tei-conversion-tools/wiki/Greek-Betacode-to-Unicode-Transformations). The format itself isn't especially hard to build a converter for — one of the converters Perseus uses is just an XSL mapping — so implementations like this one aren't rare. I think there's real value in a canonical, easily auditable, open-source converter that people can inspect and trust, but I'm not part of the classics tooling community, so I can't say whether that gap is actually filled or wanted elsewhere.

Additionally, the TLG Beta Code Manual itself defines a lot more than the letters and diacritics this library implements (and different projects may use non-standard encodings as well) and codes for metadata and formatting complicate the format meaningfully, even if it stays (close to?) context-free. None of that extra layer is implemented here and I suspect means that a work from the different classics library cannot be easily taken off the shelf and passed through this library.

**In short, I would not recommend this library for serious conversion work.** For quick lookups or one-off conversions, the [CLI](#command-line-usage) or interactive mode should still be useful. If you have an actual use case this falls short on and would like to use something like this library, I'd genuinely like to hear about it — a specific problem to solve would resolve most of the ambiguity in deciding what's worth improving next. Feel free to open an issue.
