[![Build Status](https://travis-ci.org/matgrioni/betacode.svg?branch=master)](https://travis-ci.org/matgrioni/betacode)
[![Coverage Status](https://coveralls.io/repos/github/matgrioni/betacode/badge.svg?branch=master)](https://coveralls.io/github/matgrioni/betacode?branch=master)

## betacode

Convert betacode to unicode and vice-versa easily.

### Install

Installation is easy. Use `pip` or your preferred method to download from PyPI.

```
pip install betacode
```

### Usage

#### Betacode to unicode

```
import betacode.conv

beta = 'analabo/ntes de\ kaq\' e(/kaston'
betacode.conv.beta_to_uni(beta) # αναλαβόντες δὲ καθ᾽ ἕκαστον
```

Note that polytonic accent marks will be used, and not monotonic accent marks. Both are de jure equivalent in Greece, and betacode was initially developed to encode classic works. In other words, the oxeîa will be used rather than tónos. The oxeîa form can be converted to the modern accent form through unicode normalization which is easy in python.

```
import unicodedata

import betacode.conv

beta = 'analabo/ntes de\ kaq\' e(/kaston'
uni = betacode.conv.beta_to_uni(beta) # αναλαβόντες δὲ καθ᾽ ἕκαστον

unicodedata.normalize('NFC', uni) # Use the appropriate normalization ('NFC', 'NFKC', etc).
```

#### Unicode to betacode
```
import betacode.conv

uni = 'αναλαβόντες δὲ καθ᾽ ἕκαστον'
betacode.conv.uni_to_beta(uni) # analabo/ntes de\ kaq\' e(/kaston
```
