#!/usr/bin/env python3
"""Pass 267: the FULL structure at the odd prime power q = 9.

Pass 262 established the headline rank at q = 9 (451, refuting the transfer
unification).  But the rank is only one component of the Pass 224/238 package.
This witness verifies the ENTIRE structure at the first odd prime power ever
reached, which is the strongest available test that the odd-q results are about
characteristic and not about primality:

    n            = (q+1)(q^2+1)   = 820
    rank_2 C      = (q^2+1)(q+2)/2 = 451     (= char-0 rank, Pass 266)
    dim C^perp    = q(q^2+1)/2     = 369     (= the SRG multiplicity g)
    k_CSS         = n - 2 dim C^perp = q^2+1 = 82
    C^perp doubly-even and self-orthogonal  => the CSS register exists at q = 9

If every one of these holds at q = 9, then the odd-q tower (Passes 224/238) is
not a prime phenomenon: it is a cross-characteristic phenomenon, exactly as
Pass 266's mechanism predicts.

We also record an honest feasibility note for the next odd prime power, q = 25
(n = 16276), which is out of reach of the present F2 elimination.
"""

from __future__ import annotations

from itertools import combinations
import json
from pathlib import Path
import sys
import time

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from analysis.w33_pass224_shadow_code_tower import (
    doubly_even_subcode,
    f2_nullspace,
    f2_rank,
    f2_rowspace_basis,
    incidence_rows,
    popcount,
    rows_to_bitmasks,
)
from analysis.w33_pass262_unified_rank_law import (
    GFpk,
    isotropic_lines_gf,
    pg3_points_gf,
)

OUT = ROOT / "data" / "w33_pass267_prime_power_full_structure.json"


def main():
    checks = {}
    q = 9
    t0 = time.time()

    F = GFpk(3, 2, [1, 0])            # GF(9) = F_3[x]/(x^2+1)
    pts = pg3_points_gf(F)
    n = len(pts)
    lines = isotropic_lines_gf(F, pts)
    rows = incidence_rows(lines, n)
    masks = rows_to_bitmasks(rows)

    checks["n_820"] = n == 820
    checks["lines_820"] = len(lines) == 820
    checks["n_matches_formula"] = n == (q + 1) * (q * q + 1)

    # ---- the incidence code and its dual
    Cbasis = f2_rowspace_basis(masks)
    dimC = len(Cbasis)
    rank_direct = f2_rank(rows)
    checks["rank_451"] = dimC == 451 == rank_direct
    checks["rank_matches_char0_law"] = dimC == (q * q + 1) * (q + 2) // 2

    # ---- the hull / sentinel
    gram_rows = [tuple(1 if popcount(a & b) & 1 else 0 for b in Cbasis)
                 for a in Cbasis]
    hull_coeffs = f2_nullspace(gram_rows, dimC)
    hull_words = []
    for cc in hull_coeffs:
        w = 0
        for i in range(dimC):
            if (cc >> i) & 1:
                w ^= Cbasis[i]
        if w:
            hull_words.append(w)
    hull_basis = f2_rowspace_basis(hull_words)
    S = doubly_even_subcode(hull_basis)
    dimS = len(S)

    checks["sentinel_369"] = dimS == 369
    checks["sentinel_matches_law"] = dimS == q * (q * q + 1) // 2
    checks["sentinel_equals_dual"] = dimS == n - dimC   # C^perp = sentinel
    checks["sentinel_is_SRG_multiplicity_g"] = dimS == q * (q * q + 1) // 2

    # doubly-even and self-orthogonal => the CSS register exists
    so = all(popcount(a & b) % 2 == 0 for a, b in combinations(S, 2)) and all(
        popcount(a) % 2 == 0 for a in S)
    de = all(popcount(a) % 4 == 0 for a in S)
    checks["sentinel_self_orthogonal"] = bool(so)
    checks["sentinel_doubly_even"] = bool(de)
    checks["css_register_exists_at_q9"] = bool(so and de)

    # ---- the logical count
    k = n - 2 * dimS
    checks["k_82"] = k == 82
    checks["k_matches_q2_plus_1"] = k == q * q + 1
    secs = round(time.time() - t0, 1)

    # ---- honest feasibility note for the next odd prime power
    q25_n = (25 + 1) * (25 * 25 + 1)
    q25_rank = (625 + 1) * 27 // 2
    feasibility = {
        "next_odd_prime_power": 25,
        "n": q25_n,
        "predicted_rank": q25_rank,
        "predicted_sentinel": 25 * (625 + 1) // 2,
        "predicted_k": 626,
        "status": "NOT ATTEMPTED -- out of reach of the present method",
        "why": (f"n = {q25_n} requires eliminating {q25_n} rows of {q25_n} bits "
                f"against ~{q25_rank} pivots (~1e8 big-integer XORs on 255-word "
                "operands); the Python bitmask elimination that handles n=4369 "
                "in seconds would take hours here. A packed uint64 / GF(2) "
                "library would be needed."),
    }

    all_pass = all(v for v in checks.values() if isinstance(v, bool))
    payload = {
        "schema": "w33.pass267.prime_power_full_structure.v1",
        "status": "PASS" if all_pass else "FAIL",
        "q": q,
        "verified_structure": {
            "n": n, "rank_2": dimC, "dim_C_perp_sentinel": dimS,
            "k_css": k, "sentinel_self_orthogonal": bool(so),
            "sentinel_doubly_even": bool(de), "seconds": secs,
        },
        "laws_checked_at_q9": {
            "n = (q+1)(q^2+1)": n == (q + 1) * (q * q + 1),
            "rank = (q^2+1)(q+2)/2": dimC == (q * q + 1) * (q + 2) // 2,
            "sentinel = q(q^2+1)/2": dimS == q * (q * q + 1) // 2,
            "k = q^2+1": k == q * q + 1,
            "CSS register exists": bool(so and de),
        },
        "feasibility_q25": feasibility,
        "reading": (
            "Every component of the odd-q package -- the point count, the "
            "characteristic-0 rank, the sentinel dimension (= the SRG "
            "multiplicity g of Pass 266), the logical count k = q^2+1, and the "
            "doubly-even self-orthogonality that makes the CSS register exist -- "
            "holds exactly at q = 9. Since 9 is a prime POWER, this confirms "
            "Pass 266's mechanism: the odd-q tower is a CROSS-CHARACTERISTIC "
            "phenomenon (2 does not divide q), with no dependence on the "
            "Frobenius degree t. The next odd prime power q=25 is honestly out "
            "of computational reach here and is left as a stated prediction."
        ),
        "checks": {k2: bool(v) for k2, v in checks.items() if isinstance(v, bool)},
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(payload, indent=2))
    return 0 if all_pass else 1


if __name__ == "__main__":
    raise SystemExit(main())
