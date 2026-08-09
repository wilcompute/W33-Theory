#!/usr/bin/env python3
"""Pass 4532 -- exact fusion of the Borel gauge cell with the protected 240-edge action.

Pass 4513 identifies the protected 240-set equivariantly with the 240 edges of
the dual-W33 line graph.  Pass 4510 identifies the optimal flag-gauge support
with the closed neighborhood S of the fixed line, inducing K1 join 4K3.
This pass computes the exact Borel orbits on those 240 edges and their position
relative to S.

Result: orbit sizes are 3,3,9,9,27,27,81,81.  The first four are the 24 edges
inside S; the 27+81 pair touching S gives 108 boundary edges; the other 27+81
pair gives 108 exterior edges.
"""
from __future__ import annotations

import json
from collections import Counter
from pathlib import Path

from w33_apartment_section_core import (
    build_geometry, build_line_perm, perm_group, transvection_matrix,
)

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data/PART_W33_PASS4532_BOREL_EDGE_LOCAL_CELL_FUSION.json"


def main() -> int:
    pts, pidx, lines, lidx, _Apoint, Astar, *_ = build_geometry()
    trans = [build_line_perm(transvection_matrix(v), pts, pidx, lines, lidx) for v in pts]
    gens = []
    G = {tuple(range(40))}
    for g in trans:
        trial = perm_group(gens + [g], 40)
        if len(trial) > len(G):
            gens.append(g); G = trial
        if len(G) == 25920:
            break
    assert len(G) == 25920

    pencils = [frozenset(i for i, L in enumerate(lines) if p in L) for p in range(40)]
    pencil_index = {S: i for i, S in enumerate(pencils)}
    def point_image(g, p):
        return pencil_index[frozenset(g[i] for i in pencils[p])]

    fp, fl = min((p, li) for li, L in enumerate(lines) for p in L)
    H = {g for g in G if g[fl] == fl and point_image(g, fp) == fp}
    assert len(H) == 162

    S = {fl} | set(int(x) for x in Astar[fl].nonzero()[0])
    c4504 = json.loads((ROOT / "data/PART_W33_PASS4504_MINIMAL_FLAG_SECTION.json").read_text())
    assert S == set(c4504["optimum"]["union"])
    assert len(S) == 13

    # Borel vertex orbits.
    rem = set(range(40)); vertex_orbits = []
    while rem:
        x = min(rem)
        orb = {g[x] for g in H}
        vertex_orbits.append(sorted(orb)); rem -= orb
    vertex_orbits.sort(key=lambda o: (len(o), o))
    assert [len(o) for o in vertex_orbits] == [1,3,9,27]
    vtype = {x: i for i, o in enumerate(vertex_orbits) for x in o}

    edges = {(i,j) for i in range(40) for j in range(i+1,40) if Astar[i,j]}
    assert len(edges) == 240
    rem = set(edges); rows = []
    while rem:
        e = min(rem)
        orb = {tuple(sorted((g[e[0]], g[e[1]]))) for g in H}
        rem -= orb
        inS = Counter(sum(x in S for x in a) for a in orb)
        type_profile = Counter(tuple(sorted((vtype[a[0]], vtype[a[1]]))) for a in orb)
        assert len(inS) == 1 and len(type_profile) == 1
        endpoints_in_cell = next(iter(inS))
        loc = {2: "internal", 1: "boundary", 0: "exterior"}[endpoints_in_cell]
        rows.append({
            "orbit_size": len(orb),
            "representative": list(e),
            "stabilizer_order_in_Borel": 162 // len(orb),
            "cell_location": loc,
            "endpoints_in_13_line_cell": endpoints_in_cell,
            "vertex_orbit_types": list(next(iter(type_profile))),
        })
    rows.sort(key=lambda r: (r["orbit_size"], r["representative"]))
    assert [r["orbit_size"] for r in rows] == [3,3,9,9,27,27,81,81]

    totals = Counter()
    for r in rows:
        totals[r["cell_location"]] += r["orbit_size"]
    assert totals == {"internal": 24, "boundary": 108, "exterior": 108}

    internal = [e for e in edges if e[0] in S and e[1] in S]
    center_spokes = [e for e in internal if fl in e]
    tangential = [e for e in internal if fl not in e]
    assert (len(internal), len(center_spokes), len(tangential)) == (24,12,12)

    out = {
        "pass": 4532,
        "Borel_order": 162,
        "fixed_flag": {"point": fp, "line": fl},
        "line_vertex_orbit_sizes": [1,3,9,27],
        "local_cell": {"size": 13, "support": sorted(S), "induced_graph": "K1 join 4K3", "internal_edges": 24, "center_spokes": 12, "triangle_edges": 12},
        "protected_edge_orbits": rows,
        "edge_location_totals": dict(totals),
        "orbit_size_identity": "240 = 2*(3+9+27+81)",
        "theorem": "Under the splitting Borel, the protected dual-W33 240-edge carrier decomposes into eight power-of-three orbits; the 13-line gauge cell contains exactly the four smallest orbits (24 edges), with 108 boundary and 108 exterior edges.",
        "boundary": "This is an exact finite Borel-orbit/locality decomposition of the Pass-4513 edge action. It is not an E8 identification, spacetime locality statement, or decoder-performance claim."
    }
    OUT.write_text(json.dumps(out, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(out, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
