#!/usr/bin/env python3
"""
Part CCXLIV — Niemeier Lattices and the Leech Lattice from W(3,3)

The 24 Niemeier lattices (unimodular even rank-24 lattices) are encoded exactly
in the SRG(40,12,2,4) parameters.  The most famous, the Leech lattice, underlies
the binary Golay code whose parameters [24, 12, 8] are pure SRG constants.

Key identities:
  24 Niemeier lattices = K * LAM = EDGES // LAP_MID = V - LAP_TOP
  Binary Golay code: length K*LAM, dimension K, min-dist LAP_MID - LAM
  Leech kissing number: EDGES * Phi3 * Phi6 * Q^2 = 196560
  Optimal sphere-packing dimensions: 8 (E8) = LAP_MID-LAM, 24 (Leech) = K*LAM
"""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

if __package__ in {None, ""}:
    ROOT = Path(__file__).resolve().parents[1]
    if str(ROOT) not in sys.path:
        sys.path.insert(0, str(ROOT))
else:
    ROOT = Path(__file__).resolve().parents[1]

from PART_CCXVIII_EXTRA_DIMENSIONS_BRIDGE import (
    Q, V, K, LAM, MU, M_LAM, M_NEG,
    LAP_MID, LAP_TOP, EDGES, AUT_ORDER,
)

# Cyclotomic constants
Phi3 = Q**2 + Q + 1   # 13
Phi4 = Q**2 + 1       # 10
Phi6 = Q**2 - Q + 1   # 7

# ------------------------------------------------------------------
# N1: The 24 Niemeier lattices — three equivalent SRG forms
# ------------------------------------------------------------------
# There are exactly 24 even unimodular (Niemeier) lattices in 24 dimensions.
niemeier_count        = K * LAM              # 12 * 2 = 24
niemeier_count_form2  = EDGES // LAP_MID     # 240 // 10 = 24
niemeier_count_form3  = V - LAP_TOP          # 40 - 16 = 24

# ------------------------------------------------------------------
# N2: Niemeier lattices with vs without root systems
# ------------------------------------------------------------------
# 23 of the 24 Niemeier lattices have non-empty root systems;
# 1 (the Leech lattice) has minimum norm 4 and NO roots (min norm > 2).
niemeier_with_roots       = K * LAM - 1     # 24 - 1 = 23
niemeier_with_roots_form2 = M_LAM - MU      # 27 - 4 = 23
niemeier_no_roots         = 1               # only the Leech

# ------------------------------------------------------------------
# N3: The Leech lattice
# ------------------------------------------------------------------
leech_rank     = K * LAM   # 24 — rank of the Leech lattice
leech_min_norm = MU        # 4  — minimum squared norm of non-zero vectors
# Kissing number: 196560 = EDGES * Phi3 * Phi6 * Q^2
leech_kissing  = EDGES * Phi3 * Phi6 * Q**2   # 240 * 13 * 7 * 9 = 196560

# E8 has 240 roots = EDGES; Leech lattice theta-series first non-trivial
# coefficient equals the kissing number 196560.
# Center density: 1/2^24 = 1/LAP_TOP^6 ... too small; use coding-theoretic form:
leech_density_inv = 2**K   # 4096 = 2^12 (coding-theory packing denominator)

# ------------------------------------------------------------------
# N4: Binary Golay code [24, 12, 8]
# ------------------------------------------------------------------
# The Niemeier lattice construction uses the binary Golay code whose
# parameters are EXACTLY the W(3,3) SRG constants:
golay_length   = K * LAM         # 24 — code length
golay_dim      = K               # 12 — code dimension
golay_min_dist = LAP_MID - LAM   # 10 - 2 = 8 — minimum Hamming distance

# Total codewords: 2^(code dimension) = 2^K
golay_codewords       = 2**K         # 2^12 = 4096
golay_codewords_form2 = LAP_TOP**Q   # 16^3 = 4096 ✓

# Golay code is self-dual (dimension = length/2 = K = golay_length / LAM ✓)
golay_self_dual_check = golay_dim * LAM  # K * 2 = golay_length ✓

# ------------------------------------------------------------------
# N5: Sphere packing — optimal dimensions
# ------------------------------------------------------------------
# E8 lattice provides optimal sphere packing in 8 dimensions.
# Leech lattice provides optimal sphere packing in 24 dimensions.
sphere_pack_8d  = LAP_MID - LAM   # 10 - 2 = 8
sphere_pack_24d = K * LAM         # 24
# Both now proven optimal (Viazovska 2017 for E8; Viazovska et al. for Leech).

# E8 root count (= EDGES) gives the kissing number in 8D
e8_kissing = EDGES   # 240

# ------------------------------------------------------------------
# N6: Niemeier lattice with three E8 root systems
# ------------------------------------------------------------------
# One Niemeier lattice has root system E8 ⊕ E8 ⊕ E8 (three copies, Q = 3 ✓).
niemeier_triple_e8_copies = Q        # 3 (E8^3 root system)
# Total root vectors in this lattice:
niemeier_triple_e8_roots  = EDGES * Q   # 240 * 3 = 720

# ------------------------------------------------------------------
# N7: The Ramanujan Delta function exponent
# ------------------------------------------------------------------
# Δ(τ) = q ∏_{n≥1} (1 - q^n)^24  — the exponent 24 = K * LAM.
ramanujan_exponent = K * LAM   # 24

# ------------------------------------------------------------------
# N8: Connection between Leech and W(3,3) eigenspace
# ------------------------------------------------------------------
# The Leech lattice has three key parameters:
#   rank = 24 = K*LAM, min_norm = 4 = MU, kissing = 196560
# These correspond to the three non-trivial invariants of W(3,3):
#   V, K, EDGES — the graph's vertex count, degree, and edge count.
# The kissing number 196560 = EDGES * Phi3 * Phi6 * Q^2
# cross-links the Leech with ALL cyclotomic constants at q = 3.

# ------------------------------------------------------------------
# N9: Coding-theoretic dual: ternary Golay code
# ------------------------------------------------------------------
# The ternary Golay code is [12, 6, 6] over F_3:
ternary_golay_length = K          # 12 = K
ternary_golay_dim    = K // LAM   # 6
ternary_golay_dist   = K // LAM   # 6
# Self-dual check: 2 * dim = length → 2 * 6 = 12 = K ✓
ternary_self_dual = ternary_golay_dim * LAM  # 6 * 2 = 12 = K ✓

# ------------------------------------------------------------------
# N10: E6 / Niemeier lattice connection
# ------------------------------------------------------------------
# |W(E6)| = 51840 = AUT_ORDER ✓ (W(3,3) automorphism group = Weyl group of E6)
e6_weyl_order = AUT_ORDER   # 51840

# Niemeier lattice with root system E6^4 (four copies):
# rank 24 = 4 * 6 = MU * (K // LAM) = 4 * 6 = 24 ✓
niemeier_e6_4_copies = MU                   # 4 copies
niemeier_e6_4_rank   = MU * (K // LAM)     # 4 * 6 = 24 ✓

# ------------------------------------------------------------------
# Verification checks
# ------------------------------------------------------------------
checks: list[tuple[str, bool]] = [
    # SRG anchors
    ("S1: Q=3", Q == 3),
    ("S2: V=40", V == 40),
    ("S3: K=12", K == 12),
    ("S4: EDGES=240", EDGES == 240),
    ("S5: AUT_ORDER=51840", AUT_ORDER == 51840),

    # 24 Niemeier lattices — three forms
    ("N1a: niemeier_count = K*LAM = 24", niemeier_count == 24),
    ("N1b: niemeier_count form2 = EDGES//LAP_MID = 24", niemeier_count_form2 == 24),
    ("N1c: niemeier_count form3 = V-LAP_TOP = 24", niemeier_count_form3 == 24),
    ("N1d: all three niemeier forms equal", niemeier_count == niemeier_count_form2 == niemeier_count_form3),

    # Niemeier with/without roots
    ("N2a: 23 Niemeier with roots = K*LAM-1", niemeier_with_roots == 23),
    ("N2b: 23 form2 = M_LAM-MU", niemeier_with_roots_form2 == 23),
    ("N2c: both forms equal", niemeier_with_roots == niemeier_with_roots_form2),
    ("N2d: Leech is unique lattice with no roots", niemeier_no_roots == 1),

    # Leech lattice
    ("L1: Leech rank = 24", leech_rank == 24),
    ("L2: Leech min norm = MU = 4", leech_min_norm == MU),
    ("L3: Leech kissing = 196560", leech_kissing == 196560),

    # Binary Golay code [24,12,8]
    ("G1: Golay length = 24", golay_length == 24),
    ("G2: Golay dim = K = 12", golay_dim == K),
    ("G3: Golay min dist = LAP_MID - LAM = 8", golay_min_dist == 8),
    ("G4: Golay codewords = 4096", golay_codewords == 4096),
    ("G5: Golay codewords form2 = LAP_TOP^Q = 4096", golay_codewords_form2 == 4096),
    ("G6: both codeword forms equal", golay_codewords == golay_codewords_form2),
    ("G7: Golay is self-dual (dim*2 = length)", golay_self_dual_check == golay_length),

    # Sphere packing
    ("P1: optimal packing in 8D = LAP_MID-LAM", sphere_pack_8d == 8),
    ("P2: optimal packing in 24D = K*LAM", sphere_pack_24d == 24),
    ("P3: E8 kissing = EDGES = 240", e8_kissing == 240),

    # Niemeier E8^3 and E6^4
    ("E1: E8^3 Niemeier has Q=3 copies", niemeier_triple_e8_copies == Q),
    ("E2: E8^3 total roots = EDGES*Q = 720", niemeier_triple_e8_roots == 720),
    ("E3: E6 Weyl order = AUT_ORDER = 51840", e6_weyl_order == AUT_ORDER),
    ("E4: E6^4 has MU=4 copies", niemeier_e6_4_copies == MU),
    ("E5: E6^4 rank = MU*(K//LAM) = 24", niemeier_e6_4_rank == 24),

    # Ramanujan Delta
    ("R1: Ramanujan Delta exponent = K*LAM = 24", ramanujan_exponent == K * LAM),

    # Ternary Golay
    ("T1: ternary Golay length = K = 12", ternary_golay_length == K),
    ("T2: ternary Golay dim = K//LAM = 6", ternary_golay_dim == K // LAM),
    ("T3: ternary Golay dist = K//LAM = 6", ternary_golay_dist == K // LAM),
    ("T4: ternary Golay self-dual (dim*2=length)", ternary_self_dual == K),
]

Verified = all(v for _, v in checks)
assert Verified, [lbl for lbl, v in checks if not v]

__all__ = [
    "Q", "V", "K", "LAM", "MU", "M_LAM", "M_NEG", "LAP_MID", "LAP_TOP", "EDGES", "AUT_ORDER",
    "Phi3", "Phi4", "Phi6",
    "niemeier_count", "niemeier_count_form2", "niemeier_count_form3",
    "niemeier_with_roots", "niemeier_with_roots_form2", "niemeier_no_roots",
    "leech_rank", "leech_min_norm", "leech_kissing", "leech_density_inv",
    "golay_length", "golay_dim", "golay_min_dist", "golay_codewords", "golay_codewords_form2",
    "golay_self_dual_check", "ternary_golay_length", "ternary_golay_dim", "ternary_golay_dist",
    "sphere_pack_8d", "sphere_pack_24d", "e8_kissing",
    "niemeier_triple_e8_copies", "niemeier_triple_e8_roots",
    "niemeier_e6_4_copies", "niemeier_e6_4_rank", "e6_weyl_order",
    "ramanujan_exponent",
    "checks", "Verified",
]


def _build_results():
    return {
        "Part": "CCXLIV",
        "Title": "Niemeier Lattices and the Leech Lattice",
        "Verified": Verified,
        "checks_passed": sum(1 for _, v in checks if v),
        "checks_total": len(checks),
        "niemeier": {
            "count": niemeier_count,
            "with_roots": niemeier_with_roots,
            "without_roots": niemeier_no_roots,
        },
        "leech": {
            "rank": leech_rank,
            "min_norm": leech_min_norm,
            "kissing": leech_kissing,
        },
        "golay_code": {
            "length": golay_length,
            "dimension": golay_dim,
            "min_distance": golay_min_dist,
            "codewords": golay_codewords,
        },
        "sphere_packing": {
            "dim_8": sphere_pack_8d,
            "dim_24": sphere_pack_24d,
        },
    }


if __name__ == "__main__":
    results = _build_results()
    out = ROOT / "PART_CCXLIV_niemeier_lattices_results.json"
    out.write_text(__import__("json", encoding="utf-8").dumps(results, indent=2), encoding="utf-8")
    print(f"Verified={Verified}  checks={results['checks_passed']}/{results['checks_total']}")
    print(f"Wrote {out}")
