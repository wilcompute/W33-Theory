#!/usr/bin/env python3
"""Pass 180: the route-dark lattice is the Q(4,3) trade lattice.

The parallel track's Pass 173/174 charted L_route = ker_Z(N^T) as the
"route-dark pentad lattice".  This witness fuses it into the trade tower:

1. THE IDENTIFICATION.  L_route is tautologically the trade lattice of
   the DUAL generalized quadrangle Q(4,3) (points = W(3,3) lines).  An
   exact span census records the classical boundary: W(3,3) has span
   size 4 and Q(4,3) has span size 2.  This is a regular/antiregular
   correlation with the 90-vs-432 shells, not a proof that regularity
   alone causes or determines those lattice minima.

2. THE MOD-8 CROSS-CHECK.  The Milgram signature, per-prime Gauss phases,
   and the value 11/8 on one selected Smith Z/8 generator.  Pass 174
   proves that this value is not generator-invariant: fixed generators
   split between 11/8 and 3/8.  Therefore it is an existence statement,
   not a new law or invariant of incidence duality.

3. REGRESSION CROSS-CHECKS of Pass 173's stronger PARI-certified
   invariants: det = 2^11 3^14, minimum 10, 432 candidate minimal
   vectors, and the [40,15,10] code.
"""

from __future__ import annotations

from collections import Counter
from itertools import combinations
import json
import math
from pathlib import Path
import sys

import numpy as np
from sympy import Matrix, ZZ
from sympy.matrices.normalforms import smith_normal_form

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from analysis.w33_pass158_chiral_trade_lattice_two_480s import (
    build_w33,
    w33_lines,
)
from analysis.w33_pass160_trade_tower_gq42 import (
    generic_saturated_kernel,
    staged_minimal_shell,
)
from analysis.w33_pass162_mod8_anomaly_ledger import (
    eighth_root_index,
    p_adic_snf_generators,
    p_part_gauss_sum,
    p_valuation,
)

OUT = ROOT / "data" / "w33_pass180_dual_trade_lattice_q43.json"


def main():
    _, adjacency, _ = build_w33()
    lines = w33_lines(adjacency)
    checks = {}

    incidence = np.zeros((40, 40), dtype=np.int64)
    for row, line in enumerate(lines):
        for p in line:
            incidence[row, p] = 1

    # the dual geometry Q(4,3): points = W33 lines, adjacency = concurrence
    line_gram = incidence @ incidence.T
    dual_adjacency = (line_gram > 0).astype(np.int64) - np.eye(40, dtype=np.int64)

    # 1. regular vs antiregular
    def span_size(graph, a, b):
        perp = np.flatnonzero(graph[a] & graph[b])
        mask = np.ones(40, dtype=bool)
        for p in perp:
            mask &= graph[p].astype(bool)
        return int(mask.sum())

    w33_spans = {
        span_size(adjacency, a, b)
        for a, b in combinations(range(40), 2)
        if not adjacency[a, b]
    }
    dual_spans = {
        span_size(dual_adjacency, a, b)
        for a, b in combinations(range(40), 2)
        if not dual_adjacency[a, b]
    }
    checks["w33_points_regular_span_4"] = w33_spans == {4}
    checks["q43_points_antiregular_span_2"] = dual_spans == {2}

    # the route lattice = trade lattice of Q(4,3) = ker(N^T)
    route = generic_saturated_kernel(incidence.T)
    checks["route_rank_15"] = route.shape == (40, 15)
    gram = np.array(route.T @ route, dtype=np.int64)
    smith = smith_normal_form(Matrix(gram.tolist()), domain=ZZ)
    invariants = [abs(int(smith[i, i])) for i in range(15)]
    determinant = 1
    for v in invariants:
        determinant *= max(v, 1)
    checks["route_det_2_11_3_14"] = determinant == 2**11 * 3**14
    checks["route_even"] = bool(all(int(gram[i, i]) % 2 == 0 for i in range(15)))
    checks["route_smith_profile"] = sorted(
        Counter(v for v in invariants if v > 1).items()
    ) == [(3, 5), (6, 8), (24, 1)]

    min_norm, shell = staged_minimal_shell(route, bounds=(4, 6, 8, 10, 12))
    checks["route_min_norm_10"] = min_norm == 10
    checks["route_shell_432"] = len(shell) == 432
    supports432 = {frozenset(np.flatnonzero(np.asarray(v)).tolist()) for v in shell}
    checks["route_projective_minima_216"] = len(supports432) == 216

    # the F2 route code
    basis2 = (route % 2).astype(np.uint8).T
    coeffs = np.array(
        [[(m >> b) & 1 for b in range(15)] for m in range(2**15)],
        dtype=np.uint8,
    )
    words = (coeffs @ basis2) % 2
    weights = words.sum(axis=1)
    enum = Counter(int(w) for w in weights)
    checks["route_code_min_distance_10"] = (
        min(w for w in enum if w > 0) == 10 and enum[10] == 216
    )

    # 2. the mod-8 row for the law table
    total = 1.0 + 0.0j
    total_size = 1
    p_phases = {}
    z8_q = None
    for prime in (2, 3):
        val = p_valuation(determinant, prime, 64)
        generators, dual_ok = p_adic_snf_generators(gram, prime, val)
        checks[f"route_p{prime}_dual_certificate"] = bool(dual_ok)
        size, gauss, _, distinct = p_part_gauss_sum(gram, generators, prime)
        checks[f"route_p{prime}_distinct"] = bool(distinct)
        checks[f"route_p{prime}_size"] = size == prime**val
        index, residual = eighth_root_index(gauss / math.sqrt(size))
        checks[f"route_p{prime}_eighth_root"] = residual < 1e-6
        p_phases[str(prime)] = index
        total *= gauss / math.sqrt(size)
        total_size *= size
        if prime == 2:
            for order, column in generators:
                if order == 8:
                    reduced = np.array([int(v) % 8 for v in column], dtype=np.int64)
                    z8_q = int(reduced @ gram @ reduced) % 128
    index, residual = eighth_root_index(total)
    checks["route_milgram_signature_7"] = residual < 1e-6 and index == 15 % 8
    checks["route_discriminant_complete"] = total_size == determinant
    checks["route_has_z8_block"] = z8_q is not None

    q_fraction = None
    law_holds = None
    if z8_q is not None:
        g = math.gcd(z8_q, 64) or 1
        q_fraction = f"{z8_q // g}/{64 // g}"
        law_holds = (z8_q // g) == 11 and (64 // g) == 8
    checks["selected_z8_generator_has_q_11_over_8"] = law_holds is True

    all_pass = all(checks.values())
    payload = {
        "schema": "w33.pass180.dual_trade_lattice_q43.v2",
        "status": "PASS" if all_pass else "FAIL",
        "identification": {
            "statement": (
                "L_route = ker_Z(N^T) is the trade lattice of the dual "
                "quadrangle Q(4,3). W(3,3) and Q(4,3) are a nonisomorphic "
                "dual pair, not an incidence-self-dual geometry"
            ),
            "w33_span_sizes": sorted(w33_spans),
            "q43_span_sizes": sorted(dual_spans),
            "boundary": (
                "the exact 4-versus-2 span census records the regular versus "
                "antiregular distinction; it does not by itself derive the "
                "90-versus-432 lattice-shell dichotomy"
            ),
        },
        "mod8_row": {
            "rank": 15,
            "signature_mod_8": 7,
            "determinant": determinant,
            "p_phases_eighths": p_phases,
            "selected_smith_z8_generator_q_value": q_fraction,
            "selected_generator_has_q_11_over_8": law_holds,
            "fixed_generator_values_from_pass174": ["11/8", "3/8"],
            "reading": (
                "one selected Smith generator has q=11/8, while Pass 174 "
                "proves that the fixed order-eight generators split equally "
                "between q=11/8 and q=3/8; 11/8 exists but is not canonical"
            ),
        },
        "scope": (
            "the determinant, Smith form, minimum census, and code repeat "
            "Pass 173; the new exact content here is the dual-geometry naming "
            "and the span-size 4-versus-2 census"
        ),
        "route_code_weight_enumerator": {
            str(k): int(v) for k, v in sorted(enum.items())
        },
        "checks": {name: bool(value) for name, value in checks.items()},
    }

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(payload, indent=2))
    return 0 if all_pass else 1


if __name__ == "__main__":
    raise SystemExit(main())
