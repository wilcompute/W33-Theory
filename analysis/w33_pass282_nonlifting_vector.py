#!/usr/bin/env python3
"""Pass 282: exhibit the single non-lifting kernel vector at q=4.

Pass 276 localised the whole characteristic-2 anomaly at q=4 to ONE mod-2 kernel
direction with no integral origin (dim ker_F2 = 35 = g+1). This witness finds it
and describes it: the smallest possible instance of the delta phenomenon.
"""
from __future__ import annotations
import json
from collections import Counter
from pathlib import Path
import sys
import sympy as sp
ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
from analysis.w33_pass224_shadow_code_tower import f2_nullspace, incidence_rows, popcount
from analysis.w33_pass232_even_q_sister_tower import GF, isotropic_lines_gf, pg3_points_gf
OUT = ROOT / "data" / "w33_pass282_nonlifting_vector.json"

def main():
    checks = {}
    q = 4
    gf = GF(2); pts = pg3_points_gf(gf); lines = isotropic_lines_gf(gf, pts)
    n = len(pts); rows = incidence_rows(lines, n)
    checks["q4_n_85"] = n == 85
    g = q * (q * q + 1) // 2                      # 34
    kerF2 = f2_nullspace(rows, n)
    checks["dim_ker_F2_is_35"] = len(kerF2) == 35
    checks["g_is_34"] = g == 34
    checks["exactly_one_extra_direction"] = len(kerF2) - g == 1

    # the reduction of the integral kernel
    M = sp.Matrix([[int(x) for x in r] for r in rows])
    ker = M.nullspace()
    checks["dim_ker_Q_is_g"] = len(ker) == g
    red = []
    for vec in ker:
        dens = [sp.nsimplify(x).q for x in vec]
        lcm = sp.ilcm(*dens) if dens else 1
        iv = [int(sp.nsimplify(x) * lcm) for x in vec]
        gg = sp.igcd(*[abs(t) for t in iv if t != 0]) or 1
        iv = [t // gg for t in iv]
        mask = 0
        for i, t in enumerate(iv):
            if t % 2:
                mask |= 1 << i
        red.append(mask)
    basis = []
    for v in red:
        cur = v
        for b in basis:
            cur = min(cur, cur ^ b)
        if cur:
            basis.append(cur); basis.sort(reverse=True)
    checks["reduced_integral_kernel_has_dim_g"] = len(basis) == g

    # find a mod-2 kernel vector OUTSIDE the reduction: the non-lifting one
    witness = None
    for v in kerF2:
        cur = v
        for b in basis:
            cur = min(cur, cur ^ b)
        if cur:
            witness = v
            break
    checks["found_the_nonlifting_vector"] = witness is not None
    # reduce it to a canonical low-weight representative modulo the lifting part
    best = witness
    for b in basis:
        if popcount(best ^ b) < popcount(best):
            best = best ^ b
    for _ in range(4):
        for b in basis:
            if popcount(best ^ b) < popcount(best):
                best = best ^ b
    wt = popcount(best)
    support = [i for i in range(n) if (best >> i) & 1]
    # how does it meet the lines?
    meets = Counter(popcount(best & m) for m in
                    [sum(1 << p for p in l) for l in lines])
    checks["witness_meets_every_line_evenly"] = all(
        k % 2 == 0 for k in meets)
    all_pass = all(v for v in checks.values() if isinstance(v, bool))
    payload = {
        "schema": "w33.pass282.nonlifting_vector.v1",
        "status": "PASS" if all_pass else "FAIL",
        "setting": {"q": q, "n": n, "g": g, "dim_ker_F2": len(kerF2),
                    "delta": len(kerF2) - g},
        "the_vector": {
            "weight_after_reduction": wt,
            "support_size": len(support),
            "support_first_20": support[:20],
            "line_intersection_profile": {str(k): v for k, v in sorted(meets.items())},
            "note": "a mod-2 kernel vector: it meets every isotropic line in an "
                    "EVEN number of points, yet no integral kernel vector reduces "
                    "to it",
        },
        "reading": (
            "This is the entire characteristic-2 anomaly at q=4, made explicit: "
            "one F2 vector that is orthogonal to every line mod 2 but has no "
            "integral origin. It is the smallest instance of the delta = "
            "0,1,27,423 phenomenon -- delta(4) = 1 is exactly this one direction "
            "(equivalently, Pass 271's single even invariant factor of value 2). "
            "Its weight and line-intersection profile are recorded as the "
            "concrete fingerprint of the defect."
        ),
        "checks": {k: bool(v) for k, v in checks.items() if isinstance(v, bool)},
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(payload, indent=2))
    return 0 if all_pass else 1

if __name__ == "__main__":
    raise SystemExit(main())
