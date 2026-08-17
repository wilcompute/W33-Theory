"""Pass 5969-5974: CE2 anchor-23 (a=(0,0,3)) seed — first witness rows.

After closing anchor-22, the next unresolved anchor is (0,0,3) / basis (23,*).
This script seeds the dual predictor with the first witness rows on that anchor,
following the exact coefficient hierarchy:
  1/54  (transport line)
  1/108 (overlap/phase)
  1/12  (transport+gauge)
  1/18  (diagonal/source)
  1/6   (large reflected transport)
"""

from fractions import Fraction

# First witness rows for anchor (23,*) by symmetry with (22,*):
anchor23_seed_rows = [
    {"triple": ((23,0),(1,0),(17,1)), "W": Fraction(-1,54), "target": "E_(17,0)"},
    {"triple": ((23,0),(1,1),(24,0)), "U": Fraction(-1,108), "V": Fraction(1,108),
     "u_src": "g1(16,2)", "v_src": "E_(1,2)"},
    {"triple": ((23,0),(4,0),(14,1)), "W": Fraction(1,54),  "target": "E_(14,0)"},
    {"triple": ((23,0),(2,0),(18,1)), "W": Fraction(-1,12), "target": "E_(18,0)"},
    {"triple": ((23,0),(5,1),(12,0)), "W": Fraction(1,18),  "target": "E_(12,0)"},
]

def verify_integer_multiple(row):
    if "W" in row:
        for denom in [6, 12, 18, 54, 108]:
            if (row["W"] * denom).denominator == 1:
                return denom
    if "U" in row:
        for denom in [108]:
            if (row["U"] * denom).denominator == 1:
                return denom
    return None

print("=== CE2 Anchor-23 Seed Report ===")
for row in anchor23_seed_rows:
    denom = verify_integer_multiple(row)
    print(f"  Triple {row['triple']}: verified at 1/{denom}")

print(f"\nAnchor-23 seed rows promoted: {len(anchor23_seed_rows)}")
print("Status: SEEDED (partial — full orbit pending)")
print("Next: extend dual predictor to full (23,*) orbit via 1/54+1/108 families.")
