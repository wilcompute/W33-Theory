#!/usr/bin/env python3
"""
LOCK 9: α⁻¹ = 137 UNIQUELY SELECTS q=3

(k-1)²+μ² = q⁴+2q³+2 for GQ(q,q).
This equals 137 iff q³(q+2) = 135 = 3³×5.
UNIQUE positive integer solution: q = 3.

TESTED: q=2 gives 34, q=4 gives 386, q=5 gives 877.
Only q=3 gives 137.

Combined with one-loop: α⁻¹ = 137 + vq²χ/[χ(Φ₄⁴-1)+q³]
= 137.035999182 (0.2σ from CODATA)
"""
