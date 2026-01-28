#!/usr/bin/env python3
"""Try to find simple roots of a subsystem by selecting a generic linear functional and extracting indecomposable positive roots."""

import itertools
import json
from fractions import Fraction
from pathlib import Path

# build E8 roots as Fractions
orth = data[0]["orth_indices"]
E8 = []
assert len(E8) == 240

subset = [E8[i] for i in orth]
# pick generic linear functional v: e.g., sum of coordinates with random small integer coefficients
coeffs = [1, 2, 3, 5, 7, 11, 13, 17]
v = [Fraction(c) for c in coeffs]


def dot(u, v):
    return sum(ui * vi for ui, vi in zip(u, v))


import random

results = []


def main():
    data = json.loads(Path("PART_CVII_e6_via_A2.json").read_text())
    for i in range(8):
        for j in range(i + 1, 8):
            for si in (-1, 1):
                for sj in (-1, 1):
                    r = [0] * 8
                    r[i] = si
                    r[j] = sj
                    E8.append(tuple(Fraction(x) for x in r))
    for signs in itertools.product([-1, 1], repeat=8):
        if sum(1 for s in signs if s < 0) % 2 == 0:
            r = tuple(Fraction(s, 2) for s in signs)
            E8.append(r)
    for trial in range(20):
        coeffs = [random.randint(1, 20) for _ in range(8)]
        v = [Fraction(c) for c in coeffs]
        positives = []
        for idx, r in zip(orth, subset):
            val = dot(r, v)
            if val > 0:
                positives.append((idx, r))
        pos_vectors = [r for i, r in positives]
        pos_set = set(pos_vectors)
        indecomp = []
        for r in pos_vectors:
            can = False
            for a in pos_vectors:
                if a == r:
                    continue
                b = tuple(rr - aa for rr, aa in zip(r, a))
                if b in pos_set:
                    can = True
                    break
            if not can:
                indecomp.append(r)
        if len(indecomp) == 6:
            M = [[0] * 6 for _ in range(6)]
            for i in range(6):
                for j in range(6):
                    M[i][j] = (
                        2
                        * sum(indecomp[i][k] * indecomp[j][k] for k in range(8))
                        / sum(indecomp[i][k] * indecomp[i][k] for k in range(8))
                    )
            results.append(
                {
                    "trial": trial,
                    "coeffs": coeffs,
                    "indecomp_cartan": [[float(x) for x in row] for row in M],
                }
            )
            print(f"Trial {trial}: Found indecomp=6, Cartan matrix:")
            for row in M:
                print(row)
        else:
            print(f"Trial {trial}: indecomp={len(indecomp)}")
    Path("PART_CVII_e6_indec_simple_trials.json").write_text(
        json.dumps(results, indent=2)
    )
    print("Wrote PART_CVII_e6_indec_simple_trials.json")


if __name__ == "__main__":
    main()
