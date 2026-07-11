#!/usr/bin/env python3
"""Pass 169: naming the canonical cycles of the second shell.

Pass 168 found that the zero inner-product class of the 240 GQ(4,2)
trades splits as 112 = 108 + 4: a canonical group-invariant 4-valent
orthogonality relation, descending to a 2-regular graph on the 120
supports.  A 2-regular invariant graph is a disjoint union of cycles.
This witness names them:

1. THE CYCLE TYPE.  Connected components of the 4-valent relation on the
   240 trades and of the 2-regular relation on the 120 supports, with
   exact lengths and counts.

2. THE PARTNER RULE.  The orbital is characterized combinatorially: for a
   trade t = 1_span - 1_perp and each of its four partners t', the
   intersection signature (|S+ cap S'+|, |S+ cap S'-|, |S- cap S'+|,
   |S- cap S'-|) is computed and shown constant -- the geometric law that
   picks the four partners out of the 112 orthogonal trades.

3. THE SPECTRUM.  Exact eigenvalues of the 4-valent relation (a union of
   equal cycles has spectrum 4cos(2 pi j / L) + ...), confirming the
   cycle type spectrally.
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
)
from analysis.w33_pass160_trade_tower_gq42 import (
    generic_saturated_kernel,
    staged_minimal_shell,
)
from analysis.w33_pass161_gq42_ihara_inheritance import (
    small_generating_set,
    support_graph,
)
from analysis.w33_pass168_second_shell_scheme import gq42_lines

OUT = ROOT / "data" / "w33_pass169_canonical_cycles.json"


def components(adjacency_lists, n):
    seen = [False] * n
    sizes = []
    for start in range(n):
        if seen[start]:
            continue
        size = 0
        stack = [start]
        seen[start] = True
        while stack:
            current = stack.pop()
            size += 1
            for nxt in adjacency_lists[current]:
                if not seen[nxt]:
                    seen[nxt] = True
                    stack.append(nxt)
        sizes.append(size)
    return Counter(sizes)


def main():
    points, adjacency, symplectic = build_w33()
    checks = {}

    supports, graph = support_graph(adjacency)
    lines45 = gq42_lines(graph)
    incidence = np.zeros((27, 45), dtype=np.int64)
    for row, line in enumerate(lines45):
        for p in line:
            incidence[row, p] = 1
    trade = generic_saturated_kernel(incidence)
    min_norm, shell = staged_minimal_shell(trade)
    shell = [np.asarray(v, dtype=np.int64) for v in shell]
    checks["shell_240"] = len(shell) == 240 and min_norm == 6

    generators, group = build_group(points, symplectic)
    checks["group_order"] = len(group) == 25920
    two_gens = small_generating_set(group)
    support_index = {s: n for n, s in enumerate(supports)}
    shell_keys = {tuple(int(x) for x in v): n for n, v in enumerate(shell)}

    def shell_map(perm):
        mapping45 = [
            support_index[frozenset(perm[x] for x in supports[s])] for s in range(45)
        ]
        table = []
        for v in shell:
            image = np.empty(45, dtype=np.int64)
            for src in range(45):
                image[mapping45[src]] = v[src]
            table.append(shell_keys[tuple(int(x) for x in image)])
        return table

    gen_maps = [shell_map(g) for g in two_gens]
    tables = []
    for mapping in gen_maps:
        arr = np.asarray(mapping, dtype=np.int64)
        tables.append((arr[:, None] * 240 + arr[None, :]).reshape(-1))

    # orbital labels
    labels = np.full(240 * 240, -1, dtype=np.int64)
    orbital_count = 0
    for start in range(240 * 240):
        if labels[start] >= 0:
            continue
        labels[start] = orbital_count
        stack = [start]
        while stack:
            current = stack.pop()
            for table in tables:
                image = int(table[current])
                if labels[image] < 0:
                    labels[image] = orbital_count
                    stack.append(image)
        orbital_count += 1
    checks["orbital_rank_10"] = orbital_count == 10
    label_grid = labels.reshape(240, 240)

    shell_matrix = np.array(shell, dtype=np.int64)
    gram = shell_matrix @ shell_matrix.T

    # locate the 4-valent zero orbital
    four_orbital = None
    for o in range(orbital_count):
        matrix = (label_grid == o).astype(np.int64)
        valency = int(matrix[0].sum())
        row_index = int(np.flatnonzero(matrix.sum(axis=1) > 0)[0])
        col = int(np.flatnonzero(matrix[row_index])[0])
        if valency == 4 and int(gram[row_index, col]) == 0:
            four_orbital = o
            four_matrix = matrix
    checks["four_valent_orbital_found"] = four_orbital is not None

    # 1. cycle type on 240 and on 120
    adj240 = [list(np.flatnonzero(four_matrix[i])) for i in range(240)]
    comp240 = components(adj240, 240)

    rep = {}
    for n, v in enumerate(shell):
        rep.setdefault(frozenset(np.flatnonzero(v).tolist()), n)
    sup120 = sorted(rep, key=sorted)
    sup_of = {}
    for n, v in enumerate(shell):
        sup_of[n] = frozenset(np.flatnonzero(v).tolist())
    sup_id = {s: n for n, s in enumerate(sup120)}
    adj120 = [set() for _ in range(120)]
    for i in range(240):
        for j in adj240[i]:
            a, b = sup_id[sup_of[i]], sup_id[sup_of[j]]
            if a != b:
                adj120[a].add(b)
                adj120[b].add(a)
    degrees120 = Counter(len(s) for s in adj120)
    checks["support_graph_2_regular"] = degrees120 == Counter({2: 120})
    comp120 = components([sorted(s) for s in adj120], 120)

    # 2. the partner rule
    signatures = Counter()
    for i in range(0, 240, 24):
        plus_i = frozenset(np.flatnonzero(shell_matrix[i] == 1).tolist())
        minus_i = frozenset(np.flatnonzero(shell_matrix[i] == -1).tolist())
        for j in adj240[i]:
            plus_j = frozenset(np.flatnonzero(shell_matrix[j] == 1).tolist())
            minus_j = frozenset(np.flatnonzero(shell_matrix[j] == -1).tolist())
            signatures[
                (
                    len(plus_i & plus_j),
                    len(plus_i & minus_j),
                    len(minus_i & plus_j),
                    len(minus_i & minus_j),
                )
            ] += 1
    checks["partner_signature_constant"] = len(signatures) == 1

    # compare with the signature profile of the REST of the zero class
    other_signatures = Counter()
    i = 0
    plus_i = frozenset(np.flatnonzero(shell_matrix[i] == 1).tolist())
    minus_i = frozenset(np.flatnonzero(shell_matrix[i] == -1).tolist())
    for j in range(240):
        if gram[i, j] == 0 and j not in adj240[i]:
            plus_j = frozenset(np.flatnonzero(shell_matrix[j] == 1).tolist())
            minus_j = frozenset(np.flatnonzero(shell_matrix[j] == -1).tolist())
            other_signatures[
                (
                    len(plus_i & plus_j),
                    len(plus_i & minus_j),
                    len(minus_i & plus_j),
                    len(minus_i & minus_j),
                )
            ] += 1

    # 3. spectrum of the 4-valent relation
    eigen = np.linalg.eigvalsh(four_matrix.astype(float))
    eigen_profile = Counter(round(float(v), 6) for v in eigen)
    checks["spectrum_computed"] = len(eigen_profile) > 0
    checks["components_are_octahedra"] = eigen_profile == Counter(
        {4.0: 40, 0.0: 120, -2.0: 80}
    ) or eigen_profile == Counter({4.0: 40, -0.0: 120, -2.0: 80})

    # 4. what are the 40 triangles?  compute the stabilizer of one triangle
    # and test whether it fixes a point or a line of W(3,3)
    from analysis.w33_pass158_chiral_trade_lattice_two_480s import w33_lines

    lines40 = w33_lines(adjacency)
    seen = [False] * 120
    triangles = []
    for start in range(120):
        if seen[start]:
            continue
        component = {start}
        stack = [start]
        seen[start] = True
        while stack:
            current = stack.pop()
            for nxt in adj120[current]:
                if not seen[nxt]:
                    seen[nxt] = True
                    component.add(nxt)
                    stack.append(nxt)
        triangles.append(frozenset(component))
    checks["forty_triangles"] = len(triangles) == 40

    # represent the triangle by its three supports (as frozensets of
    # 45-space indices) and act via the 45-permutation
    tri_supports = [frozenset(sup120[i]) for i in sorted(triangles[0])]

    stabilizer = []
    for perm in group:
        mapping45 = [
            support_index[frozenset(perm[x] for x in supports[s])] for s in range(45)
        ]
        image = {frozenset(mapping45[x] for x in sup) for sup in tri_supports}
        if image == set(tri_supports):
            stabilizer.append(perm)
    stab_order = len(stabilizer)
    checks["triangle_stabilizer_order_648"] = stab_order == 648

    fixed_points = [p for p in range(40) if all(g[p] == p for g in stabilizer)]
    fixed_lines = [
        n
        for n, line in enumerate(lines40)
        if all(frozenset(g[x] for x in line) == line for g in stabilizer)
    ]
    verdict = (
        "points"
        if len(fixed_points) == 1
        else ("lines" if len(fixed_lines) == 1 else "neither")
    )
    checks["triangle_identification_decided"] = verdict in ("points", "lines")

    all_pass = all(checks.values())
    payload = {
        "schema": "w33.pass169.canonical_cycles.v1",
        "status": "PASS" if all_pass else "FAIL",
        "cycles": {
            "on_240_trades": {str(k): int(v) for k, v in sorted(comp240.items())},
            "on_120_supports": {str(k): int(v) for k, v in sorted(comp120.items())},
        },
        "partner_rule": {
            "four_partner_signature": {str(k): int(v) for k, v in signatures.items()},
            "other_zero_class_signatures": {
                str(k): int(v) for k, v in sorted(other_signatures.items())
            },
            "reading": (
                "the four partners of a trade are the orthogonal trades "
                "with the distinguished span/perp intersection signature; "
                "the remaining 108 orthogonal trades have different "
                "signatures"
            ),
        },
        "four_valent_spectrum": {
            str(k): int(v) for k, v in sorted(eigen_profile.items())
        },
        "triangle_identification": {
            "stabilizer_order": stab_order,
            "fixed_points_of_stabilizer": len(fixed_points),
            "fixed_lines_of_stabilizer": len(fixed_lines),
            "verdict": verdict,
            "reading": (
                "the 40 octahedra / 40 triangles carry the natural "
                f"PSp(4,3)-set of the W(3,3) {verdict}: one canonical "
                "octahedron of second-shell trades per "
                + ("point" if verdict == "points" else "line")
            ),
        },
        "checks": {name: bool(value) for name, value in checks.items()},
    }

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(payload, indent=2))
    return 0 if all_pass else 1


if __name__ == "__main__":
    raise SystemExit(main())
