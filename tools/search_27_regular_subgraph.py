#!/usr/bin/env python3
"""Search for a 27-vertex induced subgraph of G_lines where every node has degree 16.

Uses backtracking with pruning and a time limit.
"""
from __future__ import annotations

import time
from collections import defaultdict
from pathlib import Path
from typing import List, Set

import networkx as nx

ROOT = Path(__file__).resolve().parent
ART = ROOT / "artifacts"
ART.mkdir(exist_ok=True)

from tools.find_schlafli_embedding_in_w33 import (compute_w33_lines,
                                                  construct_w33_points)


def search(timeout=30):
    start = time.time()
    pts = construct_w33_points()
    lines = compute_w33_lines(pts)
    n = len(lines)
    G = nx.Graph()
    G.add_nodes_from(range(n))
    neigh = {i: set() for i in range(n)}
    for i in range(n):
        for j in range(i + 1, n):
            if set(lines[i]).isdisjoint(set(lines[j])):
                G.add_edge(i, j)
                neigh[i].add(j)
                neigh[j].add(i)

    target_k = 27
    target_deg = 16

    # Precompute degree bounds for pruning
    deg = {i: len(neigh[i]) for i in range(n)}

    # Quick feasibility: need at least 27 nodes with deg >= target_deg
    if sum(1 for d in deg.values() if d >= target_deg) < target_k:
        print("Not enough high-degree nodes")
        return None

    # Order vertices for branching: sort by degree descending
    verts = sorted(range(n), key=lambda i: -deg[i])

    # State for search
    chosen: List[int] = []
    chosen_set: Set[int] = set()
    current_intra_deg = defaultdict(int)  # counts of neighbors inside chosen

    # remaining pool
    remaining = list(verts)

    solution = None

    def can_still_succeed():
        # For each chosen vertex v, current_intra_deg[v] must be <= target_deg
        # and possible additional neighbors among remaining must be enough to reach target
        rem_set = set(remaining) - set(chosen)
        rem_size = target_k - len(chosen)
        for v in chosen:
            curr = current_intra_deg[v]
            possible = len(neigh[v] & rem_set)
            if curr > target_deg:
                return False
            if curr + possible < target_deg:
                return False
        # For each candidate in remaining, check if its degree among remaining+chosen can reach target
        # but that's expensive; we skip more aggressive pruning for now
        return True

    def backtrack(idx):
        nonlocal solution
        if solution is not None:
            return True
        if time.time() - start > timeout:
            return False
        # if chosen size reached target_k, check all chosen nodes have degree target_deg within chosen
        if len(chosen) == target_k:
            ok = True
            for v in chosen:
                if current_intra_deg[v] != target_deg:
                    ok = False
                    break
            if ok:
                solution = list(chosen)
                return True
            return False

        # prune
        if not can_still_succeed():
            return False

        # pick next candidate index from remaining order
        # prefer vertices that are most connected to current chosen set (to reach target_deg quickly)
        # compute scores
        rem_candidates = [v for v in verts if v not in chosen_set and v in remaining]
        # Heuristic: sort by number of edges into chosen (descending)
        rem_candidates.sort(key=lambda v: -len(neigh[v] & chosen_set))

        for v in rem_candidates:
            # quick check: v must be able to reach target_deg (current edges into chosen + possible from remaining)
            curr_into_chosen = len(neigh[v] & chosen_set)
            possible_from_remaining = len(neigh[v] & (set(rem_candidates) - {v}))
            if curr_into_chosen > target_deg:
                continue
            if curr_into_chosen + possible_from_remaining < target_deg:
                continue

            # choose v
            chosen.append(v)
            chosen_set.add(v)
            # update intra_deg counts for neighbors
            changed = []
            for u in neigh[v] & chosen_set:
                current_intra_deg[u] += 1
                changed.append(u)
            current_intra_deg[v] = curr_into_chosen

            # update remaining
            # temporarily remove v from remaining
            rem_prev = list(remaining)
            if v in remaining:
                remaining.remove(v)

            if backtrack(idx + 1):
                return True

            # undo
            remaining.clear()
            remaining.extend(rem_prev)
            for u in changed:
                current_intra_deg[u] -= 1
            current_intra_deg.pop(v, None)
            chosen.pop()
            chosen_set.remove(v)
            if time.time() - start > timeout:
                return False
        return False

    found = backtrack(0)
    if found and solution:
        print("Found solution subset of size", len(solution))
        (ART / "w33_schlafli_candidate_subset.json").write_text(
            json.dumps({"subset": solution}, indent=2)
        )
        return solution
    print("No solution found within time limit")
    return None


if __name__ == "__main__":
    search(30)
