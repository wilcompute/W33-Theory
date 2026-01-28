#!/usr/bin/env python3
"""Given orthogonal complement roots (72 indices), search for simple root sets of E6 within them."""

import itertools
import json
from fractions import Fraction
from pathlib import Path

if not data:
    print("No A2 complement found")
    raise SystemExit(1)
orth = data[0]["orth_indices"]

# build E8 roots rational as before
E8 = []
import itertools as _it

assert len(E8) == 240

# dot product
DP = [
    [sum(E8[i][k] * E8[j][k] for k in range(8)) for j in range(240)] for i in range(240)
]

# dynkin E6 edges set (for nodes 0..5 as before)
E6_edges = {(0, 2), (1, 2), (2, 3), (3, 4), (4, 5)}

# search among orth set for 6 roots forming E6 simple system
orth_roots = orth
solutions = []

def main():
    data = json.loads(Path("PART_CVII_e6_via_A2.json").read_text())
    print("orth size", len(orth))
    for i in range(8):
        for j in range(i + 1, 8):
            for si in (-1, 1):
                for sj in (-1, 1):
                    r = [0] * 8
                    r[i] = si
                    r[j] = sj
                    E8.append(tuple(Fraction(x) for x in r))
    for signs in _it.product([-1, 1], repeat=8):
        if sum(1 for s in signs if s < 0) % 2 == 0:
            r = tuple(Fraction(s, 2) for s in signs)
            E8.append(r)
    for comb in itertools.combinations(orth_roots, 6):
        # compute Cartan matrix
        M = [[0] * 6 for _ in range(6)]
        ok = True
        for i in range(6):
            for j in range(6):
                M[i][j] = Fraction(2) * DP[comb[i]][comb[j]] / DP[comb[i]][comb[i]]
        # check if entries are in {-1,0,2}
        valid = True
        for i in range(6):
            for j in range(6):
                if i == j:
                    if M[i][j] != 2:
                        valid = False
                else:
                    if M[i][j] not in (Fraction(0), Fraction(-1)):
                        valid = False
        if not valid:
            continue
        # check graph is E6 up to permutation
        # try permutations
        found_equiv = False
        import itertools
    pass
        for p in itertools.permutations(range(6)):
            match = True
            for i in range(6):
                for j in range(6):
                    expected = (
                        2 if i == j else (-1 if (min(i, j), max(i, j)) in E6_edges else 0)
                    )
                    if M[p[i]][p[j]] != expected:
                        match = False
                        break
                if not match:
                    break
            if match:
                found_equiv = True
                break
        if found_equiv:
            solutions.append({"comb": comb})
            print("Found E6 simple comb:", comb)
            break
    Path("PART_CVII_e6_in_e8_combs.json").write_text(json.dumps(solutions, indent=2))
    print("Done, found", len(solutions))


if __name__ == '__main__':
    main()

