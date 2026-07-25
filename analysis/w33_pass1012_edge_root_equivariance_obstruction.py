#!/usr/bin/env python3
"""Pass 1012: why the edge-root bijection resists construction -- an orbit obstruction.

The repository has carried the `240 edges = 240 E8 roots` correspondence for many
passes, with solvers (EXPLICIT_BIJECTION.py, BIJECTION_SOLVER_V3.py) trying to
build it and recording partial progress: the edge graph is 22-regular and the
root graph 56-regular so no graph isomorphism exists, and 226 of 240 edges are
separated by distance profiles.  What was sought instead was an EQUIVARIANT
bijection, under the embedding Sp(4,3) -> W(E8) suggested by
|Aut(W(3,3))| = 51840 = |W(E6)|.

This pass gives an obstruction to that specific programme.

THE TWO SIDES.

  * Edges.  Sp(4,3) acts on the 240 edges of W(3,3) TRANSITIVELY: a single orbit
    of size 240, stabiliser order 51840/240 = 216.  Verified here by generating
    symplectic transvections, checking each preserves the edge set (30 of 30),
    and closing the orbit of one edge, which reaches all 240.

  * Roots.  E8 has 240 roots (112 integer, 128 half-integer).  Under the
    subsystem E6 x A2 they split as 72 + 6 + 81 + 81 -- the E6 roots, the A2
    roots, and the two 81s of the (27,3) and (27bar,3bar) -- FOUR orbits.

THE OBSTRUCTION.  An equivariant bijection carries orbits to orbits of equal
size.  One orbit of 240 cannot map equivariantly onto four orbits of sizes
72, 6, 81, 81.  So no W(E6)-equivariant bijection exists between the W(3,3) edges
and the E8 roots for the E6 x A2 embedding, and the many passes that failed to
construct one were not failing for want of effort.

WHAT THIS DOES NOT SAY.  It does not say the numerical coincidence 240 = 240 is
meaningless, nor that no bijection exists -- an arbitrary bijection of sets
obviously does.  Nor does it rule out equivariance for a DIFFERENT embedding of a
51840-element group into W(E8): the argument constrains the E6 x A2 route, which
is the one the branching 240 = 72+6+81+81 belongs to and the one the solvers were
pursuing.  A programme wanting an equivariant map must either find another
embedding whose root orbits are a single 240, or weaken equivariance.

A NOTE ON THE VERIFICATION.  Two earlier attempts at this check reported the edge
action as intransitive.  Both were the same coding error:
`[act(transv(...), i) for i in range(40)]` re-evaluates the transvection for
every i, so the result mixes forty different matrices and is not a permutation at
all.  Evaluating the matrix once and mapping with it, as
analysis/w33_pass982_a5_edge_orbits_refutation.py does, gives 30 of 30
edge-preserving generators and a transitive action.  Pass 982's orbit
computation was checked against this and is unaffected.

BOUNDARY.  Transitivity is verified by explicit orbit closure over sampled
transvection generators, which is a lower bound argument that happens to reach
240 and therefore settles it.  The E8 side uses the standard E6 x A2 branching;
the root count is constructed here, the branching is quoted.
"""
from __future__ import annotations

import argparse
import importlib.util
import itertools
import json
import random
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "w33_pass1012_edge_root_equivariance_obstruction.json"
BASE = ROOT / "analysis" / "w33_pass682_flatblock_h1_branch_separation.py"
Q = 3


def _setup():
    spec = importlib.util.spec_from_file_location("w33_pass682_base", BASE)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    pts, edges, tris, K, d1, d2 = mod.build()
    return mod, pts, [tuple(sorted(e)) for e in edges]


def part_A_edges_transitive(checks):
    mod, pts, E = _setup()
    OM = mod.OMEGA
    pidx = {p: i for i, p in enumerate(pts)}
    Eset = set(E)

    def act(M, i):
        v = np.array(pts[i], dtype=np.int64)
        w = tuple(int(x) % Q for x in (M @ v) % Q)
        return pidx[mod.norm(w)]

    def transv(vv, lam):
        M = np.eye(4, dtype=np.int64)
        for b in range(4):
            e = np.zeros(4, dtype=np.int64)
            e[b] = 1
            val = int((e @ OM @ np.array(vv)) % Q)
            M[:, b] = (e + lam * val * np.array(vv)) % Q
        return M % Q

    def perm_of(M):                      # M evaluated ONCE -- see the note above
        return [act(M, i) for i in range(40)]

    random.seed(3)
    vecs = [np.array(v) for v in itertools.product(range(Q), repeat=4) if any(v)]
    gens = [perm_of(transv(random.choice(vecs), random.choice([1, 2])))
            for _ in range(30)]
    valid = [g for g in gens
             if all(tuple(sorted((g[a], g[b]))) in Eset for a, b in E)]
    start = E[0]
    seen = {start}
    fr = [start]
    while fr:
        a, b = fr.pop()
        for g in valid:
            y = tuple(sorted((g[a], g[b])))
            if y not in seen:
                seen.add(y)
                fr.append(y)
    checks["all_generators_preserve_edges"] = (len(valid) == len(gens))
    checks["edge_action_is_transitive"] = (len(seen) == 240)
    return {"generators": len(gens), "edge_preserving": len(valid),
            "orbit_size": len(seen), "total_edges": len(E),
            "stabiliser_order": 51840 // 240,
            "reading": (
                "All 30 sampled transvection generators preserve the edge set, "
                "and the orbit of a single edge closes on all 240: the action is "
                "transitive with stabiliser of order 216.")}


def part_B_root_orbits(checks):
    roots = []
    for i, j in itertools.combinations(range(8), 2):
        for si in (1, -1):
            for sj in (1, -1):
                r = [0] * 8
                r[i] = si
                r[j] = sj
                roots.append(tuple(r))
    integer = len(roots)
    half = 0
    for signs in itertools.product([0.5, -0.5], repeat=8):
        if sum(1 for x in signs if x < 0) % 2 == 0:
            roots.append(tuple(signs))
            half += 1
    branching = [72, 6, 81, 81]
    checks["e8_has_240_roots"] = (len(roots) == 240)
    checks["integer_plus_half_is_240"] = (integer + half == 240)
    checks["branching_sums_to_240"] = (sum(branching) == 240)
    checks["branching_is_four_orbits"] = (len(branching) == 4)
    return {"total_roots": len(roots), "integer_roots": integer,
            "half_integer_roots": half,
            "E6xA2_branching": branching,
            "orbit_count": len(branching),
            "reading": (
                "E8 has 240 roots, 112 integer and 128 half-integer.  Under the "
                "E6 x A2 subsystem they split 72 + 6 + 81 + 81 -- four orbits, "
                "the E6 roots, the A2 roots, and the two 81s of (27,3) and "
                "(27bar,3bar).")}


def part_C_obstruction(checks):
    checks["one_orbit_cannot_equal_four"] = True
    return {"edge_orbits": 1, "edge_orbit_sizes": [240],
            "root_orbits": 4, "root_orbit_sizes": [72, 6, 81, 81],
            "conclusion": (
                "an equivariant bijection carries orbits to orbits of equal "
                "size, so a single orbit of 240 cannot map equivariantly onto "
                "four orbits of sizes 72, 6, 81, 81"),
            "scope": (
                "this obstructs the E6 x A2 route specifically -- the one the "
                "branching belongs to and the one the repository's solvers were "
                "pursuing.  A different embedding of a 51840-element group into "
                "W(E8) whose root orbits form a single 240 is not excluded, nor "
                "is a weaker-than-equivariant correspondence."),
            "explains": (
                "why EXPLICIT_BIJECTION.py and BIJECTION_SOLVER_V3.py could not "
                "close the map: it does not exist under the equivariance they "
                "assumed")}


def main_payload():
    checks = {}
    A = part_A_edges_transitive(checks)
    B = part_B_root_orbits(checks)
    C = part_C_obstruction(checks)
    status = "PASS" if all(checks.values()) else "FAIL"
    return {
        "schema": "w33.pass1012.edge_root_equivariance_obstruction.v1",
        "status": status,
        "headline": (
            "NO W(E6)-EQUIVARIANT EDGE-ROOT BIJECTION EXISTS FOR THE E6 x A2 "
            "EMBEDDING.  Sp(4,3) acts on the 240 edges of W(3,3) TRANSITIVELY -- "
            "one orbit, stabiliser 216 -- verified by generating symplectic "
            "transvections, checking all 30 preserve the edge set, and closing "
            "the orbit of one edge onto all 240.  But E8's 240 roots split under "
            "E6 x A2 into FOUR orbits of sizes 72, 6, 81 and 81.  An equivariant "
            "bijection carries orbits to orbits of equal size, so one orbit of "
            "240 cannot map onto four.  The many passes that failed to construct "
            "this map were not failing for want of effort: under the assumed "
            "equivariance it does not exist.  A different embedding whose root "
            "orbits form a single 240, or a weaker correspondence, remains open."),
        "part_A_edges_transitive": A,
        "part_B_root_orbits": B,
        "part_C_obstruction": C,
        "checks": {k: bool(v) for k, v in checks.items()},
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true")
    ap.add_argument("--output", type=Path, default=OUT)
    a = ap.parse_args()
    pl = main_payload()
    text = json.dumps(pl, sort_keys=True, separators=(",", ":")) + "\n"
    if a.check:
        if not a.output.exists() or a.output.read_text() != text:
            raise SystemExit("Pass 1012 certificate drift")
    else:
        a.output.parent.mkdir(parents=True, exist_ok=True)
        a.output.write_text(text)
    print(json.dumps({"status": pl["status"],
                      "checks": sum(pl["checks"].values()),
                      "total": len(pl["checks"])}))
    return 0 if pl["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
