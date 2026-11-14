"""Exact common-section census for two compact root-packet Wilson loops."""

from collections import Counter
from itertools import combinations
from pathlib import Path
import json

import networkx as nx
import numpy as np

import toe_20261113_e6_root_matching_projection_clock as roots

OUT = Path(__file__).resolve().parents[1] / "data/toe_20261114_e6_paired_wilson_sections.json"


def calculate():
    _, cubic, _, _, generators = roots.load()
    _, compact = roots.pack_roots(generators)
    identity = np.eye(27, dtype=np.int64)
    gates = [identity + k + k @ k for k in compact]

    incidence = nx.Graph()
    incidence.add_nodes_from(range(27))
    for triple in cubic:
        incidence.add_edges_from(combinations(triple, 2))
    sections = tuple(sorted(tuple(sorted(s)) for s in nx.find_cliques(nx.complement(incidence))))
    assert Counter(map(len, sections)) == {5: 216, 6: 72}

    loops = []
    for i, j in combinations(range(len(gates)), 2):
        u, v = gates[i], gates[j]
        loop = u @ v @ u.T @ v.T
        if np.array_equal(loop, identity):
            continue
        permutation = np.argmax(abs(loop), axis=0)
        assert np.array_equal(loop.T @ loop, identity)
        fixed = tuple(sum(1 << k for k, s in enumerate(sections)
                          if len(s) == size and tuple(sorted(permutation[list(s)])) == s)
                      for size in (5, 6))
        assert all(fixed)
        loops.append(((i, j), loop, fixed))
    assert len(loops) == 360

    counts, shared = Counter(), Counter()
    witness = None
    for (i, a, a_fixed), (j, b, b_fixed) in combinations(loops, 2):
        five, six = (m & n for m, n in zip(a_fixed, b_fixed, strict=True))
        signature = f"{int(bool(five))}{int(bool(six))}"
        counts[signature] += 1
        if set(i) & set(j):
            shared[signature] += 1
        if signature == "01" and witness is None:
            witness = dict(links=[i, j], common_six=[s for k, s in enumerate(sections) if six & (1 << k)],
                           loop_actions=[int(27-np.trace(x)) for x in (a,b)],
                           trace_product=int(np.trace(a @ b)),
                           commute=bool(np.array_equal(a @ b, b @ a)))

    assert counts == {"11": 44100, "00": 19440, "01": 1080}
    assert shared == {"11": 6840}
    assert witness["links"] == [(0, 1), (14, 15)] and len(witness["common_six"]) == 6
    assert witness["loop_actions"] == [18, 18] and witness["commute"]

    # Intersections give the common fixed sections of any tuple. States
    # with no six-section cannot produce one by adding more plaquettes.
    masks = {fixed for _, _, fixed in loops}
    reachable = masks.copy()
    levels = [len(reachable)]
    while True:
        extended = {(f & g, s & t) for f, s in reachable for g, t in masks if s & t}
        if extended == reachable:
            break
        reachable = extended
        levels.append(len(reachable))
    six_only_counts = Counter(s.bit_count() for f, s in reachable if not f)
    assert levels == [120, 726, 762]
    assert min(s.bit_count() for _, s in reachable) == 2

    marker_ids = (0, 1, 2, 3, 4, 8)
    markers = [gates[i] @ gates[i] for i in marker_ids]
    assert all(np.array_equal(m, np.diag(np.diag(m))) and np.array_equal(m @ m, identity)
               for m in markers)
    signatures = np.array([np.diag(m) for m in markers]).T
    assert len(set(map(tuple, signatures))) == 27
    # Each section invariant under the markers is a direct sum of the
    # one-dimensional joint eigenspaces. Check the corresponding projectors.
    for i, signs in enumerate(signatures):
        projector_times_64 = identity.copy()
        for marker, sign in zip(markers, signs, strict=True):
            projector_times_64 = projector_times_64 @ (identity + sign * marker)
        assert np.array_equal(projector_times_64, 64 * np.outer(identity[i], identity[i]))

    return dict(status="PASS", nonflat_pairs=sum(counts.values()), coordinate_counts=counts,
                shared_link_counts=shared, witness=witness, marker_gate_squares=marker_ids,
                distinct_joint_characters=len(signatures),
                closure_sizes=levels, six_only_closure_counts=six_only_counts)


if __name__ == "__main__":
    result = calculate()
    OUT.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(result, flush=True)
