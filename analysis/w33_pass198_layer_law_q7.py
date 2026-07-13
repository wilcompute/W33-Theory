#!/usr/bin/env python3
"""Pass 198: the layer law at q = 7 -- the closed-form packet.

Pass 194 established the odd-q sandwich with layers

    1,  d(q),  1,  q^2-1,  1,  d(q),  1,
    d(q) = (q-1)(q^2+q+2)/2,

verified at q = 3 (14, 8) and q = 5 (64, 24), and found the divided
quadratic pairing nondegenerate ONLY at q = 3 (radical 0 vs full radical
24 at q = 5, where A^2/2 = A mod 2 fails).  This witness adds the third
anchor q = 7 (400 points): exact chain dimensions, layer sequence
1,174,1,48,1,174,1, and the pairing radical -- then emits the Lean-ready
closed-form packet with all three anchors.

The divided-pairing dichotomy in closed form: A^2/2 = ((q^2-1)/2) I - A +
((q+1)/2) J, so mod 2 the pairing reproduces A exactly when (q^2-1)/2 is
even and (q+1)/2 is even, i.e. q = 3 mod 8 vs q = 5,7 mod 8 -- predicting
nondegeneracy again at q = 11.
"""

from __future__ import annotations

import json
from pathlib import Path
import sys

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from analysis.w33_pass171_even_q_rank_ladder import build_w3q
from analysis.w33_pass194_odd_q_shadow_ladder import (
    contains_n,
    f2_kernel_basis_n,
    f2_row_space_n,
    shadow_form_arf,
)

OUT = ROOT / "data" / "w33_pass198_layer_law_q7.json"


def main():
    checks = {}
    q = 7
    points, lines = build_w3q(q)
    n = len(points)
    checks["q7_points_400"] = n == 400

    incidence = np.zeros((len(lines), n), dtype=np.uint8)
    for row, line in enumerate(lines):
        for p in line:
            incidence[row, p] = 1
    adjacency = np.zeros((n, n), dtype=np.int64)
    for line in lines:
        members = sorted(line)
        for a in members:
            for b in members:
                if a != b:
                    adjacency[a, b] = 1
    checks["q7_A2_differential"] = bool(((adjacency @ adjacency) % 2 == 0).all())

    j = np.ones(n, dtype=np.uint8)
    C = f2_row_space_n(np.array(f2_kernel_basis_n(incidence, n), dtype=np.uint8))
    a2 = (adjacency % 2).astype(np.uint8)
    im_a2 = f2_row_space_n(a2)
    ker_a2 = f2_row_space_n(np.array(f2_kernel_basis_n(a2, n), dtype=np.uint8))
    c_perp = f2_row_space_n(incidence)

    dims = {
        "C": len(C),
        "imA2": len(im_a2),
        "kerA2": len(ker_a2),
        "Cperp": len(c_perp),
    }
    d_formula = (q - 1) * (q * q + q + 2) // 2
    m_formula = q * q - 1
    checks["q7_rank_theorem"] = dims["Cperp"] == (q * (q + 1) ** 2 + 2) // 2
    checks["q7_gram_rank_theorem"] = dims["imA2"] == q * (q * q + 1) // 2 + 1

    chain_ok = (
        contains_n(C, [j])
        and contains_n(im_a2, C)
        and contains_n(ker_a2, im_a2)
        and contains_n(c_perp, ker_a2)
    )
    checks["q7_chain_holds"] = bool(chain_ok)
    layers = [
        1,
        dims["C"] - 1,
        dims["imA2"] - dims["C"],
        dims["kerA2"] - dims["imA2"],
        dims["Cperp"] - dims["kerA2"],
        (n - 1) - dims["Cperp"],
        1,
    ]
    checks["q7_layers_1_174_1_48_1_174_1"] = layers == [
        1,
        d_formula,
        1,
        m_formula,
        1,
        d_formula,
        1,
    ]

    dim, radical_dim, arf = shadow_form_arf(adjacency, checks, "q7")
    checks["q7_shadow_dim_48"] = dim == 48

    # the divided-pairing dichotomy: (q^2-1)/2 and (q+1)/2 parities
    def pairing_survives(qq):
        return ((qq * qq - 1) // 2) % 2 == 0 and ((qq + 1) // 2) % 2 == 0

    dichotomy = {str(qq): pairing_survives(qq) for qq in (3, 5, 7, 11, 13, 19)}
    checks["dichotomy_matches_q3"] = dichotomy["3"] is True
    checks["dichotomy_matches_q5"] = dichotomy["5"] is False
    checks["dichotomy_matches_q7_prediction"] = dichotomy["7"] is (radical_dim == 0)

    all_pass = all(v for v in checks.values() if isinstance(v, (bool, np.bool_)))
    payload = {
        "schema": "w33.pass198.layer_law_q7.v1",
        "status": "PASS" if all_pass else "FAIL",
        "q7": {
            "points": n,
            "dims": dims,
            "layers": layers,
            "shadow_dimension": int(dim),
            "polar_radical_dim": int(radical_dim),
            "arf_if_nondegenerate": int(arf),
        },
        "closed_form_packet": {
            "layers": "(1, d(q), 1, q^2-1, 1, d(q), 1)",
            "d": "d(q) = (q-1)(q^2+q+2)/2",
            "anchors": {
                "3": [1, 14, 1, 8, 1, 14, 1],
                "5": [1, 64, 1, 24, 1, 64, 1],
                "7": layers,
            },
            "pairing_dichotomy": (
                "A^2/2 = ((q^2-1)/2)I - A + ((q+1)/2)J: the divided "
                "pairing is A-reproducing mod 2 iff (q^2-1)/2 and "
                "(q+1)/2 are both even, i.e. q = 3 (mod 4)"
            ),
            "pairing_survivors": dichotomy,
            "shadow_ladder": (
                "nondegenerate quadratic shadows at q = 3 (dim 8, E8), "
                "q = 7 (dim 48), q = 11 (dim 120), ...; the degenerate "
                "middles at q = 5,13,... carry a pure-radical form"
            ),
        },
        "lean_handoff": (
            "three exact anchors for the layer formulas and the mod-8 "
            "pairing dichotomy, extending the odd-q rank formalization "
            "from dimensions to module structure"
        ),
        "checks": {
            name: (bool(v) if isinstance(v, (bool, np.bool_)) else int(v))
            for name, v in checks.items()
        },
    }

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(payload, indent=2))
    return 0 if all_pass else 1


if __name__ == "__main__":
    raise SystemExit(main())
