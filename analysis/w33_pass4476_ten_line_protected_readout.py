#!/usr/bin/env python3
"""Pass 4476 -- optimal ten-line protected readout frame.

The apartment code has a 10-dimensional protected quotient H10 (Pass 4469).
Pass 4474 shows every geometric line gives both a weight-162 apartment generator
and a weight-4 minimum logical line class.  This pass asks for a sparse geometric
basis of that protected quotient and for the exact linear post-processing needed
to read it out.

A deterministic 10-line witness is

    S = [1,5,14,15,19,23,24,33,35,39]

in the repo's lexicographic line ordering.  Its induced dual-W33 intersection
graph is

    P4 disjoint-union 3 K2,

so it has only six intersecting pairs.  The 10x10 adjacency/pairing matrix is
nonsingular over F2, hence these ten line classes form an H10 basis and the ten
corresponding apartment generators form a basis of C_ap/rad.

The six intersections are MINIMAL among all 10-line H10 bases.  A nonsingular
10x10 alternating adjacency matrix has a perfect matching.  If a 10-vertex
basis graph had only five edges, it would have to be exactly 5 K2, i.e. an
induced matching of size five in the dual W33 graph.  An exact clique search in
the edge-compatibility graph proves that the maximum induced matching size of
W33 is four.  Therefore every 10-line basis has at least six intersections, and
the P4 + 3K2 witness is optimal.

Protected readout is then information-theoretically optimal.  For an apartment
syndrome y in C_ap, define the ten software parity bits

    p_i = <y,g_i>,

where g_i is the weight-162 apartment signature of the i-th selected line.  The
radical is orthogonal to every g_i, so p depends only on the protected quotient.
If c are the ten H10 coordinates in this line basis and G is the 10x10 selected
pairing matrix, then

    p = c G,
    c = p G^{-1}.

All 2^10 quotient classes are verified.  Ten output bits are minimal for an
injective linear readout of a 10-dimensional quotient.

Boundary: these are ten LINEAR POST-PROCESSING bits of the apartment-parity
syndrome.  Each p_i is the XOR of the 162 apartment bits containing the selected
line.  This is not a claim that ten individual apartment measurements replace
the full physical syndrome-acquisition problem.  The six-edge optimum minimizes
pairwise line intersections among geometric H10 bases; it does not prove an
optical hardware-cost optimum.
"""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np

from w33_pass4461_line_signing_apartment_trace import geometry, simple_four_cycles
from w33_pass4463_apartment_parity_tomography import rank_mod2
from w33_pass4469_apartment_css_h10_intertwiner import nullspace_mod2, rref_rows

ROOT = Path(__file__).resolve().parents[1]
SELECTED = [1, 5, 14, 15, 19, 23, 24, 33, 35, 39]


def inverse_mod2(M: np.ndarray) -> np.ndarray:
    M = (np.asarray(M, dtype=np.uint8) & 1).copy()
    n = M.shape[0]
    aug = np.hstack((M, np.eye(n, dtype=np.uint8)))
    r = 0
    for c in range(n):
        piv = next((i for i in range(r, n) if aug[i, c]), None)
        if piv is None:
            raise ValueError("matrix singular over F2")
        if piv != r:
            aug[[r, piv]] = aug[[piv, r]]
        for i in range(n):
            if i != r and aug[i, c]:
                aug[i] ^= aug[r]
        r += 1
    if not np.array_equal(aug[:, :n], np.eye(n, dtype=np.uint8)):
        raise ValueError("matrix inversion failed")
    return aug[:, n:]


def compatible_induced_edges(e1, e2, A: np.ndarray) -> bool:
    a, b = e1
    c, d = e2
    if len({a, b, c, d}) < 4:
        return False
    return not any(A[u, v] for u in (a, b) for v in (c, d))


def find_compatible_clique(edges, compatibility, target: int):
    """Exact recursive target-clique search; returns one witness or None."""
    def rec(candidates: tuple[int, ...], chosen: tuple[int, ...]):
        need = target - len(chosen)
        if need == 0:
            return chosen
        if len(candidates) < need:
            return None
        candidates = tuple(candidates)
        while len(candidates) >= need:
            v = candidates[0]
            rest = candidates[1:]
            next_candidates = tuple(u for u in rest if u in compatibility[v])
            hit = rec(next_candidates, chosen + (v,))
            if hit is not None:
                return hit
            candidates = rest
        return None
    return rec(tuple(range(len(edges))), tuple())


def main() -> int:
    _, lines, A_point, N_int, edge_line = geometry()
    N = (N_int % 2).astype(np.uint8)
    Astar = (N.T @ N) % 2
    cycles = simple_four_cycles(A_point)
    supports = [frozenset(edge_line[e] for e in C4) for C4 in cycles]
    H = np.zeros((40, 1620), dtype=np.uint8)
    for j, support in enumerate(supports):
        for li in support:
            H[li, j] = 1

    checks: list[tuple[str, bool]] = []

    def check(name: str, cond) -> None:
        ok = bool(cond)
        checks.append((name, ok))
        if not ok:
            raise AssertionError(name)

    sentinel = rref_rows(nullspace_mod2(N.T))
    ker_astar = rref_rows(nullspace_mod2(Astar))
    radical = rref_rows(np.asarray([(H.T @ k) % 2 for k in ker_astar], dtype=np.uint8))

    selected_gram = Astar[np.ix_(SELECTED, SELECTED)].astype(np.uint8)
    selected_logicals = N[:, SELECTED].T.copy()
    selected_apartment = H[SELECTED].copy()

    check("ten selected lines", len(SELECTED) == 10 and len(set(SELECTED)) == 10)
    check("selected Gram alternating", np.all(np.diag(selected_gram) == 0))
    check("selected Gram nonsingular", rank_mod2(selected_gram) == 10)
    check("ten logical lines add ten dimensions over C", rank_mod2(np.vstack((sentinel, selected_logicals))) == 25)
    check("ten apartment lines add ten dimensions over radical", rank_mod2(np.vstack((radical, selected_apartment))) == 39)
    check("selected apartment signatures weight 162", all(int(v.sum()) == 162 for v in selected_apartment))
    check("selected logical representatives weight 4", all(int(v.sum()) == 4 for v in selected_logicals))

    edge_count = int(selected_gram.sum() // 2)
    degrees = sorted(int(x) for x in selected_gram.sum(axis=1))
    # Component sizes without networkx.
    unseen = set(range(10))
    component_sizes = []
    while unseen:
        start = min(unseen)
        comp = {start}
        frontier = [start]
        while frontier:
            v = frontier.pop()
            for w in np.flatnonzero(selected_gram[v]):
                w = int(w)
                if w not in comp:
                    comp.add(w)
                    frontier.append(w)
        unseen.difference_update(comp)
        component_sizes.append(len(comp))
    component_sizes.sort()
    check("selected basis has six intersections", edge_count == 6)
    check("selected basis graph is P4 plus 3K2", component_sizes == [2, 2, 2, 4] and degrees == [1]*8 + [2]*2)

    # Exact induced-matching obstruction to a five-edge basis.
    dual_edges = [(i, j) for i in range(40) for j in range(i + 1, 40) if Astar[i, j]]
    check("dual W33 has 240 edges", len(dual_edges) == 240)
    compatibility = [set() for _ in dual_edges]
    for i in range(len(dual_edges)):
        for j in range(i + 1, len(dual_edges)):
            if compatible_induced_edges(dual_edges[i], dual_edges[j], Astar):
                compatibility[i].add(j)
                compatibility[j].add(i)
    match5 = find_compatible_clique(dual_edges, compatibility, 5)
    match4 = find_compatible_clique(dual_edges, compatibility, 4)
    check("no induced matching of size 5", match5 is None)
    check("induced matching of size 4 exists", match4 is not None)
    check("six intersections is optimal among ten-line nonsingular bases", match5 is None and edge_count == 6)

    # Ten-bit protected software readout.
    Ginv = inverse_mod2(selected_gram)
    check("Gram inverse verified", np.array_equal((selected_gram @ Ginv) % 2, np.eye(10, dtype=np.uint8)))
    check("radical orthogonal to selected basis", not np.any((radical @ selected_apartment.T) % 2))

    recovered_all = True
    for mask in range(1 << 10):
        c = np.array([(mask >> i) & 1 for i in range(10)], dtype=np.uint8)
        y = (c @ selected_apartment) % 2
        p = (y @ selected_apartment.T) % 2
        c2 = (p @ Ginv) % 2
        if not np.array_equal(c, c2):
            recovered_all = False
            break
    check("ten readout bits recover all 1024 protected classes", recovered_all)

    selected_lines = [list(map(int, lines[i])) for i in SELECTED]
    result = {
        "pass": 4476,
        "theorem": "W33 optimal ten-line protected readout theorem",
        "selected_line_indices": SELECTED,
        "selected_line_point_sets": selected_lines,
        "basis_graph": {
            "type": "P4 disjoint-union 3K2",
            "edges": edge_count,
            "component_sizes": component_sizes,
            "degree_sequence": degrees,
            "Gram_rank_F2": rank_mod2(selected_gram),
            "minimum_intersections_among_ten_line_bases": 6,
            "lower_bound_certificate": "a 5-edge nonsingular graph would be 5K2, but exact search gives induced-matching number 4",
            "maximum_induced_matching": 4,
        },
        "protected_readout": {
            "bits": 10,
            "formula": "p_i=<y,g_i>; c=p G^{-1}",
            "each_g_i_weight": 162,
            "all_1024_classes_verified": recovered_all,
            "optimal_bit_count_reason": "injective linear readout of a 10-dimensional quotient requires at least 10 bits",
        },
        "boundary": (
            "The ten bits are linear software post-processing of an acquired apartment-parity syndrome; each is an XOR "
            "of 162 apartment bits.  This is not ten physical apartment measurements.  The six-edge optimum minimizes "
            "pairwise line intersections among geometric H10 bases, not optical hardware cost."
        ),
        "checks": {"passed": sum(ok for _, ok in checks), "total": len(checks)},
    }

    out = ROOT / "data" / "PART_W33_PASS4476_TEN_LINE_PROTECTED_READOUT.json"
    out.parent.mkdir(exist_ok=True)
    out.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    print("Pass 4476 -- optimal ten-line protected readout")
    print("  basis graph: P4 + 3K2, six intersections, Gram rank 10")
    print("  exact induced-matching maximum = 4 -> five intersections impossible")
    print("  10 software parity bits recover all 1024 protected classes")
    print(f"  checks: {result['checks']['passed']}/{result['checks']['total']} PASS")
    print(f"  wrote {out.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
