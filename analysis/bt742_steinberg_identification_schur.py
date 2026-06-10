#!/usr/bin/env python3
"""
BT742 - chart81 and Levi E4 are BOTH the Steinberg representation;
        selector uniqueness IS Schur's lemma.

GAP INPUT (verified, CharacterTable("U4(2)")):
    CharacterDegrees = [[1,1],[5,2],[6,1],[10,2],[15,2],[20,1],[24,1],
                        [30,3],[40,2],[45,2],[60,1],[64,1],[81,1]]
    => U4(2) = PSp(4,3) has EXACTLY ONE irreducible of degree 81:
       the Steinberg representation St (dim q^(n^2) = 3^4 = 81).
    => minimal nontrivial degree is 5 (this also re-proves the BT739
       forcing argument).

STRATEGY (pure permutation counting -- no projector arithmetic):

  1. Enumerate U4(2) as the 25920 point-permutations of the 40 points of
     W(3,3) (image of Sp(4,3); the center +-I acts trivially), by BFS over
     symplectic transvections t_v(x) = x + omega(x,v) v.

  2. The Levi cycle space (= image of the Hodge idempotent E4, dim 81) sits
     in the exact sequence of G-modules
         0 -> Cycle -> F[flags] -> F[points + lines] -> F(trivial) -> 0,
     which is G-equivariant because Sp(4,3) preserves the bipartition
     (points never map to lines), so with all flags oriented point->line the
     signed and unsigned flag permutation modules coincide.  Hence
         chi_E4(g) = #fixed_flags(g) - #fixed_Levi_vertices(g) + 1.

  3. <chi_E4, chi_E4> = 1  =>  E4 irreducible; dim 81 + GAP uniqueness
     =>  E4 = Steinberg.

  4. <chi_chart, chi_E4> = multiplicity of St in the 240-chart permutation
     module.  If it equals 1, St embeds in exactly one HH^T eigenspace; the
     eigenspace dims are {1, 24, 75, 81, 24, 35} (BT700) and only the 81 can
     contain an 81-dim irreducible; therefore chart81 = St exactly.

  5. Schur's lemma: dim Hom_G(chart81, CycleSpace) = dim Hom_G(St, St) = 1.
     Consequences:
       * the BT714/BT715 bridge intertwiner is UNIQUE up to scalar -- the
         BT720 orbit-uniqueness theorem is Schur's lemma in disguise;
       * any nonzero equivariant map chart81 -> cycle space is injective --
         the BT739 full-rank theorem is also Schur's lemma.

  Bonus diagnostics: <chi_chart, chi_chart>, <chi_flag, chi_flag>,
  <chi_chart, 1>, <chi_flag, 1>, <chi_E4, 1>, and the point-permutation
  character norm, with their representation-theoretic readings.
"""
from __future__ import annotations

from collections import Counter, defaultdict
from itertools import combinations
import json


def inv3(a: int) -> int:
    a %= 3
    if a == 1:
        return 1
    if a == 2:
        return 2
    raise ZeroDivisionError


def canon(v):
    for x in v:
        if x % 3:
            c = inv3(x)
            return tuple((c * y) % 3 for y in v)
    raise ValueError("zero vector")


def points():
    return sorted({
        canon((a, b, c, d))
        for a in range(3) for b in range(3) for c in range(3) for d in range(3)
        if (a, b, c, d) != (0, 0, 0, 0)
    })


def symp(x, y) -> int:
    return (x[0]*y[2] - x[2]*y[0] + x[1]*y[3] - x[3]*y[1]) % 3


def main() -> None:
    pts = points()
    n = 40
    pt_index = {p: i for i, p in enumerate(pts)}

    # --- transvection generators t_v(x) = x + omega(x, v) v --------------
    def transvection_perm(v):
        perm = []
        for x in pts:
            w = symp(x, v)
            img = canon(tuple((x[k] + w * v[k]) % 3 for k in range(4)))
            perm.append(pt_index[img])
        return tuple(perm)

    gens = [transvection_perm(v) for v in pts]   # all 40 transvections

    # --- BFS enumeration of the point-permutation group ------------------
    ident = tuple(range(n))
    seen = {ident}
    frontier = [ident]
    while frontier:
        nxt = []
        for g in frontier:
            for h in gens:
                gh = tuple(h[g[i]] for i in range(n))
                if gh not in seen:
                    seen.add(gh)
                    nxt.append(gh)
        frontier = nxt
    group = sorted(seen)
    NG = len(group)
    print(f"|G| (point perms) = {NG}")
    assert NG == 25920, NG     # PSp(4,3) = U4(2)

    # --- lines, charts, flags --------------------------------------------
    adj = [[False] * n for _ in range(n)]
    for i, j in combinations(range(n), 2):
        if symp(pts[i], pts[j]) == 0:
            adj[i][j] = adj[j][i] = True
    lines = [frozenset(q) for q in combinations(range(n), 4)
             if all(adj[i][j] for i, j in combinations(q, 2))]
    assert len(lines) == 40
    line_index = {l: i for i, l in enumerate(lines)}
    through = defaultdict(list)
    for li, l in enumerate(lines):
        for p in l:
            through[p].append(li)

    charts = []
    for p in range(n):
        for li, lj in combinations(sorted(through[p]), 2):
            charts.append((p, li, lj))
    assert len(charts) == 240
    chart_index = {c: i for i, c in enumerate(charts)}

    flags = [(p, li) for li, l in enumerate(lines) for p in sorted(l)]
    assert len(flags) == 160
    flag_index = {f: i for i, f in enumerate(flags)}

    # --- characters by fixed-point counting -------------------------------
    # For each group element, compute:
    #   fp  = fixed points (40-set)
    #   fl  = fixed lines
    #   fch = fixed charts
    #   ffl = fixed flags
    # chi_E4 = ffl - (fp + fl) + 1
    sum_E4_sq = 0
    sum_E4 = 0
    sum_ch_sq = 0
    sum_ch = 0
    sum_fl_sq = 0
    sum_fl = 0
    sum_ch_E4 = 0
    sum_pt_sq = 0
    chiE4_at_1 = None

    for g in group:
        fp = sum(1 for i in range(n) if g[i] == i)
        # induced line permutation
        lperm = {}
        for li, l in enumerate(lines):
            img = frozenset(g[i] for i in l)
            lperm[li] = line_index[img]
        fl = sum(1 for li in range(40) if lperm[li] == li)
        fch = 0
        for (p, li, lj) in charts:
            if g[p] == p and {lperm[li], lperm[lj]} == {li, lj}:
                fch += 1
        ffl = sum(1 for (p, li) in flags if g[p] == p and lperm[li] == li)

        chiE4 = ffl - (fp + fl) + 1
        if g == ident:
            chiE4_at_1 = chiE4
        sum_E4 += chiE4
        sum_E4_sq += chiE4 * chiE4
        sum_ch += fch
        sum_ch_sq += fch * fch
        sum_fl += ffl
        sum_fl_sq += ffl * ffl
        sum_ch_E4 += fch * chiE4
        sum_pt_sq += fp * fp

    def ip(total):
        q, r = divmod(total, NG)
        assert r == 0, (total, NG)
        return q

    norm_E4 = ip(sum_E4_sq)
    triv_E4 = ip(sum_E4)
    norm_ch = ip(sum_ch_sq)
    triv_ch = ip(sum_ch)
    norm_fl = ip(sum_fl_sq)
    triv_fl = ip(sum_fl)
    mult_ch_E4 = ip(sum_ch_E4)
    norm_pt = ip(sum_pt_sq)

    print()
    print(f"chi_E4(1) = {chiE4_at_1}   (expect 81)")
    print(f"<chi_E4, chi_E4>     = {norm_E4}   (1 <=> irreducible)")
    print(f"<chi_E4, 1>          = {triv_E4}   (0 <=> no trivial part)")
    print(f"<chi_chart, chi_E4>  = {mult_ch_E4}   (multiplicity of St in chart module)")
    print(f"<chi_chart, chi_chart> = {norm_ch}  (commutant dim of chart module)")
    print(f"<chi_chart, 1>       = {triv_ch}   (orbit count = 1)")
    print(f"<chi_flag, chi_flag> = {norm_fl}   (commutant dim of flag module)")
    print(f"<chi_flag, 1>        = {triv_fl}")
    print(f"<chi_point, chi_point> = {norm_pt} (rank of W33 scheme = 3)")

    assert chiE4_at_1 == 81
    assert norm_E4 == 1
    assert triv_E4 == 0
    assert mult_ch_E4 == 1

    print()
    print("=" * 70)
    print("THEOREM CHAIN (BT742)")
    print("=" * 70)
    print("1. <chi_E4,chi_E4>=1, dim 81: Levi cycle space is IRREDUCIBLE.")
    print("   GAP: U4(2) has a unique degree-81 irreducible = Steinberg.")
    print("   => Levi E4 sector IS the Steinberg representation.")
    print("2. <chi_chart,chi_E4>=1: St appears EXACTLY ONCE in the chart")
    print("   module.  HH^T eigenspace dims are {1,24,75,81,24,35}; only the")
    print("   81-dim eigenspace can contain an 81-dim irreducible.")
    print("   => chart81 IS the Steinberg representation.")
    print("3. Schur: dim Hom_G(chart81, LeviCycle) = dim Hom(St, St) = 1.")
    print("   * The chart81 -> LeviE4 bridge is UNIQUE up to scalar:")
    print("     BT720's selector-orbit uniqueness IS Schur's lemma.")
    print("   * Any nonzero equivariant map chart81 -> cycle space is")
    print("     injective: BT739's full-rank theorem IS Schur's lemma.")
    print("4. The substrate identity 81 = q^mu = Steinberg dim (BT538) is")
    print("   not numerology: both protected 81-sectors are THE Steinberg")
    print("   module of the substrate automorphism group.")

    out = {
        "theorem": "BT742 chart81 = LeviE4 = Steinberg; uniqueness = Schur",
        "group_order_psp43": NG,
        "gap_character_degrees_u42": [[1,1],[5,2],[6,1],[10,2],[15,2],[20,1],
                                      [24,1],[30,3],[40,2],[45,2],[60,1],
                                      [64,1],[81,1]],
        "chi_E4_degree": chiE4_at_1,
        "norm_chi_E4": norm_E4,
        "trivial_in_E4": triv_E4,
        "mult_St_in_chart_module": mult_ch_E4,
        "commutant_dim_chart_module": norm_ch,
        "orbits_on_charts": triv_ch,
        "commutant_dim_flag_module": norm_fl,
        "orbits_on_flags": triv_fl,
        "w33_scheme_rank": norm_pt,
        "consequences": [
            "LeviE4 = Steinberg (unique deg-81 irrep of U4(2))",
            "chart81 = Steinberg (multiplicity one + eigenspace dims)",
            "BT720 uniqueness = Schur's lemma",
            "BT739 full rank = Schur's lemma",
        ],
    }
    with open("data/bt742_steinberg_identification_schur.json", "w") as f:
        json.dump(out, f, indent=2)
    print("\nwrote data/bt742_steinberg_identification_schur.json")


if __name__ == "__main__":
    main()
