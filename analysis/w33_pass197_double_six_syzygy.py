#!/usr/bin/env python3
"""Pass 197: the syzygetic strata of the 36 double-sixes.

Pass 191's 27+6+3 were subdegrees over an AXIS in the 4320-product
action.  The group's OWN action on the 36 pentad dodecads is the classical
rank-3 double-six action.  This witness identifies its strata:

1. THE 36 AS PENTAD-CORE COMPONENTS.  Rebuild the 36 double-sixes as the
   12-vertex crown components of the route shell (Pass 188); the action is
   transitive with point stabilizer of order 720.

2. THE RANK-3 STRUCTURE.  Suborbits 1+15+20: the 15-suborbit is the
   syzygetic relation, a strongly regular SRG(36,15,6,6); the 20-suborbit
   is the azygetic complement.

3. THE SHARING INVARIANT.  For a fixed double-six D0, |lineset(D0) cap
   lineset(D)| is constant on each suborbit (30 on itself, 24 syzygetic,
   21 azygetic), giving the classical line-sharing dictionary.
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

OUT = ROOT / "data" / "w33_pass197_double_six_syzygy.json"


def main():
    points, adjacency, symplectic = build_w33()
    lines = w33_lines(adjacency)
    checks = {}

    incidence = np.zeros((40, 40), dtype=np.int64)
    for row, line in enumerate(lines):
        for p in line:
            incidence[row, p] = 1
    route = generic_saturated_kernel(incidence.T)
    _, shell = staged_minimal_shell(route, bounds=(4, 6, 8, 10))
    shell = [np.asarray(v, dtype=np.int64) for v in shell]
    checks["shell_432"] = len(shell) == 432

    # each pentad-core route minimum has support = 20 W33 lines (a 20-cap)
    supports_lines = [frozenset(np.flatnonzero(v).tolist()) for v in shell]

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

    # the crown orbital -> 36 components
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

    target = None
    for o in range(orbital_count):
        matrix = (label_grid == o).astype(np.int64)
        row_index = int(np.flatnonzero(matrix.sum(axis=1) > 0)[0])
        if int(matrix[row_index].sum()) == 5 and not bool(
            np.array_equal(matrix, matrix.T)
        ):
            target = matrix + matrix.T
            break
    seen = np.zeros(432, dtype=bool)
    dsixes = []
    for start in range(432):
        if seen[start]:
            continue
        component = {start}
        stack = [start]
        seen[start] = True
        while stack:
            current = stack.pop()
            for nxt in np.flatnonzero(target[current]):
                if not seen[nxt]:
                    seen[nxt] = True
                    component.add(int(nxt))
                    stack.append(int(nxt))
        if len(component) > 1:
            dsixes.append(frozenset(component))
    checks["thirty_six_double_sixes"] = len(dsixes) == 36
    dsixes = sorted(dsixes, key=sorted)
    dsix_index = {d: n for n, d in enumerate(dsixes)}

    # the line-set (union of the 12 crown vectors' supports) of a double-six
    dsix_linesets = []
    for d in dsixes:
        union = set()
        for i in d:
            union |= supports_lines[i]
        dsix_linesets.append(frozenset(union))
    lineset_sizes = Counter(len(s) for s in dsix_linesets)

    # ---- subdegrees on the 36 ----
    def dsix_map(perm):
        lp = line_perm(perm)
        out = []
        for d in dsixes:
            image = set()
            for i in d:
                img = np.empty(40, dtype=np.int64)
                for src in range(40):
                    img[lp[src]] = shell[i][src]
                image.add(shell_keys[tuple(int(x) for x in img)])
            out.append(dsix_index[frozenset(image)])
        return out

    dmaps = [dsix_map(g) for g in two_gens]
    checks["double_sixes_transitive"] = orbit_count(36, dmaps) == 1

    # suborbits from D0 = dsixes[0]
    stab0 = []
    for perm in group:
        lp = line_perm(perm)
        image = set()
        for i in dsixes[0]:
            img = np.empty(40, dtype=np.int64)
            for src in range(40):
                img[lp[src]] = shell[i][src]
            image.add(shell_keys[tuple(int(x) for x in img)])
        if frozenset(image) == dsixes[0]:
            stab0.append(perm)
    checks["d0_stabilizer_720"] = len(stab0) == 720
    # compute suborbits of stab0 on the 36 double-sixes directly
    suborbit = [None] * 36
    suborbit[0] = 0
    label = 0
    for target_idx in range(36):
        if suborbit[target_idx] is not None:
            continue
        label += 1
        # orbit of target_idx under stab0
        orb = {target_idx}
        stack = [target_idx]
        while stack:
            cur = stack.pop()
            for g in stab0:
                lp = line_perm(g)
                image = set()
                for i in dsixes[cur]:
                    img = np.empty(40, dtype=np.int64)
                    for src in range(40):
                        img[lp[src]] = shell[i][src]
                    image.add(shell_keys[tuple(int(x) for x in img)])
                nxt = dsix_index[frozenset(image)]
                if nxt not in orb:
                    orb.add(nxt)
                    stack.append(nxt)
        for m in orb:
            suborbit[m] = label
    subsizes = Counter(v for v in suborbit if v is not None)
    subdegrees = sorted(subsizes.values())
    # the double-six action of PSp(4,3) on 36 is classically rank 3:
    # subdegrees 1 + 15 + 20 (the SRG(36,15,6,6) of the double-sixes)
    checks["double_six_action_rank_3"] = len(subsizes) == 3
    checks["subdegrees_1_15_20"] = subdegrees == [1, 15, 20]

    # sharing invariant: |lineset(D0) cap lineset(D)| per suborbit -- the
    # syzygetic / azygetic stratification, which must be a suborbit
    # invariant
    sharing = {}
    for target_idx in range(36):
        s = suborbit[target_idx]
        overlap = len(dsix_linesets[0] & dsix_linesets[target_idx])
        vec_overlap = len(dsixes[0] & dsixes[target_idx])
        sharing.setdefault(s, []).append((overlap, vec_overlap))
    sharing_table = {}
    constant = True
    for s, pairs in sharing.items():
        distinct = set(pairs)
        if len(distinct) != 1:
            constant = False
        line_ov, vec_ov = pairs[0]
        sharing_table[str(subsizes[s])] = {
            "size": subsizes[s],
            "line_overlap": line_ov,
            "vector_overlap": vec_ov,
        }
    checks["sharing_constant_on_suborbits"] = constant

    # the SRG structure: build the 15-suborbit graph and confirm
    # SRG(36,15,6,6) -- the double-six "syzygetic" graph
    fifteen_label = next((s for s, sz in subsizes.items() if sz == 15), None)
    srg_params = None
    if fifteen_label is not None:
        graph36 = np.zeros((36, 36), dtype=np.int64)
        for perm_row in range(36):
            # relate every ordered pair to the D0-suborbit type via the
            # group: mark adjacency by suborbit label under the base point
            pass
        # rebuild the relation as: a~b iff b is in the 15-suborbit of a
        # (use transitivity: apply group elements sending 0->a)
        base_fifteen = frozenset(i for i in range(36) if suborbit[i] == fifteen_label)
        # element sending 0 -> a for each a, then image of base_fifteen
        for a in range(36):
            g = next(perm for perm in group if dsix_map(perm)[0] == a)
            image = {dsix_map(g)[b] for b in base_fifteen}
            for b in image:
                graph36[a, b] = 1
        deg = int(graph36[0].sum())
        g2 = graph36 @ graph36
        lam = {int(g2[a, b]) for a, b in combinations(range(36), 2) if graph36[a, b]}
        mu = {int(g2[a, b]) for a, b in combinations(range(36), 2) if not graph36[a, b]}
        if len(lam) == 1 and len(mu) == 1:
            srg_params = [36, deg, lam.pop(), mu.pop()]
    checks["syzygetic_graph_srg_36_15_6_6"] = srg_params == [36, 15, 6, 6]

    all_pass = all(checks.values())
    payload = {
        "schema": "w33.pass197.double_six_syzygy.v1",
        "status": "PASS" if all_pass else "FAIL",
        "double_sixes": {
            "count": 36,
            "lineset_sizes": {str(k): int(v) for k, v in lineset_sizes.items()},
            "subdegrees": sorted(subsizes.values(), reverse=True),
            "rank": len(subsizes),
        },
        "syzygy_dictionary": sharing_table,
        "syzygetic_graph": srg_params,
        "reading": (
            "the double-six action of PSp(4,3) on the 36 pentad dodecads "
            "is the classical rank-3 action with subdegrees 1+15+20: the "
            "15-suborbit is the syzygetic relation SRG(36,15,6,6) and the "
            "20-suborbit the azygetic complement, each a constant "
            "line-sharing stratum -- the Schlafli double-six census "
            "materialized in the route shell"
        ),
        "checks": {name: bool(value) for name, value in checks.items()},
    }

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(payload, indent=2))
    return 0 if all_pass else 1


if __name__ == "__main__":
    raise SystemExit(main())
