"""Exact compact obstruction and split-E6 shear for a unique six-section."""

import json
from collections import Counter
from pathlib import Path

import networkx as nx
import numpy as np

from toe_20261114_e6_packet_section_pairing import roots

OUT = Path(__file__).resolve().parents[1] / "data/toe_20261114_e6_split_six_section.json"


def calculate():
    _, cubic, _, _, generators = roots.load()
    _, compact = roots.pack_roots(generators)
    n = 27
    identity = np.eye(n, dtype=np.int64)
    support = nx.Graph()
    support.add_nodes_from(range(n))
    tensor = np.zeros((n, n, n), dtype=np.int64)
    from itertools import combinations, permutations
    for t, coefficient in cubic.items():
        support.add_edges_from(combinations(t, 2))
        for indices in permutations(t):
            tensor[indices] = coefficient
    sections = [tuple(sorted(s)) for s in nx.find_cliques(nx.complement(support))]
    assert Counter(map(len, sections)) == {5: 216, 6: 72}

    spectra, dimensions = {}, {}
    for size in (5, 6):
        spectra[size] = Counter()
        dimensions[size] = Counter()
    for section in sections:
        contraction = tensor[list(section)]
        sq = np.einsum("aik,ajk->ij", contraction, contraction)
        assert np.array_equal(sq, np.diag(np.diag(sq)))
        spectra[len(section)][tuple(sorted(Counter(map(int, np.diag(sq))).items()))] += 1
        outside = sorted(set(range(n)) - set(section))
        # Distinct matching supports prohibit cancellation on the off-block.
        rows = np.stack([k[np.ix_(outside, section)].ravel() for k in compact])
        assert np.max(np.count_nonzero(rows, axis=0)) <= 1
        dimensions[len(section)][sum(not np.any(row) for row in rows)] += 1
    assert spectra == {5: {((0, 5), (1, 10), (3, 10), (5, 2)): 216},
                       6: {((0, 6), (2, 15), (5, 6)): 72}}
    assert dimensions == {5: {11: 216}, 6: {15: 72}}

    a = (3, 4, 7, 8, 17, 24)
    b = (9, 10, 13, 14, 19, 26)
    for s, expected in ((a, b), (b, a)):
        sq = np.einsum("aik,ajk->ij", tensor[list(s)], tensor[list(s)])
        assert tuple(np.flatnonzero(np.diag(sq) == 5)) == expected

    shear = generators[2]
    assert not np.any(shear @ shear)
    roots.inf_check(shear, cubic)
    holonomy = identity + shear
    assert np.array_equal(holonomy @ (identity - shear), identity)
    # Verify the cubic under the finite shear, independently of exponentiation.
    transformed = np.einsum("abc,ai,bj,ck->ijk", tensor, holonomy, holonomy, holonomy,
                            optimize=True)
    assert np.array_equal(transformed, tensor)

    gates = [identity + k + k @ k for k in compact]
    markers = [gates[i] @ gates[i] for i in (0, 1, 2, 3, 4, 8)]
    assert all(np.array_equal(m, np.diag(np.diag(m))) and np.array_equal(m @ m, identity)
               for m in markers)
    assert len(set(zip(*(np.diag(m) for m in markers), strict=True))) == n

    def commutator(i, j):
        u, v = gates[i], gates[j]
        return u @ v @ u.T @ v.T

    def fixed(loops):
        return sorted(s for s in sections
                      if all(not np.any(loop[np.ix_(sorted(set(range(n)) - set(s)), s)])
                             for loop in loops))

    loops = [commutator(0, 1), commutator(14, 15), gates[4], *markers]
    assert fixed(loops) == [a, b]
    assert fixed([*loops, holonomy]) == [a]
    assert int(np.trace(holonomy)) == 27
    assert not np.array_equal(holonomy.T @ holonomy, identity)
    return dict(status="PASS", unique_maximal_section=a, broken_compact_partner=b,
                compact_stabilizer_dimensions={5: 11, 6: 15},
                contraction_spectra={5: {0: 5, 1: 10, 3: 10, 5: 2},
                                     6: {0: 6, 2: 15, 5: 6}},
                shear_entries=[(int(i), int(j), int(shear[i, j]))
                               for i, j in zip(*np.nonzero(shear), strict=True)],
                trace_shear=int(np.trace(holonomy)),
                squared_frobenius_identity_defect=int(np.sum((holonomy-identity)**2)))


if __name__ == "__main__":
    result = calculate()
    OUT.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(result, flush=True)
