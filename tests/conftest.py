"""
Shared pytest configuration for the betacode test suite.
"""

import pytest


def pytest_addoption(parser: pytest.Parser) -> None:
    """Register the --no-order-fuzz command-line option."""
    parser.addoption(
        "--no-order-fuzz",
        action="store_true",
        default=False,
        help=(
            "Skip generating diacritic-order permutations of beta_to_uni test "
            "inputs; only the canonical ordering is checked."
        ),
    )


@pytest.fixture(scope="session")
def order_fuzz_enabled(request: pytest.FixtureRequest) -> bool:
    """Whether tests should fuzz diacritic ordering, per --no-order-fuzz."""
    return not request.config.getoption("--no-order-fuzz")
