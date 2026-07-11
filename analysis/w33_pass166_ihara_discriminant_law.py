#!/usr/bin/env python3
"""Pass 166: the 11-law tested -- 2-adic discriminant data vs Ihara primes.

Pass 162 found the chiral trade lattice's unique Z/8 block evaluates to
q(h) = 11/8: the Ihara prime of W(3,3) over eight.  Is that a law of GQ
trade lattices or a W(3,3) miracle?  This witness computes, for the trade
lattices of the three quadrangles in the tower --

  W(2,2)   (doily,   k = 6,  Ihara prime  5, trade rank  5),
  W(3,3)   (chiral,  k = 12, Ihara prime 11, trade rank 15),
  GQ(4,2)  (support, k = 12, Ihara prime 11, trade rank 24),

-- the full Smith data, the 2-adic Jordan generator q-values as exact
fractions, the Milgram signature (verified by exact Gauss sums), and the
verdict on the candidate law "the deepest 2-adic block's q-numerator is
the Ihara prime".  Whatever the verdict, the three-lattice discriminant
table is a new exact tower invariant.
"""

from __future__ import annotations

from collections import Counter
from itertools import combinations, product
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
    saturated_kernel,
    w33_lines,
)
from analysis.w33_pass160_trade_tower_gq42 import generic_saturated_kernel
from analysis.w33_pass161_gq42_ihara_inheritance import support_graph
from analysis.w33_pass162_mod8_anomaly_ledger import (
    eighth_root_index,
    p_adic_snf_generators,
    p_part_gauss_sum,
    p_valuation,
)
from analysis.w33_pass165_doily_trade_fusion import build_doily

OUT = ROOT / "data" / "w33_pass166_ihara_discriminant_law.json"


def incidence_matrix(lines, n_points):
    matrix = np.zeros((len(lines), n_points), dtype=np.int64)
    for row, line in enumerate(lines):
        for p in line:
            matrix[row, p] = 1
    return matrix


def gq42_incidence():
    _, adjacency, _ = build_w33()
    supports, graph = support_graph(adjacency)
    lines45 = set()
    for a, b in combinations(range(45), 2):
        if not graph[a, b]:
            continue
        common = np.flatnonzero(graph[a] & graph[b])
        candidate = frozenset({a, b} | {int(c) for c in common})
        if len(candidate) == 5 and all(
            graph[x, y] for x, y in combinations(sorted(candidate), 2)
        ):
            lines45.add(candidate)
    return incidence_matrix(sorted(lines45, key=sorted), 45)


def analyze(name, gram, degree, checks):
    gram = np.array(gram, dtype=np.int64)
    rank = gram.shape[0]
    smith = smith_normal_form(Matrix(gram.tolist()), domain=ZZ)
    invariants = [abs(int(smith[i, i])) for i in range(rank)]
    determinant = 1
    for v in invariants:
        determinant *= max(v, 1)
    even = bool(all(int(gram[i, i]) % 2 == 0 for i in range(rank)))
    checks[f"{name}_even"] = even

    ihara_prime = degree - 1

    # 2-adic Jordan generator q-values as exact fractions num / 2^{2a}
    det_val2 = p_valuation(determinant, 2, 64)
    q_values = []
    deepest = 0
    deepest_q = None
    if det_val2:
        generators, dual_ok = p_adic_snf_generators(gram, 2, det_val2)
        checks[f"{name}_2adic_dual_certificate"] = bool(dual_ok)
        for order, column in generators:
            a = p_valuation(order, 2, 64)
            reduced = np.array([int(v) % order for v in column], dtype=np.int64)
            numerator = int(reduced @ gram @ reduced) % (2 * order * order)
            q_values.append({"order": int(order), "q": f"{numerator}/{order * order}"})
            if a > deepest:
                deepest = a
                g = math.gcd(numerator, order * order) or 1
                deepest_q = (numerator // g, (order * order) // g)
        size, gauss, _, distinct = p_part_gauss_sum(gram, generators, 2)
        checks[f"{name}_2adic_distinct"] = bool(distinct)
        index2, residual2 = eighth_root_index(gauss / math.sqrt(size))
        checks[f"{name}_2adic_gauss_eighth_root"] = residual2 < 1e-6
    else:
        index2 = 0

    # full Milgram signature over all primes
    total = 1.0 + 0.0j
    total_size = 1
    for prime in (2, 3, 5):
        val = p_valuation(determinant, prime, 64)
        if not val:
            continue
        generators, _ = p_adic_snf_generators(gram, prime, val)
        size, gauss, _, distinct = p_part_gauss_sum(gram, generators, prime)
        checks[f"{name}_p{prime}_distinct"] = bool(distinct)
        total *= gauss / math.sqrt(size)
        total_size *= size
    index, residual = eighth_root_index(total)
    checks[f"{name}_milgram_matches_rank"] = residual < 1e-6 and index == rank % 8
    checks[f"{name}_discriminant_complete"] = total_size == determinant

    law_holds = bool(deepest_q and deepest_q[0] == ihara_prime)
    return {
        "rank": rank,
        "degree": degree,
        "ihara_prime": ihara_prime,
        "determinant": determinant,
        "smith_profile": {
            str(k): int(v)
            for k, v in sorted(Counter(v for v in invariants if v > 1).items())
        },
        "even": even,
        "signature_mod_8": rank % 8,
        "two_adic_phase_eighths": int(index2),
        "two_adic_q_values": q_values,
        "deepest_2adic_depth": int(deepest),
        "deepest_q_value": (f"{deepest_q[0]}/{deepest_q[1]}" if deepest_q else None),
        "law_q_numerator_equals_ihara_prime": law_holds,
    }


def main():
    checks = {}

    # doily
    points2, adjacency2, lines2 = build_doily()
    incidence2 = incidence_matrix(lines2, 15)
    trade2 = generic_saturated_kernel(incidence2)
    checks["doily_trade_rank_5"] = trade2.shape == (15, 5)

    # W(3,3) chiral
    _, adjacency3, _ = build_w33()
    lines3 = w33_lines(adjacency3)
    incidence3 = incidence_matrix(lines3, 40)
    trade3 = generic_saturated_kernel(incidence3)
    checks["w33_trade_rank_15"] = trade3.shape == (40, 15)

    # GQ(4,2)
    incidence4 = gq42_incidence()
    trade4 = generic_saturated_kernel(incidence4)
    checks["gq42_trade_rank_24"] = trade4.shape == (45, 24)

    reports = {
        "doily_W22": analyze("doily", trade2.T @ trade2, 6, checks),
        "chiral_W33": analyze("w33", trade3.T @ trade3, 12, checks),
        "support_GQ42": analyze("gq42", trade4.T @ trade4, 12, checks),
    }

    checks["w33_law_holds_11_over_8"] = (
        reports["chiral_W33"]["deepest_q_value"] == "11/8"
        and reports["chiral_W33"]["law_q_numerator_equals_ihara_prime"]
    )
    checks["law_verdict_recorded"] = True

    law_table = {
        name: {
            "ihara_prime": r["ihara_prime"],
            "deepest_2adic_depth": r["deepest_2adic_depth"],
            "deepest_q_value": r["deepest_q_value"],
            "law_holds": r["law_q_numerator_equals_ihara_prime"],
        }
        for name, r in reports.items()
    }

    all_pass = all(checks.values())
    payload = {
        "schema": "w33.pass166.ihara_discriminant_law.v1",
        "status": "PASS" if all_pass else "FAIL",
        "sectors": reports,
        "law_table": law_table,
        "reading": (
            "the candidate law: the deepest 2-adic Jordan block of a GQ "
            "trade lattice evaluates to (Ihara prime)/2^depth. The table "
            "records where it holds; the three-lattice discriminant "
            "ledger is exact regardless."
        ),
        "checks": {name: bool(value) for name, value in checks.items()},
    }

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(payload, indent=2))
    return 0 if all_pass else 1


if __name__ == "__main__":
    raise SystemExit(main())
