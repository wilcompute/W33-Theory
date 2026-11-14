"""Pass 12660: the best STABILISER value for the F_q regulus sets: m*(q) = min over Lagrangians M of F_2^{4k} (stabiliser states)
of |M cap {Q = 0}| (non-zero points), since d F = |M cap C| on a stabiliser state of M.  Simulated annealing over Lagrangians with
symplectic transvection moves.  Compare with the numerical c_q (1, 1, 2.4985, 1 for q = 2, 4, 8, 16): c_q = m* means the optimum is
a stabiliser state; c_8 = 2.4985 < m*(8) would mean stabiliser states are NOT optimal at q = 8.
Control: q = 2 and q = 4 must give 1.   usage: py -3 analysis/w33_regulus_stabiliser_minimum.py [seconds_per_q]"""
import json, os, sys, time, math
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
src = open(os.path.join(HERE, "w33_regulus_constants_q16_q32.py"), encoding="utf-8").read()
g = {"__name__": "x", "__file__": os.path.join(HERE, "w33_regulus_constants_q16_q32.py")}
exec(src[: src.index("def model(")], g)
sec = float(sys.argv[1]) if len(sys.argv) > 1 else 120
out = {}
KS = tuple(int(a) for a in sys.argv[2].split(",")) if len(sys.argv) > 2 else (1, 2, 3, 4)
for k in KS:
    q, mul, trace = g["field"](k); n = 2 * k; N = 4 * k
    # vector = (x1, x2, z1, z2) each k bits, packed: x1 | x2<<k | z1<<2k | z2<<3k ; omega = Tr(x.z' + z.x'), Q = x1 z1 + x2 z2 in F_q
    msk = q - 1
    parts = lambda v: (v & msk, (v >> k) & msk, (v >> 2 * k) & msk, (v >> 3 * k) & msk)
    Qtab = np.zeros(1 << N, dtype=np.int16)
    MUL = np.array([[mul(a, b) for b in range(q)] for a in range(q)])
    vs = np.arange(1 << N); x1, x2, z1, z2 = vs & msk, (vs >> k) & msk, (vs >> 2 * k) & msk, (vs >> 3 * k) & msk
    Qtab = MUL[x1, z1] ^ MUL[x2, z2]
    TR = np.array([trace(a) for a in range(q)])
    def om(u, v):
        a = parts(u); b = parts(v)
        return int(TR[MUL[a[0], b[2]] ^ MUL[a[1], b[3]] ^ MUL[a[2], b[0]] ^ MUL[a[3], b[1]]])
    def span(basis):
        s = np.zeros(1, dtype=np.int64)
        for b in basis: s = np.concatenate([s, s ^ b])
        return s
    cost = lambda basis: int((Qtab[span(basis)[1:]] == 0).sum())
    rng = np.random.default_rng(k); t0 = time.time(); best = None
    basis = [1 << i for i in range(n)]  # x-space: Lagrangian L_0 (all covered)
    cur = cost(basis); T = 3.0; steps = 0
    while time.time() - t0 < sec and (best is None or best[0] > 1):
        u = int(rng.integers(1, 1 << N))
        nb = [b ^ (u if om(b, u) else 0) for b in basis]  # transvection
        c2 = cost(nb); steps += 1
        if c2 <= cur or rng.random() < math.exp(-(c2 - cur) / T): basis, cur = nb, c2
        if best is None or cur < best[0]: best = (cur, list(basis))
        T = max(0.15, T * 0.9997)
        if steps % 4000 == 0: T = 2.0
    # verify Lagrangian
    assert all(om(a, b) == 0 for a in best[1] for b in best[1]) and len(set(span(best[1]).tolist())) == 1 << n
    out[f"q{q}"] = dict(m_star_found=best[0], steps=steps, seconds=round(time.time() - t0, 1), basis=[int(b) for b in best[1]])
    print(q, {kk: v for kk, v in out[f"q{q}"].items() if kk != "basis"}, flush=True)
json.dump(out, open(os.path.join(ROOT, "data", "w33_regulus_stabiliser_minimum" + ("" if KS == (1, 2, 3, 4) else "_k" + "_".join(map(str, KS))) + ".json"), "w"), indent=1)
