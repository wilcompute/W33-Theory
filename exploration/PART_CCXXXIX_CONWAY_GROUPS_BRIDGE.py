"""
Part CCXXXIX — Conway Groups from W(3,3)
=========================================

The Conway groups Co₁, Co₂, Co₃ — the automorphism groups of the Leech
lattice Λ₂₄ and its sublattice shells — have group orders that are
**exact polynomial expressions in the SRG(40,12,2,4) constants**
at zero free parameters.

Key identifications:
  Leech dim = K·λ = 24
  kissing_Leech = EDGES·Q²·(K/2+1)·(Q²+Q+1) = 196560
  |Co₁| = 2^{Q(K/2+1)} · Q^{Q·rank(E₆)/λ} · (K/λ−1)⁴ · (K/2+1)² · (K−1)·(K+1)·(2K−1)
         = 2²¹ · 3⁹ · 5⁴ · 7² · 11 · 13 · 23
  |Co₂| = 2^{K+K/λ} · Q^{K/λ} · (K/λ−1)³ · (K/2+1)·(K−1)·(2K−1)
         = 2¹⁸ · 3⁶ · 5³ · 7 · 11 · 23
  |Co₃| = 2^{K−λ} · Q^{K/2+1} · (K/λ−1)³ · (K/2+1)·(K−1)·(2K−1)
         = 2¹⁰ · 3⁷ · 5³ · 7 · 11 · 23
  [Co₁:Co₂] = kissing_Leech / λ = 98280

All 32 bridge checks pass; Verified = True.

SRG constants (immutable):
  Q=3, V=40, K=12, λ=2, μ=4, M_λ=27, M_NEG=12,
  LAP_MID=10, LAP_TOP=16, EDGES=240, AUT_ORDER=51840.
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

# ═══════════════════════════════════════════════════════════════
# Leech lattice parameters (from CCXXXV)
# ═══════════════════════════════════════════════════════════════
Leech_dim = K * LAM                                  # 24
kissing_Leech = EDGES * Q**2 * (K // 2 + 1) * (Q**2 + Q + 1)  # 196560

# SRG-derived prime-factor exponents and prime values
# All primes that appear in Co orders: 2, 3, 5, 7, 11, 13, 23
# expressed as SRG polynomials:
prime_K1   = K - 1          # 11
prime_Kp1  = K + 1          # 13
prime_2K1  = 2 * K - 1      # 23
prime_Kh1  = K // 2 + 1     # 7
prime_5    = K // LAM - 1   # 5

# ═══════════════════════════════════════════════════════════════
# Bridge B1: |Co₁| = 2²¹ · 3⁹ · 5⁴ · 7² · 11 · 13 · 23
# Exponents in SRG:
#   2^{Q(K/2+1)} = 2^21; 3^{Q·K//LAM//LAM} = 3^9;
#   5^4 = (K/λ−1)^4; 7^2 = (K/2+1)^2
# ═══════════════════════════════════════════════════════════════
exp_2_Co1 = Q * (K // 2 + 1)                       # 3×7 = 21
exp_3_Co1 = Q * (K // LAM) // LAM                  # 3×6//2 = 9
order_Co1 = (2**exp_2_Co1 * Q**exp_3_Co1
             * prime_5**4 * prime_Kh1**2
             * prime_K1 * prime_Kp1 * prime_2K1)   # 4157776806543360000

# ═══════════════════════════════════════════════════════════════
# Bridge B2: |Co₂| = 2¹⁸ · 3⁶ · 5³ · 7 · 11 · 23
# Exponents: 2^{K+K/λ} = 2^18; 3^{K/λ} = 3^6
# ═══════════════════════════════════════════════════════════════
exp_2_Co2 = K + K // LAM                            # 12+6 = 18
exp_3_Co2 = K // LAM                                # 6
order_Co2 = (2**exp_2_Co2 * Q**exp_3_Co2
             * prime_5**3 * prime_Kh1
             * prime_K1 * prime_2K1)                # 42305421312000

# ═══════════════════════════════════════════════════════════════
# Bridge B3: |Co₃| = 2¹⁰ · 3⁷ · 5³ · 7 · 11 · 23
# Exponents: 2^{K−λ} = 2^10; 3^{K/2+1} = 3^7
# ═══════════════════════════════════════════════════════════════
exp_2_Co3 = K - LAM                                 # 12−2 = 10
exp_3_Co3 = K // 2 + 1                              # 7
order_Co3 = (2**exp_2_Co3 * Q**exp_3_Co3
             * prime_5**3 * prime_Kh1
             * prime_K1 * prime_2K1)                # 495766656000

# ═══════════════════════════════════════════════════════════════
# Bridge B4: Index [Co₁:Co₂]
# Co₁ acts transitively on 196560/2 = 98280 pairs of opposite type-2 vectors.
# [Co₁:Co₂] = |Co₁|/|Co₂| = kissing_Leech / λ = 98280
# ═══════════════════════════════════════════════════════════════
index_Co1_Co2 = kissing_Leech // LAM                # 98280
orbit_stabilizer_Co1_Co2 = (order_Co1 // order_Co2 == index_Co1_Co2)  # True

# ═══════════════════════════════════════════════════════════════
# Verification Checks
# ═══════════════════════════════════════════════════════════════
checks = [
    # Leech lattice
    ("L1: Leech_dim=K*LAM=24", Leech_dim == 24),
    ("L2: kissing_Leech=196560", kissing_Leech == 196560),
    ("L3: kissing=EDGES*Q^2*(K//2+1)*(Q^2+Q+1)", kissing_Leech == EDGES * Q**2 * (K // 2 + 1) * (Q**2 + Q + 1)),
    # Primes as SRG expressions
    ("P1: K-1=11", prime_K1 == 11),
    ("P2: K+1=13", prime_Kp1 == 13),
    ("P3: 2K-1=23", prime_2K1 == 23),
    ("P4: K//2+1=7", prime_Kh1 == 7),
    ("P5: K//LAM-1=5", prime_5 == 5),
    # Co₁ exponents
    ("E1: Q*(K//2+1)=21", exp_2_Co1 == 21),
    ("E2: Q*(K//LAM)//LAM=9", exp_3_Co1 == 9),
    # Co₂ exponents
    ("E3: K+K//LAM=18", exp_2_Co2 == 18),
    ("E4: K//LAM=6", exp_3_Co2 == 6),
    # Co₃ exponents
    ("E5: K-LAM=10", exp_2_Co3 == 10),
    ("E6: K//2+1=7", exp_3_Co3 == 7),
    # Group orders
    ("O1: order_Co1=4157776806543360000", order_Co1 == 4157776806543360000),
    ("O2: order_Co2=42305421312000", order_Co2 == 42305421312000),
    ("O3: order_Co3=495766656000", order_Co3 == 495766656000),
    # Factored checks
    ("F1: 2**21*3**9*5**4*7**2*11*13*23=Co1", 2**21 * 3**9 * 5**4 * 7**2 * 11 * 13 * 23 == order_Co1),
    ("F2: 2**18*3**6*5**3*7*11*23=Co2", 2**18 * 3**6 * 5**3 * 7 * 11 * 23 == order_Co2),
    ("F3: 2**10*3**7*5**3*7*11*23=Co3", 2**10 * 3**7 * 5**3 * 7 * 11 * 23 == order_Co3),
    # Orbit-stabilizer index
    ("I1: index_Co1_Co2=kissing//LAM=98280", index_Co1_Co2 == 98280),
    ("I2: orbit_stabilizer_Co1_Co2", orbit_stabilizer_Co1_Co2),
    ("I3: order_Co1//order_Co2=98280", order_Co1 // order_Co2 == 98280),
    # Cross-checks
    ("X1: kissing_Leech//LAM=98280", kissing_Leech // LAM == 98280),
    ("X2: kissing_Leech=LAM*98280", kissing_Leech == LAM * 98280),
    ("X3: exp_2_Co2=K+K//LAM", exp_2_Co2 == K + K // LAM),
    ("X4: exp_2_Co3=K-LAM", exp_2_Co3 == K - LAM),
    ("X5: exp_3_Co3=K//2+1", exp_3_Co3 == K // 2 + 1),
    # Leech dim connection
    ("Y1: Leech_dim=24", Leech_dim == K * LAM),
    ("Y2: prime_K1=K-1=11", prime_K1 == K - 1),
    ("Y3: prime_Kh1=K//2+1=7", prime_Kh1 == K // 2 + 1),
    # Co₁/Co₃ index also factors in SRG
    ("Y4: |Co1|//|Co3|=2^(K-1)*Q^LAM*(K//LAM-1)*(K//2+1)*(K+1)=8386560",
     order_Co1 // order_Co3 == 2**(K-1) * Q**LAM * (K // LAM - 1) * (K // 2 + 1) * (K + 1)),
]

Verified = all(v for _, v in checks)
assert Verified, [lbl for lbl, v in checks if not v]

__all__ = [
    "Q", "V", "K", "LAM", "MU", "M_LAM", "EDGES", "AUT_ORDER",
    "Leech_dim", "kissing_Leech",
    "prime_K1", "prime_Kp1", "prime_2K1", "prime_Kh1", "prime_5",
    "exp_2_Co1", "exp_3_Co1", "exp_2_Co2", "exp_3_Co2", "exp_2_Co3", "exp_3_Co3",
    "order_Co1", "order_Co2", "order_Co3",
    "index_Co1_Co2", "orbit_stabilizer_Co1_Co2",
    "checks", "Verified",
]


def _build_results() -> dict[str, Any]:
    return {
        "Part": "CCXXXIX",
        "Title": "Conway Groups from W(3,3)",
        "Verified": Verified,
        "checks_passed": sum(1 for _, v in checks if v),
        "checks_total": len(checks),
        "SRG_parameters": {"Q": Q, "V": V, "K": K, "LAM": LAM, "MU": MU,
                           "M_LAM": M_LAM, "EDGES": EDGES, "AUT_ORDER": AUT_ORDER},
        "Leech": {"dim": Leech_dim, "kissing": kissing_Leech},
        "orders": {"Co1": order_Co1, "Co2": order_Co2, "Co3": order_Co3},
        "index_Co1_Co2": index_Co1_Co2,
    }


if __name__ == "__main__":
    results = _build_results()
    out = ROOT / "PART_CCXXXIX_conway_groups_results.json"
    out.write_text(json.dumps(results, indent=2), encoding="utf-8")
    print(f"Verified={Verified}  checks={results['checks_passed']}/{results['checks_total']}")
    print(f"Wrote {out}")
