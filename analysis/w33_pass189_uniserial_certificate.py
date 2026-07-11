#!/usr/bin/env python3
"""Pass 189: the permutation module is uniserial -- the socle certificate.

Pass 187 exhibited the chain 0 < j < C < im A2 < ker A2 < C-perp < j-perp
< M with irreducible layers 1,14,1,8,1,14,1.  This witness upgrades the
chain to a UNISERIALITY theorem: since every composition factor of M lies
in {1, 8, 14}, it suffices to show soc(M/M_i) is simple at every step,
i.e. exactly one of Hom(1,-), Hom(8,-), Hom(14,-) is nonzero on each
quotient, with the dimension of a single copy (1 for the 1 and the 14,
2 for the 8, whose endomorphism field is F4).  All Hom spaces are
computed by exact F2 linear algebra; the chain is therefore the unique
composition series of F2^40, and every submodule is one of the eight
chain members.

Corollary ledger: the sentinel code, the SO(10) shadow, its fixed vector,
and the E8 shadow are not merely present -- they are the ONLY invariant
binary structures the geometry has.
"""

from __future__ import annotations

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
    w33_lines,
)
from analysis.w33_pass161_gq42_ihara_inheritance import small_generating_set
from analysis.w33_pass187_f2_layer_sandwich import (
    exhaustive_cyclic_irreducible,
    f2_row_space,
    subquotient_action_matrices,
)

OUT = ROOT / "data" / "w33_pass189_uniserial_certificate.json"


def f2_kernel_dim(matrix):
    work = matrix.astype(np.uint8).copy() % 2
    rows, cols = work.shape
    rank = 0
    for col in range(cols):
        pivot = None
        for r in range(rank, rows):
            if work[r, col]:
                pivot = r
                break
        if pivot is None:
            continue
        work[[rank, pivot]] = work[[pivot, rank]]
        mask = work[:, col].astype(bool).copy()
        mask[rank] = False
        work[mask] ^= work[rank]
        rank += 1
        if rank == rows:
            break
    return cols - rank


def hom_dim_f2(act_v, act_w):
    dim_v = act_v[0].shape[0]
    dim_w = act_w[0].shape[0]
    blocks = []
    for gv, gw in zip(act_v, act_w):
        blocks.append(
            (
                np.kron(gv.T.astype(np.int64), np.eye(dim_w, dtype=np.int64))
                + np.kron(np.eye(dim_v, dtype=np.int64), gw.astype(np.int64))
            )
            % 2
        )
    return f2_kernel_dim(np.vstack(blocks).astype(np.uint8))


def f2_kernel_basis(matrix):
    work = [row.copy().astype(np.uint8) % 2 for row in matrix]
    n = matrix.shape[1]
    pivots = []
    rank = 0
    for col in range(n):
        pivot = next((r for r in range(rank, len(work)) if work[r][col]), None)
        if pivot is None:
            continue
        work[rank], work[pivot] = work[pivot], work[rank]
        for r in range(len(work)):
            if r != rank and work[r][col]:
                work[r] = work[r] ^ work[rank]
        pivots.append(col)
        rank += 1
    free = [c for c in range(n) if c not in pivots]
    out = []
    for fc in free:
        vec = np.zeros(n, dtype=np.uint8)
        vec[fc] = 1
        for r, pc in zip(work[:rank], pivots):
            if r[fc]:
                vec[pc] = 1
        out.append(vec)
    return out


def main():
    points, adjacency, symplectic = build_w33()
    lines = w33_lines(adjacency)
    checks = {}

    incidence = np.zeros((40, 40), dtype=np.uint8)
    for row, line in enumerate(lines):
        for p in line:
            incidence[row, p] = 1
    a2 = (adjacency % 2).astype(np.uint8)

    generators, group = build_group(points, symplectic)
    checks["group_order"] = len(group) == 25920
    two_gens = small_generating_set(group)

    j = np.ones(40, dtype=np.uint8)
    C = f2_row_space(np.array(f2_kernel_basis(incidence), dtype=np.uint8))
    im_a2 = f2_row_space(a2)
    ker_a2 = f2_row_space(np.array(f2_kernel_basis(a2), dtype=np.uint8))
    c_perp = f2_row_space(incidence)
    j_perp_rows = [
        np.eye(40, dtype=np.uint8)[i] ^ np.eye(40, dtype=np.uint8)[i + 1]
        for i in range(39)
    ]
    j_perp = f2_row_space(np.array(j_perp_rows, dtype=np.uint8))
    full = [np.eye(40, dtype=np.uint8)[i] for i in range(40)]

    chain = [
        ("0", []),
        ("j", [j]),
        ("C", C),
        ("imA2", im_a2),
        ("kerA2", ker_a2),
        ("Cperp", c_perp),
        ("jperp", j_perp),
    ]
    layer_names = ["1", "14", "1", "8", "1", "14", "1"]

    # simple modules as action-matrix pairs
    simple_one = [np.eye(1, dtype=np.uint8)] * 2
    simple_fourteen, d14 = subquotient_action_matrices(C, [j], two_gens)
    checks["fourteen_dim"] = d14 == 14
    simple_eight, d8 = subquotient_action_matrices(ker_a2, im_a2, two_gens)
    checks["eight_dim"] = d8 == 8

    checks["end_8_is_F4"] = hom_dim_f2(simple_eight, simple_eight) == 2
    checks["end_14_is_F2"] = hom_dim_f2(simple_fourteen, simple_fourteen) == 1
    irred14, vector_orbits14 = exhaustive_cyclic_irreducible(simple_fourteen, d14)
    irred8, vector_orbits8 = exhaustive_cyclic_irreducible(simple_eight, d8)
    checks["simple_14_irreducible_exhaustive"] = irred14
    checks["simple_8_irreducible_exhaustive"] = irred8

    simples = {"1": simple_one, "8": simple_eight, "14": simple_fourteen}
    expected_dims = {"1": 1, "8": 2, "14": 1}

    socle_table = []
    uniserial = True
    for step, (name, bottom) in enumerate(chain):
        quotient, qdim = subquotient_action_matrices(full, bottom, two_gens)
        row = {"quotient": f"M/{name}", "dimension": qdim}
        winner = None
        for sname, smod in simples.items():
            h = hom_dim_f2(smod, quotient)
            row[f"hom_{sname}"] = int(h)
            if h:
                if winner is not None:
                    uniserial = False
                winner = sname
                if h != expected_dims[sname]:
                    uniserial = False
        expected_layer = layer_names[step]
        if winner != expected_layer:
            uniserial = False
        row["socle"] = winner
        socle_table.append(row)
    checks["socle_simple_at_every_step"] = bool(uniserial)
    checks["uniserial"] = bool(uniserial)

    all_pass = all(checks.values())
    payload = {
        "schema": "w33.pass189.uniserial_certificate.v1",
        "status": "PASS" if all_pass else "FAIL",
        "theorem": (
            "F2^40 is a uniserial PSp(4,3)-module with composition series "
            "0 < j < C < im A2 < ker A2 < C_perp < j_perp < M and layers "
            "1,14,1,8,1,14,1: every invariant binary structure of W(3,3) "
            "is one of the eight chain members"
        )
        if uniserial
        else "socle table recorded; see data",
        "socle_table": socle_table,
        "endomorphism_fields": {"8": "F4", "14": "F2"},
        "simple_module_scan": {
            "14_nonzero_vectors": 2**14 - 1,
            "14_vector_orbits": vector_orbits14,
            "8_nonzero_vectors": 2**8 - 1,
            "8_vector_orbits": vector_orbits8,
        },
        "corollaries": [
            "the sentinel code [40,15,8] is the unique 15-dimensional "
            "invariant code",
            "H10 = C_perp/C with its (1,8,1) structure is forced",
            "the E8 shadow is the unique 8-dimensional subquotient",
            "there are exactly 8 invariant binary codes of length 40",
        ],
        "checks": {name: bool(value) for name, value in checks.items()},
    }

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(payload, indent=2))
    return 0 if all_pass else 1


if __name__ == "__main__":
    raise SystemExit(main())
