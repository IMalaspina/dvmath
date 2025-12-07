# DV⁸ API Documentation

This document provides a detailed API reference for the three available DV⁸ (Octonion) implementations. For performance-critical applications, the **Numba version is highly recommended**.

---

## Choosing the Right Version

| Version | File | Key Feature | Use Case |
|---|---|---|---|
| **Numba (Recommended)** | `dv8_numba.py` | **Highest Performance (4.74× speedup)** | Numerical simulations, research, performance-critical tasks |
| **Optimized (Tuple)** | `dv8_optimized_v2.py` | **No Dependencies (1.24× speedup)** | General use, environments where Numba is not available |
| **Original (Class-based)** | `dv8.py` | **Most Readable** | Educational purposes, understanding the algorithm |

---

## Common API

All three versions share the same core API for initialization and basic operations.

### Initialization

```python
# Numba version
from dvmath.research.dv8.dv8_numba import DV8, ZERO, ONE, e1, e2

# Optimized version
# from dvmath.research.dv8.dv8_optimized_v2 import DV8, ZERO, ONE, e1, e2

# Original version
# from dvmath.research.dv8.dv8 import DV8, ZERO, ONE, e1, e2

# Create an octonion from a list of 8 floats
o = DV8([1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0])

# Use pre-defined constants
zero_vec = ZERO
identity = ONE
basis_e1 = e1
```

### Properties

- `components` (Tuple[float, ...]): A tuple containing the 8 components of the octonion.

### Magic Methods

- `__repr__() -> str`: Returns an unambiguous string representation (e.g., `DV8((1.0, ...))`).
- `__str__() -> str`: Returns a human-readable string representation (e.g., `[1.0000, ...]`).
- `__add__(other: DV8) -> DV8`: Component-wise addition.
- `__sub__(other: DV8) -> DV8`: Component-wise subtraction.
- `__mul__(other: DV8) -> DV8`: Non-associative octonion multiplication.
- `__truediv__(other: DV8) -> DV8`: Division. Applies STO if `other` is a zero vector.
- `__neg__() -> DV8`: Negation.
- `__eq__(other: DV8) -> bool`: Equality check with a tolerance of `1e-10`.

---

## Core Methods

### `norm() -> float`

Calculates the Euclidean norm (magnitude) of the octonion.

```python
o = DV8([1, 1, 1, 1, 0, 0, 0, 0])
print(o.norm()) # Output: 2.0
```

### `conjugate() -> DV8`

Returns the octonion conjugate (the first component remains, the other 7 are negated).

```python
o = DV8([1, 2, 3, 4, 5, 6, 7, 8])
print(o.conjugate()) # Output: [1.0, -2.0, -3.0, -4.0, -5.0, -6.0, -7.0, -8.0]
```

### `inverse() -> DV8`

Calculates the multiplicative inverse (`a⁻¹`). Throws a `ZeroDivisionError` if the norm is zero (or near-zero).

```python
o = DV8([1, 0, 0, 0, 0, 0, 0, 0]) # Identity
print(o.inverse()) # Output: [1.0, 0.0, ...]

# Note: Division (o1 / o2) is safer as it handles zero-norm vectors with STO.
```

### `STO() -> DV8`

Applies the Singularity Treatment Operation. This is equivalent to `GTR1` and rotates the octonion into an orthogonal dimension. It is called automatically during division by zero.

```python
o = DV8([5, 0, 0, 0, 0, 0, 0, 0])
print(o.STO()) # Output: [0.0, 5.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
```

---

## Class Methods

### `zero() -> DV8`

Returns the zero octonion `[0, 0, ..., 0]`.

### `one() -> DV8`

Returns the multiplicative identity `[1, 0, ..., 0]`.

### `basis(index: int) -> DV8`

Returns the i-th basis vector (e.g., `basis(2)` returns `e2 = [0, 0, 1, 0, ...]`).

- **`index`**: An integer from 0 to 7.

---

## Performance Comparison

Benchmarks were run on a standard cloud environment (Python 3.11, AMD64). Results show the throughput for 100,000 multiplication operations.

| Implementation | Throughput (ops/sec) | Speedup vs Original |
|---|---|---|
| **Numba (JIT)** | **754,756** | **4.74×** |
| Optimized (Tuple) | 197,602 | 1.24× |
| Original (Class) | 159,222 | 1.00× |

**Conclusion**: For any serious computation, the `dv8_numba` implementation should be used. The others are provided for educational purposes and as fallbacks.
