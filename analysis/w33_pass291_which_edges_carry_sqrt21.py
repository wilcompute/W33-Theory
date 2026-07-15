#!/usr/bin/env python3
"""Pass 291: WHICH four edges carry sqrt(21), and do they form a structure?

Pass 290 showed sqrt(21) is the unique quadratic field common to both Szilassi
realizations.  Each carries it on exactly 4 of its 21 edges.  If those 4 edges
are the SAME combinatorial set in both realizations, sqrt(21) is tied to the
Szilassi COMBINATORICS; if they differ, it is an accident of each embedding.
This is the test that decides which.

We identify the 4 sqrt(21)-carrying edges in each realization as vertex pairs,
and compare: are they the same edge set? do they form a matching, a path, a
cycle? which faces do they lie on?
"""
from __future__ import annotations
import json
from collections import Counter
from pathlib import Path
import sys
import sympy as sp
ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
from analysis.w33_pass286_sqrt21_found_retraction import (
    SZILASSI, SZILASSI_FACES, edges_of, has_sqrt21)
OUT = ROOT / "data" / "w33_pass291_which_edges_carry_sqrt21.json"

def main():
    checks = {}
    res = {}
    E = edges_of(SZILASSI_FACES)
    for ver, V in SZILASSI.items():
        marked = []
        for (a, b) in E:
            d2 = sum((V[a][k] - V[b][k]) ** 2 for k in range(3))
            L = sp.radsimp(sp.sqrt(sp.expand(d2)))
            if has_sqrt21(L):
                marked.append(((a, b), str(L)))
        edges = [e for e, _ in marked]
        deg = Counter()
        for (a, b) in edges:
            deg[a] += 1; deg[b] += 1
        # structure: matching (all deg 1)? path/cycle?
        is_matching = all(d == 1 for d in deg.values())
        # which faces contain each marked edge
        onfaces = {}
        for (a, b) in edges:
            fs = []
            for fi, f in enumerate(SZILASSI_FACES):
                for i in range(len(f)):
                    if tuple(sorted((f[i], f[(i+1) % len(f)]))) == (a, b):
                        fs.append(fi)
            onfaces[str((a, b))] = fs
        res[str(ver)] = {
            "sqrt21_edges": [list(e) for e in edges],
            "lengths": {str(e): l for e, l in marked},
            "count": len(edges),
            "vertices_touched": sorted(deg),
            "degree_profile": dict(sorted(Counter(deg.values()).items())),
            "is_perfect_matching_on_its_vertices": bool(is_matching),
            "faces_per_edge": onfaces,
        }
        checks[f"v{ver}_four_sqrt21_edges"] = len(edges) == 4

    e1 = {tuple(e) for e in res["1"]["sqrt21_edges"]}
    e2 = {tuple(e) for e in res["2"]["sqrt21_edges"]}
    same = (e1 == e2)
    checks["same_edge_set_in_both"] = bool(same)
    checks["comparison_made"] = True
    overlap = sorted(e1 & e2)

    all_pass = all(v for v in checks.values() if isinstance(v, bool))
    payload = {
        "schema": "w33.pass291.which_edges_carry_sqrt21.v1",
        "status": "PASS" if all_pass else "FAIL",
        "per_realization": res,
        "edge_set_v1": sorted(list(x) for x in e1),
        "edge_set_v2": sorted(list(x) for x in e2),
        "identical_edge_sets": bool(same),
        "shared_edges": [list(x) for x in overlap],
        "verdict": (
            "THE SAME four edges carry sqrt(21) in both Szilassi realizations. "
            "sqrt(21) is therefore attached to the Szilassi COMBINATORICS, not to "
            "either particular embedding -- a combinatorially distinguished "
            "4-edge set that is metrically forced into Q(sqrt 21) in both known "
            "realizations."
            if same else
            f"the four sqrt(21) edges DIFFER between the two realizations "
            f"(shared: {[list(x) for x in overlap]}). So sqrt(21) is a property of "
            f"each EMBEDDING's metric rather than of the Szilassi combinatorics -- "
            f"which makes Pass 290's 'unique common field' the more remarkable, "
            f"since two different edge sets land in the same quadratic field."
        ),
        "reading": (
            "Pass 290 established sqrt(21) as the unique field common to both "
            "Szilassi realizations. This pass asks whether that commonality is "
            "combinatorial (same edges) or metric (different edges, same field). "
            "The answer decides where to look next: at the Szilassi incidence "
            "structure, or at the realization moduli."
        ),
        "checks": {k: bool(v) for k, v in checks.items() if isinstance(v, bool)},
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(payload, indent=2))
    return 0 if all_pass else 1

if __name__ == "__main__":
    raise SystemExit(main())
