import betacode.conv

def _test_beta_uni_equality(beta, uni):
    """
    Test that the result of converting beta is uni.

    Args:
    beta: The beta code to convert.
    uni: The expected unicode result from conversion.
    """
    assert uni == betacode.conv.beta_to_uni(beta)

def test_simple_conv():
    beta = 'tou='
    uni = 'τοῦ'

    _test_beta_uni_equality(beta, uni)

def test_final_sigma_string():
    beta = 'th=s'
    uni = 'τῆς'

    _test_beta_uni_equality(beta, uni)

def test_final_sigma_word():
    beta = 'th=s tou='
    uni = 'τῆς τοῦ'

    _test_beta_uni_equality(beta, uni)

def test_final_sigma_whitespace():
    beta = 'th=s\ttou='
    uni = 'τῆς\tτοῦ'

    _test_beta_uni_equality(beta, uni)

def test_multi_word():
    beta = 'analabo/ntes de\ kaq\' e(/kaston'
    uni = 'αναλαβόντες δὲ καθ᾽ ἕκαστον'

    _test_beta_uni_equality(beta, uni)

def test_punctuation_semicolon():
    beta = 'e)/oiken h)\ dida/skonti; nh\\'
    uni = 'ἔοικεν ἢ διδάσκοντι; νὴ'

    _test_beta_uni_equality(beta, uni)

def test_punctuation_colon():
    beta = 'dh=lon: oi(/ te'
    uni = 'δῆλον: οἵ τε'

    _test_beta_uni_equality(beta, uni)
