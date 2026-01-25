#!/usr/bin/env python3
"""Exact rational check for E8 roots lying in integer span of chosen simple roots using Fraction arithmetic."""
from fractions import Fraction
import json
from pathlib import Path

# load backtrack nodes
back = Path('PART_CVII_e6_in_e8_backtrack.json')
if not back.exists():
    print('Backtrack file missing')
    raise SystemExit(1)
nodes = json.loads(back.read_text())[0]['nodes']
print('nodes', nodes)

# build E8 roots as rational vectors
E8 = []
import itertools
for i in range(8):
    for j in range(i+1, 8):
        for si in (-1,1):
            for sj in (-1,1):
                r = [0]*8
                r[i] = si
                r[j] = sj
                E8.append(tuple(Fraction(x) for x in r))
for signs in itertools.product([-1,1], repeat=8):
    if sum(1 for s in signs if s<0) % 2 == 0:
        r = tuple(Fraction(s,2) for s in signs)
        E8.append(r)
assert len(E8) == 240

# simple roots as rational
simples = [E8[i] for i in nodes]
# form matrix T = transpose of simples: 8 x 6 matrix
T = [[simple[j] for simple in simples] for j in range(8)]  # 8 rows

# Solve T * x = r for each r with rational arithmetic using Gaussian elimination
# We'll implement a simple fractional linear solver using extended matrix

def solve_frac(A, b):
    # A is m x n matrix (list of lists of Fraction); we solve for x in least-squares sense only if square; here A is 8x6, full column rank assumed; we solve A x = b by solving normal equations (A^T A) x = A^T b using fractions
    m = len(A)
    n = len(A[0])
    # compute ATA (n x n) and ATb (n)
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
    # now solve ATA x = ATb (n x n system) via Gaussian elimination with fractions
    # build augmented matrix
    M = [row[:] + [ATb[i]] for i, row in enumerate(ATA)]
    # forward elimination
    N = n
    for col in range(N):
        # find pivot
        pivot = None
        for r in range(col, N):
            if M[r][col] != 0:
                pivot = r
                break
        if pivot is None:
            return None
        if pivot != col:
            M[col], M[pivot] = M[pivot], M[col]
        # normalize row
        pv = M[col][col]
        M[col] = [val / pv for val in M[col]]
        # eliminate below
        for r in range(col+1, N):
            factor = M[r][col]
            if factor != 0:
                M[r] = [M[r][c] - factor * M[col][c] for c in range(N+1)]
    # back substitution
    x = [Fraction(0) for _ in range(N)]
    for i in range(N-1, -1, -1):
        s = M[i][N]
        for j in range(i+1, N):
            s -= M[i][j] * x[j]
        x[i] = s / M[i][i] if M[i][i] != 0 else None
    return x

in_span = []
for idx, r in enumerate(E8):
    x = solve_frac(T, list(r))
    if x is None:
        continue
    # check exact reconstruction
    recon = [sum(T[row][col] * x[col] for col in range(len(simples))) for row in range(8)]
    if all(recon[i] == r[i] for i in range(8)):
        # check integer coefficients
        if all(xi.denominator == 1 for xi in x):
            in_span.append({'index': idx, 'coeffs': [int(xi) for xi in x]})

print('Found in_span count:', len(in_span))
Path('PART_CVII_e6_in_e8_backtrack_exact.json').write_text(json.dumps(in_span, indent=2))
print('Wrote PART_CVII_e6_in_e8_backtrack_exact.json')
