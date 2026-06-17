#!/usr/bin/env python3
"""BT1221 -- exact Sp(4,3) generator.

Generates Sp(4,3) from symplectic transvections over F3.  This is the exact
two-qutrit finite Clifford target that BT1214/BT1216 previously treated as a
static signature.

The standard symplectic form is J = [[0,I],[-I,0]] in the basis e1,e2,f1,f2.
For a nonzero vector v, the transvection is T_v = I + v (Jv)^T over F3.
The set of all nonzero-vector transvections generates Sp(4,3).
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
from collections import Counter, deque

MOD = 3
N = 4
Matrix = tuple[tuple[int, ...], ...]
J: Matrix = ((0, 0, 1, 0), (0, 0, 0, 1), (2, 0, 0, 0), (0, 2, 0, 0))


def eye(n: int = N) -> Matrix:
    return tuple(tuple(1 if i == j else 0 for j in range(n)) for i in range(n))


def matmul(a: Matrix, b: Matrix) -> Matrix:
    return tuple(
        tuple(sum(a[i][k] * b[k][j] for k in range(len(b))) % MOD for j in range(len(b[0])))
        for i in range(len(a))
    )


def transpose(a: Matrix) -> Matrix:
    return tuple(tuple(a[j][i] for j in range(len(a))) for i in range(len(a[0])))


def matadd(a: Matrix, b: Matrix) -> Matrix:
    return tuple(tuple((a[i][j] + b[i][j]) % MOD for j in range(N)) for i in range(N))


def matsub(a: Matrix, b: Matrix) -> Matrix:
    return tuple(tuple((a[i][j] - b[i][j]) % MOD for j in range(N)) for i in range(N))


def vec_col(v: tuple[int, ...]) -> tuple[tuple[int], ...]:
    return tuple((x % MOD,) for x in v)


def row_from_col(c: tuple[tuple[int], ...]) -> tuple[int, ...]:
    return tuple(x[0] for x in c)


def outer(u: tuple[int, ...], w: tuple[int, ...]) -> Matrix:
    return tuple(tuple((u[i] * w[j]) % MOD for j in range(N)) for i in range(N))


def transvection(v: tuple[int, ...]) -> Matrix:
    jv = row_from_col(matmul(J, vec_col(v)))
    return matadd(eye(), outer(v, jv))


def is_symplectic(m: Matrix) -> bool:
    return matmul(matmul(transpose(m), J), m) == J


def nonzero_vectors() -> list[tuple[int, ...]]:
    out = []
    for a in range(MOD):
        for b in range(MOD):
            for c in range(MOD):
                for d in range(MOD):
                    v = (a, b, c, d)
                    if any(v):
                        out.append(v)
    return out


def generate_group() -> set[Matrix]:
    generators = sorted(set(transvection(v) for v in nonzero_vectors()))
    assert all(is_symplectic(g) for g in generators)
    group = {eye()}
    q: deque[Matrix] = deque([eye()])
    while q:
        x = q.popleft()
        for g in generators:
            y = matmul(x, g)
            if y not in group:
                group.add(y)
                q.append(y)
    return group


def matrix_order(m: Matrix) -> int:
    x = eye()
    for k in range(1, 200):
        x = matmul(x, m)
        if x == eye():
            return k
    raise RuntimeError("matrix order search exceeded bound")


def rank_mod3(m: Matrix) -> int:
    a = [list(row) for row in m]
    r = 0
    for c in range(N):
        pivot = next((i for i in range(r, N) if a[i][c] % MOD), None)
        if pivot is None:
            continue
        a[r], a[pivot] = a[pivot], a[r]
        inv = 1 if a[r][c] == 1 else 2
        a[r] = [(x * inv) % MOD for x in a[r]]
        for i in range(N):
            if i != r and a[i][c] % MOD:
                f = a[i][c] % MOD
                a[i] = [(a[i][j] - f * a[r][j]) % MOD for j in range(N)]
        r += 1
    return r


def build_result() -> dict:
    group = generate_group()
    orders = Counter(matrix_order(m) for m in group)
    traces = Counter(sum(m[i][i] for i in range(N)) % MOD for m in group)
    ranks = Counter(rank_mod3(matsub(m, eye())) for m in group)
    return {
        "bt": 1221,
        "title": "Exact Sp(4,3) symplectic-generator certificate",
        "field": "F3",
        "dimension": 4,
        "symplectic_form": "J=[[0,I],[-I,0]]",
        "generator_type": "all nonzero-vector symplectic transvections T_v=I+v(Jv)^T",
        "unique_transvection_generators": len(set(transvection(v) for v in nonzero_vectors())),
        "order": len(group),
        "expected_order": 51840,
        "order_ok": len(group) == 51840,
        "all_generated_matrices_symplectic": all(is_symplectic(m) for m in group),
        "element_order_spectrum": {str(k): orders[k] for k in sorted(orders)},
        "trace_mod3_counts": {str(k): traces[k] for k in sorted(traces)},
        "rank_M_minus_I_counts": {str(k): ranks[k] for k in sorted(ranks)},
        "max_element_order": max(orders),
        "recovers_bt1214_two_qutrit_target": len(group) == 51840,
    }


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--out", type=Path, default=Path("data/bt1221_exact_sp43_generator.json"))
    args = p.parse_args()
    result = build_result()
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps({"bt": 1221, "order": result["order"], "order_ok": result["order_ok"], "out": str(args.out)}, indent=2))


if __name__ == "__main__":
    main()
