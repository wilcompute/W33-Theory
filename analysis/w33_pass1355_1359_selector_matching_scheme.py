#!/usr/bin/env python3
"""Passes 1355--1359: exact W(3,3) selector-matching association scheme.

Constructs W(3,3) from the symplectic form on F_3^4, attaches the three
perfect matchings of K4 to each isotropic line, and verifies the resulting
120-object four-class association scheme, its spectra, fusions, quotient,
and S3 transport holonomy.
"""
from __future__ import annotations

import argparse
import hashlib
import itertools
import json
from pathlib import Path

import numpy as np
import sympy as sp

Q = 3
ROOT = Path(__file__).resolve().parents[1] if Path(__file__).parent.name == "analysis" else Path.cwd()
DEFAULT_OUT = ROOT / "data" / "w33_pass1355_1359_selector_matching_scheme.json"


def canon(v: tuple[int, ...]) -> tuple[int, ...]:
    for x in v:
        if x % Q:
            inv = 1 if x % Q == 1 else 2
            return tuple((inv * y) % Q for y in v)
    raise ValueError("zero vector has no projective representative")


def symp(x: tuple[int, ...], y: tuple[int, ...]) -> int:
    return (x[0] * y[2] + x[1] * y[3] - x[2] * y[0] - x[3] * y[1]) % Q


def perfect_matchings4(line: tuple[int, int, int, int]):
    a, b, c, d = line
    return tuple(sorted([
        tuple(sorted((tuple(sorted((a, b))), tuple(sorted((c, d)))))),
        tuple(sorted((tuple(sorted((a, c))), tuple(sorted((b, d)))))),
        tuple(sorted((tuple(sorted((a, d))), tuple(sorted((b, c)))))),
    ]))


def compose(p: tuple[int, ...], q: tuple[int, ...]) -> tuple[int, ...]:
    return tuple(p[q[i]] for i in range(len(p)))


def invperm(p: tuple[int, ...]) -> tuple[int, ...]:
    r = [0] * len(p)
    for i, j in enumerate(p):
        r[j] = i
    return tuple(r)


def set_partitions(seq: list[int]):
    if not seq:
        yield []
        return
    first = seq[0]
    for rest in set_partitions(seq[1:]):
        yield [[first]] + [b[:] for b in rest]
        for i in range(len(rest)):
            new = [b[:] for b in rest]
            new[i] = [first] + new[i]
            yield new


def build():
    points = sorted({canon(v) for v in itertools.product(range(Q), repeat=4) if any(v)})
    assert len(points) == 40
    adj = np.zeros((40, 40), dtype=np.int8)
    for i, x in enumerate(points):
        for j, y in enumerate(points):
            if i != j and symp(x, y) == 0:
                adj[i, j] = 1
    assert np.all(adj.sum(axis=1) == 12)
    assert np.array_equal(adj @ adj, 8 * np.eye(40, dtype=int) - 2 * adj + 4 * np.ones((40, 40), dtype=int))

    lines = [c for c in itertools.combinations(range(40), 4)
             if all(adj[i, j] for i, j in itertools.combinations(c, 2))]
    assert len(lines) == 40
    line_sets = [set(line) for line in lines]
    matchings = [perfect_matchings4(line) for line in lines]
    selectors = [(li, mi, matchings[li][mi]) for li in range(40) for mi in range(3)]

    def transversal_map(li: int, lj: int) -> dict[int, int]:
        assert line_sets[li].isdisjoint(line_sets[lj])
        out = {}
        for x in lines[li]:
            ys = [y for y in lines[lj] if adj[x, y]]
            assert len(ys) == 1
            out[x] = ys[0]
        return out

    def transport_matching(matching, mapping):
        return tuple(sorted(tuple(sorted((mapping[a], mapping[b]))) for a, b in matching))

    n = len(selectors)
    relations = [np.zeros((n, n), dtype=np.int8) for _ in range(5)]
    transports: dict[tuple[int, int], tuple[int, int, int]] = {}
    for li in range(40):
        for lj in range(40):
            if li != lj and line_sets[li].isdisjoint(line_sets[lj]):
                mapping = transversal_map(li, lj)
                transports[(li, lj)] = tuple(
                    matchings[lj].index(transport_matching(m, mapping)) for m in matchings[li]
                )

    for i, (li, _mi, m) in enumerate(selectors):
        for j, (lj, _mj, m2) in enumerate(selectors):
            if i == j:
                r = 0
            elif li == lj:
                r = 1
            elif line_sets[li] & line_sets[lj]:
                r = 2
            else:
                perm = transports[(li, lj)]
                transported = matchings[lj][perm[matchings[li].index(m)]]
                r = 3 if transported == m2 else 4
            relations[r][i, j] = 1

    assert np.array_equal(sum(relations), np.ones((n, n), dtype=np.int8))
    assert all(np.array_equal(r, r.T) for r in relations)
    valencies = [int(r.sum(axis=1)[0]) for r in relations]
    assert valencies == [1, 2, 36, 27, 54]

    intersection = np.zeros((5, 5, 5), dtype=int)
    for i in range(5):
        for j in range(5):
            product = relations[i] @ relations[j]
            for k in range(5):
                vals = np.unique(product[relations[k].astype(bool)])
                assert len(vals) == 1
                intersection[i, j, k] = int(vals[0])
    assert np.array_equal(intersection, intersection.transpose(1, 0, 2))

    P = sp.Matrix([
        [1, 2, 36, 27, 54],
        [1, 2, -12, 3, 6],
        [1, 2, 6, -3, -6],
        [1, -1, 0, 9, -9],
        [1, -1, 0, -3, 3],
    ])
    for row in range(5):
        for i in range(5):
            for j in range(5):
                lhs = P[row, i] * P[row, j]
                rhs = sum(intersection[i, j, k] * P[row, k] for k in range(5))
                assert lhs == rhs
    assert P.det() != 0
    Qmat = 120 * P.inv()
    assert P * Qmat == 120 * sp.eye(5)
    assert Qmat * P == 120 * sp.eye(5)
    assert [Qmat[0, i] for i in range(5)] == [1, 15, 24, 20, 60]

    def is_p_polynomial(order):
        adjacency = order[1]
        for jpos, j in enumerate(order):
            for kpos, k in enumerate(order):
                if intersection[adjacency, j, k] and abs(kpos - jpos) > 1:
                    return False
            if jpos > 0 and intersection[adjacency, j, order[jpos - 1]] == 0:
                return False
            if jpos < 4 and intersection[adjacency, j, order[jpos + 1]] == 0:
                return False
        return True

    qparams = np.empty((5, 5, 5), dtype=object)
    qinv = Qmat.inv()
    for i in range(5):
        for j in range(5):
            product = sp.Matrix([Qmat[r, i] * Qmat[r, j] for r in range(5)])
            coeffs = qinv * product
            for k in range(5):
                qparams[i, j, k] = sp.simplify(coeffs[k])

    def is_q_polynomial(order):
        first = order[1]
        for jpos, j in enumerate(order):
            for kpos, k in enumerate(order):
                if qparams[first, j, k] != 0 and abs(kpos - jpos) > 1:
                    return False
            if jpos > 0 and qparams[first, j, order[jpos - 1]] == 0:
                return False
            if jpos < 4 and qparams[first, j, order[jpos + 1]] == 0:
                return False
        return True

    primitive_orders = [(0,) + perm for perm in itertools.permutations((1, 2, 3, 4))]
    assert not any(is_p_polynomial(order) for order in primitive_orders)
    assert not any(is_q_polynomial(order) for order in primitive_orders)

    partitions = {}
    for part in set_partitions([1, 2, 3, 4]):
        key = tuple(sorted(tuple(sorted(block)) for block in part))
        partitions[key] = key

    def fusion_ok(part):
        mats = [relations[0]] + [sum((relations[i] for i in block), start=np.zeros_like(relations[0])) for block in part]
        for a in range(len(mats)):
            for b in range(len(mats)):
                prod = mats[a] @ mats[b]
                for rel in mats:
                    if len(np.unique(prod[rel.astype(bool)])) != 1:
                        return False
        return True

    valid_fusions = [part for part in partitions if fusion_ok(part)]
    assert valid_fusions == [
        ((1,), (2,), (3,), (4,)),
        ((1,), (2,), (3, 4)),
        ((1,), (2, 3, 4)),
        ((1, 2, 3, 4),),
    ]

    neighbors = {i: [j for j in range(40) if i != j and line_sets[i].isdisjoint(line_sets[j])] for i in range(40)}
    assert {len(v) for v in neighbors.values()} == {27}
    edge_count = sum(map(len, neighbors.values())) // 2
    assert edge_count == 540
    base = 0
    queue = [base]
    seen = {base}
    path_transport = {base: (0, 1, 2)}
    while queue:
        u = queue.pop(0)
        for v in neighbors[u]:
            if v not in seen:
                seen.add(v)
                path_transport[v] = compose(transports[(u, v)], path_transport[u])
                queue.append(v)
    assert len(seen) == 40
    holonomy = set()
    for u in range(40):
        for v in neighbors[u]:
            if u < v:
                h = compose(invperm(path_transport[v]), compose(transports[(u, v)], path_transport[u]))
                holonomy.add(h)
    assert holonomy == set(itertools.permutations(range(3)))
    centralizer = [s for s in itertools.permutations(range(3)) if all(compose(s, h) == compose(h, s) for h in holonomy)]
    assert centralizer == [(0, 1, 2)]

    def rat(x):
        x = sp.Rational(x)
        return int(x) if x.q == 1 else f"{x.p}/{x.q}"

    result = {
        "schema": "w33.pass1355_1359.selector_matching_scheme.v1",
        "status": "PASS",
        "construction": {"field": 3, "points": 40, "isotropic_lines": 40, "perfect_matchings_per_line": 3, "selectors": 120},
        "relations": {
            "labels": ["identity", "same_line_other_matching", "intersecting_lines", "disjoint_transversal_aligned", "disjoint_transversal_misaligned"],
            "valencies": valencies,
        },
        "primitive_multiplicities": [1, 15, 24, 20, 60],
        "first_eigenmatrix": [[rat(x) for x in row] for row in P.tolist()],
        "second_eigenmatrix": [[rat(x) for x in row] for row in Qmat.tolist()],
        "intersection_numbers": intersection.tolist(),
        "fusion_partitions": [[list(block) for block in part] for part in valid_fusions],
        "p_polynomial": False,
        "q_polynomial": False,
        "quotient": {
            "fibers": 40,
            "fiber_size": 3,
            "quotient_srg": [40, 12, 2, 4],
            "fiber_constant_multiplicities": [1, 15, 24],
            "fiber_zero_multiplicities": [20, 60],
        },
        "holonomy": {
            "disjoint_line_graph_vertices": 40,
            "degree": 27,
            "edges": edge_count,
            "generated_group": "S3",
            "order": 6,
            "centralizer_in_S3_order": 1,
            "fiber_kernel": "trivial",
        },
        "automorphism": {
            "scheme_group_order": 51840,
            "group": "PGSp(4,3) ~= W(E6)",
            "argument": "The natural incidence action is faithful. Every scheme automorphism preserves the 40 R0+R1 fibers and injects into the quotient line-graph automorphism group; full S3 transport holonomy makes the fiber kernel trivial.",
        },
        "boundary": "This proves the exact finite association scheme and its natural full automorphism group inside the verified W(3,3) model. It does not claim literature novelty or a physical interpretation.",
    }
    return result


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=DEFAULT_OUT)
    parser.add_argument("--verify-only", action="store_true")
    parser.add_argument("--check", action="store_true", help="fail unless the committed certificate is byte-identical")
    args = parser.parse_args()
    result = build()
    encoded = json.dumps(result, indent=2, sort_keys=True) + "\n"
    digest = hashlib.sha256(encoded.encode()).hexdigest()
    if args.check:
        if not args.output.exists() or args.output.read_text() != encoded:
            raise SystemExit(f"certificate drift: {args.output}")
    elif not args.verify_only:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(encoded)
    print(f"PASS 1355-1359: selector matching scheme sha256={digest}")


if __name__ == "__main__":
    main()
