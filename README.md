[![Build Status](https://travis-ci.org/matgrioni/betacode.svg?branch=master)](https://travis-ci.org/matgrioni/betacode)
[![Coverage Status](https://coveralls.io/repos/github/matgrioni/betacode/badge.svg?branch=master)](https://coveralls.io/github/matgrioni/betacode?branch=master)

## betacode

Convert betacode to unicode and vice-versa easily. Tested on python 3.4, 3.5, and 3.6. The definition used is based off what is found at the [TLG Beta Code Manual](http://www.tlg.uci.edu/encoding/BCM.pdf). Only the Greek sections were paid attention to.

### Install

Installation is easy. Use `pip` or your preferred method to download from PyPI.

```
pip install betacode
```

### Usage

Note that in all examples, strings are unicode encoded. Input can be in upper or lower case. The official definition from TLG uses only uppercase, but many resources, such as the Perseus catalog, are encoded in lowercase. So, this package accepts both. This package also does not pay much attention to the cannonical order of Greek diacritics that is defined in the official definition. This is because it is unecessary. The only thing that matters in order for the betacode to be unambiguous is that each character must either begin with a `*` or a letter. As long as these constraints are followed, breathing marks, accents, and such can go in any order. However, the cannonical order will be returned when going from unicode to betacode. Also note that currently, only individual, non-combining characters are handled. This means that you cannot do all combinations of letters and diacritics.

#### Betacode to unicode

```
import betacode.conv

beta = 'analabo/ntes de\ kaq\' e(/kaston'
betacode.conv.beta_to_uni(beta) # αναλαβόντες δὲ καθ᾽ ἕκαστον
```

Note that polytonic accent marks will be used, and not monotonic accent marks. Both are de jure equivalent in Greece, and betacode was initially developed to encode classic works. In other words, the oxeîa will be used rather than tónos. The oxeîa form can be converted to the modern accent form easily either through search and replace, or unicode normalization.

#### Unicode to betacode
```
import betacode.conv

uni = 'αναλαβόντες δὲ καθ᾽ ἕκαστον'
betacode.conv.uni_to_beta(uni) # analabo/ntes de\ kaq\' e(/kaston
```

The unicode text should only use polytonic (oxeîa) accent marks.

### Speed

The original implementation used a custom made trie. This maybe was not the fastest (I wasn't sure). So, I compared against a third party trie implementation, pygtrie. The pygtrie had nicer prefix methods which allowed for much faster processing of large texts. This changed converting all of Strabo or Herodotus in the Perseus catalog from a many minute operation to a ~3-4 second operation.

### Modified Betacode

There is talk of a modified betacode that I have seen around on the internet. I have never been able to find a definitive definition of this so I have not implemented it. Among some differences is word final sigma usage, `_` as macron, and uppercase and lowercase roman letters instead of using `*`.


## Development

I am no classicist, and this was done in my free time. It is very possible that there are some letters missing that are not accounted for, or some punctuation that is not properly handled. If that is the case, please tell me as it is easy to fix, or please open a PR.
