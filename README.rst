|Build Status| |Coverage Status|

betacode
--------

Convert betacode to unicode and vice-versa easily. Tested on python 3.4,
3.5, and 3.6. The definition used is based off what is found at the `TLG
Beta Code Manual <http://www.tlg.uci.edu/encoding/BCM.pdf>`__. Only the
Greek sections were paid attention to.

Motivation
----------

I was working a classics research project and had to use the Perseus
catalog to extract some Greek work. Much to my surprise however, the
only download I could find was a betacode version. An encoding that is
over 30 years old, rather than modern, fancy, clean unicode. There was
no nice pip package that I could easily go to for this simple task, so I
decided to roll my own.

Install
~~~~~~~

Installation is easy. Use ``pip`` or your preferred method to download
from PyPI.

::

    pip install betacode

Usage
~~~~~

Note that in all examples, strings are unicode encoded. Input can be in
upper or lower case. The official definition from TLG uses only
uppercase, but many resources, such as the Perseus catalog, are encoded
in lowercase, so this package accepts both. This package also can
disregard the unnecessary cannonical order of Greek diacritics from the
official definition. The only thing that matters in order for the
betacode to be unambiguous is that each unit must either begin with a
``*`` or a letter. As long as these constraints are followed, breathing
marks, accents, and such can go in any order. However, the cannonical
order will be returned when going from unicode to betacode. Also note
that currently, only individual, non-combining characters are handled.
This means that you cannot do all combinations of letters and
diacritics. Only those defined as composite characters in the Greek and
Extended Greek sections of unicode.

Betacode to unicode
^^^^^^^^^^^^^^^^^^^

::

    import betacode.conv

    beta = 'analabo/ntes de\ kaq\' e(/kaston'
    betacode.conv.beta_to_uni(beta) # αναλαβόντες δὲ καθ᾽ ἕκαστον

Note that polytonic accent marks will be used, and not monotonic accent
marks. Both are de jure equivalent in Greece, but betacode was initially
developed to encode classic works so the polytonic diacritics are more
fitting. In other words, the oxeîa will be used rather than tónos. The
oxeîa form can be converted to the modern accent form easily either
through search and replace, or unicode normalization since oxeîa has
canonical decomposition into tónos.

Conversion can also be made more strict by using the ``strict`` flag.

::

    beta_to_uni(text, strict=False)

If set, only the cannonical order of diacritics is accepted in betacode.
If it is not set, then any order is allowed as long as capital letters
begin with a ``*`` and lowercase letters begin with the letter and not a
diacritic.

Unicode to betacode
^^^^^^^^^^^^^^^^^^^

::

    import betacode.conv

    uni = 'αναλαβόντες δὲ καθ᾽ ἕκαστον'
    betacode.conv.uni_to_beta(uni) # analabo/ntes de\ kaq\' e(/kaston

The unicode text can use polytonic (oxeîa) accent marks or monotonic
(tónos) accent marks can be used.

Speed
~~~~~

The original implementation used a custom made trie. This maybe was not
the fastest (I wasn't sure). So, I compared against a third party trie
implementation, pygtrie. The pygtrie had nicer prefix methods which
allowed for much faster processing of large texts. This changed
converting all of Strabo or Herodotus in the Perseus catalog from a many
minute operation to a ~3-4 second operation. I have seen implementations
that use regular expressions which I suspsect might be faster since the
underlying implementation is in C. However, this package is much smaller
and simpler if betacode conversion is all that is needed than CLTK, for
example.

Modified Betacode
~~~~~~~~~~~~~~~~~

There is talk of a modified betacode that I have seen around on the
internet. I have never been able to find a definitive definition of this
so I have not implemented it. Among some differences is word final sigma
usage, ``_`` as macron, and uppercase and lowercase roman letters
instead of using ``*``.

Development
-----------

I am no classicist, and this was done in my free time. It is very
possible that there are some letters missing that are not accounted for,
or some punctuation that is not properly handled. If that is the case,
please tell me as it is easy to fix, or please open a PR for your own
branch. Write tests if you do add a feature.

.. |Build Status| image:: https://travis-ci.org/matgrioni/betacode.svg?branch=master
   :target: https://travis-ci.org/matgrioni/betacode
.. |Coverage Status| image:: https://coveralls.io/repos/github/matgrioni/betacode/badge.svg?branch=master
   :target: https://coveralls.io/github/matgrioni/betacode?branch=master
