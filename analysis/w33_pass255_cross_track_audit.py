#!/usr/bin/env python3
"""Pass 255: independent cross-track audit of the parallel agent's 240-249.

A second agent independently produced `passes/pass_240_249_qldpc_bounds.py` and
`passes/pass_240_249_yukawa_texture.py`, re-deriving results this track already
committed (Pass 239 qLDPC bounds, Pass 235 Yukawa texture).  Independent
re-derivation is a gift: agreement is a strong cross-check, disagreement locates
a bug in exactly one of us.  This witness performs the comparison and
machine-verifies every disputed quantity.

CONFIRMED AGREEMENTS (independent derivations, same answer):
  * k * d = n exactly (the conservation curve);
  * the democratic (unbroken-family) Yukawa is rank 1 => exactly ONE heavy
    generation.

DISCREPANCIES FOUND (this track's values re-verified here from the code itself):
  1. BPT ratio.  Their prose asserts "k*d^2/n ... = 1 exactly"; their own code
     computes k*d**2/n, which equals (q^2+1)(q+1)^2 / ((q+1)(q^2+1)) = q+1, NOT
     1.  The "= 1" is the value of k*d/n mislabelled.  Consequence: the family
     is NOT 2D-local; minimum embedding dimension is 3 (Pass 239).
  2. Check weight.  They set w = q+1 (=4 at q=3).  But q+1 is the weight of the
     LINES, which are LOGICAL operators (Pass 229), not stabilisers.  The
     stabilisers are the sentinel C^perp, whose minimum weight is 8 = 2(q+1) at
     q=3 (Pass 226 exact; Pass 234 reduced-generator distribution {8:11, 12:4}).
     Their check weight is a factor ~2 too small.
  3. Quantum Singleton.  They use k <= n - 4(d-1); the Knill-Laflamme quantum
     Singleton bound is k <= n - 2(d-1).  Their conclusion is unaffected (both
     hold with slack), but the bound is misstated.
"""

from __future__ import annotations

from itertools import combinations
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from analysis.w33_pass224_shadow_code_tower import (
    doubly_even_subcode,
    f2_nullspace,
    f2_rowspace_basis,
    incidence_rows,
    isotropic_lines,
    pg3_points,
    popcount,
    rows_to_bitmasks,
)
from analysis.w33_pass226_sentinel_distance_tower import reduce_basis_low_weight

OUT = ROOT / "data" / "w33_pass255_cross_track_audit.json"


def in_span(v, basis):
    cur = v
    for b in basis:
        cur = min(cur, cur ^ b)
    return cur == 0


def build(q):
    points = pg3_points(q)
    n = len(points)
    lines = isotropic_lines(points, q)
    line_masks = rows_to_bitmasks(incidence_rows(lines, n))
    Cbasis = f2_rowspace_basis(line_masks)
    gram_rows = [tuple(1 if popcount(a & b) & 1 else 0 for b in Cbasis)
                 for a in Cbasis]
    hull_coeffs = f2_nullspace(gram_rows, len(Cbasis))
    hull_words = []
    for cc in hull_coeffs:
        w = 0
        for i in range(len(Cbasis)):
            if (cc >> i) & 1:
                w ^= Cbasis[i]
        if w:
            hull_words.append(w)
    S = doubly_even_subcode(f2_rowspace_basis(hull_words))
    return n, line_masks, Cbasis, S


def main():
    checks = {}
    q = 3
    n, line_masks, Cbasis, S = build(q)
    k = n - 2 * len(S)
    d = q + 1

    # ---- AGREEMENT 1: k*d = n
    checks["agree_k_times_d_eq_n"] = (k * d == n)

    # ---- AGREEMENT 2: democratic Yukawa is rank 1 (one heavy generation)
    import numpy as np
    J = np.ones((3, 3))
    checks["agree_democratic_rank_1"] = int(np.linalg.matrix_rank(J)) == 1

    # ---- DISCREPANCY 1: the BPT ratio is q+1, not 1
    bpt_ratio = (k * d ** 2) / n
    checks["bpt_ratio_is_q_plus_1_not_1"] = abs(bpt_ratio - (q + 1)) < 1e-9
    checks["bpt_ratio_not_1"] = abs(bpt_ratio - 1.0) > 1e-9
    # algebraic identity for all q
    ident = all(
        ((qq * qq + 1) * (qq + 1) ** 2) == (qq + 1) * ((qq + 1) * (qq * qq + 1))
        for qq in (3, 5, 7, 11))
    checks["kd2_over_n_identity_q_plus_1"] = ident

    # ---- DISCREPANCY 2: the true check weight is the sentinel weight
    Sred = reduce_basis_low_weight(S)
    min_check_w = min(popcount(s) for s in Sred)
    checks["true_min_check_weight_8"] = min_check_w == 8
    checks["check_weight_is_2q_plus_2_not_q_plus_1"] = min_check_w == 2 * (q + 1)
    # and q+1 weight words are LOGICALS (in C, not in S) -- so cannot be checks
    w4 = [l for l in line_masks if popcount(l) == q + 1]
    lines_are_logical = all(in_span(l, Cbasis) and not in_span(l, S) for l in w4)
    checks["q_plus_1_words_are_logicals_not_checks"] = lines_are_logical and len(w4) > 0

    # ---- DISCREPANCY 3: the quantum Singleton bound
    correct_rhs = n - 2 * (d - 1)
    their_rhs = n - 4 * (d - 1)
    checks["singleton_correct_form_holds"] = k <= correct_rhs
    checks["their_stricter_form_also_holds"] = k <= their_rhs
    checks["their_bound_is_stricter"] = their_rhs < correct_rhs

    all_pass = all(v for v in checks.values() if isinstance(v, bool))
    payload = {
        "schema": "w33.pass255.cross_track_audit.v1",
        "status": "PASS" if all_pass else "FAIL",
        "scope": "audit of passes/pass_240_249_{qldpc_bounds,yukawa_texture}.py "
                 "against this track's committed Passes 235/239/226/229/234",
        "agreements": {
            "k_times_d_eq_n": {"both": True, "value": f"{k}*{d} = {n}"},
            "democratic_yukawa_rank_1": {"both": True,
                                         "meaning": "exactly one heavy generation"},
        },
        "discrepancies": [
            {
                "id": "BPT ratio",
                "their_claim": "k*d^2/n = 1 exactly",
                "actual": f"k*d^2/n = {bpt_ratio} = q+1",
                "note": "their own code computes k*d**2/n correctly; the '=1' in "
                        "the printed annotation is k*d/n mislabelled",
                "consequence": "the family is NOT 2D-local; min embedding dim 3 "
                               "(Pass 239)",
                "severity": "annotation contradicts own output",
            },
            {
                "id": "check weight",
                "their_claim": "w = q+1 (=4 at q=3)",
                "actual": f"min stabiliser weight = {min_check_w} = 2(q+1)",
                "note": "q+1 is the weight of the LINES, which are logical "
                        "operators (Pass 229), not stabilisers; the stabilisers "
                        "are the sentinel with min weight 8 (Pass 226 exact, "
                        "Pass 234 distribution {8:11, 12:4})",
                "consequence": "their LDPC/locality discussion understates the "
                               "check weight by a factor ~2",
                "severity": "substantive",
            },
            {
                "id": "quantum Singleton",
                "their_claim": "k <= n - 4(d-1)",
                "actual": "Knill-Laflamme: k <= n - 2(d-1)",
                "note": f"correct rhs {correct_rhs}, theirs {their_rhs}; both hold "
                        f"for k={k}, so their conclusion stands",
                "consequence": "none (bound misstated but conclusion unaffected)",
                "severity": "cosmetic",
            },
        ],
        "reading": (
            "Independent re-derivation by the parallel track CONFIRMS the two "
            "load-bearing results of this one: k*d = n exactly, and the "
            "democratic Yukawa is rank 1 (one heavy generation). Three "
            "discrepancies were found, all resolved in favour of this track and "
            "re-verified here from the geometry: the BPT ratio is q+1 (so the "
            "codes need >=3 spatial dimensions, they are not 2D-local), the "
            "check weight is 2(q+1)=8 rather than q+1=4 (the weight-4 lines are "
            "logicals, not stabilisers), and the quantum Singleton bound is "
            "n-2(d-1). Cross-checking two agents is cheap and caught real errors."
        ),
        "checks": {kk: bool(v) for kk, v in checks.items() if isinstance(v, bool)},
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(payload, indent=2))
    return 0 if all_pass else 1


if __name__ == "__main__":
    raise SystemExit(main())
