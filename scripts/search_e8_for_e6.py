#!/usr/bin/env python3
"""Search E8 root set for 6-roots forming an E6 simple system via backtracking.
Writes PART_CVII_e6_in_e8_backtrack.json with solutions (if any) and diagnostics.
"""

import itertools
import json
from pathlib import Path

import numpy as np

# Build E8 roots explicitly (as in earlier scripts)
E8_roots = []
# Type 1
# Type 2
# Verify count
assert E8.shape[0] == 240

# Compute dot product matrix (rational floats OK)
DP = E8 @ E8.T
# For E8 roots lengths should be 2.0

# E6 Dynkin adjacency as indices 0-5 with edges: 0-2,1-2,2-3,3-4,4-5 (fork at 2)
# We'll use labeling where node 2 is the central node with degree 3.
E6_edges = {(0, 2), (1, 2), (2, 3), (3, 4), (4, 5)}
# Desired Cartan off-diagonal: -1 if connected, 0 otherwise.

n = E8.shape[0]
solutions = []

# Precompute neighbor lists: for each root i, neighbors j with dot = -1
neighbor_list = [set(np.where(np.isclose(DP[i], -1.0))[0].tolist()) for i in range(n)]

# Backtracking: choose node order [2,0,1,3,4,5] (center first) to maximize pruning
order = [2, 0, 1, 3, 4, 5]

# For every possible center root c, look for triples
# If none found


def main():
    for i in range(8):
        for j in range(i + 1, 8):
            for si in (-1, 1):
                for sj in (-1, 1):
                    r = [0] * 8
                    r[i] = si
                    r[j] = sj
                    E8_roots.append(tuple(r))
    for signs in itertools.product([-1, 1], repeat=8):
        if sum(1 for s in signs if s < 0) % 2 == 0:
            r = tuple(s * 0.5 for s in signs)
            E8_roots.append(r)
    E8 = np.array(E8_roots, dtype=float)
    lengths = np.diag(DP)
    for c in range(n):
        # nodes that have dot -1 to center: candidate for nodes 0,1,3
        neighs = neighbor_list[c]
        if len(neighs) < 3:
            continue
        # iterate combinations for nodes 0,1,3 from neighs
        # choose pairs for (0,1) among neighs that are mutually orthogonal (dot 0)
        neighs_list = list(neighs)
        for a_idx in range(len(neighs_list)):
            a = neighs_list[a_idx]
            for b_idx in range(a_idx + 1, len(neighs_list)):
                b = neighs_list[b_idx]
                # a and b should be not connected (dot 0)
                if not np.isclose(DP[a, b], 0.0):
                    continue
                # choose third neighbor d for node 3
                for d in neighs_list:
                    if d == a or d == b:
                        continue
                    # d must be not connected to a and b (dot 0)
                    if not np.isclose(DP[d, a], 0.0):
                        continue
                    if not np.isclose(DP[d, b], 0.0):
                        continue
                    # Now pick node 4 neighbor of d with dot -1, excluding c,a,b,d
                    cand4 = [x for x in neighbor_list[d] if x not in {c, a, b, d}]
                    for e in cand4:
                        # e should be dot 0 with a,b
                        if not np.isclose(DP[e, a], 0.0):
                            continue
                        if not np.isclose(DP[e, b], 0.0):
                            continue
                        # e must be connected to d (by construction), and then node 5 connected to e
                        for f in neighbor_list[e]:
                            if f in {c, a, b, d, e}:
                                continue
                            # f should be dot 0 with a,b,c,d
                            if not np.isclose(DP[f, a], 0.0):
                                continue
                            if not np.isclose(DP[f, b], 0.0):
                                continue
                            if not np.isclose(DP[f, d], 0.0):
                                continue
                            # Now we have candidate 6-tuple [a,b,c,d,e,f] in mapping to [0,1,2,3,4,5]? need order mapping
                            # Map to nodes [0,1,2,3,4,5] as [a,b,c,d,e,f]
                            idxs = [a, b, c, d, e, f]
                            # verify Cartan matrix equals E6
                            M = np.zeros((6, 6))
                            for i in range(6):
                                for j in range(6):
                                    M[i, j] = (
                                        2 * DP[idxs[i], idxs[j]] / DP[idxs[i], idxs[i]]
                                    )
                            # Check adjacency pattern off-diagonals are -1 at E6 edges
                            ok = True
                            for i in range(6):
                                for j in range(6):
                                    if i == j:
                                        if not np.isclose(M[i, j], 2.0):
                                            ok = False
                                    else:
                                        expected = (
                                            -1.0
                                            if (min(i, j), max(i, j)) in E6_edges
                                            else 0.0
                                        )
                                        if not np.isclose(M[i, j], expected):
                                            ok = False
                            if ok:
                                sol = {
                                    "center": int(c),
                                    "nodes": [int(x) for x in idxs],
                                }
                                # deduplicate by nodes set
                                nodeset = set(sol["nodes"])
                                if not any(
                                    set(s["nodes"]) == nodeset for s in solutions
                                ):
                                    solutions.append(sol)
                                    print("Found solution:", sol)
                                    Path(
                                        "PART_CVII_e6_in_e8_backtrack.json"
                                    ).write_text(json.dumps(solutions, indent=2))
                                    # continue searching until we collect many solutions
                                    if len(solutions) >= 50:
                                        print("Reached 50 solutions; stopping")
                                        Path(
                                            "PART_CVII_e6_in_e8_backtrack.json"
                                        ).write_text(json.dumps(solutions, indent=2))
                                        raise SystemExit(0)
    Path("PART_CVII_e6_in_e8_backtrack.json").write_text(
        json.dumps(solutions, indent=2)
    )
    print("Done backtracking, found", len(solutions))


if __name__ == "__main__":
    main()
