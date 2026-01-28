#!/usr/bin/env python3
"""Evaluate all backtrack-found candidate simple systems for how many E8 roots lie in their integer span."""

import itertools
import json
from fractions import Fraction
from pathlib import Path

if not back.exists():
    print("No backtrack file")
    raise SystemExit(1)

# build E8 roots
E8 = []
assert len(E8) == 240

results = []
for sol in solutions:
    nodes = sol["nodes"]
    simples = [E8[i] for i in nodes]
    # T is 8x6 matrix with rows as coordinates
    T = [[simple[j] for simple in simples] for j in range(8)]

    # precompute ATA for normal eqns
    # function to solve T x = r via normal equations with fractions
    def solve_frac(A, b):
        m = len(A)
        n = len(A[0])
        ATA = [[Fraction(0) for _ in range(n)] for __ in range(n)]
        ATb = [Fraction(0) for _ in range(n)]
        for i in range(n):
            for j in range(n):
                s = Fraction(0)
                for k in range(m):
                    s += A[k][i] * A[k][j]
                ATA[i][j] = s
            s2 = Fraction(0)
            for k in range(m):
                s2 += A[k][i] * b[k]
            ATb[i] = s2
        # solve ATA x = ATb
        M = [row[:] + [ATb[i]] for i, row in enumerate(ATA)]
        N = n
        # elimination
        for col in range(N):
            pivot = None
            for r in range(col, N):
                if M[r][col] != 0:
                    pivot = r
                    break
            if pivot is None:
                return None
            if pivot != col:
                M[col], M[pivot] = M[pivot], M[col]
            pv = M[col][col]
            M[col] = [val / pv for val in M[col]]
            for r in range(col + 1, N):
                factor = M[r][col]
                if factor != 0:
                    M[r] = [M[r][c] - factor * M[col][c] for c in range(N + 1)]
        x = [Fraction(0) for _ in range(N)]
        for i in range(N - 1, -1, -1):
            s = M[i][N]
            for j in range(i + 1, N):
                s -= M[i][j] * x[j]
            if M[i][i] == 0:
                return None
            x[i] = s / M[i][i]
        return x

    in_span = []
    for idx, r in enumerate(E8):
        x = solve_frac(T, list(r))
        if x is None:
            continue
        # reconstruct
        recon = [
            sum(T[row][col] * x[col] for col in range(len(simples))) for row in range(8)
        ]
        if all(recon[i] == r[i] for i in range(8)) and all(
            xi.denominator == 1 for xi in x
        ):
            in_span.append(idx)
    results.append(
        {"nodes": nodes, "in_span_count": len(in_span), "in_span_indices": in_span[:20]}
    )


def main():
    back = Path("PART_CVII_e6_in_e8_backtrack.json")
    solutions = json.loads(back.read_text())
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
    Path("PART_CVII_e6_backtrack_eval.json").write_text(json.dumps(results, indent=2))
    print("Wrote PART_CVII_e6_backtrack_eval.json")
    print(json.dumps(results, indent=2))


if __name__ == "__main__":
    main()
