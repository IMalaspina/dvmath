"""
DV8 Numba - JIT-Compiled High-Performance Implementation
=========================================================

This implementation uses Numba JIT compilation for maximum performance.

Author: Ivano Franco Malaspina
Date: December 2025
"""

import numpy as np
from numba import jit, float64
from numba.types import UniTuple


@jit(UniTuple(float64, 8)(UniTuple(float64, 8), UniTuple(float64, 8)), nopython=True, cache=True)
def _multiply_octonions(a, b):
    """
    JIT-compiled octonion multiplication using Cayley-Dickson construction.
    Validated formula from DV8_Optimized_V2.
    """
    # Extract components
    a0, a1, a2, a3, a4, a5, a6, a7 = a
    b0, b1, b2, b3, b4, b5, b6, b7 = b
    
    # ac (quaternion multiplication)
    ac0 = a0*b0 - a1*b1 - a2*b2 - a3*b3
    ac1 = a0*b1 + a1*b0 + a2*b3 - a3*b2
    ac2 = a0*b2 - a1*b3 + a2*b0 + a3*b1
    ac3 = a0*b3 + a1*b2 - a2*b1 + a3*b0
    
    # d*b (d conjugate times b)
    # d_conj = (b4, -b5, -b6, -b7)
    d_conj_b0 = b4*a4 - (-b5)*a5 - (-b6)*a6 - (-b7)*a7
    d_conj_b1 = b4*a5 + (-b5)*a4 + (-b6)*a7 - (-b7)*a6
    d_conj_b2 = b4*a6 - (-b5)*a7 + (-b6)*a4 + (-b7)*a5
    d_conj_b3 = b4*a7 + (-b5)*a6 - (-b6)*a5 + (-b7)*a4
    
    # First part: ac - d*b
    c0 = ac0 - d_conj_b0
    c1 = ac1 - d_conj_b1
    c2 = ac2 - d_conj_b2
    c3 = ac3 - d_conj_b3
    
    # da (quaternion multiplication)
    da0 = b4*a0 - b5*a1 - b6*a2 - b7*a3
    da1 = b4*a1 + b5*a0 + b6*a3 - b7*a2
    da2 = b4*a2 - b5*a3 + b6*a0 + b7*a1
    da3 = b4*a3 + b5*a2 - b6*a1 + b7*a0
    
    # bc* (b times c conjugate)
    # c_conj = (b0, -b1, -b2, -b3)
    bc_conj0 = a4*b0 - a5*(-b1) - a6*(-b2) - a7*(-b3)
    bc_conj1 = a4*(-b1) + a5*b0 + a6*(-b3) - a7*(-b2)
    bc_conj2 = a4*(-b2) - a5*(-b3) + a6*b0 + a7*(-b1)
    bc_conj3 = a4*(-b3) + a5*(-b2) - a6*(-b1) + a7*b0
    
    # Second part: da + bc*
    c4 = da0 + bc_conj0
    c5 = da1 + bc_conj1
    c6 = da2 + bc_conj2
    c7 = da3 + bc_conj3
    
    return (c0, c1, c2, c3, c4, c5, c6, c7)


@jit(float64(UniTuple(float64, 8)), nopython=True, cache=True)
def _norm(a):
    """JIT-compiled norm calculation."""
    return np.sqrt(a[0]**2 + a[1]**2 + a[2]**2 + a[3]**2 + 
                   a[4]**2 + a[5]**2 + a[6]**2 + a[7]**2)


@jit(UniTuple(float64, 8)(UniTuple(float64, 8)), nopython=True, cache=True)
def _conjugate(a):
    """JIT-compiled conjugate."""
    return (a[0], -a[1], -a[2], -a[3], -a[4], -a[5], -a[6], -a[7])


@jit(UniTuple(float64, 8)(UniTuple(float64, 8)), nopython=True, cache=True)
def _sto(a):
    """JIT-compiled STO operation."""
    return (-a[1], a[0], a[3], -a[2], -a[5], a[4], a[7], -a[6])


class DV8_Numba:
    """
    DV8 implementation using Numba JIT compilation.
    """
    
    __slots__ = ('_data',)
    
    def __init__(self, *args):
        """Initialize from 8 components or a tuple."""
        if len(args) == 1 and isinstance(args[0], tuple):
            self._data = args[0]
        elif len(args) == 8:
            self._data = tuple(float(x) for x in args)
        else:
            self._data = (0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0)
    
    @property
    def components(self):
        """Return components as tuple."""
        return self._data
    
    def __repr__(self) -> str:
        return f"DV8_Numba({', '.join(f'{c:.4f}' for c in self._data)})"
    
    def __str__(self) -> str:
        return f"[{', '.join(f'{c:.4f}' for c in self._data)}]"
    
    def __eq__(self, other) -> bool:
        if not isinstance(other, DV8_Numba):
            return False
        return all(abs(a - b) < 1e-9 for a, b in zip(self._data, other._data))
    
    def __add__(self, other):
        """Component-wise addition."""
        if isinstance(other, (int, float)):
            return DV8_Numba(tuple(self._data[0] + other if i == 0 else self._data[i] 
                                   for i in range(8)))
        return DV8_Numba(tuple(a + b for a, b in zip(self._data, other._data)))
    
    __radd__ = __add__
    
    def __sub__(self, other):
        """Component-wise subtraction."""
        if isinstance(other, (int, float)):
            return DV8_Numba(tuple(self._data[0] - other if i == 0 else self._data[i] 
                                   for i in range(8)))
        return DV8_Numba(tuple(a - b for a, b in zip(self._data, other._data)))
    
    def __mul__(self, other):
        """JIT-compiled multiplication."""
        if isinstance(other, (int, float)):
            return DV8_Numba(tuple(c * other for c in self._data))
        elif isinstance(other, DV8_Numba):
            result = _multiply_octonions(self._data, other._data)
            return DV8_Numba(result)
        else:
            raise TypeError(f"Cannot multiply DV8_Numba with {type(other)}")
    
    __rmul__ = __mul__
    
    def __truediv__(self, other):
        """Division."""
        if isinstance(other, (int, float)):
            if abs(other) < 1e-10:
                return self.STO()
            return DV8_Numba(tuple(c / other for c in self._data))
        elif isinstance(other, DV8_Numba):
            norm_sq = sum(c**2 for c in other._data)
            if norm_sq < 1e-10:
                return self.STO()
            return self * other.inverse()
        else:
            raise TypeError(f"Cannot divide DV8_Numba by {type(other)}")
    
    def __neg__(self):
        """Additive inverse."""
        return DV8_Numba(tuple(-c for c in self._data))
    
    def norm(self) -> float:
        """JIT-compiled norm."""
        return _norm(self._data)
    
    def is_zero(self) -> bool:
        """Check if zero (within tolerance)."""
        return self.norm() < 1e-10
    
    def conjugate(self):
        """JIT-compiled conjugate."""
        return DV8_Numba(_conjugate(self._data))
    
    def inverse(self):
        """Multiplicative inverse."""
        norm_sq = sum(c**2 for c in self._data)
        if norm_sq < 1e-10:
            raise ZeroDivisionError("Cannot invert zero-norm vector. Use STO instead.")
        conj = _conjugate(self._data)
        return DV8_Numba(tuple(c / norm_sq for c in conj))
    
    def STO(self):
        """JIT-compiled STO operation."""
        return DV8_Numba(_sto(self._data))


# Validation
if __name__ == "__main__":
    import sys
    sys.path.insert(0, '/home/ubuntu/dvmath/research/dv8')
    from dv8 import DV8
    
    print("=" * 70)
    print("VALIDATION: Numba vs Original")
    print("=" * 70)
    
    np.random.seed(42)
    n_tests = 1000
    max_error = 0.0
    
    # Warm up JIT
    print("\nWarming up JIT compiler...")
    a_warm = DV8_Numba(1, 2, 3, 4, 5, 6, 7, 8)
    b_warm = DV8_Numba(8, 7, 6, 5, 4, 3, 2, 1)
    _ = a_warm * b_warm
    print("JIT compilation complete.")
    
    print(f"\nRunning {n_tests} validation tests...")
    for _ in range(n_tests):
        components_a = np.random.randn(8)
        components_b = np.random.randn(8)
        
        a_orig = DV8(*components_a)
        a_numba = DV8_Numba(*components_a)
        
        b_orig = DV8(*components_b)
        b_numba = DV8_Numba(*components_b)
        
        result_orig = a_orig * b_orig
        result_numba = a_numba * b_numba
        
        error = max(abs(o - n) for o, n in zip(result_orig.components, result_numba.components))
        max_error = max(max_error, error)
    
    print(f"\nTests run: {n_tests}")
    print(f"Max error: {max_error:.2e}")
    
    if max_error < 1e-12:
        print("\n✓ VALIDATION PASSED: Results are identical!")
    else:
        print("\n✗ VALIDATION FAILED: Results differ!")
