"""Pass 12672: torus-Clifford eigenspace reduction of the regulus certainty problem (q + 1 MUBs of C^{q^2}, q = 2^k).
Phase space = 2x2 matrices m over F_q, Q = det; the regulus set is preserved by m -> g m h^T, g, h in SL(2,q).  For g, h in the
non-split torus (order q + 1) build the Clifford unitary W implementing this symplectic map (W|0> = joint +1 eigenvector of the images
of the Z generators, W|x> = prod images of X generators applied to W|0>; any such W is correct up to a Pauli correction), optionally
times a Pauli correction, split C^d into eigenspaces of W, and minimise F (CZ model) on each.  At q = 8 the minimiser c8 lies in
4-dim eigenspaces of such a W (w33_f8_torus_global_origin / Pass 12672 note).  Question here: does the reduction find values below
the stabiliser value 11 at q = 32?
Pauli convention (other track's trace pairing): label (x, z), operator psi -> i^{Tr det(x,z)} (-1)^{Tr det(y^x, z)} psi[y^x],
m = [[x_lo, x_hi], [z_hi, z_lo]], det m = Q(x, z) = x_lo z_lo + x_hi z_hi.
usage: py -3 analysis/w33_regulus_torus_clifford_eigenspaces.py k [n_pairs] [starts] [corrections] [equal]
Calibration (q = 8): equal-trace pairs give 16 eigenspaces of dim 4 and attain c8 for every Pauli correction tried; unequal traces give
9 eigenspaces of dim 5-8 with best 2.8439259824."""
import json, math, os, sys, time
import numpy as np
from scipy.optimize import minimize
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
src = open(os.path.join(HERE, "w33_regulus_constants_q16_q32.py"), encoding="utf-8").read()
gl = {"__name__": "x", "__file__": os.path.join(HERE, "w33_regulus_constants_q16_q32.py")}
exec(src[: src.index("rng = np.random")], gl)
K = int(sys.argv[1]) if len(sys.argv) > 1 else 3
NPAIRS = int(sys.argv[2]) if len(sys.argv) > 2 else 6
STARTS = int(sys.argv[3]) if len(sys.argv) > 3 else 6
NCORR = int(sys.argv[4]) if len(sys.argv) > 4 else 2
q, mul, trace = gl["field"](K); _, fg = gl["model"](K); d = q * q
rng = np.random.default_rng(12672 + K)
TR = np.array([trace(a) for a in range(q)]); MUL = np.array([[mul(a, b) for b in range(q)] for a in range(q)])
lo = lambda x: x & (q - 1); hi = lambda x: x >> K
det = lambda x, z: int(MUL[lo(x), lo(z)] ^ MUL[hi(x), hi(z)])
sites = np.arange(d)


def act(psi, x, z):
    sg = 1 - 2 * TR[MUL[lo(sites), lo(z)] ^ MUL[hi(sites), hi(z)]]
    return (1j ** TR[det(x, z)]) * (sg * psi)[sites ^ x]


def actH(psi, x, z):  # Hermitian normalisation (P^2 = c I -> P / sqrt c)
    e = np.zeros(d, complex); e[0] = 1; c = act(act(e, x, z), x, z)[0]
    return act(psi, x, z) / np.sqrt(c)


tomat = lambda x, z: ((lo(x), hi(x)), (hi(z), lo(z)))
tolab = lambda m: (m[0][0] | (m[0][1] << K), m[1][1] | (m[1][0] << K))
mm = lambda A, B: tuple(tuple(int(MUL[A[i][0], B[0][j]] ^ MUL[A[i][1], B[1][j]]) for j in range(2)) for i in range(2))
tp = lambda A: ((A[0][0], A[1][0]), (A[0][1], A[1][1]))
I2 = ((1, 0), (0, 1))


def order(A):
    M, k = A, 1
    while M != I2: M = mm(M, A); k += 1
    return k


def torus_elements():
    from math import gcd
    ncls = sum(1 for j in range(1, q + 1) if gcd(j, q + 1) == 1) // 2      # traces of elements of order q + 1: phi(q+1)/2
    out = {}
    while len(out) < ncls:
        a, b, c = (int(v) for v in rng.integers(q, size=3))
        if a == 0: continue
        inv = next(v for v in range(1, q) if MUL[a, v] == 1); dd = int(MUL[inv, 1 ^ MUL[b, c]])   # a d + b c = 1
        A = ((a, b), (c, dd))
        if order(A) == q + 1: out.setdefault(a ^ dd, A)                     # one representative per trace (conjugacy class)
    return list(out.values())


def clifford(g, h):
    S = lambda x, z: tolab(mm(mm(g, tomat(x, z)), tp(h)))
    v = rng.standard_normal(d) + 1j * rng.standard_normal(d)
    for i in range(2 * K):
        x, z = S(0, 1 << i); v = (v + actH(v, x, z)) / 2
    v /= np.linalg.norm(v)
    imgs = [S(1 << i, 0) for i in range(2 * K)]
    W = np.zeros((d, d), complex)
    for xx in range(d):
        c = v
        for i in range(2 * K):
            if xx >> i & 1: c = actH(c, *imgs[i])
        W[:, xx] = c
    assert np.allclose(W.conj().T @ W, np.eye(d), atol=1e-8)
    return W


def eigen_minima(W):
    ev, U = np.linalg.eig(W)
    groups = []
    for i in np.argsort(np.angle(ev)):
        if groups and abs(ev[groups[-1][0]] - ev[i]) < 1e-6: groups[-1].append(i)
        else: groups.append([i])
    res = []
    for idx in groups:
        Q, _ = np.linalg.qr(U[:, idx]); m = Q.shape[1]

        def f(w):
            A = Q @ (w[:m] + 1j * w[m:]); val, gr = fg(np.concatenate([A.real, A.imag]))
            G = Q.conj().T @ (gr[:d] + 1j * gr[d:]); return val, np.concatenate([G.real, G.imag])
        best = min(minimize(f, rng.standard_normal(2 * m), jac=True, method="L-BFGS-B", options=dict(maxiter=int(os.environ.get("MAXIT", "20000")), gtol=float(os.environ.get("GTOL", "1e-11")), ftol=1e-15)).fun * d
                   for _ in range(STARTS))
        res.append((m, best))
    return res


t0 = time.time(); tor = torus_elements(); print(f"q = {q}: {len(tor)} torus classes", flush=True)
out = dict(q=q, runs=[]); overall = 1e9
pairs = [(g, h) for g in tor for h in tor]; rng.shuffle(pairs)
if "equal" in sys.argv: pairs = [(g, g) for g in tor] + [(g, h) for g, h in pairs if g != h and (g[0][0] ^ g[1][1]) == (h[0][0] ^ h[1][1])]
for g, h in pairs[:NPAIRS]:
    W0 = clifford(g, h)
    for cidx in range(NCORR):
        if cidx == 0: W = W0
        else:
            x, z = int(rng.integers(d)), int(rng.integers(d)); W = np.stack([actH(W0[:, j], x, z) for j in range(d)], 1)
        mins = eigen_minima(W); best = min(v for _, v in mins); overall = min(overall, best)
        dims = sorted(m for m, _ in mins)
        out["runs"].append(dict(g=g, h=h, correction=cidx, dims=dims, best=best, values=sorted(round(v, 8) for _, v in mins)))
        print(f"trace(g)={g[0][0] ^ g[1][1]} trace(h)={h[0][0] ^ h[1][1]} corr {cidx}: {len(mins)} eigenspaces, dims {min(dims)}-{max(dims)}, "
              f"best {best:.10f}   ({time.time() - t0:.0f}s)", flush=True)
        json.dump(dict(out, overall_best=overall), open(os.path.join(ROOT, "data", f"w33_regulus_torus_clifford_q{q}.json"), "w"), indent=1)
print("overall best", overall, flush=True)
