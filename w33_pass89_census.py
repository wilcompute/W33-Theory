#!/usr/bin/env python3
"""
Pass 89 -- The arithmetic census of the 28 SRG(40,12,2,4) graphs: Smith and critical groups.

Pass 88 separated the two GQ(3,3) graphs W(3,3)/Q(4,3) by their Smith group (coker A), critical
group (coker L), and 2-rank.  This pass computes ALL of them for ALL 28 Spence graphs (GAP Smith
normal forms of A and L, w33_pass89_census.g over McKay's graph6 list) and reads off the census.

Results.
  * There are exactly 4 distinct Smith groups and 4 distinct critical groups, with the SAME
    distribution {17, 8, 2, 1} -- and it coincides graph-for-graph with the 2-rank partition
    {16:17, 14:8, 12:2, 10:1}.  So the 2-rank, the Smith group, and the critical group all induce
    the SAME 4-class partition of the 28.
  * Every critical group has 5-Sylow (Z/5)^23 -- constant across the family.  This is Ducey's
    theorem: the Sylow-p subgroup of the critical group of an SRG is determined by (v,k,lambda,mu)
    unless p | (r-s); here r-s = 2-(-4) = 6 = 2*3, so only p=2 is "difficult", and indeed all the
    variation lives in the 2-part.
  * The two generalized quadrangles sit at OPPOSITE extremes of the 2-rank spectrum: the symplectic
    W(3,3) is the generic graph (2-rank 16, shared with 16 others), while its dual, the parabolic
    quadric Q(4,3), is the UNIQUE extreme (2-rank 10, alone).

Grounding: Brouwer-van Eijl (p-ranks of SRGs), Ducey (critical-group p-part from parameters unless
p | r-s), Peter Sin (Smith normal forms of SRGs), Spence (the 28 graphs).

ASCII-only.  Reads the committed GAP census certificate.
"""
from __future__ import annotations

import json
import re
from collections import Counter
from math import prod
from pathlib import Path

ROOT = Path(__file__).resolve().parent
CENSUS = ROOT / "w33_pass89_census_out.txt"


def parse_census():
    rows = []
    for line in CENSUS.read_text().splitlines():
        if not line.strip():
            continue
        g = int(re.search(r"graph=(\d+)", line).group(1))
        a = [int(x) for x in re.search(r"smithA=\[(.*?)\]", line).group(1).split(",")]
        l = [int(x) for x in re.search(r"smithL=\[(.*?)\]", line).group(1).split(",")]
        rows.append((g, a, l))
    return rows


def factors(diag):
    return tuple(sorted(d for d in diag if d > 1))  # invariant factors > 1 (drop 0/1)


def struct(fac):
    return dict(sorted(Counter(fac).items()))


def two_rank(diag_a):
    return sum(1 for d in diag_a if d == 1)  # #units over Z ~ 2-rank via 1s (odd part)


def two_rank_from_factors(fac):
    # fac = invariant factors > 1 (all even here); 2-rank = 40 - #even elementary divisors
    return 40 - sum(1 for d in fac if d % 2 == 0)


def five_sylow(fac):
    c = Counter()
    for d in fac:
        f = 1
        while d % 5 == 0:
            d //= 5
            f *= 5
        if f > 1:
            c[f] += 1
    return dict(sorted(c.items()))


def main():
    rows = parse_census()
    smith_class = {}  # smith factors -> list of graph indices
    crit_class = {}
    two_ranks = {}
    per_graph = {}
    for g, a, l in rows:
        S = factors(a)
        K = factors(l)
        smith_class.setdefault(S, []).append(g)
        crit_class.setdefault(K, []).append(g)
        two_ranks[g] = two_rank(a)
        per_graph[g] = (S, K)

    # do Smith and critical partitions coincide graph-for-graph?
    smith_partition = {frozenset(v) for v in smith_class.values()}
    crit_partition = {frozenset(v) for v in crit_class.values()}
    partitions_coincide = smith_partition == crit_partition
    # 2-rank partition
    tr_class = {}
    for g, r in two_ranks.items():
        tr_class.setdefault(r, []).append(g)
    tr_partition = {frozenset(v) for v in tr_class.values()}
    all_three_coincide = smith_partition == crit_partition == tr_partition

    # 5-Sylow constant?
    five_sylows = {tuple(sorted(five_sylow(K).items())) for K in crit_class}
    five_constant = len(five_sylows) == 1 and list(five_sylows)[0] == ((5, 23),)

    W_index, Q_index = 28, 27  # in McKay's graph6 order for this file
    W_class_size = len(smith_class[per_graph[W_index][0]])
    Q_class_size = len(smith_class[per_graph[Q_index][0]])

    # --- the graded 2-adic transfer ladder (Wil's observation) ---
    # order the 4 Smith groups by descending 2-rank (16,14,12,10) and read the factor counts
    smith_by_rank = sorted(smith_class, key=lambda S: -two_rank_from_factors(S))
    ladder = []
    for S in smith_by_rank:
        st = struct(S)
        ladder.append(
            {
                "two_rank": two_rank_from_factors(S),
                "count": len(smith_class[S]),
                "Z2": st.get(2, 0),
                "Z4": st.get(4, 0),
                "Z8": st.get(8, 0),
                "Z24": st.get(24, 0),
            }
        )
    z2 = [r["Z2"] for r in ladder]
    z4 = [r["Z4"] for r in ladder]
    z8 = [r["Z8"] for r in ladder]
    ranks = [r["two_rank"] for r in ladder]

    # arithmetic progressions: Z2 +2, Z4 +2, Z8 -2, 2-rank -2; transfer count 0,2,4,6
    def is_ap(seq, step):
        return all(seq[i + 1] - seq[i] == step for i in range(len(seq) - 1))

    ladder_ok = (
        is_ap(z2, 2)
        and is_ap(z4, 2)
        and is_ap(z8, -2)
        and is_ap(ranks, -2)
        and z2 == [8, 10, 12, 14]
        and z8 == [15, 13, 11, 9]
    )
    transfer_counts = [
        16 - r for r in ranks
    ]  # entries transferred each side: 0,2,4,6 (Q=6 matches Pass 88)

    # --- the SAME ladder in the critical groups (2nd observation) ---
    # match each Smith class to its critical class (partitions coincide), ordered by 2-rank
    crit_ladder = []
    for S in smith_by_rank:
        g0 = smith_class[S][0]
        K = per_graph[g0][1]
        kt = struct(K)
        crit_ladder.append(
            {
                "two_rank": two_rank_from_factors(S),
                "Z2": kt.get(2, 0),
                "Z10": kt.get(10, 0),
                "Z40": kt.get(40, 0),
                "Z80": kt.get(80, 0),
                "Z160": kt.get(160, 0),
            }
        )
    c2 = [r["Z2"] for r in crit_ladder]
    c10 = [r["Z10"] for r in crit_ladder]
    c40 = [r["Z40"] for r in crit_ladder]
    c80 = [r["Z80"] for r in crit_ladder]
    c160 = [r["Z160"] for r in crit_ladder]
    crit_ladder_ok = (
        c2 == [0, 2, 4, 6]
        and c80 == [0, 2, 4, 6]
        and c160 == [14, 12, 10, 8]
        and c10 == [8, 8, 8, 8]
        and c40 == [1, 1, 1, 1]
    )

    checks = {
        "28_graphs": len(rows) == 28,
        "4_distinct_smith_groups": len(smith_class) == 4,
        "4_distinct_critical_groups": len(crit_class) == 4,
        "smith_and_critical_partitions_coincide": partitions_coincide,
        "2rank_partition_matches_too": all_three_coincide,
        "class_sizes_17_8_2_1": sorted(
            (len(v) for v in smith_class.values()), reverse=True
        )
        == [17, 8, 2, 1],
        "5_sylow_constant_Z5^23": five_constant,
        "W_generic_class_17": W_class_size == 17,
        "Q_unique_extreme_class_1": Q_class_size == 1,
        "smith_graded_2adic_transfer_ladder": ladder_ok,
        "critical_graded_2adic_transfer_ladder": crit_ladder_ok,
    }
    all_ok = all(checks.values())

    print("=" * 78)
    print("PASS 89 -- ARITHMETIC CENSUS OF THE 28 SRG(40,12,2,4) GRAPHS")
    print("=" * 78)
    print(f"distinct Smith groups (coker A): {len(smith_class)}")
    for S, gs in sorted(smith_class.items(), key=lambda x: -len(x[1])):
        print(f"   x{len(gs):<2} 2-rank {two_ranks[gs[0]]:<2} : {struct(S)}")
    print(f"distinct critical groups (coker L): {len(crit_class)}")
    for K, gs in sorted(crit_class.items(), key=lambda x: -len(x[1])):
        print(f"   x{len(gs):<2} : {struct(K)}")
    print()
    print(
        f"Smith / critical / 2-rank all induce the SAME 4-partition: {all_three_coincide}"
    )
    print(
        f"class sizes: {sorted((len(v) for v in smith_class.values()), reverse=True)}"
    )
    print(
        f"every critical group has 5-Sylow (Z/5)^23 (Ducey, 5 does not divide r-s=6): {five_constant}"
    )
    print(
        f"W(3,3) [#{W_index}] is generic (class size {W_class_size}); "
        f"Q(4,3) [#{Q_index}] is the unique extreme (class size {Q_class_size})"
    )
    print()
    print(
        "The graded 2-adic transfer LADDER (ordered by 2-rank 16,14,12,10; transfer count "
        f"{transfer_counts}):"
    )
    print(
        f"   Smith    Z/2 counts {z2} (+2),  Z/4 {z4} (+2),  Z/8 {z8} (-2),  Z/24 const  [{ladder_ok}]"
    )
    print(
        f"   Critical Z/2 {c2} (+2),  Z/80 {c80} (+2),  Z/160 {c160} (-2),  Z/10={c10} Z/40={c40} "
        f"const  [{crit_ladder_ok}]"
    )
    print(
        "   each rung = the Pass-88 balanced transfer applied k more times (1->2 up, 8->4 down);"
    )
    print(
        "   the 5-part (Z/10, Z/40 = 2*5, 8*5) is constant, so the ladder is purely 2-adic."
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
        "schema": "w33.pass89.census.v1",
        "status": "PASS" if all_ok else "FAIL",
        "num_graphs": len(rows),
        "smith_groups": [
            {
                "structure": struct(S),
                "count": len(gs),
                "graphs": sorted(gs),
                "two_rank": two_ranks[gs[0]],
            }
            for S, gs in sorted(smith_class.items(), key=lambda x: -len(x[1]))
        ],
        "critical_groups": [
            {"structure": struct(K), "count": len(gs), "graphs": sorted(gs)}
            for K, gs in sorted(crit_class.items(), key=lambda x: -len(x[1]))
        ],
        "partitions_coincide_smith_critical_2rank": all_three_coincide,
        "class_sizes": sorted((len(v) for v in smith_class.values()), reverse=True),
        "graded_transfer_ladder": {
            "ordered_by_two_rank": ranks,
            "transfer_count_from_W": transfer_counts,
            "smith": {"Z2": z2, "Z4": z4, "Z8": z8, "arithmetic_ok": ladder_ok},
            "critical": {
                "Z2": c2,
                "Z10_const": c10,
                "Z40_const": c40,
                "Z80": c80,
                "Z160": c160,
                "arithmetic_ok": crit_ladder_ok,
            },
            "reading": (
                "The 4 Smith groups and 4 critical groups each form an arithmetic ladder in "
                "their 2-adic factor counts: Z/2 +2, Z/4 (Smith) / Z/80 (critical) +2, "
                "Z/8 (Smith) / Z/160 (critical) -2 per rung. Each rung is the Pass-88 "
                "balanced 2-adic transfer applied one more time (transfer count 0,2,4,6). "
                "The 5-carrying factors (Z/10,Z/40) stay constant, so the whole family of "
                "28 is stratified into 4 rungs of a purely 2-adic transfer ladder, with "
                "W(3,3) at the bottom (generic) and Q(4,3) at the top (unique)."
            ),
        },
        "five_sylow_constant_Z5_23": five_constant,
        "W_index": W_index,
        "W_class_size": W_class_size,
        "Q_index": Q_index,
        "Q_class_size": Q_class_size,
        "ducey": "5-part parameter-determined (5 does not divide r-s=6); 2-part is the only variable prime",
        "literature": [
            "Brouwer-van Eijl (p-ranks of SRGs)",
            "Ducey (critical group from SRG parameters)",
            "Peter Sin (Smith normal forms of SRGs)",
            "Spence (the 28 SRG(40,12,2,4) graphs)",
        ],
        "checks": checks,
    }
    (ROOT / "w33_pass89_census.json").write_text(json.dumps(payload, indent=2))
    print("[wrote] w33_pass89_census.json")
    return 0 if all_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
