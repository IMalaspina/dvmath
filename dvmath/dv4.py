"""
DV4 - Four-Dimensional Dimensions-Vector Space
===============================================

DV4 represents a 4-dimensional vector space isomorphic to quaternions (ℍ).

Author: Ivano Franco Malaspina
Date: December 2025
License: MIT
"""

import math
from typing import Union


class DV4:
    """
    DV4 represents a 4-dimensional vector in DV-Space.
    
    Isomorphic to quaternions ℍ via ψ([v, d1, d2, d3]) = v + d1*i + d2*j + d3*k.
    
    Attributes:
        v (float): Value component (scalar part)
        d1 (float): First depth component (i-component)
        d2 (float): Second depth component (j-component)
        d3 (float): Third depth component (k-component)
    """
    
    __slots__ = ("v", "d1", "d2", "d3")
    
    def __init__(self, v: float, d1: float = 0.0, d2: float = 0.0, d3: float = 0.0):
        """
        Initialize a DV4 vector.
        
        Args:
            v: Value component
            d1: First depth component (default: 0.0)
            d2: Second depth component (default: 0.0)
            d3: Third depth component (default: 0.0)
        """
        self.v = float(v)
        self.d1 = float(d1)
        self.d2 = float(d2)
        self.d3 = float(d3)
    
    def __repr__(self) -> str:
        if self.d1 == 0 and self.d2 == 0 and self.d3 == 0:
            return f"DV4({self.v})"
        return f"DV4({self.v}, {self.d1}, {self.d2}, {self.d3})"
    
    def __str__(self) -> str:
        return f"[{self.v}, {self.d1}, {self.d2}, {self.d3}]"
    
    def __eq__(self, other) -> bool:
        """Check equality with tolerance for floating point errors."""
        if not isinstance(other, DV4):
            return False
        return all(math.isclose(a, b, rel_tol=1e-9) for a, b in [
            (self.v, other.v), (self.d1, other.d1), 
            (self.d2, other.d2), (self.d3, other.d3)
        ])
    
    def __add__(self, other: Union['DV4', float]) -> 'DV4':
        """Vector addition: component-wise."""
        if isinstance(other, (int, float)):
            return DV4(self.v + other, self.d1, self.d2, self.d3)
        return DV4(
            self.v + other.v,
            self.d1 + other.d1,
            self.d2 + other.d2,
            self.d3 + other.d3
        )
    
    __radd__ = __add__
    
    def __sub__(self, other: Union['DV4', float]) -> 'DV4':
        """Vector subtraction: component-wise."""
        if isinstance(other, (int, float)):
            return DV4(self.v - other, self.d1, self.d2, self.d3)
        return DV4(
            self.v - other.v,
            self.d1 - other.d1,
            self.d2 - other.d2,
            self.d3 - other.d3
        )
    
    def __mul__(self, other: Union['DV4', float]) -> 'DV4':
        """
        Multiplication.
        
        - Scalar multiplication: k * A = [kv, kd1, kd2, kd3]
        - DV4 multiplication: Quaternion multiplication rules (non-commutative)
        """
        if isinstance(other, (int, float)):
            return DV4(
                self.v * other,
                self.d1 * other,
                self.d2 * other,
                self.d3 * other
            )
        elif isinstance(other, DV4):
            # Quaternion multiplication: (a + bi + cj + dk)(e + fi + gj + hk)
            return DV4(
                self.v * other.v - self.d1 * other.d1 - self.d2 * other.d2 - self.d3 * other.d3,
                self.v * other.d1 + self.d1 * other.v + self.d2 * other.d3 - self.d3 * other.d2,
                self.v * other.d2 - self.d1 * other.d3 + self.d2 * other.v + self.d3 * other.d1,
                self.v * other.d3 + self.d1 * other.d2 - self.d2 * other.d1 + self.d3 * other.v
            )
        else:
            raise TypeError(f"Cannot multiply DV4 with {type(other)}")
    
    __rmul__ = __mul__
    
    def __truediv__(self, other: Union['DV4', float]) -> 'DV4':
        """
        Division.
        
        - Scalar division: A / k = [v/k, d1/k, d2/k, d3/k]
        - DV4 division: A / B = A * B^(-1)
        - If B is zero-norm, apply STO to A
        """
        if isinstance(other, (int, float)):
            if abs(other) < 1e-10:
                return self.STO()
            return DV4(
                self.v / other,
                self.d1 / other,
                self.d2 / other,
                self.d3 / other
            )
        elif isinstance(other, DV4):
            if other.is_zero():
                return self.STO()
            return self * other.inverse()
        else:
            raise TypeError(f"Cannot divide DV4 by {type(other)}")
    
    def __neg__(self) -> 'DV4':
        """Additive inverse."""
        return DV4(-self.v, -self.d1, -self.d2, -self.d3)
    
    def norm(self) -> float:
        """Euclidean norm: ||A|| = sqrt(v^2 + d1^2 + d2^2 + d3^2)."""
        return math.sqrt(self.v**2 + self.d1**2 + self.d2**2 + self.d3**2)
    
    def is_zero(self) -> bool:
        """Check if the vector is zero (within tolerance)."""
        return self.norm() < 1e-10
    
    def conjugate(self) -> 'DV4':
        """Conjugate: [v, d1, d2, d3]* = [v, -d1, -d2, -d3]."""
        return DV4(self.v, -self.d1, -self.d2, -self.d3)
    
    def inverse(self) -> 'DV4':
        """
        Multiplicative inverse: A^(-1) = A* / ||A||^2.
        
        Raises:
            ZeroDivisionError: If the vector has zero norm.
        """
        norm_sq = self.v**2 + self.d1**2 + self.d2**2 + self.d3**2
        if norm_sq < 1e-10:
            raise ZeroDivisionError("Cannot invert zero-norm vector. Use STO instead.")
        return DV4(
            self.v / norm_sq,
            -self.d1 / norm_sq,
            -self.d2 / norm_sq,
            -self.d3 / norm_sq
        )
    
    def GTR1(self) -> 'DV4':
        """
        Generalized Tiefenrotation 1 (GTR1): Multiplication by i.
        
        GTR1([v, d1, d2, d3]) = [-d1, v, d3, -d2]
        
        This is the validated definition, equivalent to quaternion multiplication by i.
        """
        return DV4(-self.d1, self.v, self.d3, -self.d2)
    
    def GTR2(self) -> 'DV4':
        """
        Generalized Tiefenrotation 2 (GTR2): Multiplication by j.
        
        GTR2([v, d1, d2, d3]) = [-d2, -d3, v, d1]
        """
        return DV4(-self.d2, -self.d3, self.v, self.d1)
    
    def GTR3(self) -> 'DV4':
        """
        Generalized Tiefenrotation 3 (GTR3): Multiplication by k.
        
        GTR3([v, d1, d2, d3]) = [-d3, d2, -d1, v]
        """
        return DV4(-self.d3, self.d2, -self.d1, self.v)
    
    def STO(self) -> 'DV4':
        """
        Singularity Treatment Operation (STO).
        
        For consistency across dimensions, STO is defined as the primary rotation.
        In DV4, this corresponds to GTR1 (multiplication by i).
        
        STO([v, d1, d2, d3]) = GTR1([v, d1, d2, d3]) = [-d1, v, d3, -d2]
        """
        return self.GTR1()
