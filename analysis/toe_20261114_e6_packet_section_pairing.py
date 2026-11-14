"""Verify the six-section pairing and an isolated five-section for packet words."""

from collections import Counter
from itertools import combinations
from pathlib import Path
import json

import networkx as nx
import numpy as np

from toe_20261114_e6_paired_wilson_sections import roots

OUT = Path(__file__).resolve().parents[1] / "data/toe_20261114_e6_packet_section_pairing.json"


def calculate():
    _, cubic, _, _, generators = roots.load()
    _, compact = roots.pack_roots(generators)
    identity = np.eye(27, dtype=np.int64)
    gates = [identity + k + k @ k for k in compact]

    graph = nx.Graph()
    graph.add_nodes_from(range(27))
    for triple in cubic:
        graph.add_edges_from(combinations(triple, 2))
    sections = sorted(tuple(sorted(s)) for s in nx.find_cliques(nx.complement(graph)))
    assert Counter(map(len, sections)) == {5: 216, 6: 72}
    six = [frozenset(s) for s in sections if len(s) == 6]
    neighbors = {v: set(graph[v]) for v in graph}
    partner = {}
    for source in six:
        scores = {target: sum(len(neighbors[v] & target) for v in source)
                  for target in six if not source & target}
        assert Counter(scores.values()) == {21: 20, 30: 1}
        partner[source], = (target for target, score in scores.items() if score == 30)
    assert all(partner[target] == source for source, target in partner.items())

    def permutation(g):
        assert np.array_equal(g.T @ g, identity)
        return tuple(map(int, np.argmax(abs(g), axis=0)))

    for gate in gates:
        p = permutation(gate)
        assert all(graph.has_edge(p[i], p[j]) for i, j in graph.edges)
        for source, target in partner.items():
            image = frozenset(p[i] for i in source)
            assert partner[image] == frozenset(p[i] for i in target)

    def commutator(i, j):
        a, b = gates[i], gates[j]
        return a @ b @ a.T @ b.T

    five_loops = [gates[0], commutator(11, 35), commutator(14, 26)]
    six_loops = [commutator(0, 1), commutator(14, 15), gates[4]]
    markers = [gates[i] @ gates[i] for i in (0, 1, 2, 3, 4, 8)]
    assert all(np.array_equal(m, np.diag(np.diag(m))) and np.array_equal(m @ m, identity)
               for m in markers)
    assert len(set(zip(*(np.diag(m) for m in markers), strict=True))) == 27

    def fixed(loops):
        perms = [permutation(loop) for loop in loops]
        return [s for s in sections if all(tuple(sorted(p[i] for i in s)) == s for p in perms)]

    isolated = fixed(five_loops)
    assert isolated == [(2, 3, 5, 9, 21)]
    paired = fixed(six_loops)
    assert len(paired) == 2 and partner[frozenset(paired[0])] == frozenset(paired[1])

    def action(loops):
        return sum(int(27 - np.trace(loop)) for loop in loops)

    return dict(status="PASS", six_sections=len(six), pairs=len(six)//2,
                six_pairs=sorted({tuple(sorted((tuple(sorted(a)), tuple(sorted(b)))))
                                  for a, b in partner.items()}),
                isolated_five=isolated[0], surviving_six_pair=paired,
                marker_ids=[0, 1, 2, 3, 4, 8],
                five_strip_action=action(five_loops + markers),
                six_strip_action=action(six_loops + markers))


if __name__ == "__main__":
    result = calculate()
    OUT.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print({k: v for k, v in result.items() if k != "six_pairs"}, flush=True)
