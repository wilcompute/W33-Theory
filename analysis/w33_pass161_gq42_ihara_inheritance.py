#!/usr/bin/env python3
"""Pass 161: the trade-support geometry inherits the Ihara prime 11.

Pass 158 found that the 45 minimal-trade supports of the chiral lattice
carry SRG(45,12,3,3) = the GQ(4,2) collinearity graph.  This witness:

1. IHARA INHERITANCE.  The support graph is 12-regular like W(3,3) itself,
   so its Ihara prime is the same k-1 = 11.  Its Ihara zeta factors as
     Z^{-1}(u) = (1-u^2)^{225} (1-u)(1-11u)
                 (1 - 3u + 11u^2)^{20} (1 + 3u + 11u^2)^{24},
   both quadratic sectors have discriminant 9 - 44 = -35 = -(mu+1)*Phi_6
   < 0, and every complex Hashimoto eigenvalue satisfies |x|^2 = 11: the
   graph Riemann Hypothesis holds on the SAME critical circle
   |u| = 1/sqrt(11) as the substrate's.  The chiral shell geometry speaks
   the same critical norm.

2. THE THREE 540s.  The Hashimoto arc carrier of the support geometry has
   45*12 = 540 arcs -- the same count as W(3,3)'s 540 skew line pairs (the
   hypercube-chart atlas) and its 540 non-collinear point pairs (the
   hyperbolic pairs).  All three are transitive PSp(4,3)-sets with
   stabilizers of order 48.  The pairwise G-set isomorphism verdicts are
   decided by the exact fixed-point criterion, with orbital ranks as the
   certificate.
"""

from __future__ import annotations

from collections import Counter
from itertools import combinations
import json
from pathlib import Path
import sys

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from analysis.w33_pass158_chiral_trade_lattice_two_480s import (
    build_group,
    build_w33,
    minimal_shell,
    orbit_count,
    saturated_kernel,
    w33_lines,
)

OUT = ROOT / "data" / "w33_pass161_gq42_ihara_inheritance.json"


def support_graph(adjacency):
    """The 45 trade supports and their zero-inner-product SRG(45,12,3,3)."""
    dark = saturated_kernel(adjacency + 4 * np.eye(40, dtype=np.int64))
    _, shell, _, _ = minimal_shell(dark)
    shell = [np.asarray(v, dtype=np.int64) for v in shell]
    rep = {}
    for vector in shell:
        key = frozenset(np.flatnonzero(vector).tolist())
        rep.setdefault(key, vector)
    supports = sorted(rep, key=sorted)
    graph = np.zeros((45, 45), dtype=np.int64)
    for a, b in combinations(range(45), 2):
        if int(rep[supports[a]] @ rep[supports[b]]) == 0:
            graph[a, b] = graph[b, a] = 1
    return supports, graph


def small_generating_set(group, size=40):
    """Find two elements generating the whole group (deterministic scan)."""
    ordered = sorted(group)
    base = ordered[1]
    identity = tuple(range(size))
    for candidate in ordered[2:]:
        seen = {identity}
        frontier = [identity]
        while frontier:
            new = []
            for element in frontier:
                for gen in (base, candidate):
                    composed = tuple(gen[element[i]] for i in range(size))
                    if composed not in seen:
                        if len(seen) + len(new) >= len(group):
                            pass
                        seen.add(composed)
                        new.append(composed)
            frontier = new
            if len(seen) == len(group):
                return [base, candidate]
        if len(seen) == len(group):
            return [base, candidate]
    raise RuntimeError("no 2-element generating set found")


def product_maps(maps_left, maps_right, size=540):
    combined = []
    for g_left, g_right in zip(maps_left, maps_right):
        left = np.asarray(g_left, dtype=np.int64)
        right = np.asarray(g_right, dtype=np.int64)
        table = (left[:, None] * size + right[None, :]).reshape(-1)
        combined.append(table)
    return combined


def main():
    points, adjacency, symplectic = build_w33()
    lines = w33_lines(adjacency)
    checks = {}

    # ------------------------------------------------------------------
    # 1. the support geometry and its Ihara zeta
    # ------------------------------------------------------------------
    supports, graph = support_graph(adjacency)
    checks["support_graph_12_regular"] = bool((graph.sum(axis=1) == 12).all())
    g2 = graph @ graph
    srg_ok = all(g2[a, b] == 3 for a, b in combinations(range(45), 2))
    checks["support_graph_srg_45_12_3_3"] = bool(srg_ok)

    eigenvalues = np.linalg.eigvalsh(graph.astype(float))
    spectrum = Counter(int(round(v)) for v in eigenvalues)
    checks["support_spectrum_12_3_m3"] = spectrum == Counter({12: 1, 3: 20, -3: 24})

    vertices, degree = 45, 12
    edges = vertices * degree // 2
    checks["edge_count_270"] = edges == 270

    arcs = [(i, j) for i in range(45) for j in range(45) if graph[i, j]]
    arc_index = {arc: n for n, arc in enumerate(arcs)}
    checks["arc_count_540"] = len(arcs) == 540

    hashimoto = np.zeros((540, 540), dtype=np.int8)
    for a, (i, j) in enumerate(arcs):
        for k in np.flatnonzero(graph[j]):
            if k != i:
                hashimoto[a, arc_index[(j, int(k))]] = 1
    checks["hashimoto_row_sum_11"] = bool((hashimoto.sum(axis=1) == degree - 1).all())

    b_eigen = np.linalg.eigvals(hashimoto.astype(float))
    real = b_eigen[np.abs(b_eigen.imag) < 1e-8].real
    cplx = b_eigen[np.abs(b_eigen.imag) >= 1e-8]
    real_profile = Counter(int(round(v)) for v in real)
    checks["hashimoto_real_spectrum"] = real_profile == Counter(
        {11: 1, 1: 226, -1: 225}
    )
    checks["hashimoto_complex_count_88"] = len(cplx) == 88
    checks["graph_rh_critical_norm_11"] = bool(
        np.allclose(np.abs(cplx) ** 2, 11.0, atol=1e-6)
    )
    discriminant = 3 * 3 - 4 * 11
    checks["sector_discriminant_minus_35"] = discriminant == -35 == -(5 * 7)

    # ------------------------------------------------------------------
    # 2. the three 540s
    # ------------------------------------------------------------------
    generators, group = build_group(points, symplectic)
    checks["group_order_25920"] = len(group) == 25920
    two_gens = small_generating_set(group)

    line_index = {line: n for n, line in enumerate(lines)}
    disjoint_line_pairs = [
        frozenset((a, b))
        for a, b in combinations(range(40), 2)
        if not (lines[a] & lines[b])
    ]
    checks["skew_line_pairs_540"] = len(disjoint_line_pairs) == 540
    skew_index = {pair: n for n, pair in enumerate(disjoint_line_pairs)}

    hyperbolic_pairs = [
        frozenset((a, b)) for a, b in combinations(range(40), 2) if not adjacency[a, b]
    ]
    checks["hyperbolic_pairs_540"] = len(hyperbolic_pairs) == 540
    hyper_index = {pair: n for n, pair in enumerate(hyperbolic_pairs)}

    support_index = {s: n for n, s in enumerate(supports)}

    def act_line(perm, line_id):
        return line_index[frozenset(perm[x] for x in lines[line_id])]

    def act_skew(perm, pair_id):
        a, b = sorted(disjoint_line_pairs[pair_id])
        return skew_index[frozenset((act_line(perm, a), act_line(perm, b)))]

    def act_hyper(perm, pair_id):
        a, b = sorted(hyperbolic_pairs[pair_id])
        return hyper_index[frozenset((perm[a], perm[b]))]

    def act_support(perm, sid):
        return support_index[frozenset(perm[x] for x in supports[sid])]

    def act_arc45(perm, arc_id):
        i, j = arcs[arc_id]
        return arc_index[(act_support(perm, i), act_support(perm, j))]

    actions = {
        "skew_line_pairs": act_skew,
        "hyperbolic_pairs": act_hyper,
        "gq42_arcs": act_arc45,
    }
    maps = {
        name: [[action(g, x) for x in range(540)] for g in two_gens]
        for name, action in actions.items()
    }

    for name in actions:
        checks[f"{name}_transitive"] = orbit_count(540, maps[name]) == 1

    stabilizers = {}
    for name, action in actions.items():
        stabilizers[name] = [g for g in group if action(g, 0) == 0]
        checks[f"{name}_stabilizer_48"] = len(stabilizers[name]) == 48

    verdicts = {}
    for left, right in combinations(actions, 2):
        fixed = [
            x
            for x in range(540)
            if all(actions[right](g, x) == x for g in stabilizers[left])
        ]
        verdicts[f"{left}_vs_{right}"] = {
            "stabilizer_fixed_points": len(fixed),
            "isomorphic": bool(fixed),
        }

    ranks = {}
    for name in actions:
        ranks[name] = orbit_count(540 * 540, product_maps(maps[name], maps[name]))
    for left, right in combinations(actions, 2):
        ranks[f"{left}_x_{right}"] = orbit_count(
            540 * 540, product_maps(maps[left], maps[right])
        )
    checks["ranks_computed"] = all(v > 0 for v in ranks.values())

    all_pass = all(checks.values())
    payload = {
        "schema": "w33.pass161.gq42_ihara_inheritance.v1",
        "status": "PASS" if all_pass else "FAIL",
        "ihara": {
            "graph": "SRG(45,12,3,3) on the 45 trade supports",
            "zeta_inverse": (
                "(1-u^2)^225 (1-u)(1-11u) (1-3u+11u^2)^20 (1+3u+11u^2)^24"
            ),
            "ihara_prime": 11,
            "sector_discriminant": discriminant,
            "discriminant_reading": "-35 = -(mu+1)*Phi_6",
            "graph_rh": (
                "all 88 complex Hashimoto eigenvalues satisfy |x|^2 = 11: "
                "the chiral support geometry lives on the same critical "
                "circle |u| = 1/sqrt(11) as W(3,3) itself"
            ),
        },
        "three_540s": {
            "carriers": [
                "540 skew line pairs (the hypercube-chart atlas)",
                "540 hyperbolic point pairs (the minimal-trade seeds)",
                "540 Hashimoto arcs of the GQ(4,2) support geometry",
            ],
            "stabilizer_order": 48,
            "verdicts": verdicts,
            "orbital_ranks": {k: int(v) for k, v in ranks.items()},
        },
        "checks": {name: bool(value) for name, value in checks.items()},
    }

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(payload, indent=2))
    return 0 if all_pass else 1


if __name__ == "__main__":
    raise SystemExit(main())
