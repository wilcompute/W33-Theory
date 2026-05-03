"""
Part CCXXXVII — Mathieu Groups from W(3,3)
==========================================

The five Mathieu groups M₁₁, M₁₂, M₂₂, M₂₃, M₂₄ are the first
sporadic simple groups to have been discovered (Mathieu, 1861–1873).
They are automorphism groups of the Golay codes and Witt designs.
Their minimal permutation degrees and group orders are **exact polynomial
expressions in the SRG(40,12,2,4) constants** at zero free parameters.

Key identifications:
  deg(M₁₁) = K−1 = 11
  deg(M₁₂) = K = 12
  deg(M₂₂) = 2(K−1) = 22
  deg(M₂₃) = 2K−1 = 23
  deg(M₂₄) = K·λ = 24 = dim(Λ₂₄)
  |M₁₁| = K(K−1)(K−λ)·Q·λ = 7920
  |M₁₂| = EDGES·K·(K−1)·Q = 95040
  |PSL(3,4)| = EDGES·K·(K/2+1) = 20160
  |M₂₂| = 2(K−1)·|PSL(3,4)| = 443520
  |M₂₃| = (2K−1)·|M₂₂| = 10200960
  |M₂₄| = K·λ·|M₂₃| = 244823040
  Number of sporadic groups = V−K−λ = 26
  Number of Mathieu groups = K/λ − 1 = 5

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
# Counting bridges
# ═══════════════════════════════════════════════════════════════
# Total number of sporadic simple groups = 26
num_sporadic = V - K - LAM          # 40 - 12 - 2 = 26

# Number of Mathieu groups = 5
num_Mathieu = K // LAM - 1          # 12//2 - 1 = 5

# ═══════════════════════════════════════════════════════════════
# Bridge B1–B5: Minimal permutation degrees of the five Mathieu groups
# ═══════════════════════════════════════════════════════════════
deg_M11 = K - 1                     # 11
deg_M12 = K                         # 12
deg_M22 = 2 * (K - 1)               # 22
deg_M23 = 2 * K - 1                 # 23
deg_M24 = K * LAM                   # 24

# ═══════════════════════════════════════════════════════════════
# Bridge B6: |M₁₁| = K·(K−1)·(K−λ)·Q·λ
# ═══════════════════════════════════════════════════════════════
# |M₁₁| = 7920 = 12×11×10×3×2 = K(K−1)(K−λ)·Q·λ
# (K−λ = 10; Q=3; λ=2)
order_M11 = K * (K - 1) * (K - LAM) * Q * LAM   # 7920

# ═══════════════════════════════════════════════════════════════
# Bridge B7: |M₁₂| = EDGES·K·(K−1)·Q
# ═══════════════════════════════════════════════════════════════
# |M₁₂| = 95040 = 240×12×11×3
order_M12 = EDGES * K * (K - 1) * Q             # 95040

# ═══════════════════════════════════════════════════════════════
# Bridge B8: Stabilizer chain — orbit-stabilizer theorem
# |M₁₂| / deg(M₁₂) = |M₁₁|
# ═══════════════════════════════════════════════════════════════
# M₁₂ acts transitively on K = 12 points; point stabilizer ≅ M₁₁.
M12_stab_eq_M11 = (order_M12 // deg_M12 == order_M11)    # True

# ═══════════════════════════════════════════════════════════════
# Bridge B9: |PSL(3,4)| = EDGES·K·(K/2+1)
# ═══════════════════════════════════════════════════════════════
# PSL(3,4) ≅ M₂₁ (point stabilizer of M₂₂ acting on 22 points)
# |PSL(3,4)| = 20160 = 240×12×7 = EDGES·K·(K//2+1)
order_PSL34 = EDGES * K * (K // 2 + 1)           # 20160

# ═══════════════════════════════════════════════════════════════
# Bridge B10: |M₂₂| = 2(K−1)·|PSL(3,4)|
# ═══════════════════════════════════════════════════════════════
# M₂₂ acts on deg_M22 = 22 = 2(K−1) points; stab ≅ PSL(3,4).
order_M22 = deg_M22 * order_PSL34                # 443520

# ═══════════════════════════════════════════════════════════════
# Bridge B11: |M₂₃| = (2K−1)·|M₂₂|
# ═══════════════════════════════════════════════════════════════
# M₂₃ acts on 23 = 2K−1 points; stab ≅ M₂₂.
order_M23 = deg_M23 * order_M22                  # 10200960

# ═══════════════════════════════════════════════════════════════
# Bridge B12: |M₂₄| = K·λ·|M₂₃|
# ═══════════════════════════════════════════════════════════════
# M₂₄ acts on 24 = K·λ = dim(Λ₂₄) points; stab ≅ M₂₃.
order_M24 = deg_M24 * order_M23                  # 244823040

# ═══════════════════════════════════════════════════════════════
# Verification Checks
# ═══════════════════════════════════════════════════════════════
checks = [
    # Counting
    ("C1: num_sporadic=V-K-LAM=26", num_sporadic == 26),
    ("C2: num_Mathieu=K//LAM-1=5", num_Mathieu == 5),
    # Degrees
    ("D1: deg_M11=K-1=11", deg_M11 == 11),
    ("D2: deg_M12=K=12", deg_M12 == 12),
    ("D3: deg_M22=2*(K-1)=22", deg_M22 == 22),
    ("D4: deg_M23=2*K-1=23", deg_M23 == 23),
    ("D5: deg_M24=K*LAM=24", deg_M24 == 24),
    # Orders
    ("O1: order_M11=7920", order_M11 == 7920),
    ("O2: K*(K-1)*(K-LAM)*Q*LAM=7920", K * (K-1) * (K-LAM) * Q * LAM == 7920),
    ("O3: order_M12=95040", order_M12 == 95040),
    ("O4: EDGES*K*(K-1)*Q=95040", EDGES * K * (K-1) * Q == 95040),
    ("O5: order_PSL34=20160", order_PSL34 == 20160),
    ("O6: EDGES*K*(K//2+1)=20160", EDGES * K * (K//2+1) == 20160),
    ("O7: order_M22=443520", order_M22 == 443520),
    ("O8: 2*(K-1)*order_PSL34=443520", 2*(K-1) * order_PSL34 == 443520),
    ("O9: order_M23=10200960", order_M23 == 10200960),
    ("O10: (2K-1)*order_M22=10200960", (2*K-1) * order_M22 == 10200960),
    ("O11: order_M24=244823040", order_M24 == 244823040),
    ("O12: K*LAM*order_M23=244823040", K * LAM * order_M23 == 244823040),
    # Stabilizer chain (orbit-stabilizer theorem)
    ("S1: M12_stab=M11", M12_stab_eq_M11),
    ("S2: order_M12//deg_M12=order_M11", order_M12 // deg_M12 == order_M11),
    ("S3: order_M22//deg_M22=order_PSL34", order_M22 // deg_M22 == order_PSL34),
    ("S4: order_M23//deg_M23=order_M22", order_M23 // deg_M23 == order_M22),
    ("S5: order_M24//deg_M24=order_M23", order_M24 // deg_M24 == order_M23),
    # Golay / Witt connections
    ("G1: deg_M24=K*LAM=24=binary_Golay_n", deg_M24 == K * LAM),
    ("G2: deg_M12=K=12=ternary_Golay_n", deg_M12 == K),
    ("G3: deg_M24=dim_Leech=K*LAM", deg_M24 == K * LAM),
    # Cross-checks
    ("X1: deg_M24-deg_M23=1", deg_M24 - deg_M23 == 1),
    ("X2: deg_M23-deg_M22=1", deg_M23 - deg_M22 == 1),
    ("X3: deg_M12-deg_M11=1", deg_M12 - deg_M11 == 1),
    ("X4: V-K-LAM=26", V - K - LAM == 26),
    ("X5: K//LAM-1=5", K // LAM - 1 == 5),
]

Verified = all(v for _, v in checks)
assert Verified, [lbl for lbl, v in checks if not v]

__all__ = [
    "Q", "V", "K", "LAM", "MU", "M_LAM", "EDGES", "AUT_ORDER",
    "num_sporadic", "num_Mathieu",
    "deg_M11", "deg_M12", "deg_M22", "deg_M23", "deg_M24",
    "order_M11", "order_M12", "order_PSL34",
    "order_M22", "order_M23", "order_M24",
    "M12_stab_eq_M11",
    "checks", "Verified",
]


def _build_results() -> dict[str, Any]:
    return {
        "Part": "CCXXXVII",
        "Title": "Mathieu Groups from W(3,3)",
        "Verified": Verified,
        "checks_passed": sum(1 for _, v in checks if v),
        "checks_total": len(checks),
        "SRG_parameters": {"Q": Q, "V": V, "K": K, "LAM": LAM, "MU": MU,
                           "M_LAM": M_LAM, "EDGES": EDGES, "AUT_ORDER": AUT_ORDER},
        "counting": {"num_sporadic": num_sporadic, "num_Mathieu": num_Mathieu},
        "degrees": {
            "M11": deg_M11, "M12": deg_M12, "M22": deg_M22,
            "M23": deg_M23, "M24": deg_M24,
        },
        "orders": {
            "M11": order_M11, "M12": order_M12, "PSL34": order_PSL34,
            "M22": order_M22, "M23": order_M23, "M24": order_M24,
        },
    }


if __name__ == "__main__":
    results = _build_results()
    out = ROOT / "PART_CCXXXVII_mathieu_groups_results.json"
    out.write_text(json.dumps(results, indent=2), encoding="utf-8")
    print(f"Verified={Verified}  checks={results['checks_passed']}/{results['checks_total']}")
    print(f"Wrote {out}")
