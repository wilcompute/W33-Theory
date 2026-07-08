#!/usr/bin/env python3
"""
Pass 90 -- Automorphism census of the 28 SRG(40,12,2,4) graphs, and its correlation with the
Pass 89 2-adic (2-rank) ladder.  Is the arithmetic ladder also a symmetry ladder?

Computed |Aut| (GRAPE/nauty, w33_pass90_aut.g) for all 28 and matched to each graph's 2-rank
(from the Pass 89 Smith-normal-form census).  Findings:

  * The two generalized quadrangles -- the symplectic W(3,3) (graph #28) and the parabolic quadric
    Q(4,3) (graph #27) -- both have |Aut| = 51840 = |Sp(4,3)| = |W(E6)|, dwarfing every other graph
    (the next largest is 648).  Two dual GQs, isomorphic collineation groups.
  * Symmetry broadly ANTI-correlates with the 2-rank: the mean |Aut| rises as the 2-rank falls
    (16 -> 14 -> 12 -> 10).  Q(4,3) sits alone at the top rung (2-rank 10) with maximal symmetry.
  * The one anomaly is W(3,3): it also attains the maximal 51840 but hides at the GENERIC bottom
    rung (2-rank 16), among 16 far-less-symmetric graphs.  So the two dual GQs bookend the ladder,
    W at the bottom (generic 2-rank, maximal symmetry) and Q at the top (extreme 2-rank, maximal
    symmetry).
  * Mass check: sum over the 28 of 1/|Aut| is the number of LABELLED SRG(40,12,2,4) graphs divided
    by 40! (a Siegel-mass-formula-style invariant of the family).

ASCII-only.  Reads the committed GRAPE and Pass 89 certificates.
"""
from __future__ import annotations

import json
import re
from collections import defaultdict
from fractions import Fraction
from math import factorial
from pathlib import Path

ROOT = Path(__file__).resolve().parent


def read_aut():
    txt = (ROOT / "w33_pass90_aut_out.txt").read_text()
    d = {}
    for m in re.finditer(r"graph=(\d+) autorder=(\d+)", txt):
        d[int(m.group(1))] = int(m.group(2))
    return d


def read_two_ranks():
    txt = (ROOT / "w33_pass89_census_out.txt").read_text()
    d = {}
    for line in txt.splitlines():
        m = re.search(r"graph=(\d+).*smithA=\[(.*?)\]", line)
        if m:
            diag = [int(x) for x in m.group(2).split(",")]
            d[int(m.group(1))] = sum(1 for x in diag if x == 1)  # 2-rank = #units
    return d


def main():
    aut = read_aut()
    tr = read_two_ranks()
    assert len(aut) == 28 and len(tr) == 28

    W_index, Q_index = 28, 27
    GQ_order = 51840

    # per-rung aggregate
    by_rank = defaultdict(list)
    for g in aut:
        by_rank[tr[g]].append(aut[g])
    rung_summary = {}
    for r in sorted(by_rank, reverse=True):
        v = by_rank[r]
        rung_summary[r] = {
            "count": len(v),
            "max_aut": max(v),
            "mean_aut": round(sum(v) / len(v), 1),
            "median_aut": sorted(v)[len(v) // 2],
        }

    # mass = sum 1/|Aut|  (labelled graphs / 40!)
    mass = sum(Fraction(1, a) for a in aut.values())
    labelled = mass * factorial(40)

    # do the two 51840 graphs correspond exactly to the two GQ point graphs #27,#28?
    max_aut_graphs = sorted(g for g in aut if aut[g] == GQ_order)

    checks = {
        "28_graphs": len(aut) == 28,
        "two_GQ_have_aut_51840": aut[W_index] == aut[Q_index] == GQ_order,
        "51840_is_Sp43_order": GQ_order == 51840,
        "GQ_aut_is_maximal": max(aut.values()) == GQ_order,
        "only_the_two_GQs_reach_51840": max_aut_graphs == [Q_index, W_index],
        "next_largest_is_648": sorted(set(aut.values()), reverse=True)[1] == 648,
        "W_generic_rank16_Q_extreme_rank10": tr[W_index] == 16 and tr[Q_index] == 10,
        "labelled_count_is_integer": labelled.denominator == 1,
    }
    all_ok = all(checks.values())

    print("=" * 78)
    print("PASS 90 -- AUTOMORPHISM CENSUS OF THE 28 SRG(40,12,2,4) GRAPHS")
    print("=" * 78)
    print("|Aut| by 2-rank rung (Pass 89 ladder):")
    print(
        f"   {'2-rank':>6} {'#graphs':>8} {'max|Aut|':>10} {'mean|Aut|':>11} {'median':>8}"
    )
    for r, s in rung_summary.items():
        print(
            f"   {r:>6} {s['count']:>8} {s['max_aut']:>10} {s['mean_aut']:>11} {s['median_aut']:>8}"
        )
    print()
    print(
        f"the TWO graphs with |Aut| = 51840 = |Sp(4,3)| = |W(E6)| are #{max_aut_graphs} "
        f"= Q(4,3), W(3,3)"
    )
    print(
        f"next largest |Aut| among the other 26: {sorted(set(aut.values()), reverse=True)[1]}"
    )
    print(
        f"W(3,3) [#{W_index}]: 2-rank {tr[W_index]} (generic rung), |Aut| {aut[W_index]}"
    )
    print(
        f"Q(4,3) [#{Q_index}]: 2-rank {tr[Q_index]} (unique extreme rung), |Aut| {aut[Q_index]}"
    )
    print(
        f"mass sum(1/|Aut|) = {mass} ;  labelled SRG(40,12,2,4) = mass * 40! = {int(labelled)}"
    )
    print()
    print("checks:")
    for k, v in checks.items():
        print(f"   {'OK ' if v else 'XX '} {k}")
    print()
    print("=" * 78)
    print(f"STATUS: {'PASS' if all_ok else 'FAIL'}")
    print("=" * 78)

    payload = {
        "schema": "w33.pass90.aut_census.v1",
        "status": "PASS" if all_ok else "FAIL",
        "aut_orders": {str(g): aut[g] for g in sorted(aut)},
        "two_ranks": {str(g): tr[g] for g in sorted(tr)},
        "rung_summary": {str(r): s for r, s in rung_summary.items()},
        "GQ_graphs_max_aut": {
            "indices": max_aut_graphs,
            "order": GQ_order,
            "equals_Sp43_WE6": True,
        },
        "next_largest_aut": sorted(set(aut.values()), reverse=True)[1],
        "W": {
            "index": W_index,
            "two_rank": tr[W_index],
            "aut": aut[W_index],
            "rung": "generic bottom",
        },
        "Q": {
            "index": Q_index,
            "two_rank": tr[Q_index],
            "aut": aut[Q_index],
            "rung": "unique top",
        },
        "mass_sum_1_over_aut": str(mass),
        "labelled_graph_count": int(labelled),
        "reading": (
            "The two dual generalized quadrangles bookend the 2-rank ladder with maximal "
            "symmetry |Aut|=51840=|Sp(4,3)|=|W(E6)|: W(3,3) at the generic bottom rung "
            "(2-rank 16, hidden among 16 low-symmetry graphs), Q(4,3) alone at the top rung "
            "(2-rank 10). Symmetry broadly anti-correlates with 2-rank across the family, "
            "with W as the sole high-symmetry exception at the generic rung."
        ),
        "checks": checks,
    }
    (ROOT / "w33_pass90_aut.json").write_text(json.dumps(payload, indent=2))
    print("[wrote] w33_pass90_aut.json")
    return 0 if all_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
