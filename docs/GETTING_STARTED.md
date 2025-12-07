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
