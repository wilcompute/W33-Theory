#!/usr/bin/env python3
"""Exact F3 matrix and W33 geometry core for Passes 2762-2766."""
from __future__ import annotations
from collections import Counter, defaultdict, deque
from pathlib import Path
import hashlib
import itertools
import json
Q = 3
I = tuple((tuple((int(i == j) for j in range(4))) for i in range(4)))
J = ((0, 1, 0, 0), (2, 0, 0, 0), (0, 0, 0, 1), (0, 0, 2, 0))
NEG_I = tuple((tuple((2 if i == j else 0 for j in range(4))) for i in range(4)))
F_P = ((0, 2, 0, 0), (1, 0, 0, 0), (0, 0, 1, 0), (0, 0, 0, 1))
F_F = ((1, 0, 0, 0), (0, 1, 0, 0), (0, 0, 0, 2), (0, 0, 1, 0))
S_P = ((1, 0, 0, 0), (1, 1, 0, 0), (0, 0, 1, 0), (0, 0, 0, 1))
S_F = ((1, 0, 0, 0), (0, 1, 0, 0), (0, 0, 1, 0), (0, 0, 1, 1))
CX_PF = ((1, 0, 0, 0), (0, 1, 0, 2), (1, 0, 1, 0), (0, 0, 0, 1))
TRANSPOSE = ((0, 0, 1, 0), (0, 0, 0, 2), (1, 0, 0, 0), (0, 2, 0, 0))
GENERATORS = (F_P, F_F, S_P, S_F, CX_PF)
MAGIC_GRADE_MAP = (2, 2, 2, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 1, 1, 1, 1)

def mm(a, b):
    return tuple((tuple((sum((a[i][k] * b[k][j] for k in range(4))) % Q for j in range(4))) for i in range(4)))

def mv(a, v):
    return tuple((sum((a[i][k] * v[k] for k in range(4))) % Q for i in range(4)))

def tr(a):
    return tuple(zip(*a))

def madd(a, b):
    return tuple((tuple(((a[i][j] + b[i][j]) % Q for j in range(4))) for i in range(4)))

def msub(a, b):
    return tuple((tuple(((a[i][j] - b[i][j]) % Q for j in range(4))) for i in range(4)))

def mpow(a, n):
    out = I
    while n:
        if n & 1:
            out = mm(out, a)
        a = mm(a, a)
        n >>= 1
    return out

def inv(a):
    aug = [list(a[i]) + [int(i == j) for j in range(4)] for i in range(4)]
    for c in range(4):
        p = next((i for i in range(c, 4) if aug[i][c] % Q))
        aug[c], aug[p] = (aug[p], aug[c])
        z = aug[c][c] % Q
        iz = 1 if z == 1 else 2
        aug[c] = [iz * x % Q for x in aug[c]]
        for i in range(4):
            if i != c and aug[i][c] % Q:
                f = aug[i][c] % Q
                aug[i] = [(aug[i][j] - f * aug[c][j]) % Q for j in range(8)]
    return tuple((tuple(row[4:]) for row in aug))

def rank(a):
    m = [list(r) for r in a]
    r = 0
    for c in range(len(m[0])):
        p = next((i for i in range(r, len(m)) if m[i][c] % Q), None)
        if p is None:
            continue
        m[r], m[p] = (m[p], m[r])
        iz = 1 if m[r][c] % Q == 1 else 2
        m[r] = [iz * x % Q for x in m[r]]
        for i in range(len(m)):
            if i != r and m[i][c] % Q:
                f = m[i][c] % Q
                m[i] = [(m[i][j] - f * m[r][j]) % Q for j in range(len(m[0]))]
        r += 1
    return r

def order(a):
    x = I
    for n in range(1, 100):
        x = mm(a, x)
        if x == I:
            return n
    raise AssertionError('matrix order exceeded search bound')

def closure(gens):
    seen = {I}
    q = deque([I])
    while q:
        x = q.popleft()
        for g in gens:
            y = mm(g, x)
            if y not in seen:
                seen.add(y)
                q.append(y)
    return seen

def commutator(a, b):
    return mm(mm(mm(inv(a), inv(b)), a), b)

def symp(u, v):
    return (u[0] * v[1] - u[1] * v[0] + u[2] * v[3] - u[3] * v[2]) % Q

def norm(v):
    v = tuple((x % Q for x in v))
    first = next((x for x in v if x))
    scale = 1 if first == 1 else 2
    return tuple((scale * x % Q for x in v))

def cycle_profile(perm):
    seen = [False] * len(perm)
    out = Counter()
    for i in range(len(perm)):
        if seen[i]:
            continue
        n = 0
        j = i
        while not seen[j]:
            seen[j] = True
            n += 1
            j = perm[j]
        out[n] += 1
    return tuple(sorted(out.items()))

def profile_json(p):
    return {str(k): v for k, v in p}

def build_geometry():
    points = sorted({norm(v) for v in itertools.product(range(3), repeat=4) if any(v)})
    p_index = {p: i for i, p in enumerate(points)}
    lines = set()
    for i, u in enumerate(points):
        for v in points[i + 1:]:
            if symp(u, v):
                continue
            line = frozenset((norm(tuple((a * u[k] + b * v[k] for k in range(4)))) for a in range(3) for b in range(3) if a or b))
            if len(line) == 4:
                lines.add(line)
    lines = sorted(lines, key=lambda L: tuple(sorted((p_index[p] for p in L))))
    l_index = {L: i for i, L in enumerate(lines)}
    incident = [[] for _ in points]
    pair_line = {}
    for j, line in enumerate(lines):
        ids = sorted((p_index[p] for p in line))
        for p in ids:
            incident[p].append(j)
        for a, b in itertools.combinations(ids, 2):
            pair_line[a, b] = j
    flags = [(p, l) for p in range(40) for l in incident[p]]
    f_index = {f: i for i, f in enumerate(flags)}
    edges = sorted(pair_line)
    e_index = {e: i for i, e in enumerate(edges)}
    apartments = set()
    for p0, p1, p2, p3 in itertools.permutations(range(40), 4):
        adjacent = (tuple(sorted((p0, p1))), tuple(sorted((p1, p2))), tuple(sorted((p2, p3))), tuple(sorted((p3, p0))))
        if any((pair not in pair_line for pair in adjacent)):
            continue
        if tuple(sorted((p0, p2))) in pair_line or tuple(sorted((p1, p3))) in pair_line:
            continue
        ls = tuple((pair_line[pair] for pair in adjacent))
        if len(set(ls)) != 4:
            continue
        apartments.add((frozenset((p0, p1, p2, p3)), frozenset(ls)))
    apartments = sorted(apartments, key=lambda a: (tuple(sorted(a[0])), tuple(sorted(a[1]))))
    a_index = {a: i for i, a in enumerate(apartments)}
    return (points, p_index, lines, l_index, flags, f_index, edges, e_index, apartments, a_index)
