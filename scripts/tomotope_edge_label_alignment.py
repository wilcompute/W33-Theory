#!/usr/bin/env python3
"""Tomotope edge label alignment: internal r1 vs published p0..p3.

This script reads `data/tomotope_edge_orbits_report.json` (produced by
`scripts/tomotope_edge_orbit_report.py`) and searches for a relabeling of the
12 tomotope edges that conjugates the internal r1 permutation into one of the
published generators p0..p3 from Klitzing/MPW.

Goal:
    Find a permutation pi ∈ S_12 and a generator name `g` such that

        pi ∘ r1 ∘ pi^{-1} = p_g

If successful, the script writes `data/tomotope_edge_label_alignment.json`
containing:

    - which published generator r1 matches (by conjugacy),
    - the explicit permutation `pi` as a list of 12 integers,
    - its inverse,
    - a check flag confirming the equality pi ∘ r1 ∘ pi^{-1} = p_g.

This gives an explicit identification between the internal edge numbering in the
192-flag model and the published 12-edge maniplex generators.
"""

from __future__ import annotations

import json
from itertools import permutations, product
from pathlib import Path
from typing import Dict, List, Tuple

ROOT = Path(__file__).resolve().parents[1]
REPORT_PATH = ROOT / "data" / "tomotope_edge_orbits_report.json"
OUT_PATH = ROOT / "data" / "tomotope_edge_label_alignment.json"


def cycle_decomposition(perm: List[int]) -> List[List[int]]:
    """Return nontrivial cycles of `perm` as lists of indices.

    perm is a list of length n with entries in {0,..,n-1}.
    Fixed points (1-cycles) are omitted.
    """
    n = len(perm)
    seen = [False] * n
    cycles: List[List[int]] = []
    for i in range(n):
        if seen[i] or perm[i] == i:
            continue
        cycle = []
        j = i
        while not seen[j]:
            seen[j] = True
            cycle.append(j)
            j = perm[j]
        if len(cycle) > 1:
            cycles.append(cycle)
    return cycles


def cycle_type(perm: List[int]) -> Tuple[int, ...]:
    """Return the sorted multiset of nontrivial cycle lengths."""
    return tuple(sorted(len(c) for c in cycle_decomposition(perm)))


def build_conjugacy_maps(r1: List[int], p: List[int]) -> List[List[int]]:
    """Find all permutations pi with pi r1 pi^{-1} = p, via cycle-matching.

    Strategy:
      - Decompose r1 and p into nontrivial cycles.
      - If the multisets of lengths differ, no solution.
      - For each bijection between cycles of equal length and for each choice
        of rotation offset within each cycle, build a candidate pi on the
        union of moved points, then extend by fixing fixed points.
      - Filter candidates by verifying pi ∘ r1 ∘ pi^{-1} == p.

    This avoids a brute-force 12! search and only explores cycle-compatible
    relabelings.
    """
    n = len(r1)
    if len(p) != n:
        return []

    cycles_r = cycle_decomposition(r1)
    cycles_p = cycle_decomposition(p)

    if cycle_type(r1) != cycle_type(p):
        return []

    # Group cycles by length
    def group_by_length(cycles: List[List[int]]) -> Dict[int, List[List[int]]]:
        g: Dict[int, List[List[int]]] = {}
        for c in cycles:
            g.setdefault(len(c), []).append(c)
        return g

    gr = group_by_length(cycles_r)
    gp = group_by_length(cycles_p)

    # For each length l, we must choose a permutation between the k_l cycles
    # of r and the k_l cycles of p, and for each matched pair choose a
    # rotation offset.

    # Collect lengths to process
    lengths = sorted(gr.keys())

    # Precompute permutations of cycle indices for each length
    cycle_index_perms: Dict[int, List[Tuple[int, ...]]] = {}
    for l in lengths:
        k = len(gr[l])
        # All permutations of {0,..,k-1}
        cycle_index_perms[l] = list(permutations(range(k)))

    solutions: List[List[int]] = []

    def build_pi() -> None:
        # Candidate pi initialized as identity
        pi = list(range(n))

        # For each length, we will iterate over:
        #   - a permutation of cycle indices,
        #   - a tuple of offsets (one per cycle).
        # To keep things manageable, we build incrementally.

        def helper(idx_len: int, current_pi: List[int]) -> None:
            nonlocal solutions

            if idx_len == len(lengths):
                # At this point current_pi is fully defined on moved points.
                # Verify conjugacy.
                if all(current_pi[r1[i]] == p[current_pi[i]] for i in range(n)):
                    solutions.append(current_pi.copy())
                return

            l = lengths[idx_len]
            r_cycles = gr[l]
            p_cycles = gp[l]
            k = len(r_cycles)

            for perm_idx in cycle_index_perms[l]:  # mapping r_cycle idx -> p_cycle idx
                # For each mapping of cycles, choose rotation offsets
                for offsets in product(range(l), repeat=k):
                    pi_local = current_pi.copy()
                    ok = True
                    # Apply each cycle mapping with given offset
                    for r_idx, p_idx in enumerate(perm_idx):
                        cr = r_cycles[r_idx]
                        cp = p_cycles[p_idx]
                        off = offsets[r_idx]
                        for pos in range(l):
                            src = cr[pos]
                            dst = cp[(pos + off) % l]
                            # If conflicting assignment, skip
                            if pi_local[src] != src and pi_local[src] != dst:
                                ok = False
                                break
                            pi_local[src] = dst
                        if not ok:
                            break
                    if not ok:
                        continue
                    helper(idx_len + 1, pi_local)

        helper(0, pi)

    build_pi()
    return solutions


def main() -> None:
    if not REPORT_PATH.exists():
        raise SystemExit(f"Report file not found: {REPORT_PATH}")

    data = json.loads(REPORT_PATH.read_text(encoding="utf-8"))
    r1 = data["r1_on_edges"]
    p_maps: Dict[str, List[int]] = data["published_generators"]

    results = {}
    for name, p in p_maps.items():
        if cycle_type(r1) != cycle_type(p):
            continue
        sols = build_conjugacy_maps(r1, p)
        if sols:
            results[name] = []
            for pi in sols:
                # Build inverse and sanity-check conjugacy
                inv = [0] * len(pi)
                for i, j in enumerate(pi):
                    inv[j] = i
                # Verify conjugacy
                ok = all(pi[r1[i]] == p[pi[i]] for i in range(len(pi)))
                results[name].append({
                    "pi": pi,
                    "pi_inv": inv,
                    "conjugacy_ok": ok,
                })

    out = {
        "r1": r1,
        "published_generators": p_maps,
        "matches": results,
        "note": (
            "Each entry in matches[name] gives a permutation pi such that pi r1 pi^{-1} = p_maps[name]. "
            "This identifies the internal edge labels (0..11) with the published edge labels for that generator."
        ),
    }

    OUT_PATH.write_text(json.dumps(out, indent=2), encoding="utf-8")
    print("Wrote alignment data to", OUT_PATH)
    if results:
        print("Found matches for:", ", ".join(results.keys()))
    else:
        print("No conjugacy matches found; check that tomotope_edge_orbits_report.json is up to date.")


if __name__ == "__main__":
    main()
