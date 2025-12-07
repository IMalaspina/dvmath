"""
DV8 Optimized V2 - Simplified approach
=======================================

Instead of manually expanding Cayley-Dickson, we inline the Quaternion
class operations to avoid object creation overhead.

Author: Ivano Franco Malaspina
Date: December 2025
"""

import math


class DV8_Optimized_V2:
    """
    Optimized DV8 with inlined quaternion operations.
    """
    
    __slots__ = ('components',)
    
    def __init__(self, v=0.0, d1=0.0, d2=0.0, d3=0.0, d4=0.0, d5=0.0, d6=0.0, d7=0.0):
        self.components = (float(v), float(d1), float(d2), float(d3),
                          float(d4), float(d5), float(d6), float(d7))
    
    def __repr__(self) -> str:
        return f"DV8_Opt({', '.join(f'{c:.4f}' for c in self.components)})"
    
    def __str__(self) -> str:
        return f"[{', '.join(f'{c:.4f}' for c in self.components)}]"
    
    def __eq__(self, other) -> bool:
        if not isinstance(other, DV8_Optimized_V2):
            return False
        return all(abs(a - b) < 1e-9 for a, b in zip(self.components, other.components))
    
    def __add__(self, other):
        if isinstance(other, (int, float)):
            return DV8_Optimized_V2(self.components[0] + other, *self.components[1:])
        return DV8_Optimized_V2(*(a + b for a, b in zip(self.components, other.components)))
    
    __radd__ = __add__
    
    def __sub__(self, other):
        if isinstance(other, (int, float)):
            return DV8_Optimized_V2(self.components[0] - other, *self.components[1:])
        return DV8_Optimized_V2(*(a - b for a, b in zip(self.components, other.components)))
    
    def __mul__(self, other):
        """
        Optimized multiplication using inlined quaternion operations.
        
        Cayley-Dickson: (a, b) * (c, d) = (ac - d*b, da + bc*)
        where a, b, c, d are quaternions represented as tuples.
        """
        if isinstance(other, (int, float)):
            return DV8_Optimized_V2(*(c * other for c in self.components))
        elif isinstance(other, DV8_Optimized_V2):
            # Split into quaternions (as tuples, no object creation)
            a = self.components[0:4]   # (a0, a1, a2, a3)
            b = self.components[4:8]   # (a4, a5, a6, a7)
            c = other.components[0:4]  # (b0, b1, b2, b3)
            d = other.components[4:8]  # (b4, b5, b6, b7)
            
            # Inline quaternion multiplication: ac
            ac = (
                a[0]*c[0] - a[1]*c[1] - a[2]*c[2] - a[3]*c[3],
                a[0]*c[1] + a[1]*c[0] + a[2]*c[3] - a[3]*c[2],
                a[0]*c[2] - a[1]*c[3] + a[2]*c[0] + a[3]*c[1],
                a[0]*c[3] + a[1]*c[2] - a[2]*c[1] + a[3]*c[0]
            )
            
            # Inline quaternion conjugate: d*
            d_conj = (d[0], -d[1], -d[2], -d[3])
            
            # Inline quaternion multiplication: d*b
            d_conj_b = (
                d_conj[0]*b[0] - d_conj[1]*b[1] - d_conj[2]*b[2] - d_conj[3]*b[3],
                d_conj[0]*b[1] + d_conj[1]*b[0] + d_conj[2]*b[3] - d_conj[3]*b[2],
                d_conj[0]*b[2] - d_conj[1]*b[3] + d_conj[2]*b[0] + d_conj[3]*b[1],
                d_conj[0]*b[3] + d_conj[1]*b[2] - d_conj[2]*b[1] + d_conj[3]*b[0]
            )
            
            # First part: ac - d*b
            first_part = tuple(ac[i] - d_conj_b[i] for i in range(4))
            
            # Inline quaternion multiplication: da
            da = (
                d[0]*a[0] - d[1]*a[1] - d[2]*a[2] - d[3]*a[3],
                d[0]*a[1] + d[1]*a[0] + d[2]*a[3] - d[3]*a[2],
                d[0]*a[2] - d[1]*a[3] + d[2]*a[0] + d[3]*a[1],
                d[0]*a[3] + d[1]*a[2] - d[2]*a[1] + d[3]*a[0]
            )
            
            # Inline quaternion conjugate: c*
            c_conj = (c[0], -c[1], -c[2], -c[3])
            
            # Inline quaternion multiplication: bc*
            bc_conj = (
                b[0]*c_conj[0] - b[1]*c_conj[1] - b[2]*c_conj[2] - b[3]*c_conj[3],
                b[0]*c_conj[1] + b[1]*c_conj[0] + b[2]*c_conj[3] - b[3]*c_conj[2],
                b[0]*c_conj[2] - b[1]*c_conj[3] + b[2]*c_conj[0] + b[3]*c_conj[1],
                b[0]*c_conj[3] + b[1]*c_conj[2] - b[2]*c_conj[1] + b[3]*c_conj[0]
            )
            
            # Second part: da + bc*
            second_part = tuple(da[i] + bc_conj[i] for i in range(4))
            
            return DV8_Optimized_V2(*first_part, *second_part)
        else:
            raise TypeError(f"Cannot multiply DV8_Optimized_V2 with {type(other)}")
    
    __rmul__ = __mul__
    
    def __truediv__(self, other):
        if isinstance(other, (int, float)):
            if abs(other) < 1e-10:
                return self.STO()
            return DV8_Optimized_V2(*(c / other for c in self.components))
        elif isinstance(other, DV8_Optimized_V2):
            norm_sq = sum(c**2 for c in other.components)
            if norm_sq < 1e-10:
                return self.STO()
            return self * other.inverse()
        else:
            raise TypeError(f"Cannot divide DV8_Optimized_V2 by {type(other)}")
    
    def __neg__(self):
        return DV8_Optimized_V2(*(-c for c in self.components))
    
    def norm(self) -> float:
        return math.sqrt(sum(c**2 for c in self.components))
    
    def is_zero(self) -> bool:
        return self.norm() < 1e-10
    
    def conjugate(self):
        return DV8_Optimized_V2(self.components[0], *(-c for c in self.components[1:]))
    
    def inverse(self):
        norm_sq = sum(c**2 for c in self.components)
        if norm_sq < 1e-10:
            raise ZeroDivisionError("Cannot invert zero-norm vector. Use STO instead.")
        conj = self.conjugate()
        return DV8_Optimized_V2(*(c / norm_sq for c in conj.components))
    
    def STO(self):
        # Optimized: e1 * self without creating e1 object
        a0, a1, a2, a3, a4, a5, a6, a7 = self.components
        return DV8_Optimized_V2(-a1, a0, a3, -a2, -a5, a4, a7, -a6)


# Validation
if __name__ == "__main__":
    import sys
    sys.path.insert(0, '/home/ubuntu/dvmath/research/dv8')
    from dv8 import DV8
    import numpy as np
    
    print("=" * 70)
    print("VALIDATION: Optimized V2 vs Original")
    print("=" * 70)
    
    np.random.seed(42)
    n_tests = 1000
    max_error = 0.0
    
    for _ in range(n_tests):
        components_a = np.random.randn(8)
        components_b = np.random.randn(8)
        
        a_orig = DV8(*components_a)
        a_opt = DV8_Optimized_V2(*components_a)
        
        b_orig = DV8(*components_b)
        b_opt = DV8_Optimized_V2(*components_b)
        
        result_orig = a_orig * b_orig
        result_opt = a_opt * b_opt
        
        error = max(abs(o - p) for o, p in zip(result_orig.components, result_opt.components))
        max_error = max(max_error, error)
    
    print(f"\nTests run: {n_tests}")
    print(f"Max error: {max_error:.2e}")
    
    if max_error < 1e-12:
        print("\n✓ VALIDATION PASSED: Results are identical!")
    else:
        print("\n✗ VALIDATION FAILED: Results differ!")
        print("\nDebug single case:")
        a_orig = DV8(1, 2, 3, 4, 5, 6, 7, 8)
        a_opt = DV8_Optimized_V2(1, 2, 3, 4, 5, 6, 7, 8)
        b_orig = DV8(8, 7, 6, 5, 4, 3, 2, 1)
        b_opt = DV8_Optimized_V2(8, 7, 6, 5, 4, 3, 2, 1)
        result_orig = a_orig * b_orig
        result_opt = a_opt * b_opt
        print(f"Original: {result_orig}")
        print(f"Optimized: {result_opt}")
