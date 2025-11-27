# dvmath/constants.py – KEINE Imports mehr! Nur Definitionen!

# Diese Datei wird erst NACH core.py geladen → kein Zyklus mehr
# Die eigentlichen Objekte werden erst in __init__.py erzeugt

zero = None  # wird später gesetzt
one  = None  # wird später gesetzt
I    = None  # wird später gesetzt

__all__ = ["zero", "one", "I"]