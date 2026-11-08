"""Element orders of Sp(2n,3) by random products of symplectic transvections T_v(x) = x + w(x,v) v over F_3 (n = 2: the W(3,3) group Sp(4,3); n = 3: three qutrits).
Question from Pass 12629: which qutrit Clifford symplectic group contains a cyclic element of order N >= 21 (the cyclic-partner protection threshold at 16 keV, arXiv:2610.30253)?  Control: Sp(4,3) must give maximal order 18 (known in the repo: w33_BREAKTHROUGH_542; Chat 75f2a7e02).
Sampling finds orders that occur; it does not prove maximality (stated).  usage: py -3 sp_orders.py"""
import json
import numpy as np

rng = np.random.default_rng(1)
out = {}
import sys
NS = [int(x) for x in sys.argv[1:]] or [2, 3]
for n in NS:
    d = 2 * n
    J = np.zeros((d, d), int)
    for i in range(n):
        J[i, n + i], J[n + i, i] = 1, -1

    def transvection(v):
        return (np.eye(d, dtype=int) + np.outer(v, v @ J.T % 3 * 0 + (J @ v) % 3)) % 3

    def tv(v):
        # T(x) = x + (x^T J v) v  ->  matrix I + v (J v)^T ... acting on column x: T x = x + v (v^T J^T x)? use w(x,v) = x^T J v
        return (np.eye(d, dtype=int) + np.outer(v, (J @ v) % 3)) % 3

    def order(M, cap=1200):
        P = M.copy()
        for k in range(1, cap + 1):
            if np.array_equal(P, np.eye(d, dtype=int)):
                return k
            P = (P @ M) % 3
        return None

    orders = {}
    for _ in range({2: 20000, 3: 40000}.get(n, 15000)):
        M = np.eye(d, dtype=int)
        for _ in range(rng.integers(1, 3 * d)):
            v = rng.integers(0, 3, d)
            if not v.any():
                continue
            M = (M @ tv(v)) % 3
        assert np.array_equal((M.T @ J @ M) % 3, J % 3), "not symplectic"
        o = order(M)
        orders[o] = orders.get(o, 0) + 1
    ks = sorted(k for k in orders if k)
    out[f"Sp({d},3)"] = dict(orders_found=ks, max_found=max(ks), counts={str(k): orders[k] for k in ks})
    print("Sp(%d,3): orders found %s, max %d" % (d, ks, max(ks)))
json.dump(out, open("sp_orders.json" if NS == [2, 3] else "sp_orders_%s.json" % "_".join(map(str, NS)), "w"), indent=1)
