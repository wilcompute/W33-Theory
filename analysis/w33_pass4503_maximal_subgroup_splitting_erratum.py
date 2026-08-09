#!/usr/bin/env python3
"""Pass 4503 -- maximal-subgroup splitting census and Pass-4493 erratum.

The full apartment extension is

    0 -> K/J (29) -> E=M/J (39) -> V=M/K=H10 (10) -> 0.

Pass 4493 correctly reproduced the full-group nonsplitting rank 389/390, but its
reported restricted point/line/flag/apartment section ranks do not reproduce
from its own current exact dependencies.  This pass rebuilds every object from
GF(3)^4, reruns the exact section equations, and extends the audit to all five
maximal subgroup types of PSp(4,3) ~= U4(2).

Exact results:

  maximal subgroup representative        order   rank A / aug   split
  2^4:A5 (index 27)                       960       388 / 389      NO
  spread stabilizer S6 (index 36)          720       386 / 387      NO
  line stabilizer (index 40)               648       386 / 387      NO
  point stabilizer (index 40)              648       387 / 388      NO
  class-45 involution centralizer (45)      576       386 / 387      NO

Thus the extension remains nonsplit on EVERY maximal subgroup type.  In
particular, the old claim that fixing one point or one line already selects an
equivariant 10D complement is false.

The canonical incident-flag stabilizer, order 162, DOES split:

    rank A = rank aug = 384, affine section-family dimension = 6.

So the corrected natural geometric statement is only that a flag stabilizer is
a verified splitting subgroup.  This pass does not classify every subgroup and
does not claim order 162 is globally maximal among all splitting subgroups.
"""
from __future__ import annotations

import itertools
import json
import random
from collections import deque
from pathlib import Path

import numpy as np

from w33_pass4493_symmetry_breaking_section_threshold import (
    actions_from_line_gens,
    build_geometry,
    build_line_perm,
    compose,
    fixed_dimension,
    line_perm_from_point_perm,
    perm_group,
    point_perm_from_matrix,
    quotient_model,
    section_system,
    small_generating_set,
    transvection_matrix,
)

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "PART_W33_PASS4503_MAXIMAL_SUBGROUP_SPLITTING_ERRATUM.json"


def generated_limited(gens, n=40, limit=2000):
    ident = tuple(range(n))
    seen = {ident}
    q = deque([ident])
    while q:
        g = q.popleft()
        for h in gens:
            k = compose(h, g)
            if k not in seen:
                seen.add(k)
                if len(seen) > limit:
                    return seen
                q.append(k)
    return seen


def enumerate_spreads(lines):
    by_point = [[] for _ in range(40)]
    for li, line in enumerate(lines):
        for p in line:
            by_point[p].append(li)
    spreads = []

    def rec(chosen, used):
        if len(chosen) == 10:
            spreads.append(tuple(chosen))
            return
        p = next(i for i in range(40) if i not in used)
        for li in by_point[p]:
            line = set(lines[li])
            if not (line & used):
                rec(chosen + [li], used | line)

    rec([], set())
    return spreads


def subgroup_stats(group, Ereps, Vreps, coordE, coordV, Pi):
    gens = small_generating_set(group, 40)
    GE, GV = actions_from_line_gens(gens, Ereps, Vreps, coordE, coordV)
    sec = section_system(Pi, GE, GV)
    return {
        "order": len(group),
        "index": 25920 // len(group),
        "generators_used": len(gens),
        "fixed_dim_E39": fixed_dimension(GE, 39),
        "fixed_dim_V10": fixed_dimension(GV, 10),
        "rank_coefficient": sec["rank_coefficient"],
        "rank_augmented": sec["rank_augmented"],
        "split": sec["consistent"],
        "affine_section_dimension": sec["affine_dimension"],
    }


def main() -> int:
    pts, pidx, lines, lidx, _, Astar, *_ = build_geometry()
    Astar = np.asarray(Astar, dtype=np.uint8)
    _, Ereps, Vreps, coordE, coordV, Pi = quotient_model(Astar)

    matrices = [transvection_matrix(v) for v in pts]
    point_trans = [point_perm_from_matrix(M, pts, pidx) for M in matrices]
    line_trans = [build_line_perm(M, pts, pidx, lines, lidx) for M in matrices]

    selected = []
    full_line = {tuple(range(40))}
    for i, lp in enumerate(line_trans):
        trial = perm_group([line_trans[j] for j in selected] + [lp], 40)
        if len(trial) > len(full_line):
            selected.append(i)
            full_line = trial
        if len(full_line) == 25920:
            break
    assert len(full_line) == 25920
    full_point = perm_group([point_trans[i] for i in selected], 40)
    assert len(full_point) == 25920

    line_stab = {g for g in full_line if g[0] == 0}
    point_stab_point = {g for g in full_point if g[0] == 0}
    point_stab = {line_perm_from_point_perm(g, lines, lidx) for g in point_stab_point}
    assert len(line_stab) == len(point_stab) == 648

    # Canonical flag stabilizer.
    fp, fl = min((p, li) for li, line in enumerate(lines) for p in line)
    flag_point = {
        g for g in full_point
        if g[fp] == fp and line_perm_from_point_perm(g, lines, lidx)[fl] == fl
    }
    flag_stab = {line_perm_from_point_perm(g, lines, lidx) for g in flag_point}
    assert len(flag_stab) == 162

    # The 36 W33 spreads form the canonical index-36 action; one stabilizer is S6.
    spreads = enumerate_spreads(lines)
    assert len(spreads) == 36
    spread0 = set(spreads[0])
    spread_stab = {g for g in full_line if {g[x] for x in spread0} == spread0}
    assert len(spread_stab) == 720

    # The size-45 involution class is recognized internally by 16 fixed lines;
    # its centralizer has order 25920/45 = 576.
    ident = tuple(range(40))
    involutions = [g for g in full_line if g != ident and compose(g, g) == ident]
    fixed16 = [g for g in involutions if sum(i == g[i] for i in range(40)) == 16]
    assert len(involutions) == 315 and len(fixed16) == 45
    t45 = fixed16[0]
    c576 = {g for g in full_line if compose(g, t45) == compose(t45, g)}
    assert len(c576) == 576

    # Unique maximal order-960 type 2^4:A5.  Deterministic pair search over the
    # exact 25920-element action; Pass 1443 independently identifies this class.
    glist = sorted(full_line)
    rng = random.Random(4503)
    m20 = None
    search_trial = None
    for trial in range(1000):
        a, b = rng.sample(glist, 2)
        h = generated_limited([a, b], limit=2000)
        if len(h) == 960:
            m20 = h
            search_trial = trial
            break
    assert m20 is not None and len(m20) == 960

    groups = {
        "maximal_2^4_A5_order960": m20,
        "maximal_spread_S6_order720": spread_stab,
        "maximal_line_stabilizer_order648": line_stab,
        "maximal_point_stabilizer_order648": point_stab,
        "maximal_class45_involution_centralizer_order576": c576,
        "canonical_flag_stabilizer_order162": flag_stab,
        "full_PSp4_3": full_line,
    }
    results = {
        name: subgroup_stats(group, Ereps, Vreps, coordE, coordV, Pi)
        for name, group in groups.items()
    }

    expected = {
        "maximal_2^4_A5_order960": (388, 389, False),
        "maximal_spread_S6_order720": (386, 387, False),
        "maximal_line_stabilizer_order648": (386, 387, False),
        "maximal_point_stabilizer_order648": (387, 388, False),
        "maximal_class45_involution_centralizer_order576": (386, 387, False),
        "canonical_flag_stabilizer_order162": (384, 384, True),
        "full_PSp4_3": (389, 390, False),
    }
    for name, (r, a, split) in expected.items():
        got = results[name]
        assert (got["rank_coefficient"], got["rank_augmented"], got["split"]) == (r, a, split), (name, got)
    assert results["canonical_flag_stabilizer_order162"]["affine_section_dimension"] == 6

    out = {
        "pass": 4503,
        "theorem": "all five maximal PSp(4,3) subgroup types retain the apartment-extension obstruction",
        "erratum": {
            "supersedes": "Pass 4493 restricted-subgroup ranks only",
            "still_valid_from_4493": "full PSp(4,3) rank 389/390 nonsplitting",
            "withdrawn": "point/line order-648 splitting and old flag/apartment rank table",
            "corrected_natural_split": "canonical incident-flag stabilizer order 162 splits with rank 384/384 and a 6-dimensional affine section family",
        },
        "maximal_subgroup_orders": [960, 720, 648, 648, 576],
        "all_five_maximal_types_nonsplit": all(
            not results[k]["split"] for k in list(results)[:5]
        ),
        "results": results,
        "geometry": {
            "spreads": len(spreads),
            "involutions_total": len(involutions),
            "class45_involutions": len(fixed16),
            "deterministic_M20_pair_search_trial": search_trial,
            "flag": {"point": fp, "line": fl},
        },
        "boundary": "This proves nonsplitting on every maximal subgroup type and splitting on one canonical order-162 flag stabilizer. It does not classify every subgroup or prove that 162 is the globally largest splitting order.",
    }
    OUT.write_text(json.dumps(out, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(out, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
