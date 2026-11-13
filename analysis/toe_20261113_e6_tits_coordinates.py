"""Construct the Tits extension in the repository's signed 27 coordinates."""

import json
from collections import deque
from itertools import combinations
from pathlib import Path

import networkx as nx
import numpy as np


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data/toe_20261113_e6_tits_coordinates.json"


def orbit(start, generators, action):
    seen = {start}
    pending = deque([start])
    while pending:
        item = pending.popleft()
        for generator in generators:
            image = action(generator, item)
            if image not in seen:
                seen.add(image)
                pending.append(image)
    return seen


def quotient_lifts(permutations, sign_masks):
    identity = tuple(range(27))
    lifts = {identity: 0}
    pending = deque([identity])
    while pending:
        p = pending.popleft()
        for generator, signs in zip(permutations, sign_masks):
            q = tuple(generator[i] for i in p)
            if q not in lifts:
                lifts[q] = lifts[p] ^ sum(((signs >> i) & 1) << j for j, i in enumerate(p))
                pending.append(q)
    return lifts


def calculate():
    export = np.load(ROOT / "artifacts/e6_27rep_basis_export/E6_basis_78.npy")
    assert not export.imag.any()
    basis = export.real.astype(np.int64)
    assert np.array_equal(basis, export.real)
    diagonal = [a.diagonal() for a in basis if not np.any(a-np.diag(a.diagonal()))]
    assert len(diagonal) == 6
    roots = {}
    for e in basis:
        if not np.any(e-np.diag(e.diagonal())):
            continue
        h = e @ e.T-e.T @ e
        assert np.array_equal(h, np.diag(h.diagonal())) and not np.any(e @ e)
        assert np.array_equal(h @ e-e @ h, 2*e)
        roots[tuple(h.diagonal())] = e
    assert len(roots) == 72
    chamber = np.arange(1, 28, dtype=np.int64)**4
    positive = {h for h in roots if chamber @ h > 0}
    assert len(positive) == 36
    decomposable = {tuple(a+b for a, b in zip(h, k)) for h in positive for k in positive}
    simple = sorted(positive-decomposable)
    assert len(simple) == 6

    identity = np.eye(27, dtype=np.int64)
    signs = json.loads((ROOT/"artifacts/canonical_su3_gauge_and_cubic.json").read_text(encoding="utf-8"))
    cubic = {tuple(sorted(row["triple"])): 1 if row["sign"] % 3 == 1 else -1
             for row in signs["solution"]["d_triples"]}
    lifts, permutations, squares, sign_masks = [], [], [], []
    for h in simple:
        e = roots[h]
        n = (identity+e) @ (identity-e.T) @ (identity+e)
        np.testing.assert_array_equal(n.T @ n, identity)
        square = np.diag(np.where(np.array(h)%2, -1, 1))
        np.testing.assert_array_equal(n @ n, square)
        perm = np.argmax(abs(n), axis=0)
        s = n[perm, np.arange(27)]
        assert all(cubic[tuple(sorted(perm[list(t)]))]*int(np.prod(s[list(t)])) == value
                   for t, value in cubic.items())
        sign_masks.append(sum(int(x < 0) << i for i, x in enumerate(s)))
        lifts.append(n)
        permutations.append(tuple(map(int, perm)))
        squares.append((square.diagonal() < 0).astype(int))
    gram = np.array(simple) @ np.array(simple).T
    assert not np.any(gram % 6)
    cartan = gram // 6
    assert np.all(cartan.diagonal() == 2) and round(np.linalg.det(cartan)) == 3
    for i, j in combinations(range(6), 2):
        a, b = lifts[i], lifts[j]
        if cartan[i,j] == -1:
            np.testing.assert_array_equal(a @ b @ a, b @ a @ b)
        else:
            assert cartan[i,j] == 0
            np.testing.assert_array_equal(a @ b, b @ a)
        # Torus conjugation is the signed-lift version of the simple reflection.
        reflected = np.array(simple[j])-cartan[i,j]*np.array(simple[i])
        np.testing.assert_array_equal(a @ np.diag((-1)**squares[j]) @ a.T,
                                      np.diag(np.where(reflected%2, -1, 1)))
    kernel = {tuple(bits @ np.array(squares)%2) for bits in np.ndindex(*(2,)*6)}
    assert len(kernel) == 64
    assert all(sum(v[i] for i in t)%2 == 0 for v in kernel for t in cubic)
    group = quotient_lifts(permutations, sign_masks)
    assert len(group) == 51840
    graph = nx.Graph()
    graph.add_nodes_from(range(27))
    graph.add_edges_from(pair for t in cubic for pair in combinations(t, 2))
    sections = {}
    for size, expected in ((5,216), (6,72)):
        section = min(tuple(sorted(c)) for c in nx.find_cliques(nx.complement(graph)) if len(c)==size)
        images = orbit(section, permutations, lambda p, c: tuple(sorted(p[i] for i in c)))
        assert len(images) == expected
        stabilizer = [p for p in group if tuple(sorted(p[i] for i in section)) == section]
        restrictions = {tuple(section.index(p[i]) for i in section) for p in stabilizer}
        assert len(restrictions) == (120 if size == 5 else 720)
        restricted_kernel = sum(all(v[i] == 0 for i in section) for v in kernel)
        diagonal_restrictions = {tuple(int(v[i]) for i in section) for v in kernel}
        signed_image = {
            (tuple(section.index(p[i]) for i in section),
             tuple(((group[p] >> i) & 1) ^ k for i, k in zip(section, sign)))
            for p in stabilizer for sign in diagonal_restrictions
        }
        assert len(signed_image) == (1920 if size == 5 else 46080)
        determinant_exponents = {
            (sum(sign) + sum(p[i] > p[j] for i, j in combinations(range(size), 2))) % 2
            for p, sign in signed_image
        }
        assert determinant_exponents == ({0} if size == 5 else {0, 1})
        section_mask = sum(1 << i for i in section)
        masks = [sum(int(bit) << i for i, bit in enumerate(v)) for v in kernel]
        fixing = [
            (p, group[p] ^ mask)
            for p in stabilizer if all(p[i] == i for i in section)
            for mask in masks if (group[p] ^ mask) & section_mask == 0
        ]
        order_four = sum(
            mask != sum(((mask >> p[i]) & 1) << i for i in range(27))
            for p, mask in fixing
        )
        assert all(p[p[i]] == i for p, _ in fixing for i in range(27))
        assert len(fixing)*len(signed_image) == 64*len(stabilizer)
        sections[size] = dict(
            representative=section, orbit=len(images), unsigned_stabilizer=len(stabilizer),
            unsigned_image_order=len(restrictions), signed_image_order=len(signed_image),
            signed_image_determinants=sorted((-1)**d for d in determinant_exponents),
            signed_pointwise_kernel=len(fixing), pointwise_kernel_order_four=order_four,
            diagonal_kernel_fixing_section_pointwise=restricted_kernel,
            signed_stabilizer_order=64*len(stabilizer),
        )
    return dict(status="PASS", cartan=cartan.tolist(), signed_generators=[n.tolist() for n in lifts],
                torus_order=len(kernel), quotient_order=len(group), group_order=64*len(group),
                sections=sections)


if __name__ == "__main__":
    result = calculate()
    OUT.write_text(json.dumps(result, indent=2)+"\n", encoding="utf-8")
    print(result["cartan"], result["group_order"], result["sections"], flush=True)
