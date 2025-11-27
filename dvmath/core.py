# dvmath/core.py – DIE DEFINITIVE, FEHLERFREIE VERSION
import math
from typing import Union
from .constants import one  # ← wichtig! Wir benutzen die Konstante one

Number = Union[int, float]


class DV:
    """Dimensions-Vector Space – Ivano Franco Malaspina, 27.11.2025"""

    __slots__ = ("v", "d")

    def __init__(self, v: Number, d: Number = 0.0):
        self.v = float(v)
        self.d = float(d)

    def __repr__(self) -> str:
        if self.d == 0:
            return f"DV({self.v})"
        return f"DV({self.v}, {self.d})"

    def __str__(self) -> str:
        return f"[{self.v}, {self.d}]"

    def __eq__(self, other) -> bool:
        if isinstance(other, DV):
            return math.isclose(self.v, other.v) and math.isclose(self.d, other.d)
        return False

    def __add__(self, other) -> "DV":
        if isinstance(other, (int, float)): return DV(self.v + other, self.d)
        return DV(self.v + other.v, self.d + other.d)

    __radd__ = __add__

    def __neg__(self) -> "DV":
        return DV(-self.v, -self.d)

    def __sub__(self, other) -> "DV":
        return self + (-other)

    def __mul__(self, other) -> "DV":
        if isinstance(other, (int, float)): return DV(self.v * other, self.d * other)
        v = self.v * other.v - self.d * other.d
        d = self.v * other.d + self.d * other.v
        return DV(v, d)

    __rmul__ = __mul__

    def rotate(self) -> "DV":
        return DV(-self.d, self.v)

    def norm(self) -> float:
        return math.hypot(self.v, self.d)

    def conj(self) -> "DV":
        return DV(self.v, -self.d)

    def inv(self) -> "DV":
        n2 = self.v ** 2 + self.d ** 2
        if n2 == 0:
            raise ZeroDivisionError("Inverse von [0,0] nicht definiert")
        return DV(self.v / n2, -self.d / n2)

    def __truediv__(self, other) -> "DV":
        if isinstance(other, (int, float)):
            return DV(self.v / other, self.d / other)
        if other.v == 0 and other.d == 0:
            print("Division durch Null → Rotation in die Tiefe!")
            return self.rotate()
        return self * other.inv()

    # DIE WICHTIGE METHODE – jetzt 100 % funktionsfähig!
    def __pow__(self, exponent: int) -> "DV":
        if not isinstance(exponent, int):
            raise TypeError("Nur ganzzahlige Exponenten erlaubt")
        if exponent == 0:
            return DV(1.0, 0.0)  # direkt one, ohne Import!
        if exponent < 0:
            return self.inv() ** (-exponent)

        # Effizientes Potenzieren
        result = DV(1.0, 0.0)
        base = self
        n = exponent
        while n > 0:
            if n % 2 == 1:
                result = result * base
            base = base * base
            n //= 2
        return result

        # Effizientes Potenzieren durch Quadrieren
        result = one
        base = self
        n = exponent
        while n > 0:
            if n % 2 == 1:
                result = result * base
            base = base * base
            n //= 2
        return result

    def as_complex(self) -> complex:
        return complex(self.v, self.d)