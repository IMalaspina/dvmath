"""
DV-Mathematics Core Module
===========================

This module provides the core functionality for DV-Mathematics (Dimensions-Vectors),
a framework for handling singularities through geometric rotations in higher-dimensional spaces.

Author: Ivano Franco Malaspina
Date: December 2025
License: MIT
"""

# Import all classes for convenience
from .dv2 import DV2, DV
from .dv4 import DV4

__all__ = ['DV2', 'DV', 'DV4']
