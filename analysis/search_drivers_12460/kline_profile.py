"""12460: the k-line lemma.  If S = N y is the mod-2 sum of k distinct lines of W(3,q) (any GQ of order (q,q)), each line of y meets the
other k - 1 lines in at most k - 1 points, so at least q + 2 - k of its points are covered by it alone, hence lie in S, and these sets are
disjoint for different lines:  |S| >= k (q + 2 - k)  (2 <= k <= q + 1).  For 2 <= k <= q the right side is >= 2q (concave in k, equal to 2q
at k = 2 and k = q).  So every nonzero kernel word that is a sum of at most q lines has weight >= 2q; this contains the other track's
exhaustive q = 7 three-line computation (7d27e910c: 10,586,800 triples) as the case k <= 3 and extends it to k <= 7 for q = 7.
Exhaustive profile at q = 3: for every nonzero word of ker_2 A, its weight and its minimal representation size k_min (ILP over line
sets with N y = S mod 2); checks |S| >= k_min (q + 2 - k_min) whenever k_min <= q + 1, and records how large k_min gets for small weights."""
import sys, json, itertools
import numpy as np
from scipy.optimize import milp, LinearConstraint, Bounds
sys.path.insert(0, '../search_drivers_12419')
from two_codes import w3q
from sympy import GF
from sympy.polys.matrices import DomainMatrix

q = 3
A = w3q(q); n = len(A)
# lines = maximal cliques of size q+1 of the collinearity graph
lines = set()
for a in range(n):
    for b in range(a + 1, n):
        if A[a, b]:
            L = [x for x in range(n) if x in (a, b) or (A[a, x] and A[b, x])]
            if len(L) == q + 1 and all(A[u, v] for u, v in itertools.combinations(L, 2)): lines.add(tuple(sorted(L)))
lines = sorted(lines); m = len(lines)
N = np.zeros((n, m), dtype=int)
for j, L in enumerate(lines): N[list(L), j] = 1
assert m == (q + 1) * (q * q + 1)
# kernel basis of A over GF(2)
K = DomainMatrix([[GF(2)(int(v)) for v in r] for r in A], (n, n), GF(2)).nullspace().to_Matrix()
K = np.array([[int(x) % 2 for x in row] for row in K.tolist()])
dim = K.shape[0]; assert dim == n - 16 and dim == 24      # ker A has dim n - rank_2 A = 24 (logical qubits q^2 - 1 = 8 = 24 - 16)


def kmin(S):
    # min sum y  s.t. N y - 2 z = S,  y binary, z integer >= 0
    c = np.concatenate([np.ones(m), np.zeros(n)])
    M = np.hstack([N, -2 * np.eye(n)])
    r = milp(c, constraints=LinearConstraint(M, S, S), integrality=np.ones(m + n), bounds=Bounds(np.zeros(m + n), np.concatenate([np.ones(m), np.full(n, q + 1)])))
    return int(round(r.fun))


import random
random.seed(12460)
# (1) every sum of k distinct lines, 2 <= k <= q + 1: weight vs the lemma bound
sums = {}
viol = 0
for k in range(2, q + 2):
    hist = {}
    for Y in itertools.combinations(range(m), k):
        S = N[:, Y].sum(1) % 2; w = int(S.sum())
        hist[w] = hist.get(w, 0) + 1
        if w < k * (q + 2 - k): viol += 1
    sums[k] = dict(sorted(hist.items()))
    print(k, 'min weight', min(hist), 'bound', k * (q + 2 - k), flush=True)
# (2) random kernel words: weight vs minimal representation size
samp = {}
for _ in range(300):
    S = (np.array([random.randint(0, 1) for _ in range(dim)]) @ K) % 2
    if not S.any(): continue
    w = int(S.sum()); k = kmin(S); samp.setdefault(w, []).append(k)
out = dict(q=q, lines=m, kernel_dim=dim, sums_of_k_lines={str(k): {str(w): c for w, c in v.items()} for k, v in sums.items()}, lemma_violations=viol,
           random_words={str(w): sorted(v) for w, v in sorted(samp.items())},
           min_k_seen_for_weight_le_2q={str(w): min(v) for w, v in samp.items() if w <= 2 * q})
print(json.dumps({k: v for k, v in out.items() if k != 'sums_of_k_lines'}))
json.dump(out, open('kline_profile_q3.json', 'w'), indent=1)
