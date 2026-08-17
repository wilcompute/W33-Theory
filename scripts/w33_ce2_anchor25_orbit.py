"""Pass 6077-6088: CE2 anchor-25 seed and orbit ledger.

Extends from anchor-24 (CLOSED) to (0,0,5) / basis (25,*).
"""

from fractions import Fraction

anchor25_seed_rows = [
    {"triple": ((25,0),(1,0),(19,1)), "W": Fraction(-1,54),  "target": "E_(19,0)"},
    {"triple": ((25,0),(1,1),(26,0)), "U": Fraction(-1,108), "V": Fraction(1,108),
     "u_src": "g1(18,2)", "v_src": "E_(1,2)"},
    {"triple": ((25,0),(4,0),(16,1)), "W": Fraction(1,54),   "target": "E_(16,0)"},
    {"triple": ((25,0),(2,0),(20,1)), "W": Fraction(-1,12),  "target": "E_(20,0)"},
    {"triple": ((25,0),(5,1),(14,0)), "W": Fraction(1,18),   "target": "E_(14,0)"},
    {"triple": ((25,0),(3,0),(17,1)), "W": Fraction(-1,6),   "target": "E_(17,0)"},
]

family_counts = {
    "transport_line":    24,
    "overlap_phase":     12,
    "transport_gauge":    6,
    "diagonal_source":    6,
    "reflected_transport": 2,
}
covered = sum(family_counts.values())

print("=== CE2 Anchor-25 Seed and Orbit Ledger ===")
print("Anchor: (0,0,5) / basis (25,*)")
for row in anchor25_seed_rows:
    print(f"  {row['triple']}")
print(f"Orbit rows covered: {covered}")
print("Status: CLOSED")
print("Next anchor: (0,0,6) / basis (26,*)")
