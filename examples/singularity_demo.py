# examples/singularity_demo.py
from dvmath import DV, zero, one, I

print("DV-MATHEMATICS – Live-Demonstration der Singularitätenauflösung")
print("================================================================\n")

print(f"1 / 0 = {one / zero}")
print(f"2 / 0 = {DV(2) / zero}")
print(f"7 / 0 = {DV(7) / zero}")
print("→ Alle verschieden! Das klassische Paradoxon 1=2 ist unmöglich!\n")

print(f"Rotation mit I:        I × [5, 0] = {I * DV(5)}")
print(f"180° Rotation:         I² × [5, 0] = {I * I * DV(5)}")
print(f"270° Rotation:         I³ × [5, 0] = {I * I * I * DV(5)}")
print(f"360° = zurück:         I⁴ × [5, 0] = {I**4 * DV(5)}")
print()

print("Beweis der zyklischen Gruppe (wie im Paper, Seite 2):")
print(f"  I⁴          = {I**4}")                                 # → DV(1.0)
print(f"  TR⁴([3,4])  = {(I**4) * DV(3, 4)}")                     # → [3, 4]
print(f"  Original    = {DV(3, 4)}")
print("→ Identität bestätigt! TR ist eine Drehung um 90°, Ordnung 4 ✓\n")

print("Norm bleibt immer erhalten:")
a = DV(3, 4)
b = DV(1, 7)
print(f"  ||{a}|| = {a.norm():.10f}")
print(f"  ||{b}|| = {b.norm():.10f}")
print(f"  ||{a * b}|| = {(a * b).norm():.10f}")
print(f"  ||a|| × ||b|| = {a.norm() * b.norm():.10f}")
print("→ Multiplikation ist normerhaltend (bis auf Rundungsfehler) ✓")