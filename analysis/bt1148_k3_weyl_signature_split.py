#!/usr/bin/env python3
"""BT1148 -- K3 Weyl basket split from chi and signature.

In the corpus convention used by BT1138--BT1145,

  A4_corpus = W_total_norm = chi(K3) = 24.

The four-dimensional signature theorem fixes the normalized chiral difference by

  W_plus_norm - W_minus_norm = (3/2) tau.

For K3, tau=-16, so the chiral difference is -24.  Therefore, in this
orientation, W_plus_norm=0 and W_minus_norm=24.  Reversing orientation swaps the
roles.  This fixes the integrated Weyl-squared basket on Ricci-flat K3, but not a
pointwise Weyl density or a non-Ricci-flat deformation.
"""

from __future__ import annotations

import json
from fractions import Fraction

chi = 24
tau = -16
w_total = Fraction(chi, 1)
w_diff = Fraction(3, 2) * tau
w_plus = (w_total + w_diff) / 2
w_minus = (w_total - w_diff) / 2

N = 440
F4_half = 8160
C4_total = N * w_total + F4_half
C4_plus = N * w_plus
C4_minus = N * w_minus

payload = {
    "bt": 1148,
    "title": "K3 Weyl basket signature split",
    "inputs": {"chi": chi, "tau": tau, "A4_corpus": str(w_total)},
    "signature_relation": "W_plus_norm - W_minus_norm = (3/2)*tau",
    "weyl_split_orientation_tau_minus_16": {
        "W_total_norm": str(w_total),
        "W_difference_norm": str(w_diff),
        "W_plus_norm": str(w_plus),
        "W_minus_norm": str(w_minus),
    },
    "product_slots": {
        "C4_total_corpus": str(C4_total),
        "C4_plus_part_without_finite_constant": str(C4_plus),
        "C4_minus_part_without_finite_constant": str(C4_minus),
        "finite_constant_TrDF4_over_2": F4_half,
    },
    "interpretation": {
        "fixed": "integrated Weyl-squared basket on Ricci-flat K3",
        "not_fixed": "pointwise Weyl density or non-Ricci-flat Weyl^2 deformation",
        "orientation_reversal": "swaps W_plus_norm and W_minus_norm",
    },
    "checks": {
        "total_is_24": w_total == 24,
        "difference_is_minus_24": w_diff == -24,
        "plus_is_zero": w_plus == 0,
        "minus_is_24": w_minus == 24,
        "C4_total_is_18720": C4_total == 18720,
    },
}
payload["checks"]["all_checks_pass"] = all(payload["checks"].values())
print(json.dumps(payload, indent=2, sort_keys=True))
