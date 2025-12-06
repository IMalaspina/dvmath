"""
DV2 - Two-Dimensional Dimensions-Vector Space
==============================================

DV2 represents a 2-dimensional vector space isomorphic to complex numbers (ℂ).

Author: Ivano Franco Malaspina
Date: December 2025
License: MIT
"""

import math
from typing import Union


class DV2:
    """
    DV2 represents a 2-dimensional vector in DV-Space.
    
    Isomorphic to complex numbers ℂ via φ([v, d]) = v + di.
    
    Attributes:
        v (float): Value component (real part)
        d (float): Depth component (imaginary part)
    """
    
    __slots__ = ("v", "d")
    
    def __init__(self, v: float, d: float = 0.0):
        """
        Initialize a DV2 vector.
        
        Args:
            v: Value component
            d: Depth component (default: 0.0)
        """
        self.v = float(v)
        self.d = float(d)
    
    def __repr__(self) -> str:
        if self.d == 0:
            return f"DV2({self.v})"
        return f"DV2({self.v}, {self.d})"
    
    def __str__(self) -> str:
        return f"[{self.v}, {self.d}]"
    
    def __eq__(self, other) -> bool:
        """Check equality with tolerance for floating point errors."""
        if not isinstance(other, DV2):
            return False
        return math.isclose(self.v, other.v, rel_tol=1e-9) and \
               math.isclose(self.d, other.d, rel_tol=1e-9)
    
    def __add__(self, other: Union['DV2', float]) -> 'DV2':
        """Vector addition: component-wise."""
        if isinstance(other, (int, float)):
            return DV2(self.v + other, self.d)
        return DV2(self.v + other.v, self.d + other.d)
    
    __radd__ = __add__
    
    def __sub__(self, other: Union['DV2', float]) -> 'DV2':
        """Vector subtraction: component-wise."""
        if isinstance(other, (int, float)):
            return DV2(self.v - other, self.d)
        return DV2(self.v - other.v, self.d - other.d)
    
    def __mul__(self, other: Union['DV2', float]) -> 'DV2':
        """
        Multiplication.
        
        - Scalar multiplication: k * [v, d] = [kv, kd]
        - DV2 multiplication: [v1, d1] * [v2, d2] = [v1*v2 - d1*d2, v1*d2 + d1*v2]
        """
        if isinstance(other, (int, float)):
            return DV2(self.v * other, self.d * other)
        elif isinstance(other, DV2):
            return DV2(
                self.v * other.v - self.d * other.d,
                self.v * other.d + self.d * other.v
            )
        else:
            raise TypeError(f"Cannot multiply DV2 with {type(other)}")
    
    __rmul__ = __mul__
    
    def __truediv__(self, other: Union['DV2', float]) -> 'DV2':
        """
        Division.
        
        - Scalar division: [v, d] / k = [v/k, d/k]
        - DV2 division: A / B = A * B^(-1)
        - If B is zero-norm, apply STO to A
        """
        if isinstance(other, (int, float)):
            if abs(other) < 1e-10:
                return self.STO()
            return DV2(self.v / other, self.d / other)
        elif isinstance(other, DV2):
            if other.is_zero():
                return self.STO()
            return self * other.inverse()
        else:
            raise TypeError(f"Cannot divide DV2 by {type(other)}")
    
    def __neg__(self) -> 'DV2':
        """Additive inverse."""
        return DV2(-self.v, -self.d)
    
    def __pow__(self, exponent: int) -> 'DV2':
        """
        Exponentiation (integer exponents only).
        
        Uses efficient binary exponentiation.
        """
        if not isinstance(exponent, int):
            raise TypeError("Only integer exponents are supported")
        if exponent == 0:
            return DV2(1.0, 0.0)
        if exponent < 0:
            return self.inverse() ** (-exponent)
        
        # Binary exponentiation
        result = DV2(1.0, 0.0)
        base = self
        n = exponent
        while n > 0:
            if n % 2 == 1:
                result = result * base
            base = base * base
            n //= 2
        return result
    
    def norm(self) -> float:
        """Euclidean norm: ||[v, d]|| = sqrt(v^2 + d^2)."""
        return math.sqrt(self.v**2 + self.d**2)
    
    def is_zero(self) -> bool:
        """Check if the vector is zero (within tolerance)."""
        return self.norm() < 1e-10
    
    def conjugate(self) -> 'DV2':
        """Conjugate: [v, d]* = [v, -d]."""
        return DV2(self.v, -self.d)
    
    def inverse(self) -> 'DV2':
        """
        Multiplicative inverse: [v, d]^(-1) = [v, -d] / (v^2 + d^2).
        
        Raises:
            ZeroDivisionError: If the vector has zero norm.
        """
        norm_sq = self.v**2 + self.d**2
        if norm_sq < 1e-10:
            raise ZeroDivisionError("Cannot invert zero-norm vector. Use STO instead.")
        return DV2(self.v / norm_sq, -self.d / norm_sq)
    
    def TR(self) -> 'DV2':
        """
        Tiefenrotation (TR): 90-degree counter-clockwise rotation.
        
        TR([v, d]) = [-d, v]
        
        This is the algebraic operation equivalent to multiplication by i in ℂ.
        """
        return DV2(-self.d, self.v)
    
    def STO(self) -> 'DV2':
        """
        Singularity Treatment Operation (STO).
        
        This is NOT a new algebraic operation, but a conceptual rule:
        When division by zero occurs, apply TR to the numerator.
        
        STO([v, d]) = TR([v, d]) = [-d, v]
        """
        return self.TR()
    
    def to_complex(self) -> complex:
        """Convert to Python complex number (isomorphism)."""
        return complex(self.v, self.d)
    
    @staticmethod
    def from_complex(c: complex) -> 'DV2':
        """Create DV2 from Python complex number (isomorphism)."""
        return DV2(c.real, c.imag)


# Convenience aliases for backward compatibility
DV = DV2
