# Getting Started with DV-Mathematics

**Welcome to the DV-Mathematics framework!** This guide will walk you through the installation, basic concepts, and practical usage of the `dvmath` library.

---

## 1. Installation

### Prerequisites
- Python 3.8+
- `git`
- `pip`

### Recommended Installation

For the best performance, we recommend installing the library directly from GitHub and including the `numba` dependency for JIT-optimized DV⁸ operations.

```bash
# 1. Clone the repository
git clone https://github.com/IMalaspina/dvmath.git
cd dvmath

# 2. Install dependencies (including Numba for DV⁸ performance)
pip install -r requirements.txt

# 3. Install the package in editable mode
pip install -e .
```

This setup ensures you have the latest validated code and the fastest possible implementation for octonion (DV⁸) calculations.

---

## 2. Core Concepts

### DV-Vectors

A DV-Vector is the fundamental data structure. It's a list of numbers representing a point in a higher-dimensional space. For example:
- **DV²**: `[value, depth1]` (e.g., `[3, 4]` represents `3 + 4i`)
- **DV⁴**: `[value, d1, d2, d3]` (e.g., `[1, 0, 1, 0]` represents `1 + j`)
- **DV⁸**: `[v, d1, ..., d7]`

### STO (Singularity Treatment Operation)

This is the core feature of DV-Math. Instead of throwing an error, division by zero triggers a **norm-preserving rotation**.

```python
from dvmath import DV2

# Standard division
result = DV2(4, 2) / DV2(2, 0)  # (4+2i) / 2 = 2+i
print(result)  # Output: [2.0, 1.0]

# Division by zero
zero_vec = DV2(0, 0)
result_sto = DV2(5, 0) / zero_vec  # Triggers STO

# The value 5 is rotated into the depth dimension
print(result_sto)  # Output: [0.0, 5.0]
```

**The key takeaway**: Information is preserved, not lost. `1/0` and `2/0` produce different, well-defined results.

---

## 3. Practical Usage

### Example 1: Complex Number Arithmetic (DV²)

DV² behaves exactly like complex numbers, but with the added benefit of STO.

```python
from dvmath import DV2

a = DV2(3, 4)  # 3 + 4i
b = DV2(1, -2) # 1 - 2i

# Basic operations
print(f"Sum: {a + b}")
print(f"Product: {a * b}")

# Norm and Inverse
print(f"Norm of a: {a.norm()}")        # Should be 5
print(f"Inverse of a: {a.inverse()}")

# STO in action
print(f"a / 0: {a / DV2(0,0)}") # Rotates [3, 4] -> [-4, 3]
```

### Example 2: 3D Rotations with Quaternions (DV⁴)

DV⁴ is isomorphic to quaternions and can be used for efficient, gimbal-lock-free 3D rotations.

```python
from dvmath import DV4
import math

# Vector to rotate
v = DV4([0, 10, 0, 0]) # A vector (10, 0, 0) in 3D space

# Rotation axis (y-axis) and angle (90 degrees)
angle = math.pi / 2
axis = DV4([0, 0, 1, 0]) # y-axis

# Create the rotation quaternion
q_rot = DV4([
    math.cos(angle / 2),
    math.sin(angle / 2) * axis.components[1],
    math.sin(angle / 2) * axis.components[2],
    math.sin(angle / 2) * axis.components[3]
])

# Apply the rotation: p' = q * p * q⁻¹
v_rotated = q_rot * v * q_rot.inverse()

print(f"Original vector: {v}")
print(f"Rotated vector: {v_rotated}") # Should be rotated around y-axis
```

### Example 3: High-Performance Octonion Math (DV⁸)

For performance-critical research involving octonions, always use the Numba-optimized version.

```python
# Import the Numba-optimized DV8 class
from dvmath.research.dv8.dv8_numba import DV8

# Create two octonions
o1 = DV8([1, 2, 3, 4, 5, 6, 7, 8])
o2 = DV8([8, 7, 6, 5, 4, 3, 2, 1])

# Perform non-associative multiplication
result = o1 * o2

print(f"Result of o1 * o2: {result}")

# Demonstrate non-associativity
o3 = DV8([1, 0, 1, 0, 1, 0, 1, 0])

assoc_check1 = (o1 * o2) * o3
assoc_check2 = o1 * (o2 * o3)

print(f"(o1*o2)*o3 == o1*(o2*o3): {assoc_check1 == assoc_check2}") # Will be False
```

---

## 4. Next Steps

- **Explore the `examples/` directory** for more detailed use cases.
- **Read the scientific paper** in `docs/DV_Paper_Revised.pdf` for the full theoretical background.
- **Consult the API documentation** (coming soon) for a detailed reference of all classes and methods.
- **Contribute!** If you find new applications or ways to improve the library, please open an issue or pull request on GitHub.

---

## 5. Mathematical Solidity: The Formal Proofs

DV-Mathematics is not just a programming library; it is a mathematically rigorous framework built on a solid theoretical foundation. To ensure its validity, the core components have been formally proven:

### Isomorphism to Established Algebras

Formal proofs have been established to show that the core DV algebras are **isomorphic** (mathematically identical) to the classical normed division algebras:

- **DV² ≅ ℂ (Complex Numbers):** The algebra of DV² is structurally identical to the complex numbers.
- **DV⁴ ≅ ℍ (Quaternions):** The algebra of DV⁴ is structurally identical to the quaternions.
- **DV⁸ ≅ 𝕆 (Octonions):** The algebra of DV⁸ is structurally identical to the octonions.

**What this means for you:** You are not using a new, unproven system. You are using a framework that is built upon centuries of established mathematics, but with a new, powerful perspective on handling singularities.

### Consistency of the STO Rule

A formal proof demonstrates that the Singularity Treatment Operation (STO) is **mathematically consistent**:

- **Norm Preservation:** STO is an isometry, meaning it preserves the magnitude (norm) of the vector. No information is lost.
- **Paradox-Free:** The rule resolves the classical paradox 1/0 = 2/0 by providing distinct, proportional results.

**What this means for you:** The singularity handling in DV-Math is not an arbitrary "hack". It is a consistent, predictable, and paradox-free rule that you can rely on in your applications.

> For the complete mathematical details, please see the full paper: [**Formal Proofs of the DV-Mathematics Framework**](formal_proofs_complete.pdf).

---

## 6. Further Resources

- **Scientific Paper:** [DV_Paper_Revised.pdf](DV_Paper_Revised.pdf) - Complete theoretical background
- **Objections & Rebuttals:** [objections_rebuttals_en.pdf](objections_rebuttals_en.pdf) - Addressing common criticisms
- **API Documentation:** [research/dv8/API_DOCUMENTATION.md](../research/dv8/API_DOCUMENTATION.md) - Detailed reference for all DV⁸ versions
- **GitHub Repository:** [github.com/IMalaspina/dvmath](https://github.com/IMalaspina/dvmath)
