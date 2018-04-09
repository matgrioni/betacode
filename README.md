[![Build Status](https://travis-ci.org/matgrioni/betacode.svg?branch=master)](https://travis-ci.org/matgrioni/betacode)

## betaconv

Convert betacode to unicode and vice-versa easily.

### Install

Installation is easy. Use `pip` or your preferred method to download from PyPI.

```
pip install betaconv
```

### Usage

#### Betacode to unicode

```
import betacode.conv

beta = 'analabo/ntes de\ kaq\' e(/kaston'
betacode.conv.beta_to_uni(beta) # αναλαβόντες δὲ καθ᾽ ἕκαστον
```

#### Unicode to betacode
```
import betacode.conv

uni = 'αναλαβόντες δὲ καθ᾽ ἕκαστον'
betacode.conv.uni_to_beta(uni) # analabo/ntes de\ kaq\' e(/kaston
```
