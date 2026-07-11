#!/usr/bin/env python3
"""Pass 172: the 90-trade association scheme of W(3,3).

Pass 168 showed the 240-shell of GQ(4,2) hides a rank-10 non-commutative
configuration under its inner-product classes.  This witness settles the
symmetric question one level up: the 90 minimal trades of W(3,3)'s chiral
lattice carry inner-product classes {8(id), -8, 2, -2, 0} of valencies
{1, 1, 32, 32, 24} -- and here the orbital rank equals 5, so the fusion IS
the orbital scheme:

1. COHERENCE + EXACT INTERSECTION NUMBERS.  All products constant on
   classes; the scheme is commutative and symmetric.

2. THE EIGENMATRIX.  The five common eigenspaces and the full first
   eigenmatrix P, integral and exact.

3. THE ANTIPODAL QUOTIENT.  The -8 class is the antipodal pairing; the
   quotient scheme on the 45 supports is the rank-3 scheme of
   SRG(45,12,3,3) = GQ(4,2), re-derived from the quotient relations:
   the 90-scheme is an antipodal double cover of the support geometry.
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
)
from analysis.w33_pass161_gq42_ihara_inheritance import small_generating_set

OUT = ROOT / "data" / "w33_pass172_ninety_trade_scheme.json"


def main():
    points, adjacency, symplectic = build_w33()
    checks = {}

    dark = saturated_kernel(adjacency + 4 * np.eye(40, dtype=np.int64))
    min_norm, shell, _, _ = minimal_shell(dark)
    shell = [np.asarray(v, dtype=np.int64) for v in shell]
    checks["ninety_trades"] = len(shell) == 90 and min_norm == 8

    shell_matrix = np.array(shell, dtype=np.int64)
    gram = shell_matrix @ shell_matrix.T
    values = sorted(set(int(v) for v in gram.reshape(-1)))
    checks["five_ip_classes"] = values == [-8, -2, 0, 2, 8]

    relations = {"id": np.eye(90, dtype=np.int64)}
    for value in (-8, -2, 0, 2):
        relations[str(value)] = (gram == value).astype(np.int64)
    checks["partition"] = bool(
        np.array_equal(sum(relations.values()), np.ones((90, 90), dtype=np.int64))
    )
    valencies = {k: int(m[0].sum()) for k, m in relations.items()}

    # coherence + intersection numbers
    keys = list(relations)
    intersection = {}
    coherent = True
    commutative = True
    symmetric = all(np.array_equal(relations[k], relations[k].T) for k in keys)
    for i in keys:
        for j in keys:
            product = relations[i] @ relations[j]
            if not np.array_equal(product, relations[j] @ relations[i]):
                commutative = False
            numbers = {}
            for k in keys:
                cells = np.diag(product) if k == "id" else product[relations[k] == 1]
                distinct = set(int(v) for v in cells)
                if len(distinct) != 1:
                    coherent = False
                    break
                numbers[k] = distinct.pop()
            if not coherent:
                break
            intersection[f"{i}*{j}"] = numbers
        if not coherent:
            break
    checks["coherent"] = bool(coherent)
    checks["commutative"] = bool(commutative)
    checks["symmetric"] = bool(symmetric)

    # schurian: orbital rank equals 5
    generators, group = build_group(points, symplectic)
    checks["group_order"] = len(group) == 25920
    two_gens = small_generating_set(group)
    shell_keys = {tuple(int(x) for x in v): n for n, v in enumerate(shell)}
    gen_maps = []
    for g in two_gens:
        table = []
        for v in shell:
            image = np.empty(40, dtype=np.int64)
            for src in range(40):
                image[g[src]] = v[src]
            table.append(shell_keys[tuple(int(x) for x in image)])
        gen_maps.append(table)
    checks["transitive"] = orbit_count(90, gen_maps) == 1
    tables = []
    for mapping in gen_maps:
        arr = np.asarray(mapping, dtype=np.int64)
        tables.append((arr[:, None] * 90 + arr[None, :]).reshape(-1))
    rank = orbit_count(90 * 90, tables)
    checks["schurian_rank_5"] = rank == 5

    # eigenmatrix via a generic element of the Bose-Mesner algebra
    generic = (
        1.0 * relations["2"]
        + np.pi * relations["-2"]
        + np.e * relations["0"]
        + np.sqrt(2) * relations["-8"]
    ).astype(float)
    eigvals, eigvecs = np.linalg.eigh(generic)
    groups = {}
    for idx, value in enumerate(eigvals):
        placed = False
        for key in groups:
            if abs(key - float(value)) < 1e-8:
                groups[key].append(idx)
                placed = True
                break
        if not placed:
            groups[float(value)] = [idx]
    eigenmatrix = []
    multiplicities = []
    consistent = True
    integral = True
    for key in sorted(groups, reverse=True):
        basis = eigvecs[:, groups[key]]
        row = []
        for name in ("id", "2", "-2", "0", "-8"):
            block = basis.T @ relations[name].astype(float) @ basis
            scalar = float(np.trace(block)) / block.shape[0]
            off = np.abs(block - scalar * np.eye(block.shape[0])).max()
            if off > 1e-6:
                consistent = False
            if abs(scalar - round(scalar)) > 1e-6:
                integral = False
            row.append(round(scalar, 6))
        eigenmatrix.append(row)
        multiplicities.append(len(groups[key]))
    checks["eigenmatrix_consistent"] = bool(consistent)
    checks["eigenspace_count_5"] = len(eigenmatrix) == 5
    checks["multiplicities_sum_90"] = sum(multiplicities) == 90
    checks["eigenmatrix_integral"] = bool(integral)

    # antipodal quotient onto the 45 supports
    checks["antipode_is_negation"] = all(
        int(gram[i, j]) != -8 or np.array_equal(shell_matrix[i], -shell_matrix[j])
        for i in range(90)
        for j in range(90)
    )
    rep = {}
    for n, v in enumerate(shell):
        rep.setdefault(frozenset(np.flatnonzero(v).tolist()), n)
    sup45 = sorted(rep, key=sorted)
    sup_id = {s: n for n, s in enumerate(sup45)}
    quotient0 = np.zeros((45, 45), dtype=np.int64)
    for i, j in combinations(range(90), 2):
        if gram[i, j] == 0:
            a = sup_id[frozenset(np.flatnonzero(shell_matrix[i]).tolist())]
            b = sup_id[frozenset(np.flatnonzero(shell_matrix[j]).tolist())]
            if a != b:
                quotient0[a, b] = quotient0[b, a] = 1
    q2 = quotient0 @ quotient0
    srg_ok = bool((quotient0.sum(axis=1) == 12).all()) and all(
        q2[a, b] == 3 for a, b in combinations(range(45), 2)
    )
    checks["quotient_zero_relation_is_gq42_srg"] = srg_ok

    all_pass = all(checks.values())
    payload = {
        "schema": "w33.pass172.ninety_trade_scheme.v1",
        "status": "PASS" if all_pass else "FAIL",
        "scheme": {
            "size": 90,
            "classes": 4,
            "valencies": valencies,
            "coherent": bool(coherent),
            "commutative": bool(commutative),
            "symmetric": bool(symmetric),
            "schurian_rank": int(rank),
            "reading": (
                "unlike the 240-shell one level down, the 90-shell's "
                "inner-product classes ARE the orbitals: a symmetric "
                "commutative 4-class association scheme, the antipodal "
                "double cover of the GQ(4,2) support geometry"
            ),
        },
        "eigenmatrix": {
            "row_order": "eigenspaces of the 0-relation, descending",
            "column_order": ["id", "2", "-2", "0", "-8"],
            "P": eigenmatrix,
            "multiplicities": multiplicities,
        },
        "intersection_numbers": intersection,
        "checks": {name: bool(value) for name, value in checks.items()},
    }

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(payload, indent=2))
    return 0 if all_pass else 1


if __name__ == "__main__":
    raise SystemExit(main())
