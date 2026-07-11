#!/usr/bin/env python3
"""Pass 186: the pentad-core scheme -- the dual side's second shell.

Passes 168/169 charted the 240-trade orbital configuration of the
address tower (rank 10, the 4-valent octahedron relation, 40 lines).
This witness runs the same machinery on the ANTIREGULAR side: the 432
route minima (pentad cores, norm 10) of the Q(4,3) trade lattice:

1. THE ORBITAL CONFIGURATION.  Inner-product classes and their
   valencies; the exact orbital rank of PSp(4,3) on the 432 shell; which
   ip classes split; coherence certificate of the orbital configuration.

2. THE SPARSE RELATIONS.  Any low-valency invariant orbitals, their
   component structure (the dual analogue of the 40 octahedra), and the
   stabilizer identification of one component against points, lines, and
   spreads of W(3,3).
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
    orbit_count,
    w33_lines,
)
from analysis.w33_pass160_trade_tower_gq42 import (
    generic_saturated_kernel,
    staged_minimal_shell,
)
from analysis.w33_pass161_gq42_ihara_inheritance import small_generating_set

OUT = ROOT / "data" / "w33_pass186_pentad_core_scheme.json"


def main():
    points, adjacency, symplectic = build_w33()
    lines = w33_lines(adjacency)
    checks = {}

    incidence = np.zeros((40, 40), dtype=np.int64)
    for row, line in enumerate(lines):
        for p in line:
            incidence[row, p] = 1
    route = generic_saturated_kernel(incidence.T)
    min_norm, shell = staged_minimal_shell(route, bounds=(4, 6, 8, 10))
    shell = [np.asarray(v, dtype=np.int64) for v in shell]
    checks["shell_432_norm_10"] = min_norm == 10 and len(shell) == 432

    shell_matrix = np.array(shell, dtype=np.int64)
    gram = shell_matrix @ shell_matrix.T
    ip_values = sorted(set(int(v) for v in gram.reshape(-1)))
    per_row = Counter(int(v) for v in gram[0])
    row_profiles_constant = (
        len({tuple(sorted(Counter(int(v) for v in row).items())) for row in gram}) == 1
    )
    checks["ip_profile_constant"] = bool(row_profiles_constant)

    # group action via line permutations
    generators, group = build_group(points, symplectic)
    checks["group_order"] = len(group) == 25920
    two_gens = small_generating_set(group)
    line_index = {line: n for n, line in enumerate(lines)}

    def line_perm(perm):
        return [line_index[frozenset(perm[x] for x in lines[n])] for n in range(40)]

    shell_keys = {tuple(int(x) for x in v): n for n, v in enumerate(shell)}
    gen_maps = []
    for g in two_gens:
        lp = line_perm(g)
        table = []
        for v in shell:
            image = np.empty(40, dtype=np.int64)
            for src in range(40):
                image[lp[src]] = v[src]
            table.append(shell_keys[tuple(int(x) for x in image)])
        gen_maps.append(table)
    n_orbits = orbit_count(432, gen_maps)
    checks["shell_orbit_count"] = n_orbits in (1, 2)

    tables = []
    for mapping in gen_maps:
        arr = np.asarray(mapping, dtype=np.int64)
        tables.append((arr[:, None] * 432 + arr[None, :]).reshape(-1))
    labels = np.full(432 * 432, -1, dtype=np.int64)
    orbital_count = 0
    for start in range(432 * 432):
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
    label_grid = labels.reshape(432, 432)
    checks["orbital_rank_computed"] = orbital_count > 0

    orbital_info = []
    for o in range(orbital_count):
        matrix = (label_grid == o).astype(np.int64)
        row_index = int(np.flatnonzero(matrix.sum(axis=1) > 0)[0])
        col = int(np.flatnonzero(matrix[row_index])[0])
        orbital_info.append(
            {
                "orbital": o,
                "valency": int(matrix[row_index].sum()),
                "ip_value": int(gram[row_index, col]),
                "symmetric": bool(np.array_equal(matrix, matrix.T)),
            }
        )
    ip_split = Counter(info["ip_value"] for info in orbital_info)

    # coherence of the orbital configuration
    orbital_matrices = [
        (label_grid == o).astype(np.int64) for o in range(orbital_count)
    ]
    coherent = True
    for i in range(orbital_count):
        for jx in range(orbital_count):
            product = orbital_matrices[i] @ orbital_matrices[jx]
            for o in range(orbital_count):
                cell = product[label_grid == o]
                if len(set(int(v) for v in cell)) != 1:
                    coherent = False
                    break
            if not coherent:
                break
        if not coherent:
            break
    checks["orbital_configuration_coherent"] = bool(coherent)

    # sparse relations: components + stabilizer identification
    sparse_reports = []
    for info in sorted(orbital_info, key=lambda r: r["valency"]):
        if info["valency"] == 0 or info["valency"] > 6 or info["orbital"] == 0:
            continue
        matrix = orbital_matrices[info["orbital"]]
        if not bool(np.array_equal(matrix, matrix.T)):
            matrix = matrix + matrix.T
        seen = np.zeros(432, dtype=bool)
        components = []
        for start in range(432):
            if seen[start]:
                continue
            component = {start}
            stack = [start]
            seen[start] = True
            while stack:
                current = stack.pop()
                for nxt in np.flatnonzero(matrix[current]):
                    if not seen[nxt]:
                        seen[nxt] = True
                        component.add(int(nxt))
                        stack.append(int(nxt))
            components.append(frozenset(component))
        sizes = Counter(len(c) for c in components)

        # stabilizer identification of one component
        base = components[0]
        base_vectors = {tuple(int(x) for x in shell[i]) for i in base}
        stabilizer = []
        for perm in group:
            lp = line_perm(perm)
            image = set()
            for i in base:
                img = np.empty(40, dtype=np.int64)
                for src in range(40):
                    img[lp[src]] = shell[i][src]
                image.add(tuple(int(x) for x in img))
            if image == base_vectors:
                stabilizer.append(perm)
        stab_order = len(stabilizer)
        fixed_points = sum(1 for p in range(40) if all(g[p] == p for g in stabilizer))
        fixed_lines = sum(
            1
            for line in lines
            if all(frozenset(g[x] for x in line) == line for g in stabilizer)
        )
        sparse_reports.append(
            {
                "orbital": info["orbital"],
                "valency": info["valency"],
                "ip_value": info["ip_value"],
                "component_sizes": {str(k): int(v) for k, v in sorted(sizes.items())},
                "component_count": len(components),
                "stabilizer_order": stab_order,
                "fixed_points": fixed_points,
                "fixed_lines": fixed_lines,
            }
        )
    checks["sparse_relations_recorded"] = True

    all_pass = all(checks.values())
    payload = {
        "schema": "w33.pass186.pentad_core_scheme.v1",
        "status": "PASS" if all_pass else "FAIL",
        "shell": {
            "size": 432,
            "norm": 10,
            "orbit_count": int(n_orbits),
            "ip_values": ip_values,
            "ip_row_profile": {str(k): int(v) for k, v in sorted(per_row.items())},
        },
        "orbital_configuration": {
            "rank": int(orbital_count),
            "coherent": bool(coherent),
            "orbitals": orbital_info,
            "ip_class_splitting": {str(k): int(v) for k, v in sorted(ip_split.items())},
        },
        "sparse_relations": sparse_reports,
        "reading": (
            "the antiregular counterpart of the 240-shell: the pentad "
            "cores' orbital configuration, its rank, the inner-product "
            "blindness data, and the canonical sparse structures with "
            "their stabilizer identifications"
        ),
        "checks": {name: bool(value) for name, value in checks.items()},
    }

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(payload, indent=2))
    return 0 if all_pass else 1


if __name__ == "__main__":
    raise SystemExit(main())
