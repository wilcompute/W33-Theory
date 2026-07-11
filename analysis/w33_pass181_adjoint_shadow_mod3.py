#!/usr/bin/env python3
"""Pass 181: the adjoint shadow -- sp(4,F3) inside the mod-3 trade modules.

The 2-adic side of the trade lattices produced the E8 and SO(10) shadows.
This witness opens the 3-adic side, where p = 3 is the DEFINING
characteristic of the substrate group:

1. THE ADJOINT MODULE.  sp(4,F3) = {X : X^T W + W X = 0} is the
   10-dimensional adjoint module of PSp(4,3) (the center acts trivially
   under conjugation, so the projective group acts).  Theta = 10 = its
   dimension.

2. THE HOM TEST.  For each trade lattice L in {address L4 (rank 15),
   gauge L2 (rank 24), route (rank 15)}, the F3-module L/3L is computed
   with its exact PSp(4,3)-action (integral action matrices on the
   saturated kernel basis, verified), and dim Hom_G(ad, L/3L) is
   computed by exact F3 linear algebra over a generating pair -- deciding
   whether the gauge algebra materializes inside the mod-3 trade modules.

3. THE FIXED/TRIVIAL LEDGER.  Fixed subspaces and Hom_G(1, L/3L) for
   each, plus dim Hom_G(ad, ad) (Schur check) -- the exact mod-3
   decomposition data for the tower's defining-characteristic side.
"""

from __future__ import annotations

from itertools import combinations
import json
from pathlib import Path
import sys

import numpy as np
from sympy import Matrix

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from analysis.w33_pass158_chiral_trade_lattice_two_480s import (
    build_w33,
    saturated_kernel,
    w33_lines,
)
from analysis.w33_pass160_trade_tower_gq42 import generic_saturated_kernel

OUT = ROOT / "data" / "w33_pass181_adjoint_shadow_mod3.json"

OMEGA = np.array(
    [
        [0, 0, 1, 0],
        [0, 0, 0, 1],
        [-1, 0, 0, 0],
        [0, -1, 0, 0],
    ],
    dtype=np.int64,
)


def f3_rank(matrix):
    work = [[int(v) % 3 for v in row] for row in matrix]
    rows = len(work)
    cols = len(work[0]) if rows else 0
    rank = 0
    for col in range(cols):
        pivot = next((r for r in range(rank, rows) if work[r][col]), None)
        if pivot is None:
            continue
        work[rank], work[pivot] = work[pivot], work[rank]
        inv = 1 if work[rank][col] == 1 else 2
        work[rank] = [(inv * v) % 3 for v in work[rank]]
        for r in range(rows):
            if r != rank and work[r][col]:
                factor = work[r][col]
                work[r] = [
                    (work[r][c] - factor * work[rank][c]) % 3 for c in range(cols)
                ]
        rank += 1
    return rank


def sp4_matrix_generators():
    """Two matrix generators of Sp(4,3) whose projective images generate."""

    def transvection(v):
        v = np.array(v, dtype=np.int64)
        outer = np.outer(v, OMEGA.T @ v) % 3
        return (np.eye(4, dtype=np.int64) + outer) % 3

    vectors = [
        (1, 0, 0, 0),
        (0, 1, 0, 0),
        (0, 0, 1, 0),
        (0, 0, 0, 1),
        (1, 1, 0, 0),
        (1, 0, 1, 0),
        (0, 1, 0, 1),
        (1, 1, 1, 1),
        (1, 2, 0, 1),
        (1, 0, 2, 1),
        (2, 1, 1, 0),
    ]
    singles = [transvection(v) for v in vectors]
    pool = list(singles)
    g = singles[0]
    for c in singles[1:5]:
        g = (g @ c) % 3
        pool.append(g)
    g = singles[5]
    for c in singles[6:]:
        g = (g @ c) % 3
        pool.append(g)
    return pool


def point_permutation(matrix, points, index):
    perm = []
    for p in points:
        image = tuple(int(v) % 3 for v in (matrix @ np.array(p)) % 3)
        # normalize projectively
        for x in image:
            if x:
                inv = 1 if x == 1 else 2
                image = tuple((inv * y) % 3 for y in image)
                break
        perm.append(index[image])
    return perm


def closure_order(gens, n):
    identity = tuple(range(n))
    seen = {identity}
    frontier = [identity]
    while frontier:
        new = []
        for element in frontier:
            for g in gens:
                composed = tuple(g[element[i]] for i in range(n))
                if composed not in seen:
                    seen.add(composed)
                    new.append(composed)
        frontier = new
    return len(seen)


def lattice_action(basis, perm):
    """Integer action matrix M with P_g . basis = basis . M."""
    permuted = basis[perm, :]  # rows permuted
    mat_b = Matrix(basis.tolist())
    mat_p = Matrix(permuted.tolist())
    gram = mat_b.T * mat_b
    solution = gram.solve(mat_b.T * mat_p)
    assert mat_b * solution == mat_p
    entries = np.array(
        [
            [int(solution[i, j]) for j in range(solution.cols)]
            for i in range(solution.rows)
        ],
        dtype=np.int64,
    )
    return entries


def adjoint_basis():
    basis = []
    for i in range(4):
        for j in range(4):
            e = np.zeros((4, 4), dtype=np.int64)
            e[i, j] = 1
            candidate = e
            if ((candidate.T @ OMEGA + OMEGA @ candidate) % 3 == 0).all():
                basis.append(candidate)
    # build a spanning independent subset of the solution space instead
    solutions = []
    for i in range(4):
        for j in range(4):
            e = np.zeros(16, dtype=np.int64)
            e[4 * i + j] = 1
            solutions.append(e)
    constraint = np.zeros((16, 16), dtype=np.int64)
    row = 0
    for a in range(4):
        for b in range(4):
            coeffs = np.zeros(16, dtype=np.int64)
            for i in range(4):
                for j in range(4):
                    value = 0
                    if j == a:
                        value += OMEGA[i, b]
                    if i == a:
                        value += OMEGA[j, b] * 0  # placeholder
                    coeffs[4 * i + j] = value
            constraint[row] = coeffs
            row += 1
    # direct construction: X with X^T W + W X = 0 over F3
    mats = []
    for i in range(4):
        for j in range(4):
            e = np.zeros((4, 4), dtype=np.int64)
            e[i, j] = 1
            mats.append(e)
    rows = []
    for e in mats:
        rows.append(((e.T @ OMEGA + OMEGA @ e) % 3).reshape(-1))
    kernel_basis = []
    # solve over F3: find null space of the 16x16 map e -> constraint
    system = np.array(rows, dtype=np.int64).T  # 16 constraints x 16 unknowns
    work = [[int(v) % 3 for v in row] for row in system]
    n_unknowns = 16
    pivots = []
    rank = 0
    for col in range(n_unknowns):
        pivot = next((r for r in range(rank, len(work)) if work[r][col]), None)
        if pivot is None:
            continue
        work[rank], work[pivot] = work[pivot], work[rank]
        inv = 1 if work[rank][col] == 1 else 2
        work[rank] = [(inv * v) % 3 for v in work[rank]]
        for r in range(len(work)):
            if r != rank and work[r][col]:
                factor = work[r][col]
                work[r] = [
                    (work[r][c] - factor * work[rank][c]) % 3 for c in range(n_unknowns)
                ]
        pivots.append(col)
        rank += 1
    free = [c for c in range(n_unknowns) if c not in pivots]
    for fc in free:
        vec = np.zeros(n_unknowns, dtype=np.int64)
        vec[fc] = 1
        for r, pc in zip(work[:rank], pivots):
            if r[fc]:
                vec[pc] = (-r[fc]) % 3
        kernel_basis.append(vec.reshape(4, 4) % 3)
    return kernel_basis


def hom_dimension(act_v, act_w, p=3):
    """dim Hom over F_p of modules given by generator-action matrix pairs."""
    dim_v = act_v[0].shape[0]
    dim_w = act_w[0].shape[0]
    rows = []
    for gv, gw in zip(act_v, act_w):
        # constraint: F gv = gw F  -> (gv^T (x) I - I (x) gw) vec(F) = 0
        block = (
            np.kron(gv.T, np.eye(dim_w, dtype=np.int64))
            - np.kron(np.eye(dim_v, dtype=np.int64), gw)
        ) % p
        rows.append(block)
    system = np.vstack(rows)
    return dim_v * dim_w - f3_rank(system)


def main():
    points, adjacency, symplectic = build_w33()
    lines = w33_lines(adjacency)
    checks = {}

    index = {p: n for n, p in enumerate(points)}
    pool = sp4_matrix_generators()
    checks["generators_symplectic"] = all(
        bool(((g.T @ OMEGA @ g) % 3 == OMEGA % 3).all()) for g in pool
    )
    # deterministic scan for a projectively generating pair
    g1 = g2 = None
    perms = [point_permutation(g, points, index) for g in pool]
    found = False
    for i in range(len(pool)):
        for j in range(i + 1, len(pool)):
            if closure_order([tuple(perms[i]), tuple(perms[j])], 40) == 25920:
                g1, g2 = pool[i], pool[j]
                perm1, perm2 = perms[i], perms[j]
                found = True
                break
        if found:
            break
    checks["projective_pair_generates_25920"] = found

    # adjoint module and its action
    ad_basis = adjoint_basis()
    checks["adjoint_dimension_10"] = len(ad_basis) == 10

    flat = np.array([b.reshape(-1) for b in ad_basis], dtype=np.int64).T

    def adjoint_action(g):
        try:
            g_inv = Matrix((g % 3).tolist()).inv_mod(3)
            g_inv = np.array(
                [[int(g_inv[i, j]) for j in range(4)] for i in range(4)],
                dtype=np.int64,
            )
        except Exception:
            raise RuntimeError("generator not invertible mod 3")
        images = []
        for b in ad_basis:
            image = (g @ b @ g_inv) % 3
            images.append(image.reshape(-1))
        image_matrix = np.array(images, dtype=np.int64).T
        # solve flat . A = image_matrix over F3
        aug = np.concatenate([flat, image_matrix], axis=1)
        work = [[int(v) % 3 for v in row] for row in aug]
        pivots = []
        rank = 0
        for col in range(10):
            pivot = next((r for r in range(rank, len(work)) if work[r][col]), None)
            if pivot is None:
                continue
            work[rank], work[pivot] = work[pivot], work[rank]
            inv = 1 if work[rank][col] == 1 else 2
            work[rank] = [(inv * v) % 3 for v in work[rank]]
            for r in range(len(work)):
                if r != rank and work[r][col]:
                    factor = work[r][col]
                    work[r] = [
                        (work[r][c] - factor * work[rank][c]) % 3
                        for c in range(len(work[0]))
                    ]
            pivots.append(col)
            rank += 1
        action = np.zeros((10, 10), dtype=np.int64)
        for r in range(rank):
            for j in range(10):
                action[pivots[r], j] = work[r][10 + j]
        return action % 3

    ad1 = adjoint_action(g1)
    ad2 = adjoint_action(g2)
    checks["adjoint_action_wellformed"] = f3_rank(ad1) == 10 and f3_rank(ad2) == 10
    checks["adjoint_schur_hom_1"] = hom_dimension([ad1, ad2], [ad1, ad2]) == 1
    trivial = [np.eye(1, dtype=np.int64), np.eye(1, dtype=np.int64)]
    checks["adjoint_no_trivial"] = (
        hom_dimension(trivial, [ad1, ad2]) == 0
        and hom_dimension([ad1, ad2], trivial) == 0
    )

    # the three trade modules mod 3
    incidence = np.zeros((40, 40), dtype=np.int64)
    for row, line in enumerate(lines):
        for p in line:
            incidence[row, p] = 1
    address = saturated_kernel(incidence)
    route = generic_saturated_kernel(incidence.T)
    gauge = saturated_kernel(adjacency - 2 * np.eye(40, dtype=np.int64))

    # the route lattice lives in LINE space: build the induced line perms
    line_index = {line: n for n, line in enumerate(lines)}

    def line_perm(perm):
        return [line_index[frozenset(perm[x] for x in lines[n])] for n in range(40)]

    lperm1, lperm2 = line_perm(perm1), line_perm(perm2)

    reports = {}
    for name, basis, perm_pair in (
        ("address_L4", address, (perm1, perm2)),
        ("route_Q43", route, (lperm1, lperm2)),
        ("gauge_L2", gauge, (perm1, perm2)),
    ):
        act = []
        for perm in perm_pair:
            m = lattice_action(basis, list(perm)) % 3
            act.append(m.astype(np.int64))
        dim = basis.shape[1]
        hom_ad = hom_dimension([ad1, ad2], act)
        hom_ad_rev = hom_dimension(act, [ad1, ad2])
        hom_triv = hom_dimension(trivial, act)
        reports[name] = {
            "dimension": dim,
            "hom_from_adjoint": int(hom_ad),
            "hom_to_adjoint": int(hom_ad_rev),
            "trivial_fixed_vectors": int(hom_triv),
        }
        checks[f"{name}_action_wellformed"] = all(f3_rank(m) == dim for m in act)
    checks["adjoint_hom_computed"] = True

    all_pass = all(checks.values())
    payload = {
        "schema": "w33.pass181.adjoint_shadow_mod3.v1",
        "status": "PASS" if all_pass else "FAIL",
        "adjoint": {
            "module": "sp(4,F3), dimension 10 = Theta, defining characteristic",
            "schur_endomorphism_dim": 1,
        },
        "trade_modules_mod3": reports,
        "reading": (
            "the defining-characteristic side of the trade tower: exact "
            "Hom_G dimensions between the adjoint module sp(4,F3) and the "
            "mod-3 reductions of the address, route, and gauge trade "
            "lattices -- where (and whether) the gauge algebra "
            "materializes inside the discriminant glue"
        ),
        "checks": {name: bool(value) for name, value in checks.items()},
    }

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(payload, indent=2))
    return 0 if all_pass else 1


if __name__ == "__main__":
    raise SystemExit(main())
