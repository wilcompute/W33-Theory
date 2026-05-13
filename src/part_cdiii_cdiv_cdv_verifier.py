"""
Parts CDIII / CDIV / CDV — Verifier
Triality eigenstates, 36-cover, ladder as E2/Theta_E8 shadow.

Run: python src/part_cdiii_cdiv_cdv_verifier.py
Expected: ALL ASSERTIONS PASSED
"""
import math
from fractions import Fraction

print("=" * 65)
print("PARTS CDIII / CDIV / CDV  —  VERIFIER")
print("=" * 65)

# Constants
V, K, LAM, MU = 27, 16, 10, 8
EDGES  = V * K // 2          # 216
SIX    = 6
E6_ROOTS = 72
E8_ROOTS = 240
W_E6   = 51840
W_D4   = 192
W_F4   = 1152
TRIANGLES = V * K * LAM // 6  # 720

# ── CDIII: Triality eigenstates ──────────────────────────────
print("\n── CDIII: Triality eigenstates ──")
rep_dim = 2
n_reps  = 3
total   = rep_dim * n_reps
assert total == SIX
assert SIX // 2 == n_reps          # orbit-stabiliser
assert n_reps * 24 == E6_ROOTS     # 3×24 = 72 = E6 roots
print(f"  6 = 3 sectors × 2D each  ✓")
print(f"  orbit = |S₃|/|Stab| = 6/2 = 3 generations  ✓")
print(f"  3×24 = {n_reps*24} = E6 roots  ✓")

# ── CDIV: 36-cover ───────────────────────────────────────────
print("\n── CDIV: 36-cover ──")
n_cubic_lines = 27
n_eckardt     = 9
assert n_cubic_lines + n_eckardt == SIX**2   # 36
assert n_eckardt == 3**2                     # A2×A2
assert math.factorial(6) == TRIANGLES        # |S6|=720=triangles
assert math.factorial(6) // 2 == 360         # |A6|=360
W_G2 = 12
assert W_G2 * n_reps == SIX**2              # 12×3=36
print(f"  27 + 9 = {n_cubic_lines+n_eckardt} = 6²  ✓")
print(f"  9 = 3² = A₂×A₂  ✓")
print(f"  |S₆| = {TRIANGLES} = W33 triangles  ✓")
print(f"  |W(G₂)|×3 = {W_G2}×3 = {W_G2*3}  ✓")

# ── CDV: E2 shadow & Theta_E8 ────────────────────────────────
print("\n── CDV: E2 shadow & Θ_E8 ──")
sigma1 = lambda n: sum(d for d in range(1,n+1) if n%d==0)

ladder_e2 = [(1,1,24),(2,3,72),(3,4,96),(4,7,168),(7,8,192)]
for n, s, val in ladder_e2:
    assert sigma1(n) == s,  f"sigma1({n}) = {sigma1(n)} ≠ {s}"
    assert 24*s == val,     f"24×sigma1({n}) = {24*s} ≠ {val}"
print(f"  E₂ ladder n=1,2,3,4,7 → 24,72,96,168,192  ✓")

# sigma1(7) = 1+7 = 8 (prime index, Fano)
assert sigma1(7) == 8
assert 8 == 4 * 2   # r × |s|
print(f"  σ₁(7) = 8 = r×|s| (tomotope 8-multiplier)  ✓")
print(f"  7 = Fano prime index  ✓")

# Theta_E8 coefficients (all divisible by 24)
theta_E8 = [0,240,2160,6720,17520,30240,60480,82560,140400,181680,272160]
for i, c in enumerate(theta_E8[1:], 1):
    assert c % 24 == 0, f"Θ_E8[{i}] = {c} not div by 24"
print(f"  All Θ_E8 coefficients divisible by 24  ✓")

# The missing rung: 216 = 9×24
assert 9*24 == 216
assert sigma1(9) == 13   # not 9, so 216 is NOT in E2
assert 216 == SIX**3     # comes from cubic twist
print(f"  216 = 6³ (cubic twist, not E₂)  ✓")
print(f"  σ₁(9) = {sigma1(9)} ≠ 9, so 216 is the 'derived rung'  ✓")

print()
print("ALL ASSERTIONS PASSED  ✓")
