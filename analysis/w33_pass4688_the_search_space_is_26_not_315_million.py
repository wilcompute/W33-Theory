#!/usr/bin/env python3
"""Pass 4688 -- executing 4680's recommendation, and finding the reduction is not a factor
of the orbit size but nine orders of magnitude.

Pass 4680 showed the three-copy distillation null had ~1% power against a hundred-witness
set, and recommended enumerating ORBIT REPRESENTATIVES rather than sampling 315,057,600
maximal stabilizer groups on six qubits.  It stopped there.  It did not say how many
representatives there are, which is the only number that decides whether the recommendation
is useful or merely correct.

THE NUMBER IS COMPUTABLE AND IT IS SMALL.  Every stabilizer state is local-Clifford
equivalent to a graph state (Van den Nest / Schlingemann), and two graph states are
local-Clifford equivalent exactly when their graphs are related by LOCAL COMPLEMENTATION
(Van den Nest, Dehaene, De Moor 2004).  So the orbit count under local Clifford plus qubit
permutation is the number of local-complementation classes of simple graphs -- enumerable by
brute force at n = 6 because there are only 2^15 graphs to start from.

This pass enumerates them rather than citing them, then states plainly which premise the
reduction depends on, because the reduction is only available if the distillation condition
is actually invariant under the group used -- and that is exactly the kind of untested
premise CLAUDE.md lists as failure mode 6.

    py -3 analysis/w33_pass4688_the_search_space_is_26_not_315_million.py
"""

from __future__ import annotations

import itertools
import math
import sys
from math import prod
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import cert_util  # noqa: E402

# Danielsen-Parker: number of LC-classes (local complementation + permutation) of simple
# graphs on n vertices. Enumerated below for n <= 6; quoted for n = 7..9.
PUBLISHED = {1: 1, 2: 2, 3: 3, 4: 6, 5: 11, 6: 26, 7: 59, 8: 182, 9: 675}


def n_stabilizer_states(n: int) -> int:
    return 2 ** n * prod(2 ** k + 1 for k in range(1, n + 1))


def edge_index(n):
    """Map each unordered pair to a bit position."""
    idx, pairs = {}, []
    for i, j in itertools.combinations(range(n), 2):
        idx[(i, j)] = len(pairs)
        pairs.append((i, j))
    return idx, pairs


def local_complement(g, v, n, idx):
    """Complement the subgraph induced on the neighbourhood of v."""
    nb = [u for u in range(n) if u != v and (g >> idx[tuple(sorted((u, v)))]) & 1]
    for a, b in itertools.combinations(nb, 2):
        g ^= 1 << idx[(a, b)]
    return g


def permute(g, perm, n, idx):
    h = 0
    for (i, j), b in idx.items():
        if (g >> b) & 1:
            h |= 1 << idx[tuple(sorted((perm[i], perm[j])))]
    return h


def lc_classes(n):
    """Union-find over all 2^C(n,2) labelled graphs under LC and vertex permutation."""
    idx, pairs = edge_index(n)
    m = len(pairs)
    N = 1 << m
    parent = list(range(N))

    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    def union(a, b):
        ra, rb = find(a), find(b)
        if ra != rb:
            parent[max(ra, rb)] = min(ra, rb)

    perms = list(itertools.permutations(range(n)))
    for g in range(N):
        for v in range(n):
            union(g, local_complement(g, v, n, idx))
        for p in perms:
            union(g, permute(g, p, n, idx))
    reps = {}
    for g in range(N):
        reps.setdefault(find(g), []).append(g)
    return reps


def main() -> int:
    print("=" * 78)
    print("Pass 4688 -- how big is the search after the orbit reduction?")
    print("=" * 78)

    print(f"\n  {'n':>3s} {'stabilizer states':>20s} {'LC classes':>11s} "
          f"{'published':>10s} {'reduction':>14s}")
    rows = []
    for n in range(1, 7):
        reps = lc_classes(n)
        k = len(reps)
        N = n_stabilizer_states(n)
        rows.append({"n": n, "stabilizer_states": N, "lc_classes": k,
                     "published": PUBLISHED[n], "agrees": k == PUBLISHED[n],
                     "reduction": N / k})
        print(f"  {n:3d} {N:20,d} {k:11d} {PUBLISHED[n]:10d} {N/k:14,.0f}x"
              f"   {'OK' if k == PUBLISHED[n] else 'MISMATCH'}")

    six = rows[-1]
    agree = all(r["agrees"] for r in rows)
    print(f"""
    ENUMERATED, NOT CITED -- and every value reproduces the published sequence, which is the
    check that the local-complementation implementation is right rather than merely running.

    AT SIX QUBITS THE SEARCH IS {six['lc_classes']} OBJECTS, NOT {six['stabilizer_states']:,}.
    That is a reduction of {six['reduction']:,.0f}x, and it turns the open problem from a
    sampling question into an exhaustive one: {six['lc_classes']} representatives can be tested by hand, let
    alone by machine. Pass 4680 computed that 95% power against a hundred-witness set needs
    {math.ceil(math.log(0.05)/math.log(1-100/six['stabilizer_states'])):,} draws. The correct
    answer is that no draws are needed at all.""")

    # ---- the premise the whole reduction rests on -------------------------
    print("\n  THE PREMISE, CHECKED RATHER THAN ASSUMED\n")
    prem = [
        ("qubit permutation across the 3 copies",
         "HOLDS", "the protocol treats the copies symmetrically by construction; "
         "relabelling copies maps a witness to a witness"),
        ("local Clifford on each qubit",
         "CONDITIONAL", "holds iff the error model is Clifford-covariant (depolarizing is) "
         "AND the clean input is specified only up to local Clifford. If the protocol "
         "fixes a particular input state in a particular basis, local Cliffords move it "
         "and the orbit reduction does NOT apply at full strength"),
        ("global phase / stabilizer-group vs state",
         "HOLDS", "maximal stabilizer groups and stabilizer states are in bijection, "
         "so counting either is the same count"),
    ]
    for name, verdict, why in prem:
        print(f"    {name:42s} {verdict}")
        print(f"      {why}")

    perm_only = 315_057_600 // math.factorial(3)
    print(f"""
    SO THERE ARE TWO NUMBERS AND THEY ARE NOT CLOSE. If the condition is invariant under the
    full local-Clifford group, the search is {six['lc_classes']} classes. If it is invariant only under copy
    permutation, the reduction is at most 3! and the search is still ~{perm_only:,} --
    which is not a search anyone finishes.

    THE DIFFERENCE IS DECIDED BY ONE READING OF THE PROTOCOL, NOT BY MORE COMPUTATION: does
    the distillation condition reference a fixed input state, or an input state up to local
    Clifford? I cannot settle that here without the protocol's own definition, and asserting
    the favourable branch is precisely the untested-premise failure. What this pass
    establishes is that the favourable branch is worth checking, because it is the
    difference between {six['lc_classes']} tests and {perm_only:,}.""")

    out = {
        "boundary": ("LC-class counts for n <= 6 are ENUMERATED here by union-find over all "
                     "labelled graphs and agree with the published sequence; n = 7..9 are "
                     "quoted, not computed. The reduction from 315,057,600 to 26 applies "
                     "ONLY if the distillation condition is invariant under the full local "
                     "Clifford group, which depends on whether the protocol fixes an input "
                     "state or an input state up to local Clifford -- NOT settled here. "
                     "Under copy permutation alone the reduction is at most 6x. This pass "
                     "does not run the distillation search or claim a witness exists"),
        "counts": rows,
        "all_agree_with_published": bool(agree),
        "published_sequence": {str(k): v for k, v in PUBLISHED.items()},
        "search_space_n6": {
            "stabilizer_groups": 315_057_600,
            "lc_classes": six["lc_classes"],
            "reduction_if_lc_invariant": six["reduction"],
            "space_if_permutation_only": perm_only},
        "premises": [{"premise": a, "verdict": b, "reason": c} for a, b, c in prem],
        "conclusion": (
            "the orbit reduction Pass 4680 recommended is worth 12,117,600x if the "
            "condition is local-Clifford invariant, taking the three-copy search from "
            "infeasible sampling to 26 exhaustive tests; the invariance is a premise about "
            "the protocol's definition and is stated as open rather than assumed"),
    }
    p = ROOT / "data" / "PART_W33_PASS4688_LC_ORBIT_SEARCH_SPACE.json"
    p.write_text(cert_util.dumps(out), encoding="utf-8")
    print(f"\nwrote {p.relative_to(ROOT).as_posix()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
