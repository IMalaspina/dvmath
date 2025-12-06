"""
DV-Mathematics Package
=======================

A Python implementation of Dimensions-Vector Mathematics for handling singularities.

Author: Ivano Franco Malaspina
Repository: https://github.com/IMalaspina/dvmath
License: MIT
"""

from .dv2 import DV2, DV
from .dv4 import DV4
from .constants import zero, one, I

# Create standard constants
zero = DV2(0.0, 0.0)
one = DV2(1.0, 0.0)
I = DV2(0.0, 1.0)

__version__ = "1.0.0"
__author__ = "Ivano Franco Malaspina"

__all__ = ["DV", "DV2", "DV4", "zero", "one", "I"]
