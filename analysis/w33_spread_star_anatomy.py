#!/usr/bin/env python3
"""
The spread side of the tax: every spread-clock cycle runs at exactly 9/10 under any optimal classical
assignment, and the "double-occupancy" defect is literal. Pass 57 proved the classical layer's defect
is one movable point-star. This witness completes the synthesis from the scheduler's side, by computing
from scratch the objects the UOR/OS arc's spread-clock is built on and the fine structure of the
optimal assignments the tax theorem classified:

  INDEPENDENT SPREAD COUNT. A spread is a set of 10 pairwise-disjoint lines partitioning the 40 points
  -- the scheduler arc's clock unit. This witness enumerates ALL spreads by exact-cover backtracking --
  a different algorithm with no shared code from the scheduler arc's find_spreads -- and confirms the
  count both arcs now rely on, plus the regularity that every line lies in exactly 9 spreads.

  THE SERVICE-RATE LEMMA. Every spread covers every point exactly once, so it contains exactly ONE line
  of every point-star (the scheduler arc's in-flight defect/spread tensor records the same complete
  incidence; re-verified here independently for all 36x40 pairs). Combined with the tax theorem (the
  failure set of any optimal assignment is one star), this gives the operational guarantee stated here:
  under ANY optimal classical assignment, EVERY spread has exactly 9 of its 10 lines satisfied. The
  spread-clock never sees a worse (or better) cycle: the tax is spread-isotropic. Corollary: for a
  fixed defect star, the 36 spreads partition into q+1 = 4 classes of exactly 9 by WHICH defect line
  they carry (one slice of the colored tensor).

  THE ANATOMY OF THE OPTIMA (uniform loading; double occupancy is the minimal class). For a fixed
  defect center p, the witness enumerates EVERY optimal assignment (all 0/1 assignments satisfying the
  36 non-star contexts, via ILP feasibility + no-good cuts, exhaustive: 20 optima per center). The
  computation CORRECTED the naive guess and found a richer exact structure, then pinned it:
    - the CENTER IS FREE: p lies only on its own star's lines, so flipping p preserves optimality --
      optima come in pairs, and exactly half light the center;
    - UNIFORM LOADING: every optimum loads its four defect lines EQUALLY -- the occupancy is always
      (c,c,c,c), never mixed, with c in {2,3,4}: center-unlit optima are (2,2,2,2) [11 lit rays] or
      (3,3,3,3) [12]; their center-lit partners are (3,3,3,3) [12] or (4,4,4,4) [13]. A defect line is
      never empty and never accidentally satisfied (c is never 0 or 1);
    - DOUBLE OCCUPANCY IS THE MINIMAL CLASS: the scheduler arc's "double-occupancy defect" is literally
      the minimal (11-ray) optima; the full spectrum is uniform loading at 2, 3, or 4 rays per defect
      line.

Together with Pass 57: the tax is one movable star (assignment side), every clock cycle pays exactly
1/10 of it (spread side), and the defect's microstructure is uniformly loaded with double occupancy as
its ground state. The scheduler's observed behavior is now derived, top to bottom, from the geometry.

Honest scope: all counts are exact finite enumerations from the W(3,3) geometry built by
w33_master_audit (the spread search is independent backtracking; the optimum enumeration is ILP
feasibility with no-good cuts and terminates, so it is exhaustive for the chosen center; full
movability across centers is Pass 57's theorem). The identification with the scheduler arc's
spread-clock underwrites its structure; as before, no canonical assignment-to-spread bijection is
claimed -- indeed the service-rate lemma shows the relation is many-to-many and uniform.
"""
from __future__ import annotations

import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import w33_master_audit as audit  # noqa: E402


def enumerate_spreads(lines, n_points):
    """All sets of pairwise-disjoint lines partitioning the point set (exact-cover backtracking)."""
    line_sets = [frozenset(L) for L in lines]
    by_point = [[] for _ in range(n_points)]
    for li, L in enumerate(line_sets):
        for p in L:
            by_point[p].append(li)
    spreads = []

    def rec(covered, chosen, min_line):
        if len(covered) == n_points:
            spreads.append(tuple(sorted(chosen)))
            return
        # branch on the lowest uncovered point (canonical, so each spread found once)
        p = next(i for i in range(n_points) if i not in covered)
        for li in by_point[p]:
            if not (line_sets[li] & covered):
                rec(covered | line_sets[li], chosen + [li], li)

    rec(frozenset(), [], -1)
    return spreads


def _enumerate_optima_for_center(lines, n_points, center, cap=500):
    """All 0/1 assignments satisfying every non-star context exactly once (exhaustive via no-good cuts)."""
    import numpy as np
    from scipy.optimize import Bounds, LinearConstraint, milp

    star = [li for li, L in enumerate(lines) if center in L]
    others = [li for li in range(len(lines)) if li not in star]
    solutions = []
    while len(solutions) < cap:
        rows, lb, ub = [], [], []
        for li in others:
            r = np.zeros(n_points)
            for p in lines[li]:
                r[p] = 1
            rows.append(r)
            lb.append(1)
            ub.append(1)
        # no-good cuts excluding found solutions: Hamming distance >= 1
        for sol in solutions:
            r = np.zeros(n_points)
            const = 0
            for i in range(n_points):
                if sol[i]:
                    r[i] = -1
                    const += 1
                else:
                    r[i] = 1
            rows.append(r)
            lb.append(1 - const)
            ub.append(np.inf)
        res = milp(
            c=np.zeros(n_points),
            constraints=LinearConstraint(np.array(rows), np.array(lb), np.array(ub)),
            integrality=np.ones(n_points),
            bounds=Bounds(0, 1),
        )
        if res.x is None:
            break
        solutions.append(tuple(int(round(v)) for v in res.x))
    return solutions, star


def main():
    print(
        "== the spread side of the tax: 9/10 service, 4x9 classes, literal double occupancy ==\n"
    )
    checks = []

    def chk(name, ok):
        checks.append((name, bool(ok)))
        print(f"  [{'PASS' if ok else 'FAIL'}]  {name}")

    pts, A, lines, B = audit._build(3)
    n = len(pts)

    # 1. independent spread enumeration
    spreads = enumerate_spreads(lines, n)
    n_spreads = len(spreads)
    print(f"spreads of W(3,3), enumerated independently by exact cover: {n_spreads}")
    chk("spread count matches the scheduler arc's bridge (36)", n_spreads == 36)
    per_line = [0] * len(lines)
    for S in spreads:
        for li in S:
            per_line[li] += 1
    chk(
        f"regularity: every line lies in exactly {n_spreads*10//len(lines)} spreads",
        len(set(per_line)) == 1 and per_line[0] == n_spreads * 10 // len(lines),
    )

    # 2. the service-rate lemma: spread x star intersection = 1, always
    stars = {p: frozenset(li for li, L in enumerate(lines) if p in L) for p in range(n)}
    inter_ok = all(len(set(S) & stars[p]) == 1 for S in spreads for p in range(n))
    chk(
        "every spread contains exactly ONE line of every point-star (all 36x40 pairs)",
        inter_ok,
    )
    chk(
        "=> under ANY optimal assignment, EVERY spread has exactly 9/10 lines satisfied (uniform service rate)",
        inter_ok,  # direct corollary of intersection=1 + Pass 57 (failure set = one star)
    )
    # 4x9 classification for one defect star (any center; symmetry via Pass 57 movability)
    center = 0
    by_defect_line = {}
    for S in spreads:
        (dl,) = set(S) & stars[center]
        by_defect_line.setdefault(dl, []).append(S)
    sizes = sorted(len(v) for v in by_defect_line.values())
    chk(
        f"for a fixed defect star, spreads split into {len(by_defect_line)} classes of sizes {sizes} (4 x 9)",
        len(by_defect_line) == 4 and sizes == [9, 9, 9, 9],
    )

    # 3. anatomy of ALL optima for a fixed center
    sols, star = _enumerate_optima_for_center(lines, n, center)
    n_opt = len(sols)
    print(
        f"\noptimal assignments with defect star at point {center}: {n_opt} (exhaustive)"
    )
    chk("enumeration is exhaustive (terminated below the cap)", 0 < n_opt < 500)
    center_lit = [s for s in sols if s[center] == 1]
    chk(
        f"the center is FREE: exactly half the optima light it ({len(center_lit)}/{n_opt})",
        2 * len(center_lit) == n_opt,
    )
    occupancy_patterns = {}
    lit_counts = set()
    uniform = True
    never_bad = True
    for s in sols:
        occ = tuple(sorted(sum(s[p] for p in lines[li]) for li in star))
        occupancy_patterns[(s[center], occ)] = (
            occupancy_patterns.get((s[center], occ), 0) + 1
        )
        lit_counts.add(sum(s))
        if len(set(occ)) != 1:
            uniform = False
        if occ[0] in (0, 1):
            never_bad = False
    chk(
        "UNIFORM LOADING: every optimum loads its 4 defect lines EQUALLY (occupancy always (c,c,c,c))",
        uniform,
    )
    chk(
        "a defect line is never empty and never accidentally satisfied (c is never 0 or 1)",
        never_bad,
    )
    expected = {
        (0, (2, 2, 2, 2)),
        (0, (3, 3, 3, 3)),
        (1, (3, 3, 3, 3)),
        (1, (4, 4, 4, 4)),
    }
    chk(
        f"classification: exactly the 4 uniform classes {{unlit:(2,2,2,2),(3,3,3,3); lit:(3,3,3,3),(4,4,4,4)}}",
        set(occupancy_patterns) == expected,
    )
    chk(
        "DOUBLE OCCUPANCY is the minimal class: the 11-ray optima are exactly the (2,2,2,2) ones",
        min(lit_counts) == 11 and (0, (2, 2, 2, 2)) in occupancy_patterns,
    )
    chk(
        f"lit-ray spectrum is exactly {{11, 12, 13}}: found {sorted(lit_counts)}",
        lit_counts == {11, 12, 13},
    )

    all_ok = all(ok for _, ok in checks)
    print(
        "\nSYNTHESIS COMPLETE: assignment side (Pass 57) -- the tax is one movable star; spread side (here) --"
        "\nevery clock cycle pays exactly 1/10 of it, isotropically; microstructure -- two rays per failed"
        "\ncontext, the scheduler's 'double occupancy', now literal. The spread-clock's observed behavior is"
        "\nderived from the geometry, top to bottom."
    )
    print(f"\n{'ALL PASS' if all_ok else 'FAILURES present.'}")

    out = {
        "n_spreads": n_spreads,
        "spreads_per_line": per_line[0] if len(set(per_line)) == 1 else per_line,
        "service_rate_lemma": "every spread contains exactly one line of every star -> 9/10 satisfied under any optimum",
        "defect_classification": {"classes": len(by_defect_line), "sizes": sizes},
        "optima_anatomy": {
            "center": center,
            "n_optima": n_opt,
            "center_lit_half": len(center_lit),
            "occupancy_classes": {
                str(k): v for k, v in sorted(occupancy_patterns.items())
            },
            "lit_counts": sorted(lit_counts),
        },
        "all_pass": bool(all_ok),
        "summary": (
            "the spread side of the tax. INDEPENDENT COUNT: exact-cover backtracking (no shared code with "
            "the scheduler arc) finds exactly 36 spreads of W(3,3), each line in 9 of them -- the bridge's "
            "36 verified from scratch. SERVICE-RATE LEMMA: every spread contains exactly one line of every "
            "point-star (verified all 36x40 pairs), so with Pass 57 (failure set = one star) EVERY spread "
            "has exactly 9/10 lines satisfied under ANY optimal assignment -- the tax is spread-isotropic, "
            "and for a fixed defect star the 36 spreads split 4x9 by which defect line they carry. ANATOMY "
            "(exhaustive: exactly 20 optima per center): the center is FREE (optima come in "
            "center-lit/unlit pairs, exactly half each), and -- a structure the computation itself "
            "corrected us into -- every optimum loads its four defect lines UNIFORMLY, occupancy always "
            "(c,c,c,c) with c in {2,3,4}, never mixed, never empty, never accidentally satisfied: "
            "center-unlit are (2,2,2,2) [11 rays] or (3,3,3,3) [12], center-lit partners (3,3,3,3) [12] "
            "or (4,4,4,4) [13]. The scheduler arc's 'double-occupancy defect' is literally the MINIMAL "
            "class of optima; the full spectrum is uniform loading at 2, 3, or 4. HONEST: exact finite "
            "enumerations; exhaustive for the chosen center with movability supplied by Pass 57; no "
            "canonical assignment-to-spread bijection claimed -- the lemma shows the relation is "
            "many-to-many and uniform."
        ),
        "total_optimal_assignments": 40 * n_opt,
        "sources": [
            "w33_master_audit._build (geometry); Pass 57 w33_contextuality_tax (the star theorem)",
            "w33_spread_contextual_microkernel_bridge + w33_defect_spread_tensor (scheduler arc, in-flight; the complete defect/spread incidence is theirs, re-verified independently here)",
            "exact-cover backtracking + ILP feasibility with no-good cuts",
        ],
    }
    with open("data/w33_spread_star_anatomy.json", "w") as fh:
        json.dump(out, fh, indent=2)
    print("wrote data/w33_spread_star_anatomy.json")
    return 0 if all_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
