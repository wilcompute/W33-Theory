"""Pass 12682: high-precision identification of the minima of F on the 16-dim code spaces of the 13 orbits (of 17) of uncovered
order-4 groups that do not attain c8 (Pass 12681).  For each orbit representative: effective four-qubit model (weights n(x,z) on
S^perp/S), BFGS from several starts, Newton polish with an analytic gradient, then 40-digit mpmath Newton (32 real parameters), and
findpoly (degree <= 8) / pslq over Q(cos 2pi/9) and small quadratic fields.  Control: the orbits whose minimum is the known saddle
level 2.7410899853553475 (root of 13c^3 - 265c^2 + 1447c - 2243, Pass 12672).   usage: py -3 analysis/w33_f8_orbit_levels_identify.py"""
import collections, contextlib, io, json, os, sys
import numpy as np
import mpmath as mp
from scipy.optimize import minimize
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
per = json.load(open(os.path.join(ROOT, "data", "w33_f8_order4_orbit_classification.json")))["per_orbit"]
src = open(os.path.join(HERE, "w33_f8_codespace_effective_sos.py"), encoding="utf-8").read()
pc = lambda n: bin(n).count("1") & 1
def model(rep):
    os.environ["GENS"] = ";".join(f"{a},{b}" for a, b in rep)
    _argv = sys.argv; sys.argv = ["x", "O", "3"]
    G = {"__name__": "x", "__file__": os.path.join(HERE, "w33_f8_codespace_effective_sos.py")}
    with contextlib.redirect_stdout(io.StringIO()):
        try: exec(src[: src.index("rng = np.random.default_rng(1)")], G)
        except AssertionError: pass
    sys.argv = _argv
    return G["weights"], G["N"]
results = []
mp.mp.dps = 40; gam = 2 * mp.cos(2 * mp.pi / 9)
for r in per:
    if r["attains_c8"]: continue
    weights, N = model(r["rep"])
    W = [(w, x, z) for (x, z), w in weights.items()]
    sgn = {(x, z): np.array([(-1) ** pc(z & (y ^ x)) for y in range(N)]) for (_, x, z) in W}
    def fg(v):
        psi = v[:N] + 1j * v[N:]; nn = np.vdot(psi, psi).real; f = 0.0; g = np.zeros(N, complex)
        for w, x, z in W:
            Pp = sgn[(x, z)] * psi[np.arange(N) ^ x]; a = np.vdot(psi, Pp); f += w * abs(a) ** 2
            PHp = (sgn[(x, z)] * psi)[np.arange(N) ^ x]       # P^dagger psi (P real, P^T = permutation back with signs)
            g += w * (np.conj(a) * Pp + a * PHp)
        f /= nn * nn; g = g / (nn * nn) - 2 * f * psi / nn
        return f, np.concatenate([2 * g.real, 2 * g.imag])
    rng = np.random.default_rng(r["orbit"])
    best = min((minimize(fg, rng.standard_normal(2 * N), jac=True, method="L-BFGS-B", options=dict(maxiter=20000, gtol=1e-12, ftol=1e-16)) for _ in range(30)), key=lambda q_: q_.fun)
    v = best.x / np.linalg.norm(best.x)
    # mp Newton
    def mp_fg(x):
        psi = [mp.mpc(x[i], x[N + i]) for i in range(N)]; nn = mp.fsum(abs(z) ** 2 for z in psi); f = mp.mpf(0); g = [mp.mpc(0)] * N
        for w, xx, zz in W:
            s = sgn[(xx, zz)]
            Pp = [s[i] * psi[i ^ xx] for i in range(N)]; a = mp.fsum(mp.conj(psi[i]) * Pp[i] for i in range(N)); f += w * abs(a) ** 2
            PHp = [s[i ^ xx] * psi[i ^ xx] for i in range(N)]
            g = [g[i] + w * (mp.conj(a) * Pp[i] + a * PHp[i]) for i in range(N)]
        f /= nn * nn; g = [gi / (nn * nn) - 2 * f * psi[i] / nn for i, gi in enumerate(g)]
        return f, [2 * mp.re(z) for z in g] + [2 * mp.im(z) for z in g]
    x = [mp.mpf(t) for t in v]; gn = None
    for it in range(6):
        f, g = mp_fg(x); gn = mp.sqrt(mp.fsum(t * t for t in g))
        if gn < mp.mpf(10) ** -35: break
        h = mp.mpf(10) ** -18; n2 = 2 * N; H = mp.matrix(n2, n2)
        for i in range(n2):
            xp = list(x); xm = list(x); xp[i] += h; xm[i] -= h; gp = mp_fg(xp)[1]; gm = mp_fg(xm)[1]
            for j in range(n2): H[j, i] = (gp[j] - gm[j]) / (2 * h)
        E, V = mp.eigsy((H + H.T) / 2); tol = mp.mpf(10) ** -10 * max(abs(e) for e in E); step = [mp.mpf(0)] * n2
        for kk in range(n2):
            if abs(E[kk]) > tol:
                co = mp.fsum(V[j, kk] * g[j] for j in range(n2)) / E[kk]
                for j in range(n2): step[j] += co * V[j, kk]
        x = [a_ - b_ for a_, b_ in zip(x, step)]
    c = mp_fg(x)[0]
    fp = None
    for deg in range(1, 9):
        fp = mp.findpoly(c, deg, maxcoeff=10 ** 6)
        if fp: break
    pq = mp.pslq([c, 1, gam, gam * gam], maxcoeff=10 ** 5, maxsteps=10 ** 6)
    rec = dict(orbit=r["orbit"], type=r["type"], value=mp.nstr(c, 32), gradient=mp.nstr(gn, 3), findpoly=str(fp), pslq_Q_cos2pi9=str(pq),
               identify=str(mp.identify(c, ["sqrt(2)", "sqrt(3)", "sqrt(5)", "sqrt(6)", "sqrt(7)", "sqrt(13)", "sqrt(17)", "sqrt(37)"])))
    results.append(rec); print(rec, flush=True)
json.dump(results, open(os.path.join(ROOT, "data", "w33_f8_orbit_levels_identify.json"), "w"), indent=1)
