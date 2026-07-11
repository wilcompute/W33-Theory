#!/usr/bin/env python3
"""Pass 184: the mod-3 factor table of the three trade modules.

Pass 181 located the adjoint sp(4,F3) inside the mod-3 address and gauge
trade modules and proved its absence from the route module.  With the
3-modular Brauer degrees of U4(2) being [1, 5, 10, 14, 25, 81], the
composition tables are forced up to order; this witness computes them
exactly:

1. ADDRESS L4/3L4 (dim 15):  adjoint 10 at the bottom, quotient of
   dimension 5 -- tested for irreducibility (exhaustive 3^5 cyclic scan)
   and splitness (Hom(Q, M)).  Conjecture: uniserial 10 | 5, the mod-3
   home of the hidden five.

2. GAUGE L2/3L2 (dim 24):  adjoint at the bottom, quotient of dimension
   14 -- End_G(Q) has dimension 1.  Thus Q is a brick; this condition
   alone does not prove that Q is simple.

3. ROUTE (dim 15):  no adjoint map and no fixed vectors, while its
   coinvariants are one-dimensional.  Hence it has an exact nonsplit
   sequence 0 -> K_14 -> route -> 1 -> 0.  The witness does not infer
   simplicity of K_14 from dimensions alone.

4. THE DEC3 LEDGER (GAP): decomposition rows of the ordinaries onto the
   six 3-modular simples, locating which characteristic-0 objects reduce
   onto each factor.
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
    build_w33,
    saturated_kernel,
    w33_lines,
)
from analysis.w33_pass160_trade_tower_gq42 import generic_saturated_kernel
from analysis.w33_pass170_modular_shadow_brauer import run_gap
from analysis.w33_pass181_adjoint_shadow_mod3 import (
    OMEGA,
    adjoint_basis,
    closure_order,
    f3_rank,
    hom_dimension,
    lattice_action,
    point_permutation,
    sp4_matrix_generators,
)

OUT = ROOT / "data" / "w33_pass184_mod3_trade_factors.json"


def f3_solve_kernel(system, unknowns):
    """Basis of the F3 null space of `system` (rows are constraints)."""
    work = [[int(v) % 3 for v in row] for row in system]
    pivots = []
    rank = 0
    for col in range(unknowns):
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
                    (work[r][c] - factor * work[rank][c]) % 3 for c in range(unknowns)
                ]
        pivots.append(col)
        rank += 1
    free = [c for c in range(unknowns) if c not in pivots]
    kernel = []
    for fc in free:
        vec = np.zeros(unknowns, dtype=np.int64)
        vec[fc] = 1
        for r, pc in zip(work[:rank], pivots):
            if r[fc]:
                vec[pc] = (-r[fc]) % 3
        kernel.append(vec % 3)
    return kernel


def equivariant_map(act_v, act_w):
    """One nonzero G-map V -> W (columns of F span the image), or None."""
    dim_v = act_v[0].shape[0]
    dim_w = act_w[0].shape[0]
    rows = []
    for gv, gw in zip(act_v, act_w):
        block = (
            np.kron(gv.T, np.eye(dim_w, dtype=np.int64))
            - np.kron(np.eye(dim_v, dtype=np.int64), gw)
        ) % 3
        rows.append(block)
    kernel = f3_solve_kernel(np.vstack(rows), dim_v * dim_w)
    if not kernel:
        return None
    return kernel[0].reshape(dim_v, dim_w).T % 3  # F: V -> W as dim_w x dim_v


def f3_inverse(matrix):
    n = matrix.shape[0]
    aug = np.concatenate([matrix % 3, np.eye(n, dtype=np.int64)], axis=1).tolist()
    work = [[int(v) % 3 for v in row] for row in aug]
    for col in range(n):
        pivot = next((r for r in range(col, n) if work[r][col]), None)
        if pivot is None:
            raise ValueError("singular")
        work[col], work[pivot] = work[pivot], work[col]
        inv = 1 if work[col][col] == 1 else 2
        work[col] = [(inv * v) % 3 for v in work[col]]
        for r in range(n):
            if r != col and work[r][col]:
                factor = work[r][col]
                work[r] = [
                    (work[r][c] - factor * work[col][c]) % 3 for c in range(2 * n)
                ]
    return np.array([row[n:] for row in work], dtype=np.int64)


def quotient_action(act, submodule_basis):
    """Quotient action matrices M/span(submodule columns)."""
    dim = act[0].shape[0]
    sub = submodule_basis % 3  # dim x k
    k = f3_rank(sub.T)
    # extend to a full basis
    columns = [sub[:, i] for i in range(sub.shape[1])]
    reduced = []
    for c in columns:
        candidate = reduced + [c]
        if f3_rank(np.array(candidate)) == len(candidate):
            reduced.append(c)
    for i in range(dim):
        e = np.zeros(dim, dtype=np.int64)
        e[i] = 1
        candidate = reduced + [e]
        if f3_rank(np.array(candidate)) == len(candidate):
            reduced.append(e)
        if len(reduced) == dim:
            break
    P = np.array(reduced, dtype=np.int64).T % 3
    P_inv = f3_inverse(P)
    out = []
    for g in act:
        conj = (P_inv @ g @ P) % 3
        out.append(conj[k:, k:] % 3)
    return out, k


def cyclic_irreducible(act, dim):
    """Exhaustive cyclic-generation over F3 (feasible for dim <= 6)."""
    total = 3**dim
    for m in range(1, total):
        digits = []
        value = m
        for _ in range(dim):
            digits.append(value % 3)
            value //= 3
        start = np.array(digits, dtype=np.int64)
        span = []
        stack = [start % 3]
        seen = set()
        while stack:
            current = stack.pop() % 3
            key = tuple(int(v) for v in current)
            if key in seen:
                continue
            seen.add(key)
            candidate = span + [current]
            if f3_rank(np.array(candidate)) == len(candidate):
                span.append(current)
                if len(span) == dim:
                    break
            for g in act:
                stack.append((g @ current) % 3)
        if len(span) != dim:
            return False
    return True


def main():
    points, adjacency, symplectic = build_w33()
    lines = w33_lines(adjacency)
    checks = {}

    index = {p: n for n, p in enumerate(points)}
    pool = sp4_matrix_generators()
    perms = [point_permutation(g, points, index) for g in pool]
    g1 = g2 = None
    for i in range(len(pool)):
        for jx in range(i + 1, len(pool)):
            if closure_order([tuple(perms[i]), tuple(perms[jx])], 40) == 25920:
                g1, g2 = pool[i], pool[jx]
                perm1, perm2 = perms[i], perms[jx]
                break
        if g1 is not None:
            break
    checks["generating_pair_found"] = g1 is not None

    ad_basis = adjoint_basis()
    flat = np.array([b.reshape(-1) for b in ad_basis], dtype=np.int64).T

    from sympy import Matrix as SymMatrix

    def adjoint_action(g):
        g_inv = SymMatrix((g % 3).tolist()).inv_mod(3)
        g_inv = np.array(
            [[int(g_inv[i, j]) for j in range(4)] for i in range(4)],
            dtype=np.int64,
        )
        images = []
        for b in ad_basis:
            images.append(((g @ b @ g_inv) % 3).reshape(-1))
        image_matrix = np.array(images, dtype=np.int64).T
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
            for jj in range(10):
                action[pivots[r], jj] = work[r][10 + jj]
        return action % 3

    ad_act = [adjoint_action(g1), adjoint_action(g2)]

    incidence = np.zeros((40, 40), dtype=np.int64)
    for row, line in enumerate(lines):
        for p in line:
            incidence[row, p] = 1
    address = saturated_kernel(incidence)
    route = generic_saturated_kernel(incidence.T)
    gauge = saturated_kernel(adjacency - 2 * np.eye(40, dtype=np.int64))

    line_index = {line: n for n, line in enumerate(lines)}

    def line_perm(perm):
        return [line_index[frozenset(perm[x] for x in lines[n])] for n in range(40)]

    module_specs = {
        "address_L4": (address, (perm1, perm2)),
        "gauge_L2": (gauge, (perm1, perm2)),
        "route_Q43": (route, (line_perm(perm1), line_perm(perm2))),
    }

    trivial = [np.eye(1, dtype=np.int64)] * 2
    reports = {}
    for name, (basis, perm_pair) in module_specs.items():
        act = [lattice_action(basis, list(p)) % 3 for p in perm_pair]
        dim = basis.shape[1]
        entry = {"dimension": dim}
        F = equivariant_map(ad_act, act)
        if F is not None:
            image_rank = f3_rank(F.T)
            entry["adjoint_image_rank"] = int(image_rank)
            quotient, k = quotient_action(act, F % 3)
            entry["quotient_dimension"] = dim - k
            end_q = hom_dimension(quotient, quotient)
            entry["quotient_end_dim"] = int(end_q)
            hom_q_m = hom_dimension(quotient, act)
            entry["hom_quotient_into_module"] = int(hom_q_m)
            entry["extension_split"] = bool(hom_q_m > 0)
            if dim - k <= 6:
                entry["quotient_irreducible_exhaustive"] = bool(
                    cyclic_irreducible(quotient, dim - k)
                )
        else:
            entry["adjoint_image_rank"] = 0
            # route: test the 14|1 structure via coinvariants
            hom_to_trivial = hom_dimension(act, trivial)
            hom_from_trivial = hom_dimension(trivial, act)
            entry["hom_to_trivial"] = int(hom_to_trivial)
            entry["hom_from_trivial"] = int(hom_from_trivial)
            end_m = hom_dimension(act, act)
            entry["end_dim"] = int(end_m)
        reports[name] = entry

    checks["address_adjoint_bottom_quotient_5"] = (
        reports["address_L4"].get("adjoint_image_rank") == 10
        and reports["address_L4"].get("quotient_dimension") == 5
    )
    checks["address_quotient_irreducible"] = bool(
        reports["address_L4"].get("quotient_irreducible_exhaustive", False)
    )
    checks["address_nonsplit"] = reports["address_L4"].get("extension_split") is False
    checks["gauge_adjoint_bottom_quotient_14"] = (
        reports["gauge_L2"].get("adjoint_image_rank") == 10
        and reports["gauge_L2"].get("quotient_dimension") == 14
    )
    checks["gauge_quotient_is_14d_brick"] = (
        reports["gauge_L2"].get("quotient_end_dim") == 1
    )
    checks["gauge_extension_nonsplit"] = (
        reports["gauge_L2"].get("extension_split") is False
    )
    checks["route_exact_nonsplit_14_to_15_to_1"] = (
        reports["route_Q43"].get("hom_to_trivial") == 1
        and reports["route_Q43"].get("hom_from_trivial") == 0
    )

    # dec3 ledger from GAP
    data = run_gap()
    mod3 = data["mod3"]
    dec3 = data["dec3"]
    ordinary = data["ordinary"]
    checks["mod3_degrees"] = sorted(mod3) == [1, 5, 10, 14, 25, 81]
    checks["dec3_complete_dimension_identities"] = (
        len(dec3) == len(ordinary) == 20
        and all(len(row) == len(mod3) for row in dec3)
        and all(
            all(isinstance(value, int) and value >= 0 for value in row)
            and sum(value * degree for value, degree in zip(row, mod3))
            == ordinary_degree
            for ordinary_degree, row in zip(ordinary, dec3)
        )
    )
    ledger = {}
    for want in (5, 10, 15, 24, 30, 81):
        rows = [
            {"ordinary": ordinary[i], "row": dec3[i]}
            for i, d in enumerate(ordinary)
            if d == want
        ]
        ledger[str(want)] = rows
    expected_row_counts = {"5": 2, "10": 2, "15": 2, "24": 1, "30": 3, "81": 1}
    checks["dec3_selected_rows_complete"] = {
        degree: len(rows) for degree, rows in ledger.items()
    } == expected_row_counts

    all_pass = all(checks.values())
    payload = {
        "schema": "w33.pass184.mod3_trade_factors.v2",
        "status": "PASS" if all_pass else "FAIL",
        "brauer_degrees_mod3": mod3,
        "factor_table": reports,
        "reading": (
            "the defining-characteristic factor table of the trade tower: "
            "address is a nonsplit extension of an exhaustively simple "
            "five-dimensional quotient by the injected adjoint 10. Gauge "
            "is a nonsplit extension with a 14-dimensional brick quotient; "
            "brick does not imply simple. Route has no adjoint map and fits "
            "0 -> K_14 -> route -> 1 -> 0 nonsplit, without a simplicity "
            "claim for K_14"
        ),
        "boundary": (
            "End_G(Q)=F3 proves that Q is a brick, not that it is irreducible; "
            "composition-factor names require a separate submodule census"
        ),
        "dec3_ledger": ledger,
        "checks": {name: bool(value) for name, value in checks.items()},
    }

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(payload, indent=2))
    return 0 if all_pass else 1


if __name__ == "__main__":
    raise SystemExit(main())
