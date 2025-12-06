# dvmath – Dimensions-Vector Mathematics

**Finite handling of singularities via orthogonal depth rotation**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)

**Author:** Ivano Franco Malaspina  
**Date:** December 2025  
**Version:** 1.0.0  

---

## Overview

DV-Mathematics (Dimensions-Vectors) is a mathematical framework for handling singularities, particularly division by zero, through geometric rotations in higher-dimensional vector spaces. The framework extends the real numbers by adding orthogonal "depth" dimensions, where singularities are treated as triggers for norm-preserving rotations rather than undefined operations.

**Key Features:**
- **DV²:** 2-dimensional algebra isomorphic to complex numbers (ℂ)
- **DV⁴:** 4-dimensional algebra isomorphic to quaternions (ℍ)
- **STO (Singularity Treatment Operation):** Conceptual rule for handling division by zero
- **Norm Preservation:** All operations maintain vector norms
- **Paradox-Free:** Resolves the classical paradox 1/0 = 2/0

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

---

## Documentation

### Papers

- **Original Paper (Nov 2025):** [docs/DV_Paper_Original.pdf](docs/DV_Paper_Original.pdf)
- **Revised Paper (Dec 2025):** [docs/DV_Paper_Revised.pdf](docs/DV_Paper_Revised.pdf)
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

---

## Research Status

### Validated and Implemented ✓
- **DV²:** Fully validated, isomorphic to ℂ
- **DV⁴:** Fully validated, isomorphic to ℍ

### Research in Progress 🔬
- **DV⁸ (Octonions):** Prototype implementation undergoing rigorous testing
  - Initial validation: 15/16 tests passed
  - Next phase: Fano plane validation, benchmarking, stability analysis
  - Expected release: Q1 2026

### Hypothetical (Not Validated) ⚠️
- Physical applications (black holes, quantum field theory)
- Higher dimensions (DV¹⁶, DV³²)

---

## Examples

See the [examples/](examples/) directory for more detailed demonstrations:
- `singularity_demo.py`: Basic singularity handling
- `quaternion_rotations.py`: 3D rotations using DV⁴
- `norm_preservation.py`: Validation of norm preservation

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
