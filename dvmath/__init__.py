# dvmath/__init__.py – Die finale, saubere Version
from .core import DV
from .constants import zero, one, I

# Jetzt erst erzeugen wir die Konstanten – NACHDEM DV existiert!
from .constants import zero as _z, one as _o, I as _i
_z = DV(0.0, 0.0)
_o = DV(1.0, 0.0)
_i = DV(0.0, 1.0)

# Und überschreiben die Platzhalter
import sys
sys.modules[__name__].zero = _z
sys.modules[__name__].one = _o
sys.modules[__name__].I = _i

__version__ = "0.1.0"
__author__ = "Ivano Franco Malaspina"

print("=" * 64)
print(" DV-MATHEMATICS – Dimensions-Vector Space")
print(" Erfinder: Ivano Franco Malaspina – 27. November 2025")
print(" Singularitäten durch Rotation in die Tiefe gelöst")
print(" Package erfolgreich geladen – bereit für die Wissenschaft!")
print("=" * 64)

__all__ = ["DV", "zero", "one", "I"]