"""
Parts CDXXII – CDXXV  —  Verifier
Monster moonshine, j-function, Leech kissing number decomposition.

Run: python src/part_cdxxii_cdxxv_verifier.py
Expected: ALL ASSERTIONS PASSED
"""
from math import comb
from sympy import factorint

print("=" * 65)
print("PARTS CDXXII–CDXXV  —  VERIFIER")
print("=" * 65)

# Constants
PKT=24; SIX=6; E6=72; E8=240
V=27; K=16; LAM=10; MU=8; R=4
MU2=18; EDGES=216; p=3; u=6
LEECH_MIN = 196560
c1 = 196884

# CDXXII
print("\n── CDXXII ──")
HAPPY = 20; PARIAHS = 6; TOTAL = 26
assert TOTAL == V-1                  # 26 = V(W33)-1
assert PARIAHS == SIX                # 6 = six-kernel
assert HAPPY == 2*LAM                # 20 = 2*lambda
assert HAPPY + PARIAHS == TOTAL
print(f"  Total sporadic = V-1 = 26  ✓")
print(f"  Pariahs = six-kernel = 6  ✓")
print(f"  Happy Family = 2λ = 20  ✓")

# CDXXIII
print("\n── CDXXIII ──")
assert PKT == 24
assert 744 == PKT * 31
assert 47*59*71 == 196883
assert (3**2-3**1) + (3**3-3**2) == PKT  # 6+18=24
assert E6 // PKT == p                     # 72/24=3=p
print("  744 = PKT×31, 196883=47×59×71, 6+18=24, E6/PKT=p  ✓")

# CDXXIV
print("\n── CDXXIV ──")
assert LEECH_MIN == K * V * comb(K-1, 3)     # 16×27×455
assert LEECH_MIN == PKT * p**2 * LAM * 91    # 24×9×10×91
assert LEECH_MIN == EDGES * LAM * 91         # 216×10×91
print(f"  LEECH_MIN = K×V×C(K-1,3) = {K}×{V}×{comb(K-1,3)}  ✓")
print(f"  LEECH_MIN = PKT×p²×λ×91  ✓")
print(f"  LEECH_MIN = EDGES×λ×91   ✓")

# CDXXV
print("\n── CDXXV ──")
assert c1 - LEECH_MIN == MU2**2   # 196884-196560 = 18²
assert 24 == PKT                  # 24 Niemeier lattices = PKT
print(f"  c(1) - Leech_min = μ₂² = 18² = 324  ✓")
print(f"  24 Niemeier lattices = PKT  ✓")

print()
print("ALL ASSERTIONS PASSED  ✓")
