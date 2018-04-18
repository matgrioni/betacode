import betacode.conv

def _test_beta_uni_equality(beta, uni):
    """
    Test that the result of converting uni is beta.

    Args:
    beta: The expected beta code result from conversion.
    uni: The unicode to convert.
    """
    assert beta == betacode.conv.uni_to_beta(uni)

def test_empty():
    uni = ''
    beta = ''

    _test_beta_uni_equality(beta, uni)

def test_simple_conv():
    uni = 'αβ'
    beta = 'ab'

    _test_beta_uni_equality(beta, uni)

def test_multi_word():
    uni = 'βίον τέχνης καὶ εὐδαιμονίας.'
    beta = 'bi/on te/xnhs kai\ eu)daimoni/as.'

    _test_beta_uni_equality(beta, uni)

def test_many_accents():
    uni = 'Ἔφορος καὶ ἄλλοι'
    beta = '*e)/foros kai\ a)/lloi'

    _test_beta_uni_equality(beta, uni)

def test_colon_punc():
    uni = 'πλείους: ἔτι δὲ οἱ μετὰ'
    beta = 'plei/ous: e)/ti de\ oi( meta\\'

    _test_beta_uni_equality(beta, uni)

def test_mixed_transfer():
    uni = 'Many python packages cannot convert this: ἔτι δὲ οἱ'
    beta = 'Many python packages cannot convert this: e)/ti de\ oi('

    _test_beta_uni_equality(beta, uni)
