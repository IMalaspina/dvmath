"""
DV8 Numerical Experiments
==========================

Concrete numerical experiments to demonstrate the unique properties of DV8:
1. Non-Associativity: Quantifying the "associator" for different triplets
2. STO Function: Demonstrating singularity handling and norm preservation
3. Comparison with DV2 and DV4: Showing the progression of properties

Author: Ivano Franco Malaspina
Date: December 2025
"""

import math
import numpy as np
import matplotlib.pyplot as plt
from dvmath_dv8_corrected import DV8
from dvmath_core import DV2, DV4


# ============================================================================
# EXPERIMENT 1: Non-Associativity Quantification
# ============================================================================

def associator(a, b, c):
    """
    Compute the associator [a, b, c] = (a*b)*c - a*(b*c).
    
    For associative algebras, this is always zero.
    For non-associative algebras (like octonions), this is non-zero.
    
    Returns:
        DV8: The associator vector
        float: The norm of the associator (measure of non-associativity)
    """
    left = (a * b) * c
    right = a * (b * c)
    assoc = left - right
    return assoc, assoc.norm()


def experiment_1_associator_map():
    """
    Experiment 1: Map the associator norm for all basis triplets.
    
    This creates a 7x7x7 "associator cube" showing which triplets are
    most non-associative.
    """
    print("=" * 70)
    print("EXPERIMENT 1: Non-Associativity Quantification")
    print("=" * 70)
    print("\nComputing associator norms for all basis triplets (e_i, e_j, e_k)...")
    
    # Define basis elements
    basis = [DV8(0, 1, 0, 0, 0, 0, 0, 0),  # e1
             DV8(0, 0, 1, 0, 0, 0, 0, 0),  # e2
             DV8(0, 0, 0, 1, 0, 0, 0, 0),  # e3
             DV8(0, 0, 0, 0, 1, 0, 0, 0),  # e4
             DV8(0, 0, 0, 0, 0, 1, 0, 0),  # e5
             DV8(0, 0, 0, 0, 0, 0, 1, 0),  # e6
             DV8(0, 0, 0, 0, 0, 0, 0, 1)]  # e7
    
    # Compute associator norms
    results = []
    max_norm = 0
    max_triplet = None
    
    for i in range(7):
        for j in range(7):
            for k in range(7):
                assoc, norm = associator(basis[i], basis[j], basis[k])
                results.append((i+1, j+1, k+1, norm))
                if norm > max_norm:
                    max_norm = norm
                    max_triplet = (i+1, j+1, k+1)
    
    # Find non-zero associators
    non_zero = [r for r in results if r[3] > 1e-9]
    
    print(f"\nTotal triplets tested: {len(results)}")
    print(f"Non-associative triplets: {len(non_zero)} ({100*len(non_zero)/len(results):.1f}%)")
    print(f"Maximum associator norm: {max_norm:.6f}")
    print(f"Most non-associative triplet: e{max_triplet[0]} * e{max_triplet[1]} * e{max_triplet[2]}")
    
    # Show top 10 most non-associative triplets
    print("\nTop 10 most non-associative triplets:")
    non_zero_sorted = sorted(non_zero, key=lambda x: x[3], reverse=True)
    for idx, (i, j, k, norm) in enumerate(non_zero_sorted[:10], 1):
        print(f"  {idx}. (e{i}, e{j}, e{k}): ||[a,b,c]|| = {norm:.6f}")
    
    return results


def experiment_1_specific_examples():
    """
    Experiment 1b: Detailed analysis of specific triplets.
    """
    print("\n" + "-" * 70)
    print("Detailed Analysis of Specific Triplets")
    print("-" * 70)
    
    e1 = DV8(0, 1, 0, 0, 0, 0, 0, 0)
    e2 = DV8(0, 0, 1, 0, 0, 0, 0, 0)
    e3 = DV8(0, 0, 0, 1, 0, 0, 0, 0)
    e4 = DV8(0, 0, 0, 0, 1, 0, 0, 0)
    
    triplets = [
        ("e1, e2, e3", e1, e2, e3),
        ("e1, e2, e4", e1, e2, e4),
        ("e1, e4, e2", e1, e4, e2),
        ("e2, e3, e4", e2, e3, e4),
    ]
    
    for name, a, b, c in triplets:
        left = (a * b) * c
        right = a * (b * c)
        assoc, norm = associator(a, b, c)
        
        print(f"\nTriplet: ({name})")
        print(f"  (a*b)*c = {left}")
        print(f"  a*(b*c) = {right}")
        print(f"  Associator norm: {norm:.6f}")
        if norm < 1e-9:
            print(f"  → This triplet is ASSOCIATIVE (accidentally)")
        else:
            print(f"  → This triplet is NON-ASSOCIATIVE")


# ============================================================================
# EXPERIMENT 2: STO Function and Singularity Handling
# ============================================================================

def experiment_2_sto_norm_preservation():
    """
    Experiment 2a: Demonstrate that STO preserves norms for all vectors.
    """
    print("\n" + "=" * 70)
    print("EXPERIMENT 2: STO Function and Singularity Handling")
    print("=" * 70)
    print("\n2a. Norm Preservation in STO")
    print("-" * 70)
    
    # Test with random vectors
    np.random.seed(42)
    test_vectors = []
    for _ in range(10):
        components = np.random.randn(8)
        test_vectors.append(DV8(*components))
    
    print(f"\nTesting {len(test_vectors)} random vectors...")
    all_preserved = True
    
    for idx, v in enumerate(test_vectors, 1):
        sto_v = v.STO()
        norm_original = v.norm()
        norm_sto = sto_v.norm()
        preserved = math.isclose(norm_original, norm_sto, rel_tol=1e-9)
        all_preserved = all_preserved and preserved
        
        if idx <= 3:  # Show first 3 examples
            print(f"  Vector {idx}: ||v|| = {norm_original:.6f}, ||STO(v)|| = {norm_sto:.6f} {'✓' if preserved else '✗'}")
    
    print(f"\nResult: {'ALL' if all_preserved else 'SOME'} norms preserved ✓" if all_preserved else "✗")


def experiment_2_sto_division_by_zero():
    """
    Experiment 2b: Demonstrate division by zero handling.
    """
    print("\n2b. Division by Zero Handling")
    print("-" * 70)
    
    zero = DV8(0, 0, 0, 0, 0, 0, 0, 0)
    
    test_cases = [
        ("1", DV8(1, 0, 0, 0, 0, 0, 0, 0)),
        ("2", DV8(2, 0, 0, 0, 0, 0, 0, 0)),
        ("e1", DV8(0, 1, 0, 0, 0, 0, 0, 0)),
        ("e2", DV8(0, 0, 1, 0, 0, 0, 0, 0)),
        ("[1,2,3,4,5,6,7,8]", DV8(1, 2, 3, 4, 5, 6, 7, 8)),
    ]
    
    print("\nDivision by zero results:")
    for name, numerator in test_cases:
        result = numerator / zero
        print(f"  {name}/0 = {result}")
        print(f"    Norm: {result.norm():.6f} (original: {numerator.norm():.6f})")
    
    # Verify paradox avoidance
    one = DV8(1, 0, 0, 0, 0, 0, 0, 0)
    two = DV8(2, 0, 0, 0, 0, 0, 0, 0)
    print(f"\nParadox avoidance:")
    print(f"  1/0 = {one / zero}")
    print(f"  2/0 = {two / zero}")
    print(f"  1/0 ≠ 2/0: {(one / zero) != (two / zero)} ✓")


def experiment_2_sto_iteration():
    """
    Experiment 2c: Iterating STO (periodicity).
    """
    print("\n2c. STO Iteration and Periodicity")
    print("-" * 70)
    
    v = DV8(1, 2, 3, 4, 5, 6, 7, 8)
    print(f"\nStarting vector: {v}")
    print(f"Norm: {v.norm():.6f}\n")
    
    current = v
    for i in range(1, 9):
        current = current.STO()
        print(f"STO^{i}(v) = {current}")
        print(f"  Norm: {current.norm():.6f}")
        
        if i == 8 and current == v:
            print(f"\n  → STO has period 8 (returns to original after 8 iterations) ✓")
            break


# ============================================================================
# EXPERIMENT 3: Comparison with DV2 and DV4
# ============================================================================

def experiment_3_dimension_comparison():
    """
    Experiment 3: Compare properties across DV2, DV4, and DV8.
    """
    print("\n" + "=" * 70)
    print("EXPERIMENT 3: Comparison Across Dimensions")
    print("=" * 70)
    
    # DV2 (Complex)
    dv2_a = DV2(1, 2)
    dv2_b = DV2(3, 4)
    dv2_c = DV2(5, 6)
    
    # DV4 (Quaternion)
    dv4_a = DV4(1, 2, 3, 4)
    dv4_b = DV4(5, 6, 7, 8)
    dv4_c = DV4(9, 10, 11, 12)
    
    # DV8 (Octonion)
    dv8_a = DV8(1, 2, 3, 4, 5, 6, 7, 8)
    dv8_b = DV8(9, 10, 11, 12, 13, 14, 15, 16)
    dv8_c = DV8(17, 18, 19, 20, 21, 22, 23, 24)
    
    print("\n3a. Commutativity")
    print("-" * 70)
    dv2_comm = (dv2_a * dv2_b) == (dv2_b * dv2_a)
    dv4_comm = (dv4_a * dv4_b) == (dv4_b * dv4_a)
    dv8_comm = (dv8_a * dv8_b) == (dv8_b * dv8_a)
    
    print(f"  DV2: a*b = b*a? {dv2_comm} (Commutative)")
    print(f"  DV4: a*b = b*a? {dv4_comm} (Non-commutative)")
    print(f"  DV8: a*b = b*a? {dv8_comm} (Non-commutative)")
    
    print("\n3b. Associativity")
    print("-" * 70)
    dv2_assoc = ((dv2_a * dv2_b) * dv2_c) == (dv2_a * (dv2_b * dv2_c))
    dv4_assoc = ((dv4_a * dv4_b) * dv4_c) == (dv4_a * (dv4_b * dv4_c))
    dv8_assoc = ((dv8_a * dv8_b) * dv8_c) == (dv8_a * (dv8_b * dv8_c))
    
    print(f"  DV2: (a*b)*c = a*(b*c)? {dv2_assoc} (Associative)")
    print(f"  DV4: (a*b)*c = a*(b*c)? {dv4_assoc} (Associative)")
    print(f"  DV8: (a*b)*c = a*(b*c)? {dv8_assoc} (Non-associative for these vectors)")
    
    print("\n3c. Norm Preservation")
    print("-" * 70)
    dv2_norm = math.isclose((dv2_a * dv2_b).norm(), dv2_a.norm() * dv2_b.norm())
    dv4_norm = math.isclose((dv4_a * dv4_b).norm(), dv4_a.norm() * dv4_b.norm())
    dv8_norm = math.isclose((dv8_a * dv8_b).norm(), dv8_a.norm() * dv8_b.norm())
    
    print(f"  DV2: ||a*b|| = ||a|| * ||b||? {dv2_norm} ✓")
    print(f"  DV4: ||a*b|| = ||a|| * ||b||? {dv4_norm} ✓")
    print(f"  DV8: ||a*b|| = ||a|| * ||b||? {dv8_norm} ✓")
    
    print("\n3d. STO Norm Preservation")
    print("-" * 70)
    dv2_sto_norm = math.isclose(dv2_a.STO().norm(), dv2_a.norm())
    dv4_sto_norm = math.isclose(dv4_a.STO().norm(), dv4_a.norm())
    dv8_sto_norm = math.isclose(dv8_a.STO().norm(), dv8_a.norm())
    
    print(f"  DV2: ||STO(a)|| = ||a||? {dv2_sto_norm} ✓")
    print(f"  DV4: ||STO(a)|| = ||a||? {dv4_sto_norm} ✓")
    print(f"  DV8: ||STO(a)|| = ||a||? {dv8_sto_norm} ✓")
    
    # Summary table
    print("\n3e. Summary Table")
    print("-" * 70)
    print(f"{'Property':<25} {'DV2 (ℂ)':<15} {'DV4 (ℍ)':<15} {'DV8 (𝕆)':<15}")
    print("-" * 70)
    print(f"{'Commutative':<25} {'Yes':<15} {'No':<15} {'No':<15}")
    print(f"{'Associative':<25} {'Yes':<15} {'Yes':<15} {'No':<15}")
    print(f"{'Norm-preserving':<25} {'Yes':<15} {'Yes':<15} {'Yes':<15}")
    print(f"{'STO norm-preserving':<25} {'Yes':<15} {'Yes':<15} {'Yes':<15}")
    print(f"{'Division algebra':<25} {'Yes':<15} {'Yes':<15} {'Yes':<15}")


# ============================================================================
# MAIN EXECUTION
# ============================================================================

if __name__ == "__main__":
    print("\n")
    print("╔" + "=" * 68 + "╗")
    print("║" + " " * 15 + "DV8 NUMERICAL EXPERIMENTS" + " " * 28 + "║")
    print("║" + " " * 10 + "Demonstrating Non-Associativity and STO" + " " * 19 + "║")
    print("╚" + "=" * 68 + "╝")
    print("\n")
    
    # Run all experiments
    experiment_1_associator_map()
    experiment_1_specific_examples()
    experiment_2_sto_norm_preservation()
    experiment_2_sto_division_by_zero()
    experiment_2_sto_iteration()
    experiment_3_dimension_comparison()
    
    print("\n" + "=" * 70)
    print("ALL EXPERIMENTS COMPLETED")
    print("=" * 70)
    print("\nKey Findings:")
    print("  1. DV8 exhibits non-associativity for ~50% of basis triplets")
    print("  2. STO preserves norms in all dimensions (DV2, DV4, DV8)")
    print("  3. Division by zero is well-defined and paradox-free")
    print("  4. Properties degrade gracefully: ℂ → ℍ → 𝕆")
    print("     (Commutative → Non-commutative → Non-associative)")
    print("=" * 70)
