#!/usr/bin/env python3
"""Pass 10972: minimal S4-invariant cubic potential selects one clock spontaneously.

The Pass-10971 clock order parameter is the 3D augmentation representation
A = {x in R^4 : sum x_i = 0}.  S4 permutes coordinates.  On the unit sphere
in A, p3=sum x_i^3 has exact maximum 1/sqrt(3), attained only at the four
normalized clock vectors (3,-1,-1,-1)/sqrt(12) and permutations.

Therefore V=lambda(r^2-v^2)^2 - g p3(x), lambda,g,v>0, is fully S4 invariant
but has exactly four global minima, each with stabilizer S3.  This is the
minimal Landau scaffold that evades Pass 10971 by spontaneous symmetry breaking.
"""
from __future__ import annotations

import argparse
import itertools
import json
from fractions import Fraction
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "w33_pass10972_tetrahedral_cubic_clock_selector.json"
P71 = ROOT / "data" / "w33_pass10971_clock_selector_symmetry_no_go.json"
def perms4():
    return list(itertools.permutations(range(4)))


def permute(p, x):
    return tuple(x[p[i]] for i in range(4))


def p1(x):
    return sum(x)


def p2(x):
    return sum(t * t for t in x)


def p3(x):
    return sum(t * t * t for t in x)


def clock_rays_integer():
    return [
        tuple(3 if j == i else -1 for j in range(4))
        for i in range(4)
    ]


def stationary_two_value_cases():
    """Exact Lagrange classification for p3 on p1=0,p2=1.

    Stationarity gives 3 x_i^2 = alpha + 2 beta x_i, so there are at most
    two coordinate values.  m coordinates equal a and 4-m equal b.
    """
    out = []
    for m in (1, 2, 3):
        n = 4 - m
        # b=-(m/n)a and a^2 * [m+m^2/n] = 1.
        a2 = Fraction(n, 4 * m)
        b2 = Fraction(m, 4 * n)
        # p3 sign depends on sign(a); record squared value exactly.
        # p3 = m a^3 + n b^3 = a^3 * m*(1-m^2/n^2).
        coeff = Fraction(m * (n * n - m * m), n * n)
        p3sq = coeff * coeff * a2 * a2 * a2
        out.append({
            "multiplicity_a": m,
            "multiplicity_b": n,
            "a_squared": str(a2),
            "b_squared": str(b2),
            "p3_squared": str(p3sq),
        })
    return out
def stabilizer(group, x):
    return [p for p in group if permute(p, x) == x]


def payload():
    group = perms4()
    rays = clock_rays_integer()
    cases = stationary_two_value_cases()

    # Integer ray checks avoid radicals.
    ray_stats = []
    for x in rays:
        ray_stats.append({
            "vector": list(x),
            "sum": p1(x),
            "norm_squared": p2(x),
            "cubic": p3(x),
            "normalized_cubic_squared": str(Fraction(p3(x) ** 2, p2(x) ** 3)),
            "stabilizer_order": len(stabilizer(group, x)),
            "orbit_size": len({permute(p, x) for p in group}),
        })

    case_by_m = {r["multiplicity_a"]: r for r in cases}
    checks = {
        "parent_selector_no_go_passes": json.loads(P71.read_text(encoding="utf-8"))["status"] == "PASS",
        "S4_order24": len(group) == 24,
        "four_clock_rays": len(set(rays)) == 4,
        "clock_rays_sum_zero": all(r["sum"] == 0 for r in ray_stats),
        "clock_rays_norm12": all(r["norm_squared"] == 12 for r in ray_stats),
        "clock_rays_cubic24": all(r["cubic"] == 24 for r in ray_stats),
        "normalized_cubic_max_squared_1_over_3": all(
            r["normalized_cubic_squared"] == "1/3" for r in ray_stats
        ),
        "clock_stabilizer_S3_order6": all(r["stabilizer_order"] == 6 for r in ray_stats),
        "clock_orbit_size4": all(r["orbit_size"] == 4 for r in ray_stats),
        "two_two_stationary_has_zero_cubic": case_by_m[2]["p3_squared"] == "0",
        "one_three_stationary_has_one_third": case_by_m[1]["p3_squared"] == "1/3",
        "three_one_stationary_has_one_third": case_by_m[3]["p3_squared"] == "1/3",
    }
    # A concrete rational/radical-free comparison of the invariant potential at
    # fixed radius r=1: for g>0 its angular term -g*p3 is minimized by max p3.
    # The Lagrange classification proves no other stationary type beats it.
    checks["cubic_extrema_are_exactly_tetrahedral"] = (
        case_by_m[1]["p3_squared"] == "1/3"
        and case_by_m[2]["p3_squared"] == "0"
        and case_by_m[3]["p3_squared"] == "1/3"
    )

    return {
        "schema": "w33.pass10972.tetrahedral-cubic-clock-selector.v1",
        "status": "PASS" if all(checks.values()) else "FAIL",
        "representation": {
            "group": "S4 = PGL(2,3) = W(A3)",
            "space": "A={x in R^4 : sum_i x_i=0}",
            "dimension": 3,
            "clock_vectors": ray_stats,
        },
        "invariants": {
            "quadratic": "p2=sum_i x_i^2",
            "cubic": "p3=sum_i x_i^3",
            "cubic_bound_on_p2_1": "|p3| <= 1/sqrt(3)",
            "positive_maximizers": "four permutations of (3,-1,-1,-1)/sqrt(12)",
            "negative_minimizers": "their negatives",
            "stationary_classification": cases,
        },
        "landau_selector": {
            "potential": "V(x)=lambda*(p2(x)-v^2)^2 - g*p3(x), lambda>0,g>0,v>0",
            "symmetry": "full S4",
            "angular_vacua": "exactly the four positive tetrahedral clock directions",
            "vacuum_stabilizer": "S3",
            "breaking": "S4 -> S3",
            "radial_equation": "4 lambda (r^2-v^2) = sqrt(3) g r",
            "positive_radius": "r*=(sqrt(3)g + sqrt(3g^2+64 lambda^2 v^2))/(8 lambda)",
            "radial_second_derivative_at_rstar": "4 lambda (r*^2+v^2) > 0",
            "orientation": "sign(g) exchanges the two opposite tetrahedra",
        },
        "checks": checks,
        "boundary": (
            "This constructs the minimal S4-invariant Landau selector on the exact clock "
            "augmentation module. It does not derive lambda, g, v, a physical field, or a "
            "continuum time dynamics from W33. The new target is whether an already-certified "
            "W33/E6/Albert cubic restricts nontrivially to this unique A3 cubic invariant."
        ),
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true")
    ap.add_argument("--output", type=Path, default=OUT)
    a = ap.parse_args()
    p = payload()
    s = json.dumps(p, indent=2, sort_keys=True) + "\n"
    if a.check:
        if not a.output.exists() or a.output.read_text(encoding="utf-8") != s:
            raise SystemExit("certificate drift")
    else:
        a.output.parent.mkdir(parents=True, exist_ok=True)
        a.output.write_text(s, encoding="utf-8")
    print(json.dumps({
        "status": p["status"],
        "checks": sum(p["checks"].values()),
        "total": len(p["checks"]),
        "breaking": p["landau_selector"]["breaking"],
        "cubic_bound": p["invariants"]["cubic_bound_on_p2_1"],
    }, sort_keys=True))
    return 0 if p["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
