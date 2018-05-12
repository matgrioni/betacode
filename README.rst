|Build Status| |Coverage Status|

betacode
--------

Convert betacode to unicode and vice-versa easily. Tested on python 3.4,
3.5, and 3.6.

Install
~~~~~~~

Installation is easy. Use ``pip`` or your preferred method to download
from PyPI.

::

    pip install betacode

Usage
~~~~~

Note that in all examples, strings are unicode encoded.

Betacode to unicode
^^^^^^^^^^^^^^^^^^^

::

    import betacode.conv

    beta = 'analabo/ntes de\ kaq\' e(/kaston'
    betacode.conv.beta_to_uni(beta) # αναλαβόντες δὲ καθ᾽ ἕκαστον

Note that polytonic accent marks will be used, and not monotonic accent
marks. Both are de jure equivalent in Greece, and betacode was initially
developed to encode classic works. In other words, the oxeîa will be
used rather than tónos. The oxeîa form can be converted to the modern
accent form through unicode normalization which is easy in python.

::

    import unicodedata

    import betacode.conv

    beta = 'analabo/ntes de\ kaq\' e(/kaston'
    uni = betacode.conv.beta_to_uni(beta) # αναλαβόντες δὲ καθ᾽ ἕκαστον

    unicodedata.normalize('NFC', uni) # Use the appropriate normalization ('NFC', 'NFKC', etc).

Unicode to betacode
^^^^^^^^^^^^^^^^^^^

::

    import betacode.conv

    uni = 'αναλαβόντες δὲ καθ᾽ ἕκαστον'
    betacode.conv.uni_to_beta(uni) # analabo/ntes de\ kaq\' e(/kaston

The unicode text can use polytonic (oxeîa) or monotonic (tónos) accent
marks and converesion will still be correct.

Speed
~~~~~

The original implementation used a custom made trie. This maybe was not
the fastest (I wasn't sure). So, I compared against a third party trie
implementation, pygtrie. The pygtrie had nicer prefix methods which
allowed for much faster processing of large texts. This changed
converting all of Strabo or Herodotus in the Perseus catalog from a many
minute operation to a ~3-4 second operation.

.. |Build Status| image:: https://travis-ci.org/matgrioni/betacode.svg?branch=master
   :target: https://travis-ci.org/matgrioni/betacode
.. |Coverage Status| image:: https://coveralls.io/repos/github/matgrioni/betacode/badge.svg?branch=master
   :target: https://coveralls.io/github/matgrioni/betacode?branch=master
