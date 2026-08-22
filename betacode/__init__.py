"""
Setups package initialization hooks.
"""

__all__ = ["conv"]

import pathlib
__version__ = (pathlib.Path(__file__).parent / "_version").read_text().strip()
del pathlib
