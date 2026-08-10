from __future__ import annotations

import json
from pathlib import Path

import numpy as np

from scripts.ce2_global_cocycle import (
    _simple_family_sign_map,
    _heisenberg_vec_maps,
    _f3_omega,
    _f3_dot,
    _f3_k_of_direction,
)

# outer twist formulas from conversation
A = np.array([[1, 2], [2, 0]], dtype=int) % 3
b = np.array([0, 2], dtype=int) % 3


def apply_outer_h27(u: tuple[int, int], t: int) -> tuple[tuple[int, int], int]:
    up = tuple(int(x) for x in (A @ np.array(u) + b) % 3)
    x, y = u
    tp = (2 * t + (2 + 2 * x + y)) % 3
    return up, int(tp)


def branch_type(c, match, other):
    # replicate constant_line test used in the closed-form routines
    e6id_to_vec, _ = _heisenberg_vec_maps()
    uc1, uc2, zc = e6id_to_vec[int(c)]
    um1, um2, zm = e6id_to_vec[int(match)]
    uo1, uo2, zo = e6id_to_vec[int(other)]
    d1 = (int(um1) - int(uc1)) % 3
    d2 = (int(um2) - int(uc2)) % 3
    if d1 == 0 and d2 == 0:
        raise ValueError("zero direction")
    w = _f3_omega((uc1, uc2), (d1, d2))
    # constant line when d1 !=0 and w == k(d)
    if d1 != 0 and int(w) == _f3_k_of_direction((d1, d2)):
        return "constant"
    return "weil"


def test_outer_twist_pushes_ce2_sign():
    # compute permutation P on e6 ids by reading the certified outer bundle
    bundle = Path("H27_OUTER_TWIST_ACTION_BUNDLE_v01")
    perm_data = json.loads((bundle / "perm40_and_H27_pg_ids.json").read_text(encoding="utf-8"))
    perm_pg = {int(k): int(v) for k, v in perm_data["perm_on_H27_pg_ids"].items()}

    # convert pg ids -> vertex_id using fusion bundle
    FUSION_DIR = Path("H27_CE2_FUSION_BRIDGE_BUNDLE_v01")
    import pandas as pd
    df_pg = pd.read_csv(FUSION_DIR / "pg_point_to_h27_vertex_coords.csv")
    pg_to_vid = {int(r.pg_id): int(r.vertex_id) for r in df_pg.itertuples(index=False)}

    coords = pd.read_csv(FUSION_DIR / "H27_v0_0_heisenberg_coords.csv")
    vid_to_xyz = {int(r.vertex): (int(r.x), int(r.y), int(r.t)) for r in coords.itertuples(index=False)}

    # E6-id -> vid via schlafli artifact
    sch = json.loads((Path("artifacts") / "schlafli_e6id_to_w33_h27.json").read_text(encoding="utf-8"))
    e6_to_vid = list(sch["maps"]["e6id_to_w33_bundle"])
    vid_to_e6 = {v: i for i, v in enumerate(e6_to_vid)}

    # now form permutation
    perm = [None] * 27
    for e6 in range(27):
        v = e6_to_vid[e6]
        # map vertex by outer permutation on pg ids -> vertex
        # find pg corresponding to this vertex
        # we need inverse of pg_to_vid
        inv_vid = {v: pg for pg, v in pg_to_vid.items()}
        pg = inv_vid[v]
        pg2 = perm_pg[pg]
        v2 = pg_to_vid[pg2]
        perm[e6] = vid_to_e6[v2]

    # verify bijection
    assert set(perm) == set(range(27))

    sign_map = _simple_family_sign_map()
    ratios = {+1: 0, -1: 0}
    branch_ratios = {"constant": {+1:0, -1:0}, "weil": {+1:0, -1:0}}

    skipped = 0
    for (c,m,o), s in sign_map.items():
        c2 = perm[c]
        m2 = perm[m]
        o2 = perm[o]
        if (c2, m2, o2) not in sign_map:
            skipped += 1
            continue
        s2 = sign_map[(c2,m2,o2)]
        r = int(s2) * int(s)
        ratios[r] += 1
        br = branch_type(c,m,o)
        branch_ratios[br][r] += 1

    # expected regression counts with current canonical bundle
    assert skipped == 510
    assert ratios[+1] == 156 and ratios[-1] == 198
    assert ratios[+1] + ratios[-1] == 354
    assert branch_ratios["constant"][+1] == 34
    assert branch_ratios["constant"][ -1] == 32
    assert branch_ratios["weil"][+1] == 122
    assert branch_ratios["weil"][ -1] == 166

    print("skipped", skipped)
    print("ratios", ratios)
    print("branch breakdown", branch_ratios)