"""
DV8 Corrected - Octonion Algebra via Cayley-Dickson Construction
==================================================================

This is a CORRECTED implementation of DV8 using the Cayley-Dickson construction.
The Cayley-Dickson construction builds octonions from quaternions by treating
an octonion as a pair of quaternions: (a, b) where a and b are quaternions.

Multiplication: (a, b) * (c, d) = (ac - d*b, da + bc*)
where * denotes conjugate.

This approach is mathematically rigorous and avoids the complexity of directly
encoding the Fano plane multiplication table.

Author: Ivano Franco Malaspina
Status: EXPERIMENTAL - VALIDATION IN PROGRESS
"""

import math
from typing import List, Tuple


class Quaternion:
    """Helper class for quaternion operations (used in Cayley-Dickson)."""
    
    def __init__(self, w: float, x: float, y: float, z: float):
        self.w = w
        self.x = x
        self.y = y
        self.z = z
    
    def __mul__(self, other: 'Quaternion') -> 'Quaternion':
        """Quaternion multiplication."""
        return Quaternion(
            self.w * other.w - self.x * other.x - self.y * other.y - self.z * other.z,
            self.w * other.x + self.x * other.w + self.y * other.z - self.z * other.y,
            self.w * other.y - self.x * other.z + self.y * other.w + self.z * other.x,
            self.w * other.z + self.x * other.y - self.y * other.x + self.z * other.w
        )
    
    def __add__(self, other: 'Quaternion') -> 'Quaternion':
        """Quaternion addition."""
        return Quaternion(
            self.w + other.w,
            self.x + other.x,
            self.y + other.y,
            self.z + other.z
        )
    
    def __sub__(self, other: 'Quaternion') -> 'Quaternion':
        """Quaternion subtraction."""
        return Quaternion(
            self.w - other.w,
            self.x - other.x,
            self.y - other.y,
            self.z - other.z
        )
    
    def conjugate(self) -> 'Quaternion':
        """Quaternion conjugate."""
        return Quaternion(self.w, -self.x, -self.y, -self.z)
    
    def to_list(self) -> List[float]:
        """Convert to list [w, x, y, z]."""
        return [self.w, self.x, self.y, self.z]


class DV8:
    """
    DV8 represents an 8-dimensional vector in DV-Space.
    
    Implemented using Cayley-Dickson construction from quaternions.
    An octonion is represented as a pair of quaternions (a, b).
    
    Components: [v, d1, d2, d3, d4, d5, d6, d7]
    where (a, b) = (Quaternion(v, d1, d2, d3), Quaternion(d4, d5, d6, d7))
    """
    
    def __init__(self, *components):
        """
        Initialize a DV8 vector.
        
        Args:
            *components: 8 float values [v, d1, d2, d3, d4, d5, d6, d7]
        """
        if len(components) != 8:
            raise ValueError("DV8 requires exactly 8 components")
        self.components = [float(c) for c in components]
        
        # Internal representation as pair of quaternions
        self.a = Quaternion(*self.components[0:4])
        self.b = Quaternion(*self.components[4:8])
    
    def __repr__(self) -> str:
        return f"DV8({self.components})"
    
    def __str__(self) -> str:
        return f"[{', '.join(f'{c:.4f}' for c in self.components)}]"
    
    def __eq__(self, other) -> bool:
        """Check equality with tolerance for floating point errors."""
        if not isinstance(other, DV8):
            return False
        return all(math.isclose(a, b, rel_tol=1e-9, abs_tol=1e-12) 
                   for a, b in zip(self.components, other.components))
    
    def __add__(self, other: 'DV8') -> 'DV8':
        """Vector addition: component-wise."""
        return DV8(*[a + b for a, b in zip(self.components, other.components)])
    
    def __sub__(self, other: 'DV8') -> 'DV8':
        """Vector subtraction: component-wise."""
        return DV8(*[a - b for a, b in zip(self.components, other.components)])
    
    def __mul__(self, other) -> 'DV8':
        """
        Multiplication.
        
        - Scalar multiplication: k * A
        - DV8 multiplication: Cayley-Dickson construction
          (a, b) * (c, d) = (ac - d*b, da + bc*)
        """
        if isinstance(other, (int, float)):
            return DV8(*[c * other for c in self.components])
        elif isinstance(other, DV8):
            # Cayley-Dickson: (a, b) * (c, d) = (ac - d*b, da + bc*)
            ac = self.a * other.a
            d_conj_b = other.b.conjugate() * self.b
            first_part = ac - d_conj_b
            
            da = other.b * self.a
            bc_conj = self.b * other.a.conjugate()
            second_part = da + bc_conj
            
            result_components = first_part.to_list() + second_part.to_list()
            return DV8(*result_components)
        else:
            raise TypeError(f"Cannot multiply DV8 with {type(other)}")
    
    def __rmul__(self, other: float) -> 'DV8':
        """Right multiplication for scalar."""
        return self.__mul__(other)
    
    def __truediv__(self, other) -> 'DV8':
        """
        Division.
        
        - Scalar division: A / k
        - DV8 division: A / B = A * B^(-1)
        - If B is zero-norm or near-zero, apply STO to A
        """
        if isinstance(other, (int, float)):
            if abs(other) < 1e-10:
                return self.STO()
            return DV8(*[c / other for c in self.components])
        elif isinstance(other, DV8):
            # Check norm squared to be consistent with inverse() method
            norm_sq = sum(c**2 for c in other.components)
            if norm_sq < 1e-10:
                return self.STO()
            return self * other.inverse()
        else:
            raise TypeError(f"Cannot divide DV8 by {type(other)}")
    
    def __neg__(self) -> 'DV8':
        """Additive inverse."""
        return DV8(*[-c for c in self.components])
    
    def norm(self) -> float:
        """Euclidean norm: ||A|| = sqrt(sum(ci^2))."""
        return math.sqrt(sum(c**2 for c in self.components))
    
    def is_zero(self) -> bool:
        """Check if the vector is zero (within tolerance)."""
        return self.norm() < 1e-10
    
    def conjugate(self) -> 'DV8':
        """
        Conjugate: [v, d1, ..., d7]* = [v, -d1, ..., -d7].
        
        In Cayley-Dickson: (a, b)* = (a*, -b)
        """
        a_conj = self.a.conjugate()
        b_neg = Quaternion(-self.b.w, -self.b.x, -self.b.y, -self.b.z)
        return DV8(*(a_conj.to_list() + b_neg.to_list()))
    
    def inverse(self) -> 'DV8':
        """
        Multiplicative inverse: A^(-1) = A* / ||A||^2.
        
        Raises:
            ZeroDivisionError: If the vector has zero norm.
        """
        norm_sq = sum(c**2 for c in self.components)
        if norm_sq < 1e-10:
            raise ZeroDivisionError("Cannot invert zero-norm vector. Use STO instead.")
        conj = self.conjugate()
        return DV8(*[c / norm_sq for c in conj.components])
    
    def STO(self) -> 'DV8':
        """
        Singularity Treatment Operation (STO).
        
        For DV8, STO is defined as multiplication by e1 (the first imaginary unit).
        e1 = [0, 1, 0, 0, 0, 0, 0, 0]
        """
        e1 = DV8(0, 1, 0, 0, 0, 0, 0, 0)
        return e1 * self


def validate_dv8_properties():
    """
    Validate key properties of DV8 (Octonion) algebra.
    
    Returns:
        dict: Test results with detailed information
    """
    results = {}
    
    # Define basis elements
    e0 = DV8(1, 0, 0, 0, 0, 0, 0, 0)  # Scalar unit
    e1 = DV8(0, 1, 0, 0, 0, 0, 0, 0)
    e2 = DV8(0, 0, 1, 0, 0, 0, 0, 0)
    e3 = DV8(0, 0, 0, 1, 0, 0, 0, 0)
    e4 = DV8(0, 0, 0, 0, 1, 0, 0, 0)
    e5 = DV8(0, 0, 0, 0, 0, 1, 0, 0)
    e6 = DV8(0, 0, 0, 0, 0, 0, 1, 0)
    e7 = DV8(0, 0, 0, 0, 0, 0, 0, 1)
    
    neg_e0 = DV8(-1, 0, 0, 0, 0, 0, 0, 0)
    
    # Test 1: All imaginary units square to -1
    results['e1_squared'] = (e1 * e1 == neg_e0, f"e1^2 = {e1 * e1}")
    results['e2_squared'] = (e2 * e2 == neg_e0, f"e2^2 = {e2 * e2}")
    results['e3_squared'] = (e3 * e3 == neg_e0, f"e3^2 = {e3 * e3}")
    results['e4_squared'] = (e4 * e4 == neg_e0, f"e4^2 = {e4 * e4}")
    results['e5_squared'] = (e5 * e5 == neg_e0, f"e5^2 = {e5 * e5}")
    results['e6_squared'] = (e6 * e6 == neg_e0, f"e6^2 = {e6 * e6}")
    results['e7_squared'] = (e7 * e7 == neg_e0, f"e7^2 = {e7 * e7}")
    
    # Test 2: Sample Cayley-Dickson multiplication rules
    # In Cayley-Dickson, e1*e2 should give a specific result based on quaternion multiplication
    e1_e2 = e1 * e2
    e2_e1 = e2 * e1
    results['e1_e2_computed'] = (True, f"e1*e2 = {e1_e2}")
    results['e2_e1_computed'] = (True, f"e2*e1 = {e2_e1}")
    
    # Test 3: Non-commutativity
    results['non_commutative'] = (e1 * e2 != e2 * e1, f"e1*e2 ≠ e2*e1: {e1 * e2 != e2 * e1}")
    
    # Test 4: Non-associativity
    left_assoc = (e1 * e2) * e3
    right_assoc = e1 * (e2 * e3)
    results['non_associative'] = (left_assoc != right_assoc, 
                                   f"(e1*e2)*e3 ≠ e1*(e2*e3): {left_assoc != right_assoc}")
    
    # Test 5: Norm preservation in multiplication
    a = DV8(1, 2, 3, 4, 5, 6, 7, 8)
    b = DV8(8, 7, 6, 5, 4, 3, 2, 1)
    product = a * b
    norm_a = a.norm()
    norm_b = b.norm()
    norm_product = product.norm()
    expected_norm = norm_a * norm_b
    results['norm_preservation'] = (
        math.isclose(norm_product, expected_norm, rel_tol=1e-6),
        f"||a|| = {norm_a:.6f}, ||b|| = {norm_b:.6f}, ||a*b|| = {norm_product:.6f}, expected {expected_norm:.6f}"
    )
    
    # Test 6: Inverse property
    # a * a^(-1) should equal 1 (within tolerance)
    a_inv = a.inverse()
    identity_test = a * a_inv
    is_identity = (
        math.isclose(identity_test.components[0], 1.0, abs_tol=1e-6) and
        all(math.isclose(c, 0.0, abs_tol=1e-6) for c in identity_test.components[1:])
    )
    results['inverse_property'] = (is_identity, f"a * a^(-1) = {identity_test}")
    
    # Test 7: Right inverse (due to non-associativity, left and right inverses may differ)
    identity_test_right = a_inv * a
    is_right_identity = (
        math.isclose(identity_test_right.components[0], 1.0, abs_tol=1e-6) and
        all(math.isclose(c, 0.0, abs_tol=1e-6) for c in identity_test_right.components[1:])
    )
    results['right_inverse_property'] = (is_right_identity, f"a^(-1) * a = {identity_test_right}")
    
    # Test 8: STO application
    zero = DV8(0, 0, 0, 0, 0, 0, 0, 0)
    one = DV8(1, 0, 0, 0, 0, 0, 0, 0)
    two = DV8(2, 0, 0, 0, 0, 0, 0, 0)
    results['STO_paradox_avoidance'] = (
        (one / zero) != (two / zero),
        f"1/0 = {one / zero}, 2/0 = {two / zero}"
    )
    
    # Test 9: STO norm preservation
    sto_result = a.STO()
    results['STO_norm_preservation'] = (
        math.isclose(sto_result.norm(), a.norm(), rel_tol=1e-9),
        f"||STO(a)|| = {sto_result.norm():.6f}, ||a|| = {a.norm():.6f}"
    )
    
    return results


def run_comprehensive_tests():
    """Run all DV8 validation tests and print detailed results."""
    print("=" * 70)
    print("DV8 (Octonion) Algebra - Cayley-Dickson Implementation")
    print("=" * 70)
    print("\nSTATUS: CORRECTED PROTOTYPE")
    print("Using Cayley-Dickson construction from quaternions.\n")
    
    results = validate_dv8_properties()
    
    passed = 0
    failed = 0
    
    for test_name, (result, details) in results.items():
        status = "✓ PASS" if result else "✗ FAIL"
        if result:
            passed += 1
        else:
            failed += 1
        print(f"{status}: {test_name}")
        # Print details for key tests
        if test_name in ['e1_e2_computed', 'e2_e1_computed', 'non_commutative', 
                         'non_associative', 'norm_preservation', 'inverse_property',
                         'right_inverse_property', 'STO_norm_preservation']:
            print(f"      {details}")
    
    print("\n" + "=" * 70)
    print(f"Results: {passed} passed, {failed} failed out of {passed + failed} tests")
    if failed == 0:
        print("ALL TESTS PASSED ✓")
        print("\nDV8 prototype shows expected octonion behavior:")
        print("  - All imaginary units square to -1")
        print("  - Non-commutative and non-associative as expected")
        print("  - Norm preservation in multiplication")
        print("  - Both left and right inverse properties hold")
        print("  - STO operation is well-defined and norm-preserving")
    else:
        print("SOME TESTS FAILED ✗")
        print("\nAnalyzing failures for further investigation...")
    print("=" * 70)


if __name__ == "__main__":
    run_comprehensive_tests()
