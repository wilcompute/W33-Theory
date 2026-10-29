"""12427: code-entanglement dictionary for the W(3,3) graph states.  For a graph state over F_p, a region R has an entanglement deficit
(S(R) < |R|) iff some nonzero x supported in R has Gamma x supported in R (then x generates a stabiliser element living inside R).  So the
smallest deficient region = min over nonzero x of |supp(x) u supp(A x)|.  Exhaustive over all x of weight <= 6 (binary) and <= 4
(ternary, x in {0,1,2}^40); every deficient region found is re-checked by the cut-rank formula.  Question: is the smallest deficient
binary region exactly the code distance d = 6 (the hexads, cross-track 923c4eb20), i.e. is every region of <= 5 points maximally
entangled?"""
import itertools, json, sys
import numpy as np
sys.path.insert(0, '../search_drivers_12419')
from two_codes import w3q, rank_mod

A = w3q(3)
n = len(A)


def region_size(x, p):
    y = (A @ x) % p
    return int(((x % p != 0) | (y != 0)).sum()), (x % p != 0) | (y != 0)


out = {}
# binary
best = {}
for w in range(1, 7):
    m = None; ex = None
    for S in itertools.combinations(range(n), w):
        x = np.zeros(n, dtype=np.int64); x[list(S)] = 1
        sz, R = region_size(x, 2)
        if m is None or sz < m:
            m, ex = sz, np.nonzero(R)[0].tolist()
    # cut-rank check of the example region
    Rl = ex; Bl = [i for i in range(n) if i not in Rl]
    S = rank_mod(A[np.ix_(Rl, Bl)], 2)
    best[w] = dict(min_region=m, example_region_cut_rank=S, example_region_size=len(Rl))
    print('F2 weight', w, best[w], flush=True)
out['F2'] = best
# ternary (weights <= 4, coefficients 1, 2)
bt = {}
for w in range(1, 5):
    m = None; ex = None
    for S in itertools.combinations(range(n), w):
        for coeffs in itertools.product((1, 2), repeat=w - 1):
            x = np.zeros(n, dtype=np.int64); x[S[0]] = 1
            for s, c in zip(S[1:], coeffs): x[s] = c
            sz, R = region_size(x, 3)
            if m is None or sz < m:
                m, ex = sz, np.nonzero(R)[0].tolist()
    Bl = [i for i in range(n) if i not in ex]
    bt[w] = dict(min_region=m, example_region_cut_rank=rank_mod(A[np.ix_(ex, Bl)], 3), example_region_size=len(ex))
    print('F3 weight', w, bt[w], flush=True)
out['F3'] = bt
json.dump(out, open('dictionary.json', 'w'), indent=1)
