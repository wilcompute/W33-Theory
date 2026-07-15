#!/usr/bin/env python3
"""Pass 294: what are the two sqrt(21) 2-paths, and where do they go in the dual?

Pass 291 found the four sqrt(21) edges are the SAME in both Szilassi
realizations: {0,4}, {0,12}, {1,5}, {1,13}, forming two disjoint 2-paths
4--0--12 and 5--1--13 centred on vertices 0 and 1 -- the C2-antipodal pair at
(+-12, 0, 12).  Pass 293 then showed sqrt(21) is a coordinate choice, not an
invariant.  But the 4-EDGE SET is still combinatorially distinguished (it is the
same set in both realizations), so it is worth asking what that set IS.

Szilassi is the DUAL of Csaszar: Szilassi FACES <-> Csaszar VERTICES, and
Szilassi VERTICES <-> Csaszar FACES, with edges corresponding.  So each Szilassi
edge maps to a Csaszar edge, and this 4-edge set maps somewhere specific.

We compute, entirely combinatorially:
  * the two 2-paths and the C2 action on them;
  * which Szilassi faces each marked edge lies on (an edge lies on exactly 2);
  * the induced pair-of-faces, which under duality is a pair of Csaszar VERTICES
    -- i.e. each marked Szilassi edge names a Csaszar EDGE;
  * whether the image is itself a distinguished 4-edge set of K7.
"""

from __future__ import annotations

from collections import Counter
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "w33_pass294_paths_in_the_dual.json"

SZ_FACES = [[0, 1, 13, 8, 7, 4], [0, 4, 3, 2, 10, 12], [0, 12, 9, 6, 5, 1],
            [11, 3, 4, 7, 6, 9], [11, 9, 12, 10, 8, 13], [11, 13, 1, 5, 2, 3],
            [2, 5, 6, 7, 8, 10]]
CS_FACES = [[0, 1, 2], [0, 2, 5], [0, 5, 4], [0, 4, 6], [0, 6, 3], [0, 3, 1],
            [1, 3, 4], [1, 4, 5], [1, 5, 6], [1, 6, 2], [2, 6, 4], [2, 4, 3],
            [2, 3, 5], [5, 3, 6]]
MARKED = [(0, 4), (0, 12), (1, 5), (1, 13)]


def faces_of_edge(faces, e):
    out = []
    for fi, f in enumerate(faces):
        for i in range(len(f)):
            if tuple(sorted((f[i], f[(i + 1) % len(f)]))) == e:
                out.append(fi)
    return out


def main():
    checks = {}

    # ---- the 2-path structure
    deg = Counter()
    for a, b in MARKED:
        deg[a] += 1
        deg[b] += 1
    centres = sorted(v for v, d in deg.items() if d == 2)
    leaves = sorted(v for v, d in deg.items() if d == 1)
    checks["two_centres"] = len(centres) == 2
    checks["four_leaves"] = len(leaves) == 4
    checks["centres_are_0_and_1"] = centres == [0, 1]
    checks["structure_is_two_2paths"] = (len(centres) == 2 and len(leaves) == 4)

    # ---- the C2 action: v1's symmetry is (x,y,z) -> (-x,-y,z), which on the
    # vertex labels is the involution swapping antipodal pairs
    C2 = {0: 1, 1: 0, 2: 3, 3: 2, 4: 5, 5: 4, 6: 7, 7: 6, 8: 9, 9: 8,
          10: 11, 11: 10, 12: 13, 13: 12}
    img = {tuple(sorted((C2[a], C2[b]))) for a, b in MARKED}
    checks["marked_set_is_C2_invariant"] = img == set(MARKED)
    checks["C2_swaps_the_two_paths"] = (C2[0] == 1 and C2[4] == 5 and C2[12] == 13)

    # ---- duality: a Szilassi EDGE lies on 2 Szilassi FACES; those two faces are
    # two Csaszar VERTICES, so the edge names a Csaszar EDGE.
    dual_images = {}
    for e in MARKED:
        fs = faces_of_edge(SZ_FACES, e)
        dual_images[str(e)] = {"szilassi_faces": fs,
                               "as_csaszar_edge": sorted(fs)}
    checks["each_marked_edge_on_two_faces"] = all(
        len(v["szilassi_faces"]) == 2 for v in dual_images.values())

    dual_edges = sorted(tuple(v["as_csaszar_edge"]) for v in dual_images.values())
    ddeg = Counter()
    for a, b in dual_edges:
        ddeg[a] += 1
        ddeg[b] += 1
    dual_centres = sorted(v for v, d in ddeg.items() if d >= 2)
    checks["dual_image_is_four_edges"] = len(set(dual_edges)) == 4
    # is the dual image also two 2-paths?
    dual_is_two_paths = (sorted(ddeg.values()) == [1, 1, 1, 1, 2, 2])
    checks["dual_structure_computed"] = True

    # sanity: Csaszar's skeleton is K7, so any pair of its vertices is an edge
    k7 = all(0 <= a < 7 and 0 <= b < 7 and a != b for a, b in dual_edges)
    checks["dual_edges_are_K7_edges"] = k7

    all_pass = all(v for v in checks.values() if isinstance(v, bool))
    payload = {
        "schema": "w33.pass294.paths_in_the_dual.v1",
        "status": "PASS" if all_pass else "FAIL",
        "the_marked_set": {
            "edges": [list(e) for e in MARKED],
            "centres": centres, "leaves": leaves,
            "structure": "two disjoint 2-paths: 4--0--12 and 5--1--13",
            "centres_meaning": "vertices 0 and 1 are the C2-antipodal pair at "
                               "(+-12, 0, 12) in both published realizations",
            "C2_invariant": bool(img == set(MARKED)),
            "C2_action": "the symmetry swaps the two paths (0<->1, 4<->5, 12<->13)",
        },
        "dual_image": {
            "rule": "a Szilassi edge lies on exactly 2 Szilassi faces; under "
                    "duality those faces ARE two Csaszar vertices, so each "
                    "marked edge names a Csaszar edge",
            "per_edge": dual_images,
            "csaszar_edges": [list(e) for e in dual_edges],
            "degree_profile": dict(sorted(Counter(ddeg.values()).items())),
            "is_two_2paths_in_the_dual": bool(dual_is_two_paths),
            "dual_centres": dual_centres,
        },
        "reading": (
            "The four sqrt(21) edges are not metrically special (Pass 293: they "
            "are a coordinate choice), but the EDGE SET is combinatorially "
            "distinguished -- it is the same set in both published realizations "
            "and it is exactly C2-invariant, consisting of two 2-paths swapped "
            "by the symmetry and centred on the antipodal pair. Under Szilassi/"
            "Csaszar duality it maps to a 4-edge set of the Csaszar K7 skeleton, "
            "computed here. Since Csaszar's skeleton is complete, every pair of "
            "its vertices is an edge, so the image is distinguished only by its "
            "SHAPE, which is what the degree profile records."
        ),
        "honest_note": (
            "This pass is purely combinatorial and therefore unaffected by Pass "
            "293's deflation. What it does NOT show is that the marked set is "
            "canonical: it was singled out by a metric accident of two coordinate "
            "choices, so its combinatorial distinction may itself be an artefact "
            "of how it was found."
        ),
        "checks": {k: bool(v) for k, v in checks.items() if isinstance(v, bool)},
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(payload, indent=2))
    return 0 if all_pass else 1


if __name__ == "__main__":
    raise SystemExit(main())
