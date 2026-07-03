#!/usr/bin/env python3
"""
The contextuality tax: the machine's irreducible scheduling defect is ONE MOVABLE POINT-STAR, and that
is the same integer as the quantum advantage. This witness puts two independent work streams together.
The contextual-fraction arc proved max_sat(W(3,3)) = 36 of 40 contexts (CF = 1/10) and the parity law
CF(q) = 0 (even q) / 1/(q^2+1) (odd q). Separately, the UOR/OS scheduler arc found that the line-context
microkernel schedules exactly 36 spreads and described its 4-context deficit as a "movable point-star
double-occupancy defect" -- explicitly flagged there as an audited numerical bridge, NOT a proven
structure. This witness proves the structure:

  DEFICIT LAW. For odd q the deficit n - max_sat is exactly q+1 = one line's worth of contexts
  (q=3: 40-36 = 4; q=5: 156-150 = 6, --deep), and 0 for even q (the ovoid). So CF = (q+1)/n =
  1/(q^2+1): the closed form is the statement "the tax is one star".

  COMPLETE CLASSIFICATION (q=3, the new result). By iterating the max-satisfiable ILP with no-good
  cuts -- each round forbidding the exact 4-line failure set just found and re-solving -- the witness
  enumerates EVERY failure set achievable by an optimal (36-context) assignment. The enumeration
  terminates when the objective drops below 36, so the classification is exhaustive, not sampled.
  The result: the achievable failure sets are exactly the 40 POINT-STARS (the 4 lines through one
  point), one for each of the 40 points. The scheduler arc's "movable point-star defect" is therefore
  a theorem: the defect is always a star, and it can sit at ANY of the 40 points (a gauge freedom of
  the classical layer), never anything else.

  WHY IT MATTERS OPERATIONALLY. The OS can classically satisfy every context except the star of one
  point of its choosing; the S3 admission controller's escalation budget is therefore exactly one
  star -- 4 contexts, 1/10 of the fabric -- per classical assignment, and the controller may MOVE the
  defect star to whichever point is least loaded (the double-occupancy site). The quantum resource
  (the priced 9^t dial) is spent exactly on the tax, nowhere else. On an even-order fabric the tax is
  zero and, consistently, there is no quantum gap to exploit either: alpha = q^2+1 = the Hoffman bound
  exactly (q=2: 5, q=4: 17), so even a realization (which for q=2 cannot exist -- Pass 56) would have
  no selection advantage to offer. Odd q keeps the gap: alpha = 7 < 10 = q^2+1 at q=3.

Honest scope: the q=3 classification is exact and exhaustive (ILP + no-good cuts, integer arithmetic
in the cuts); the deficit law is verified exactly at q in {2,3,4} (q=5 behind --deep, ~2 minutes) and
stated as the observed closed form beyond; the identification of the deficit with the scheduler arc's
"36 spreads / movable defect" underwrites that bridge's structure but, like the bridge itself, does
not claim a canonical bijection between optimal assignments and spreads. The S3/runtime tie-in is
accounting on committed constants (12-tick admission words, 2160-slot atlas, 51840 supercycle), not a
new physical claim.
"""
from __future__ import annotations

import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import w33_master_audit as audit  # noqa: E402


def _maxsat_ilp(lines, n, forbidden_failure_sets=()):
    """Max satisfiable contexts with optional no-good cuts; return (max_sat, sat_flags)."""
    import numpy as np
    from scipy.optimize import Bounds, LinearConstraint, milp

    nv = n + len(lines)
    rows, lb, ub = [], [], []
    for li, L in enumerate(lines):
        r1 = np.zeros(nv)
        r1[n + li] = 1
        for p in L:
            r1[p] -= 1
        rows.append(r1)
        lb.append(-np.inf)
        ub.append(0)
        r2 = np.zeros(nv)
        r2[n + li] = len(L) - 1
        for p in L:
            r2[p] += 1
        rows.append(r2)
        lb.append(-np.inf)
        ub.append(len(L))
    # no-good cuts: for a forbidden failure set F, require at least one line of F satisfied
    for F in forbidden_failure_sets:
        r = np.zeros(nv)
        for li in F:
            r[n + li] = 1
        rows.append(r)
        lb.append(1)
        ub.append(np.inf)
    c = np.zeros(nv)
    c[n:] = -1
    res = milp(
        c=c,
        constraints=LinearConstraint(np.array(rows), np.array(lb), np.array(ub)),
        integrality=np.ones(nv),
        bounds=Bounds(0, 1),
    )
    if res.x is None:
        return 0, None
    sat = [int(round(res.x[n + li])) for li in range(len(lines))]
    return int(round(-res.fun)), sat


def classify_failure_sets(q=3):
    """Exhaustively enumerate the failure sets of optimal assignments via no-good cuts.

    Returns (max_sat, failure_sets, all_stars, star_points): terminates when the objective drops,
    so the classification is complete.
    """
    pts, A, lines, B = audit._build(q)
    n = len(pts)
    target, _ = _maxsat_ilp(lines, n)
    found = []
    while True:
        ms, sat = _maxsat_ilp(
            lines, n, forbidden_failure_sets=[frozenset(F) for F in found]
        )
        if sat is None or ms < target:
            break
        F = tuple(sorted(li for li in range(len(lines)) if sat[li] == 0))
        found.append(F)
        if (
            len(found) > 500
        ):  # safety valve; should terminate at the number of failure sets
            break
    # star test: a failure set is a point-star iff all its lines share a common point
    star_points = []
    all_stars = True
    for F in found:
        common = set(lines[F[0]])
        for li in F[1:]:
            common &= set(lines[li])
        if len(common) == 1:
            star_points.append(next(iter(common)))
        else:
            all_stars = False
            star_points.append(None)
    return target, found, all_stars, star_points


def deficit_law(qs=(2, 3, 4)):
    """Verify deficit = 0 (even q) / q+1 (odd q) and the alpha/Hoffman gap by parity."""
    rows = []
    for q in qs:
        c = audit.audit_constants(q)
        deficit = c["lines"] - c["max_sat_contexts"]
        rows.append(
            {
                "q": q,
                "n_contexts": c["lines"],
                "max_sat": c["max_sat_contexts"],
                "deficit": deficit,
                "deficit_predicted": 0 if q % 2 == 0 else q + 1,
                "alpha": c["alpha"],
                "hoffman": c["hoffman"],
                "selection_gap_hoffman_minus_alpha": (
                    (c["hoffman"] - c["alpha"]) if c["alpha"] is not None else None
                ),
            }
        )
    return rows


def main(argv=None):
    deep = "--deep" in (argv if argv is not None else sys.argv[1:])
    print("== the contextuality tax: the defect is one movable point-star ==\n")
    checks = []

    def chk(name, ok):
        checks.append((name, bool(ok)))
        print(f"  [{'PASS' if ok else 'FAIL'}]  {name}")

    # 1. the deficit law across the family
    qs = (2, 3, 4, 5) if deep else (2, 3, 4)
    rows = deficit_law(qs)
    print("deficit law (one star of q+1 contexts for odd q, zero for even q):")
    for r in rows:
        chk(
            f"q={r['q']}: deficit {r['deficit']} = {'0 (ovoid)' if r['q'] % 2 == 0 else f'q+1 = {r['q']+1} (one star)'}",
            r["deficit"] == r["deficit_predicted"],
        )
    # the gap-by-parity corollary
    for r in rows:
        if r["alpha"] is not None:
            expect = 0 if r["q"] % 2 == 0 else None
            gap = r["selection_gap_hoffman_minus_alpha"]
            if r["q"] % 2 == 0:
                chk(
                    f"q={r['q']}: alpha = Hoffman = {r['hoffman']} (no selection gap even in principle)",
                    gap == 0,
                )
            else:
                chk(
                    f"q={r['q']}: alpha = {r['alpha']} < Hoffman = {r['hoffman']} (gap {gap} > 0)",
                    gap > 0,
                )

    # 2. the complete classification at q=3
    print(
        "\nexhaustive classification of optimal failure sets at q=3 (ILP + no-good cuts):"
    )
    target, found, all_stars, star_points = classify_failure_sets(3)
    chk("q=3: optimum re-confirmed at 36/40", target == 36)
    chk(
        f"q=3: number of achievable failure sets = 40 (one per point); found {len(found)}",
        len(found) == 40,
    )
    chk(
        "q=3: EVERY optimal failure set is a point-star (4 lines through one point)",
        all_stars,
    )
    distinct_centers = len({p for p in star_points if p is not None})
    chk(
        f"q=3: the defect star is fully movable -- {distinct_centers} distinct centers cover all 40 points",
        distinct_centers == 40,
    )

    all_ok = all(ok for _, ok in checks)
    print(
        "\nSYNTHESIS: the scheduler arc's '36 spreads / movable point-star defect' is now a theorem of the"
        "\ncontextuality arc: the classical layer can satisfy everything except the star of one point of its"
        "\nchoosing (a gauge freedom), so the OS escalation budget -- and the quantum 9^t spend -- is exactly"
        "\none star: 4 contexts, 1/10 of the fabric, per classical assignment. Even-order fabrics pay no tax"
        "\nand have no gap to exploit; odd fabrics pay exactly q+1."
    )
    print(f"\n{'ALL PASS' if all_ok else 'FAILURES present.'}")

    out = {
        "deficit_law": rows,
        "q3_classification": {
            "max_sat": target,
            "n_failure_sets": len(found),
            "all_point_stars": bool(all_stars),
            "star_centers": star_points,
            "failure_sets": [list(F) for F in found],
        },
        "runtime_tie_in": {
            "s3_admission_word_ticks": 12,
            "mirror_atlas_slots": 2160,
            "supercycle_ticks": 51840,
            "note": (
                "accounting on committed constants: per classical assignment the escalation budget is one "
                "movable star = 4 contexts = 1/10 of the fabric; the 9^t dial is spent on the tax only"
            ),
        },
        "all_pass": bool(all_ok),
        "summary": (
            "the contextuality tax: the machine's irreducible scheduling defect is ONE MOVABLE POINT-STAR. "
            "Joins the contextual-fraction arc (max_sat=36/40, parity law CF=1/(q^2+1) odd / 0 even) with "
            "the UOR/OS scheduler arc ('36 spreads, movable point-star defect', previously flagged as an "
            "unproven bridge). NEW EXACT RESULT: exhaustive enumeration of ALL optimal failure sets at q=3 "
            "via ILP + no-good cuts terminates with exactly 40 sets, each the star of one point (4 lines "
            "through it), one per point -- so the defect is always a star and fully movable, a theorem, "
            "not a metaphor. DEFICIT LAW: deficit = q+1 (one star) for odd q -- 4 at q=3, 6 at q=5 -- and "
            "0 for even q (ovoid); equivalently CF=(q+1)/n=1/(q^2+1). COROLLARY BY PARITY: even q has "
            "alpha = Hoffman = q^2+1 (no selection gap even in principle; and for q=2 no complete-basis "
            "realization exists at all, Pass 56), odd q keeps the gap (7<10 at q=3). OPERATIONALLY: the "
            "OS escalates exactly one star (1/10 of contexts) to quantum adjudication and may move it to "
            "the least-loaded point; the 9^t dial is spent on the tax only. HONEST: q=3 classification "
            "exhaustive; deficit law exact at q in {2,3,4} (+5 with --deep); no canonical "
            "assignment<->spread bijection claimed; runtime tie-in is accounting on committed constants."
        ),
        "sources": [
            "w33_master_audit (geometry + ILP); w33_audit_qscan (parity law); w33_ovoid_construct (even-q ovoid)",
            "w33_spread_contextual_microkernel_bridge (the scheduler arc's audited 36=36 bridge, in-flight)",
            "docs/index.html#holonet-s3-completion-admission-controller (12-tick words, 2160, 51840)",
        ],
    }
    with open("data/w33_contextuality_tax.json", "w") as fh:
        json.dump(out, fh, indent=2)
    print("wrote data/w33_contextuality_tax.json")
    return 0 if all_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
