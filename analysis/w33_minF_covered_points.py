"""Pass 12643 item 2: is min F = 1/d for the minimal maximal partial spreads in d = 25?
Twirl identity => F(v) = sum_{e} (|<e|v>|^2 - |v|^2/d)^2 = (1/d) sum_{u in covered points, u != 0 as vectors} |<v|W_u|v>|^2, so F depends only on
the covered point set.  Minimise over unit v (L-BFGS, analytic gradient, many starts).
Controls (known minima): two qubits size 3 -> 1/4; three qubits size 5 -> 1/8 (Pass 12642); two qutrits pentad -> 0.14711376 (Pass 12637/12639; the certified bound 1/9 is NOT tight);
two qutrits size 8 -> 4/9 (Pass 12638).  Then d = 25: the m = 2 (13 lines) and m = 1 (14 lines) uniform covers from the sentinel ILP
(Pass 12640/12641: none certifies by the degree-4 bound).
usage: py -3 analysis/w33_minF_covered_points.py"""
import itertools, json, os, contextlib, io
import numpy as np
from scipy.optimize import minimize
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
def weyl(p, n, u):
    X = np.roll(np.eye(p), 1, axis=0); Z = np.diag(np.exp(2j * np.pi * np.arange(p) / p))
    M = np.eye(1)
    for i in range(n):
        M = np.kron(M, np.linalg.matrix_power(X, u[i]) @ np.linalg.matrix_power(Z, u[n + i]))
    return M
def ops_for(p, n, pts, covered):
    Ws = []
    for i in covered:
        for k in range(1, p):
            Ws.append(weyl(p, n, tuple((k * x) % p for x in pts[i])))
    return np.array(Ws)
def Fmin(p, n, pts, covered, starts=60, seed=0, lines=None):
    d = p ** n; Ws = ops_for(p, n, pts, covered); rng = np.random.default_rng(seed)
    if lines is not None:  # sanity: Weyl ops along a line commute (convention check)
        for L in lines[:3]:
            A = [weyl(p, n, pts[i]) for i in L]
            assert all(np.allclose(a @ b, b @ a) for a, b in itertools.combinations(A, 2))
    def fg(z):
        v = z[:d] + 1j * z[d:]; nv = np.vdot(v, v).real
        Wv = Ws @ v; f = np.einsum("i,ki->k", v.conj(), Wv)
        WHv = np.einsum("kji,j->ki", Ws.conj(), v)
        g = float(np.sum(abs(f) ** 2)) / d
        dg = (np.einsum("ki,k->i", Wv, f.conj()) + np.einsum("ki,k->i", WHv, f)) / d
        val = g / nv ** 2
        gr = 2 * dg / nv ** 2 - 4 * g * v / nv ** 3
        return val, np.concatenate([gr.real, gr.imag])
    best = min(minimize(fg, rng.standard_normal(2 * d), jac=True, method="L-BFGS-B", options=dict(maxiter=3000, gtol=1e-12)).fun for _ in range(starts))
    # check identity against the basis definition at one random v
    return float(best)
res = {}
cs = {"__name__": "x", "__file__": os.path.join(HERE, "w33_strong_umub_census.py")}
_src = open(os.path.join(HERE, "w33_strong_umub_census.py"), encoding="utf-8").read()
with contextlib.redirect_stdout(io.StringIO()):
    exec(_src[: _src.index("\nres = {}")], cs)
for (p, n, size, known) in [(2, 2, 3, 1 / 4), (2, 3, 5, 1 / 8), (3, 2, 5, 0.14711376), (3, 2, 8, 4 / 9)]:
    pts, lag, w = cs["geometry"](p, n); mps, _ = cs["maximal_partial_spreads"](lag)
    S = next(sorted(S) for S in mps if len(S) == size); cov = sorted(frozenset().union(*[lag[L] for L in S]))
    lines = [sorted(lag[L]) for L in S]
    # identity check: F from bases vs formula at random v
    B = cs["bases_for"](p, n, pts, lag); d = p ** n; v = np.random.default_rng(1).standard_normal(d) + 1j * np.random.default_rng(2).standard_normal(d)
    Fb = sum((abs(np.vdot(e, v)) ** 2 - np.vdot(v, v).real / d) ** 2 for L in S for e in B[L].T)
    Ws = ops_for(p, n, pts, cov); Ff = sum(abs(np.vdot(v, W @ v)) ** 2 for W in Ws) / d
    m = Fmin(p, n, pts, cov, lines=lines)
    res["control_p%d_n%d_size%d" % (p, n, size)] = dict(min_F=m, known=known, identity_err=float(abs(Fb - Ff)))
    print("control", p, n, size, "min F %.10f known %.10f  identity err %.1e" % (m, known, abs(Fb - Ff)), flush=True)
qs = {"__name__": "x", "__file__": os.path.join(HERE, "w33_ququint_sentinel_search.py")}
_src = open(os.path.join(HERE, "w33_ququint_sentinel_search.py"), encoding="utf-8").read()
with contextlib.redirect_stdout(io.StringIO()):
    exec(_src[: _src.index("res = {}")], qs)
p = 5; pts, lag, w = qs["geometry"](p, 2)
for m in (2, 1):
    ex = []
    for k in range(2):
        with contextlib.redirect_stdout(io.StringIO()):
            r = qs["search"](p, m, exclude=tuple(ex))
        lines = r["lines"]; ex.append(lines)
        cov = sorted(frozenset().union(*[lag[L] for L in lines]))
        mf = Fmin(p, 2, pts, cov, starts=80, seed=k, lines=[sorted(lag[L]) for L in lines])
        res["d25_m%d_cover%d" % (m, k)] = dict(size=len(lines), n_covered=len(cov), degree4_delta=r["delta"], min_F=mf, min_F_times_d=mf * 25)
        print("d=25 m=%d cover %d: size %d covered %d  degree-4 delta* %+.4f  min F %.8f  (x25 = %.5f)" % (m, k, len(lines), len(cov), r["delta"], mf, mf * 25), flush=True)
json.dump(res, open(os.path.join(ROOT, "data", "w33_minF_covered_points.json"), "w"), indent=1)
