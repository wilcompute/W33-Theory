#!/usr/bin/env python3
"""Pass 4528 -- exact overgroup lattice above the splitting flag/Borel.

Pass 4519 identified the canonical incident flag stabilizer H (order 162) with
the Sylow-3 normalizer/Borel in the exact PSp(4,3) action.  This pass computes
all H-double cosets in G and, for one representative g of each, the generated
overgroup <H,g>.  This is an exact classification of overgroups containing H:
only H, the point parabolic, the line parabolic, and G occur.

The apartment-extension section system is then recomputed for those four groups.
H splits; both order-648 parabolics and G are nonsplit.  Hence H is maximal by
inclusion among splitting overgroups which contain this canonical Borel.

Boundary: this does not enumerate every unrelated subgroup of PSp(4,3), so it
does not claim that 162 is the largest possible order of an arbitrary splitting
subgroup.
"""
from __future__ import annotations

import json
from pathlib import Path

from w33_apartment_section_core import (
    actions_from_line_gens, build_geometry, build_line_perm, perm_group,
    quotient_model, section_system, small_generating_set, transvection_matrix,
)

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data/PART_W33_PASS4528_BOREL_OVERGROUP_SPLITTING.json"


def compose(p, q):
    return tuple(p[q[i]] for i in range(len(p)))


def main() -> int:
    pts, pidx, lines, lidx, _Apoint, Astar, *_ = build_geometry()
    line_trans = [build_line_perm(transvection_matrix(v), pts, pidx, lines, lidx) for v in pts]

    chosen = []
    G = {tuple(range(40))}
    for i, lp in enumerate(line_trans):
        trial = perm_group([line_trans[j] for j in chosen] + [lp], 40)
        if len(trial) > len(G):
            chosen.append(i)
            G = trial
        if len(G) == 25920:
            break
    assert len(G) == 25920

    fp, fl = min((p, li) for li, L in enumerate(lines) for p in L)
    pencils = [frozenset(i for i, L in enumerate(lines) if p in L) for p in range(40)]
    pindex = {S: i for i, S in enumerate(pencils)}
    def induced_point_at_flag(g):
        return pindex[frozenset(g[i] for i in pencils[fp])]

    H = {g for g in G if g[fl] == fl and induced_point_at_flag(g) == fp}
    Ppoint = {g for g in G if induced_point_at_flag(g) == fp}
    Pline = {g for g in G if g[fl] == fl}
    assert (len(H), len(Ppoint), len(Pline), len(Ppoint & Pline)) == (162, 648, 648, 162)
    assert Ppoint & Pline == H

    Hgens = small_generating_set(H, 40)
    _K, Ereps, Vreps, coordE, coordV, Pi = quotient_model(Astar)

    remaining = set(G)
    rows = []
    while remaining:
        g = min(remaining)
        D = {compose(compose(h1, g), h2) for h1 in H for h2 in H}
        remaining -= D
        O = perm_group(Hgens + [g], 40)
        if O == H:
            label = "Borel_flag_162"
        elif O == Ppoint:
            label = "point_parabolic_648"
        elif O == Pline:
            label = "line_parabolic_648"
        elif O == G:
            label = "full_PSp_25920"
        else:
            raise AssertionError(f"unexpected overgroup order {len(O)}")
        Ogens = small_generating_set(O, 40)
        GE, GV = actions_from_line_gens(Ogens, Ereps, Vreps, coordE, coordV)
        sys = section_system(Pi, GE, GV)
        rows.append({
            "double_coset_size": len(D),
            "generated_overgroup": label,
            "overgroup_order": len(O),
            "section_rank_coefficient": sys["rank_coefficient"],
            "section_rank_augmented": sys["rank_augmented"],
            "split": sys["consistent"],
            "section_affine_dimension": sys["affine_dimension"],
        })

    rows.sort(key=lambda r: (r["double_coset_size"], r["overgroup_order"], r["generated_overgroup"]))
    assert len(rows) == 8
    assert sum(r["double_coset_size"] for r in rows) == 25920
    assert [r["double_coset_size"] for r in rows] == [162,486,486,1458,1458,4374,4374,13122]
    assert {r["generated_overgroup"] for r in rows} == {
        "Borel_flag_162", "point_parabolic_648", "line_parabolic_648", "full_PSp_25920"
    }
    split_rows = [r for r in rows if r["split"]]
    assert len(split_rows) == 1 and split_rows[0]["generated_overgroup"] == "Borel_flag_162"

    out = {
        "pass": 4528,
        "group_order": 25920,
        "flag": {"point": fp, "line": fl, "order": 162},
        "overgroup_orders": {"Borel": 162, "point_parabolic": 648, "line_parabolic": 648, "G": 25920},
        "H_double_cosets": rows,
        "theorem": "Every overgroup of the canonical flag/Borel is H, one of the two order-648 maximal parabolics, or G; H is the unique splitting member of this overgroup interval.",
        "structural_reading": "The symmetry breaking is chamber-minimal in the exact overgroup lattice: adjoining any element outside H either restores one simple-root parabolic or generates all of PSp(4,3), and the apartment extension obstruction immediately returns.",
        "boundary": "Exact for overgroups containing this canonical Borel. It is not a census of all subgroup conjugacy classes and does not prove a global maximum splitting-subgroup order."
    }
    OUT.write_text(json.dumps(out, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(out, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
