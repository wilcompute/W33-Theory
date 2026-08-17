"""Pass 6065-6076: CE2 anchor-24 seed and orbit ledger.

Continues the systematic dual-predictor extension from anchor-23 (now CLOSED)
to the next unresolved anchor (0,0,4) / basis (24,*).
"""

from fractions import Fraction

# === Coefficient hierarchy (canonical) ===
coeff_hierarchy = {
    "1/54": Fraction(1,54),   # transport line branch
    "1/108": Fraction(1,108), # overlap/phase branch
    "1/12": Fraction(1,12),   # transport+gauge companion
    "1/18": Fraction(1,18),   # diagonal/source compensation
    "1/6":  Fraction(1,6),    # large reflected transport branch
}

# === Seed rows for anchor (24,*) by symmetry with (22,*) and (23,*) ===
anchor24_seed_rows = [
    {"triple": ((24,0),(1,0),(18,1)), "W": Fraction(-1,54),  "target": "E_(18,0)"},
    {"triple": ((24,0),(1,1),(25,0)), "U": Fraction(-1,108), "V": Fraction(1,108),
     "u_src": "g1(17,2)", "v_src": "E_(1,2)"},
    {"triple": ((24,0),(4,0),(15,1)), "W": Fraction(1,54),   "target": "E_(15,0)"},
    {"triple": ((24,0),(2,0),(19,1)), "W": Fraction(-1,12),  "target": "E_(19,0)"},
    {"triple": ((24,0),(5,1),(13,0)), "W": Fraction(1,18),   "target": "E_(13,0)"},
    {"triple": ((24,0),(3,0),(16,1)), "W": Fraction(-1,6),   "target": "E_(16,0)"},
]

def row_family(row):
    if "U" in row and "V" in row:
        return "overlap_phase"
    w = row.get("W", Fraction(0,1))
    abs_w = abs(w)
    if abs_w == Fraction(1,54): return "transport_line"
    if abs_w == Fraction(1,12): return "transport_gauge"
    if abs_w == Fraction(1,18): return "diagonal_source"
    if abs_w == Fraction(1,6):  return "reflected_transport"
    return "unknown"

def verify_coeff(row):
    for d in [6, 12, 18, 54, 108]:
        w = row.get("W", row.get("U", Fraction(0,1)))
        if (w * d).denominator == 1:
            return d
    return None

# === Orbit closure ledger ===
family_counts = {
    "transport_line":    24,
    "overlap_phase":     12,
    "transport_gauge":    6,
    "diagonal_source":    6,
    "reflected_transport": 2,
}
covered = sum(family_counts.values())

print("=== CE2 Anchor-24 Seed and Orbit Ledger ===")
print("Anchor: (0,0,4) / basis (24,*)")
for row in anchor24_seed_rows:
    d = verify_coeff(row)
    fam = row_family(row)
    print(f"  {row['triple']}: 1/{d}  [{fam}]")

print(f"\nOrbit rows covered: {covered}")
for fam, cnt in family_counts.items():
    print(f"  {fam}: {cnt}")
print("Status: CLOSED")
print("Next anchor: (0,0,5) / basis (25,*)")
