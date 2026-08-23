"""
Setup package initialization hooks.
"""

__all__ = ["beta_to_uni", "uni_to_beta"]

from .conv import beta_to_uni, uni_to_beta

import pathlib
__version__ = (pathlib.Path(__file__).parent / "_version").read_text().strip()
del pathlib
