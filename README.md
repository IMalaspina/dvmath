# dvmath – Dimensions-Vector Mathematics

**Finite handling of singularities via orthogonal depth rotation**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)

**Author:** Ivano Franco Malaspina  
**Date:** December 2025  
**Version:** 1.1.0  

---

## Overview

DV-Mathematics (Dimensions-Vectors) is a mathematical framework for handling singularities, particularly division by zero, through geometric rotations in higher-dimensional vector spaces. The framework extends the real numbers by adding orthogonal "depth" dimensions, where singularities are treated as triggers for norm-preserving rotations rather than undefined operations.

**Key Features:**
- **DV²:** 2-dimensional algebra isomorphic to complex numbers (ℂ)
- **DV⁴:** 4-dimensional algebra isomorphic to quaternions (ℍ)
- **DV⁸:** 8-dimensional algebra isomorphic to octonions (𝕆) — **Validated**
- **STO (Singularity Treatment Operation):** Conceptual rule for handling division by zero
- **Norm Preservation:** All operations maintain vector norms
- **Paradox-Free:** Resolves the classical paradox 1/0 = 2/0
- **High Performance:** Numba JIT-optimized implementation (750,000+ ops/sec for DV⁸)

---

## Quick Start

### Installation

```bash
pip install git+https://github.com/IMalaspina/dvmath.git
```

### Basic Usage (DV²)

```python
from dvmath import DV2, zero

# Division by zero is well-defined
print(DV2(1) / zero)   # → [0.0, 1.0]
print(DV2(2) / zero)   # → [0.0, 2.0]
print(DV2(7) / zero)   # → [0.0, 7.0]

# The classical paradox is resolved: 1/0 ≠ 2/0 ≠ 7/0
```

### Quaternions (DV⁴)

```python
from dvmath import DV4

# Quaternion multiplication
i = DV4(0, 1, 0, 0)
j = DV4(0, 0, 1, 0)
k = DV4(0, 0, 0, 1)

print(i * j)  # → k
print(j * k)  # → i
print(k * i)  # → j
```

### Octonions (DV⁸) — **NEW in v1.1.0**

```python
from dvmath.research.dv8.dv8_numba import DV8  # Numba-optimized version

o1 = DV8([1, 0, 0, 0, 1, 0, 0, 0])
o2 = DV8([0, 1, 0, 0, 0, 0, 0, 0])

print(o1 * o2)      # Non-associative multiplication
print(o1.norm())    # Norm is preserved
```

---

## Documentation

### Papers

- **Original Paper (Nov 2025):** [docs/DV_Paper_Original.pdf](docs/DV_Paper_Original.pdf)
- **Revised Paper (Dec 2025):** [docs/DV_Paper_Revised.pdf](docs/DV_Paper_Revised.pdf)
- **Objections & Rebuttals (Dec 2025):** [docs/objections_rebuttals_en.pdf](docs/objections_rebuttals_en.pdf) — **NEW**
- **Evolution Tracking:** [docs/evolution.md](docs/evolution.md)

### Core Concepts

#### Tiefenrotation (TR)

The Tiefenrotation is a 90-degree counter-clockwise rotation in the value-depth plane. For DV², it is equivalent to multiplication by the imaginary unit *i*.

```python
v = DV2(3, 4)
rotated = v.TR()  # [-4, 3]
```

#### Singularity Treatment Operation (STO)

STO is **not** a new algebraic operation, but a **conceptual rule**: When division by a zero-norm vector is attempted, apply TR/GTR to the numerator. This ensures finite, well-defined results without introducing paradoxes.

```python
# STO is automatically applied during division by zero
result = DV2(5, 0) / DV2(0, 0)  # Applies STO internally
```

#### Norm Preservation

All TR, GTR, and STO operations preserve the Euclidean norm of the vector, ensuring that no information is lost during singularity handling.

```python
v = DV2(3, 4)
assert v.norm() == v.TR().norm()  # ✓
assert v.norm() == v.STO().norm()  # ✓
```

---

## API Reference

### DV2 (Complex Numbers)

```python
class DV2:
    def __init__(self, v: float, d: float = 0.0)
    def TR(self) -> DV2                    # Tiefenrotation
    def STO(self) -> DV2                   # Singularity Treatment
    def norm(self) -> float                # Euclidean norm
    def conjugate(self) -> DV2             # Complex conjugate
    def inverse(self) -> DV2               # Multiplicative inverse
    def to_complex(self) -> complex        # Convert to Python complex
```

### DV4 (Quaternions)

```python
class DV4:
    def __init__(self, v: float, d1: float = 0.0, d2: float = 0.0, d3: float = 0.0)
    def GTR1(self) -> DV4                  # Rotation by i
    def GTR2(self) -> DV4                  # Rotation by j
    def GTR3(self) -> DV4                  # Rotation by k
    def STO(self) -> DV4                   # Singularity Treatment
    def norm(self) -> float                # Euclidean norm
    def conjugate(self) -> DV4             # Quaternion conjugate
    def inverse(self) -> DV4               # Multiplicative inverse
```

### DV8 (Octonions) — **NEW in v1.1.0**

```python
class DV8:
    def __init__(self, components: list[float])  # 8 components
    def __mul__(self, other: DV8) -> DV8         # Non-associative multiplication
    def STO(self) -> DV8                         # Singularity Treatment
    def norm(self) -> float                      # Euclidean norm
    def conjugate(self) -> DV8                   # Octonion conjugate
    def inverse(self) -> DV8                     # Multiplicative inverse
```

**Performance Variants:**
- `dv8.py`: Original implementation (readable, 159,000 ops/sec)
- `dv8_optimized_v2.py`: Tuple-optimized (197,000 ops/sec, 1.24× faster)
- `dv8_numba.py`: Numba JIT (754,000 ops/sec, 4.74× faster) — **Recommended**

---

## Validation Results — **NEW in v1.1.0**

### DV⁸ (Octonions)

| Test Phase | Result | Details |
|---|---|---|
| **Fano Plane** | ✓ Passed | Moufang identities: 100/100 tests |
| **Cross-Library** | ✓ Passed | Max error: < 1e-15 (machine precision) |
| **Numerical Stability** | ✓ Passed | Stable from 1e-15 to 1e+15 (30 orders of magnitude) |
| **Performance** | ✓ Passed | 754,756 ops/sec (Numba), 4.74× speedup |

**Full Reports:**
- [research/dv8/DV8_Validation_Report.md](research/dv8/DV8_Validation_Report.md)
- [research/dv8/DV8_Optimization_Report.md](research/dv8/DV8_Optimization_Report.md)

---

## Research Status

### Validated and Implemented ✓
- **DV²:** Fully validated, isomorphic to ℂ
- **DV⁴:** Fully validated, isomorphic to ℍ
- **DV⁸:** Fully validated, isomorphic to 𝕆 — **NEW in v1.1.0**

### Research in Progress 🔬
- **DV¹⁶ (Sedenions):** Prototype planned for Q1 2026
  - Challenge: Handling zero divisors and loss of norm preservation
  - Goal: Investigate if STO can be extended consistently

### Hypothetical (Not Validated) ⚠️
- Physical applications (black holes, quantum field theory)
- Lie algebra connections
- Category theory formalization

---

## Version History

### v1.1.0 (December 2025) — **Current**
- **DV⁸ Validated:** Complete 4-phase validation (Fano plane, cross-library, stability, performance)
- **Performance Optimization:** Numba JIT implementation (4.74× speedup)
- **Documentation:** Added "Objections and Rebuttals" PDF
- **Bug Fixes:** Near-zero division handling in DV⁸

### v1.0.0 (December 2025)
- **Major Milestone:** Fusion of DV² and DV⁴ into unified codebase
- **DV⁸ Research:** Prototype implementation with initial validation
- **STO Clarification:** Defined as GTR1 application at singularities
- **Bug Fixes:** Corrected unreachable code in `__pow__` method

### v0.1.0 (Initial Release)
- **DV² Implementation:** Basic complex number operations with TR
- **Prototype Status:** Initial exploration of DV framework

---

## Examples

See the [examples/](examples/) directory for more detailed demonstrations:
- `singularity_demo.py`: Basic singularity handling
- `quaternion_rotations.py`: 3D rotations using DV⁴
- `norm_preservation.py`: Validation of norm preservation
- `octonion_demo.py`: DV⁸ operations and non-associativity — **NEW**

---

## Contributing

Contributions are welcome! Please ensure:
1. All code is mathematically validated
2. Tests are included for new features
3. Hypothetical concepts are clearly labeled
4. Documentation is updated

---

## License

MIT License - see [LICENSE](LICENSE) file for details.

---

## Citation

If you use DV-Mathematics in your research, please cite:

```bibtex
@misc{malaspina2025dv,
  author = {Malaspina, Ivano Franco},
  title = {DV-Mathematics: A Framework for Handling Singularities},
  year = {2025},
  publisher = {GitHub},
  url = {https://github.com/IMalaspina/dvmath}
}
```

---

## Contact

**Ivano Franco Malaspina**  
GitHub: [@IMalaspina](https://github.com/IMalaspina)  
Repository: [github.com/IMalaspina/dvmath](https://github.com/IMalaspina/dvmath)

