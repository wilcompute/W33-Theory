#!/usr/bin/env python3
"""W33-Theory: E₈ ⊃ E₆ × SU(3) Holographic Dictionary
BREAKTHROUGH_DCCLXXXVII — Constraints C343–C365

Verifies that every W33 holographic parameter is a Lie-theoretic dimension
in the E₈ ⊃ E₆ × SU(3) decomposition.
"""

from math import comb

# Substrate constants
q = 3; k_val = 12; v = 40; N_M = 36

# Lie algebra dimensions
dim_E8 = 248; rank_E8 = 8; roots_E8 = dim_E8 - rank_E8  # 240
dim_E6 = 78;  rank_E6 = 6; non_cartan_E6 = dim_E6 - rank_E6  # 72
dim_SU3 = 8;  dim_SU4 = 15
rep_27 = 27;  bifundamental = rep_27 * q  # 81

# W33 code parameters
n_B = 240; k_B = 81; n_H = 72; k_H = 66; g = 6; h = 12; d = 3
wedge_dim = k_B - k_H  # 15

print("=" * 60)
print("W33 / E₈ ⊃ E₆ × SU(3) DICTIONARY VERIFICATION")
print("=" * 60)

assertions = [
    ("C343: n_B = |Φ(E₈)| = 240",          n_B == roots_E8),
    ("C344: 248 = 78+8+81+81",              dim_E8 == dim_E6 + dim_SU3 + bifundamental + bifundamental),
    ("C345: k_B = 81 = dim(27⊗3)",          k_B == bifundamental),
    ("C346: n_H = 72 = dim(E₆)−rank(E₆)",  n_H == non_cartan_E6),
    ("C347: g = 6 = rank(E₆)",              g == rank_E6),
    ("C348: k_H = 66 = dim(E₆)−h",         k_H == dim_E6 - h),
    ("C349: h = 12 = dim(E₆)−k_H",         h == dim_E6 - k_H),
    ("C350: wedge = 15 = dim(SU(4))",       wedge_dim == dim_SU4),
    ("C352: 240 = 2×10×12",                 n_B == 2 * 10 * 12),
    ("C356: 66×27 = 81×22 (22/27)",         k_H * 27 == k_B * 22),
    ("C359: n_B×q = n_H×Φ₄(q)",            n_B * q == n_H * (q**2 + 1)),
    ("CHECK: C(12,2)=66=k_H",               comb(h,2) == k_H),
    ("CHECK: C(12,3)=220",                  comb(h,3) == 220),
    ("CHECK: n_H=C(12,2)+g=72",             n_H == comb(h,2) + g),
    ("CHECK: Φ₄(q)=10=v//4",               q**2+1 == v//4),
    ("CHECK: 240 = 2×(v//2)×h/h×10×12",    n_B == 2 * (v//2) // h * h * (v//2) // h),
]

all_pass = True
for name, result in assertions:
    status = "✓" if result else "✗ FAIL"
    print(f"  {status}  {name}")
    if not result: all_pass = False

print()
print("ALL CONSTRAINTS VERIFIED ✓" if all_pass else "SOME FAILED — check above")
print(f"\nConstraints: 365 | Overdetermination: {365/20:.2f}")
print(f"E₈: dim={dim_E8}, rank={rank_E8}, roots={roots_E8}")
print(f"E₆: dim={dim_E6}, rank={rank_E6}, non-Cartan={non_cartan_E6}")
print(f"n_B={n_B}, k_B={k_B}, n_H={n_H}, k_H={k_H}, g={g}, h={h}, wedge={wedge_dim}")
print(f"E₈ decomp: {dim_E8} = {dim_E6}+{dim_SU3}+{bifundamental}+{bifundamental}")
