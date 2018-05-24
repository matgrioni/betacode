import unicodedata

import betacode.conv

def _test_uni_beta_equality(uni, beta):
    """
    Test that the result of converting uni is beta.

    Comparison is done via the NFC normalization for unicode.

    Args:
    uni: The unicode to convert.
    beta: The expected beta code result from conversion.
    """
    conv = betacode.conv.uni_to_beta(uni)
    conv_normalized = unicodedata.normalize('NFC', conv)
    beta_normalized = unicodedata.normalize('NFC', beta)

    assert conv_normalized == beta_normalized

def test_empty():
    uni = ''
    beta = ''

    _test_uni_beta_equality(uni, beta)

def test_simple_conv():
    uni = 'αβ'
    beta = 'ab'

    _test_uni_beta_equality(uni, beta)

def test_multi_word():
    uni = 'βίον τέχνης καὶ εὐδαιμονίας.'
    beta = 'bi/on te/xnhs kai\ eu)daimoni/as.'

    _test_uni_beta_equality(uni, beta)

def test_many_accents():
    uni = 'Ἔφορος καὶ ἄλλοι'
    beta = '*)/eforos kai\ a)/lloi'

    _test_uni_beta_equality(uni, beta)

def test_colon_punc():
    uni = 'πλείους: ἔτι δὲ οἱ μετὰ'
    beta = 'plei/ous: e)/ti de\ oi( meta\\'

    _test_uni_beta_equality(uni, beta)

def test_mixed_conversion():
    uni = 'Many python packages cannot convert this: ἔτι δὲ οἱ'
    beta = 'Many python packages cannot convert this: e)/ti de\ oi('

    _test_uni_beta_equality(uni, beta)
