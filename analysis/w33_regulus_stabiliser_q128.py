"""Pass 12663: test of the conjecture m*(q) = (q+1)/3 for odd k at q = 128 (k = 7, fourteen qubits, 129 regulus bases; predicted 43).
Table-free annealing over Lagrangians of F_2^28: the span (16,384 vectors) is rebuilt each step and Q evaluated through the 128 x 128
multiplication table.  Reports the best |M cap {Q = 0}| per seed and whether every count seen is odd (parity theorem, Pass 12663).
Annealing can only give an UPPER bound on the minimum; not reaching 43, or stopping exactly at 43, is evidence only.
usage: py -3 analysis/w33_regulus_stabiliser_q128.py [seconds] [seed]"""
import json, math, os, sys, time
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
k = 7; q = 128; POLY = 0b10000011; msk = q - 1; n = 14; N = 28
def mul(a, b):
    r = 0
    while b:
        if b & 1: r ^= a
        b >>= 1; a <<= 1
        if a >> k & 1: a ^= POLY
    return r
MUL = np.array([[mul(a, b) for b in range(q)] for a in range(q)], dtype=np.int64)
def trace(a):
    s = 0; y = a
    for _ in range(k): s ^= y; y = int(MUL[y, y])
    assert s in (0, 1); return s
TR = np.array([trace(a) for a in range(q)])
parts = lambda v: (v & msk, (v >> k) & msk, (v >> 2 * k) & msk, (v >> 3 * k) & msk)
def om(u, v):
    a = parts(u); b = parts(v)
    return int(TR[MUL[a[0], b[2]] ^ MUL[a[1], b[3]] ^ MUL[a[2], b[0]] ^ MUL[a[3], b[1]]])
def cost(basis):
    s = np.zeros(1, dtype=np.int64)
    for b in basis: s = np.concatenate([s, s ^ b])
    Q = MUL[s & msk, (s >> 2 * k) & msk] ^ MUL[(s >> k) & msk, (s >> 3 * k) & msk]
    return int((Q == 0).sum()) - 1
sec = float(sys.argv[1]) if len(sys.argv) > 1 else 600; seed = int(sys.argv[2]) if len(sys.argv) > 2 else 0
rng = np.random.default_rng(1000 + seed); t0 = time.time()
basis = [1 << i for i in range(n)]; cur = cost(basis); best = cur; T = 6.0; steps = 0; all_odd = True; hist = []
while time.time() - t0 < sec:
    u = int(rng.integers(1, 1 << N)); nb = [b ^ (u if om(b, u) else 0) for b in basis]; c2 = cost(nb); steps += 1
    all_odd &= (c2 % 2 == 1)
    if c2 <= cur or rng.random() < math.exp(-(c2 - cur) / T): basis, cur = nb, c2
    if cur < best: best = cur; hist.append((steps, best))
    T = max(0.3, T * 0.99995)
    if steps % 60000 == 0: T = 3.0
res = dict(q=q, predicted=(q + 1) // 3, seed=seed, best=best, steps=steps, all_counts_odd=bool(all_odd), seconds=round(time.time() - t0), improvements=hist[-8:], basis=[int(b) for b in basis])
print({a: b for a, b in res.items() if a != "basis"}, flush=True)
json.dump(res, open(os.path.join(ROOT, "data", f"w33_regulus_stabiliser_q128_seed{seed}.json"), "w"), indent=1)
