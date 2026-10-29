"""12453: cut-rank profile of the q-ary W(3,q) graph state.  For a bipartition (X, Y) the entanglement (in qudits) of the graph state
|G>_p across the cut is rank_p A[X, Y] (Hein-Eisert-Briegel; qudit version Bahramgiri-Beigi).  A[X,Y] = (A+I)[X,Y], so it is <= the
ceiling rank_p(A+I) (12418).  Question: are BALANCED cuts at the ceiling (maximal possible), and what is the smallest balanced cut-rank
found by local search (an upper bound on the minimum, i.e. evidence about the rank-width-type quantity that universality needs)?
Control: qubits (p = 2) on the same graphs, ceiling 5."""
import sys, json, random
import numpy as np
from sympy.polys.matrices import DomainMatrix
from sympy import GF
sys.path.insert(0, '../search_drivers_12419')
from two_codes import w3q


def rk(M, p):
    return DomainMatrix([[GF(p)(int(v)) for v in row] for row in M], M.shape, GF(p)).rank()


def cut(A, X, p):
    Y = [i for i in range(len(A)) if i not in X]
    return rk(A[np.ix_(sorted(X), Y)] % p, p)


out = {}
random.seed(12453)
for q, ps in ((3, (3, 2)), (5, (5, 2))):
    A = w3q(q); n = len(A)
    for p in ps:
        ceil = rk((A + np.eye(n, dtype=int)) % p, p)
        rand = [cut(A, set(random.sample(range(n), n // 2)), p) for _ in range(40)]
        # local search downwards: swap one vertex across the cut while the cut-rank does not increase
        best = None
        for start in range(4 if q == 3 else 2):
            X = set(random.sample(range(n), n // 2)); r = cut(A, X, p)
            for _ in range(300 if q == 3 else 80):
                a = random.choice(sorted(X)); b = random.choice([i for i in range(n) if i not in X])
                X2 = (X - {a}) | {b}; r2 = cut(A, X2, p)
                if r2 <= r: X, r = X2, r2
            best = r if best is None else min(best, r)
        out[f'q={q},p={p}'] = dict(n=n, ceiling=ceil, random_balanced=dict(min=min(rand), max=max(rand), at_ceiling=sum(x == ceil for x in rand)),
                                   local_search_min=best)
        print(q, p, out[f'q={q},p={p}'], flush=True)
json.dump(out, open('cut_rank.json', 'w'), indent=1)
