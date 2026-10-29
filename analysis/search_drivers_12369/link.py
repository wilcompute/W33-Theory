"""12371d: per light cone, the second invariant G2(omega, omega) = P(omega, kappa omega) versus the number of W(3,3) contexts kappa maps
into W(3,3): expected 16 (hyperbolic quadric = 4x4 grid) iff the invariant is 0, else 10 (elliptic quadric = ovoid)."""
import itertools, json, collections
import numpy as np
p = 3
P = np.block([[np.zeros((3, 3), dtype=np.int64), np.eye(3, dtype=np.int64)], [np.eye(3, dtype=np.int64), np.zeros((3, 3), dtype=np.int64)]])
w = np.array([0, 1, 0, 0, 2, 0], dtype=np.int64)
pts = [np.array(v, dtype=np.int64) for v in itertools.product(range(p), repeat=6) if any(v) and int(np.array(v) @ P @ np.array(v)) % p == 0 and next(x for x in v if x) == 1]
LW = [v for v in pts if int(v @ P @ w) % p == 0]
def norm(v):
    v = v % p; f = next(x for x in v if x); return tuple((v * (1 if f == 1 else 2)) % p)
LWs = {tuple(v) for v in LW}
K = np.load('allsols.npy')
tab = collections.Counter()
for k in K:
    tab[(int(w @ P @ k @ w) % p, sum(1 for v in LW if norm(k @ v) in LWs))] += 1
print(dict(tab)); json.dump({str(a): b for a, b in tab.items()}, open('link.json', 'w'), indent=1)
