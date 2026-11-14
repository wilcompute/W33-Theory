"""Pass 12662: structure of the best stabiliser Lagrangians for the F_q regulus at odd k (q = 8, 32).
(1) Several annealing seeds: best |M cap {Q = 0}| found (conjecture (q+1)/3: 3 and 11).
(2) For the best M: which regulus lines L_t (t in P^1(F_q)) carry its covered points, and how many each.
    Test of an explanation: are the hit lines an orbit of a cyclic subgroup of order (q+1)/3 of PGL(2,q) (a third of a non-split torus)?
    For q = 8 any 3 points are such an orbit (PGL(2,8) is 3-transitive), so only q = 32 is a real test.
(3) Radical data: rho_s = dim(M cap sM) for s in F_q \ F_2 (the polar form of Tr(sQ) on M has radical M cap sM, since
    Tr(s B(u,v)) = omega(su, v)); and the exact character sums S(s) = sum_{v in M} chi(sQ(v)), so that |M cap C| = q - 1 + (1/q) sum_{s != 0} S(s)... (reported).
usage: py -3 analysis/w33_regulus_odd_k_structure.py [seconds_per_seed]"""
import itertools, json, math, os, sys, time
from collections import Counter
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
src = open(os.path.join(HERE, "w33_regulus_constants_q16_q32.py"), encoding="utf-8").read()
g = {"__name__": "x", "__file__": os.path.join(HERE, "w33_regulus_constants_q16_q32.py")}
exec(src[: src.index("def model(")], g)
sec = float(sys.argv[1]) if len(sys.argv) > 1 else 150
out = {}
for k, seeds in ((3, (0, 1)), (5, (0, 1, 2))):
    q, mul, trace = g["field"](k); n = 2 * k; N = 4 * k; msk = q - 1
    MUL = np.array([[mul(a, b) for b in range(q)] for a in range(q)]); TR = np.array([trace(a) for a in range(q)])
    inv = [0] + [next(b for b in range(1, q) if mul(a, b) == 1) for a in range(1, q)]
    vs = np.arange(1 << N); X1, X2, Z1, Z2 = vs & msk, (vs >> k) & msk, (vs >> 2 * k) & msk, (vs >> 3 * k) & msk
    Qtab = MUL[X1, Z1] ^ MUL[X2, Z2]
    parts = lambda v: (v & msk, (v >> k) & msk, (v >> 2 * k) & msk, (v >> 3 * k) & msk)
    def om(u, v):
        a = parts(u); b = parts(v)
        return int(TR[MUL[a[0], b[2]] ^ MUL[a[1], b[3]] ^ MUL[a[2], b[0]] ^ MUL[a[3], b[1]]])
    def span(basis):
        s = np.zeros(1, dtype=np.int64)
        for b in basis: s = np.concatenate([s, s ^ b])
        return s
    cost = lambda basis: int((Qtab[span(basis)[1:]] == 0).sum())
    runs = []; bestM = None
    for seed in seeds:
        rng = np.random.default_rng(100 + seed); t0 = time.time()
        basis = [1 << i for i in range(n)]; cur = cost(basis); T = 3.0; steps = 0; best = (cur, list(basis))
        target = (q + 1) // 3
        while time.time() - t0 < sec:
            u = int(rng.integers(1, 1 << N)); nb = [b ^ (u if om(b, u) else 0) for b in basis]; c2 = cost(nb); steps += 1
            if c2 <= cur or rng.random() < math.exp(-(c2 - cur) / T): basis, cur = nb, c2
            if cur < best[0]: best = (cur, list(basis))
            T = max(0.15, T * 0.9997)
            if steps % 4000 == 0: T = 2.0
            if best[0] < target: break
        runs.append(dict(seed=seed, best=best[0], steps=steps))
        if bestM is None or best[0] < bestM[0]: bestM = best
    M = span(bestM[1]); Mset = set(M.tolist())
    # line of each covered point: L_inf: x = 0 ; L_t: z1 = t x2, z2 = t x1
    def line_of(v):
        x1, x2, z1, z2 = parts(v)
        if x1 == 0 and x2 == 0: return "inf"
        t = mul(z1, inv[x2]) if x2 else mul(z2, inv[x1])
        assert mul(t, x2) == z1 and mul(t, x1) == z2
        return t
    covered = [int(v) for v in M[1:] if Qtab[v] == 0]
    lines = Counter(line_of(v) for v in covered)
    # torus test (only meaningful for q = 32): is the set of hit lines an orbit of an element of PGL(2,q) of order (q+1)/3 ?
    hit = set(lines)
    def act(m, t):
        a, b, c_, d_ = m
        if t == "inf": return "inf" if c_ == 0 else mul(a, inv[c_])
        num = MUL[a, t] ^ b; den = MUL[c_, t] ^ d_
        return "inf" if den == 0 else mul(int(num), inv[int(den)])
    P1 = list(range(q)) + ["inf"]; orbit_found = False; n_checked = 0
    r = (q + 1) // 3
    if len(hit) == r:
        for a, b, c_, d_ in itertools.product(range(q), repeat=4):
            if (mul(a, d_) ^ mul(b, c_)) == 0: continue
            if not (a == 1 or (a == 0 and b == 1)): continue  # projective normalisation
            n_checked += 1; m = (a, b, c_, d_)
            t0_ = next(iter(hit)); orb = [t0_]; t = act(m, t0_)
            while t != t0_ and len(orb) <= r: orb.append(t); t = act(m, t)
            if len(orb) == r and set(orb) == hit: orbit_found = True; break
    # radicals and character sums
    rho = {}; S = {}
    for s in range(q):
        if s >= 2:
            sM = {mul(s, x1) | (mul(s, x2) << k) | (mul(s, z1) << 2 * k) | (mul(s, z2) << 3 * k) for (x1, x2, z1, z2) in (parts(int(v)) for v in M)}
            rho[s] = int(round(math.log2(len(Mset & sM))))
        S[s] = int(sum(1 - 2 * int(TR[MUL[s, Qtab[v]]]) for v in M))
    out[f"q{q}"] = dict(runs=runs, best=bestM[0], conjectured=(q + 1) // 3, basis=[int(b) for b in bestM[1]], covered_points=len(covered),
                        points_per_hit_line=sorted(lines.values()), n_hit_lines=len(hit), hit_lines=[str(x) for x in sorted(hit, key=str)],
                        hit_lines_are_cyclic_orbit_of_order_r=bool(orbit_found), pgl_elements_checked=n_checked,
                        radical_dims=dict(sorted(Counter(rho.values()).items())), char_sums=dict(sorted(Counter(S.values()).items())),
                        check_count=(sum(S.values()) // q) - 1)
    print(q, {a: b for a, b in out[f"q{q}"].items() if a != "basis"}, flush=True)
    json.dump(out, open(os.path.join(ROOT, "data", "w33_regulus_odd_k_structure.json"), "w"), indent=1, default=int)
