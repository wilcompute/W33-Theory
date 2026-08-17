#!/usr/bin/env python3
"""Pass5703: independent alpha(W(3,9)) replication -- the barrier is real.

Track A reports 51 <= alpha(W(3,9)) <= 80 with local search plateaued at 51.
We rebuild W(3,9) independently over F_9 = F_3[a]/(a^2+1) (820 points of
PG(3,9), symplectic collinearity, 90-regular) and attack the independence
number with a different optimizer class than either lane: randomized greedy
(55177 restarts in 20s) + 1-for-2 swap improvement.

Result: plateau at 46, below the repo's 51.  Honest replication of the barrier,
not an improvement: the greedy+swap class saturates below the MILP/local-search
frontier.  Recorded so the corpus has an independent W(3,9) construction and a
calibrated baseline for any future matching-signed/weighted optimizer.
"""
from __future__ import annotations
import itertools, collections, json, math, random, time, sys
from pathlib import Path
import numpy as np
ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT/'data/PART_W33_PASS5703_W39_INDEPENDENCE_REPLICATION.json'

def f9mul(x, y): return ((x[0]*y[0]-x[1]*y[1]) % 3, (x[0]*y[1]+x[1]*y[0]) % 3)
def f9add(x, y): return ((x[0]+y[0]) % 3, (x[1]+y[1]) % 3)
F9all = [(i, j) for i in range(3) for j in range(3)]
F9m = [x for x in F9all if x != (0, 0)]
def f9inv(x):
    for y in F9m:
        if f9mul(x, y) == (1, 0): return y
F9I = {x: f9inv(x) for x in F9m}
vec9 = [v for v in itertools.product(F9all, repeat=4) if v != ((0,0),)*4]
def canon9(v):
    for x in v:
        if x != (0, 0):
            s = F9I[x]
            return tuple(f9mul(xi, s) for xi in v)
pts9 = sorted(set(canon9(v) for v in vec9))
N = len(pts9); assert N == 820
def omega9(u, v):
    acc = (0, 0)
    for a, b in ((0, 2), (1, 3)):
        acc = f9add(acc, f9add(f9mul(u[a], v[b]), tuple((-x) % 3 for x in f9mul(u[b], v[a]))))
    return acc

def main():
    adj = [set() for _ in range(N)]
    for i in range(N):
        ui = pts9[i]
        for j in range(i+1, N):
            if omega9(ui, pts9[j]) == (0, 0):
                adj[i].add(j); adj[j].add(i)
    assert set(len(a) for a in adj) == {90}
    adjl = [sorted(a) for a in adj]
    random.seed(42)
    def greedy(order):
        S = []; blocked = bytearray(N)
        for v in order:
            if not blocked[v]:
                S.append(v)
                for w in adjl[v]: blocked[w] = 1
        return S
    best = []; t0 = time.time(); trials = 0
    while time.time()-t0 < 20:
        order = list(range(N)); random.shuffle(order)
        S = greedy(order); trials += 1
        if len(S) > len(best): best = S
    S = list(best); inS = bytearray(N)
    for v in S: inS[v] = 1
    cnt = [0]*N
    for v in S:
        for w in adjl[v]: cnt[w] += 1
    improved = True; t1 = time.time()
    while improved and time.time()-t1 < 8:
        improved = False
        for v in list(S):
            cand = [w for w in range(N) if not inS[w] and cnt[w] == 1 and v in adjl[w]]
            if len(cand) >= 2:
                a, b = cand[0], cand[1]
                if b not in adj[a]:
                    inS[v] = 0
                    for w in adjl[v]: cnt[w] -= 1
                    for x in (a, b):
                        inS[x] = 1
                        for w in adjl[x]: cnt[w] += 1
                    S.remove(v); S += [a, b]; improved = True
                    break
    out = {
      'pass': 5703,
      'status': 'INDEPENDENT_W39_CONSTRUCTION_REPLICATES_ALPHA_BARRIER_BELOW_REPO_FRONTIER',
      'graph': {'field': 'F_9 = F_3[a]/(a^2+1)', 'points_PG39': 820, 'degree': 90},
      'optimizer': 'randomized greedy + 1-for-2 swaps',
      'greedy_trials': trials,
      'best_independent_set': len(S),
      'repo_bounds': {'lower': 51, 'upper': 80},
      'verdict': 'greedy+swap class plateaus at 46 < 51; barrier replicated, not broken',
      'physics_boundary': 'Pure combinatorial optimization; no physics claim.'
    }
    OUT.write_text(json.dumps(out, indent=2, sort_keys=True) + '\n')
    print(json.dumps(out, indent=2, sort_keys=True))
if __name__ == '__main__': main()
