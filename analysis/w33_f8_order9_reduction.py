"""Pass 12671: symmetry reduction of the F_8 regulus problem (nine MUBs of C^64, CZ model of Pass 12659).
Step 1: find every F_8-linear index permutation (a,b) -> (a,b) g, g in GL(2,8), that preserves F (tested on
random states; F is quartic so two random states with agreement to 1e-12 suffice to reject non-symmetries).
Step 2: pick an element of order 9 among the symmetries, split C^64 into its eigenspaces, and minimise F inside each one.
Step 3: compare each eigenspace minimum with c8 = (47 - 32 cos(2 pi/9))/9 (Pass 12669).
Result (Pass 12671): all 3528 elements of GL(2,8) preserve F, but no eigenspace of the order-9 element attains c8 (minima 37/3 and
47/9); the minimiser's symmetry is a Pauli stabiliser instead (w33_f8_rank3_stabiliser_exact.py).
usage: py -3 analysis/w33_f8_order9_reduction.py [starts_per_space]"""
import json, math, os, sys, time
import numpy as np
from scipy.optimize import minimize
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
src = open(os.path.join(HERE, "w33_regulus_constants_q16_q32.py"), encoding="utf-8").read()
g = {"__name__": "x", "__file__": os.path.join(HERE, "w33_regulus_constants_q16_q32.py")}
exec(src[: src.index("rng = np.random")], g)
q, mul, trace = g["field"](3)
_, fg = g["model"](3)
STARTS = int(sys.argv[1]) if len(sys.argv) > 1 else 40
C8 = (47 - 32 * math.cos(2 * math.pi / 9)) / 9
rng = np.random.default_rng(12671)


def F(A):
    A = A / np.linalg.norm(A); w = np.concatenate([A.real.ravel(), A.imag.ravel()])
    return fg(w)[0]


def apply(gm, v):  # row vector v in F_8^2 times 2x2 matrix gm
    return (mul(v[0], gm[0][0]) ^ mul(v[1], gm[1][0]), mul(v[0], gm[0][1]) ^ mul(v[1], gm[1][1]))


def perm_of(gm):
    return np.array([8 * a + b for (a, b) in (apply(gm, (x // 8, x % 8)) for x in range(64))])


# Step 1: symmetry search over GL(2,8)
tests = [rng.standard_normal(64) + 1j * rng.standard_normal(64) for _ in range(2)]
base = [F(t.reshape(8, 8)) for t in tests]
syms = []
for a in range(8):
    for b in range(8):
        for c in range(8):
            for d in range(8):
                if mul(a, d) ^ mul(b, c) == 0: continue
                P = perm_of(((a, b), (c, d)))
                # state transformed: (UA)[x] = A[P[x]]
                if all(abs(F(t[P].reshape(8, 8)) - f0) < 1e-11 for t, f0 in zip(tests, base)):
                    syms.append(((a, b), (c, d)))
print("GL(2,8) elements preserving F:", len(syms), flush=True)


def order(gm):
    P = perm_of(gm); Q = P.copy(); k = 1
    while not np.array_equal(Q, np.arange(64)): Q = Q[P]; k += 1
    return k


orders = {}
for s in syms: orders.setdefault(order(s), []).append(s)
print("order histogram:", {k: len(v) for k, v in sorted(orders.items())}, flush=True)
res = dict(n_symmetries=len(syms), order_histogram={str(k): len(v) for k, v in sorted(orders.items())}, c8_closed=C8)
if 9 not in orders:
    res["note"] = "no order-9 linear symmetry"
    json.dump(res, open(os.path.join(ROOT, "data", "w33_f8_order9_reduction.json"), "w"), indent=1); sys.exit()
h = orders[9][0]; P = perm_of(h); res["h"] = h
# cycle structure
seen = set(); cyc = []
for x in range(64):
    if x in seen: continue
    c = [x]; y = P[x]
    while y != x: c.append(int(y)); y = P[y]
    seen |= set(c); cyc.append(c)
res["cycle_type"] = sorted(len(c) for c in cyc)
print("h =", h, "cycle type", res["cycle_type"], flush=True)
# Step 2: eigenspaces of U: (UA)[x] = A[P[x]].  Eigenvector for zeta^j: sum over cycle positions.
z = np.exp(2j * np.pi / 9)
spaces = {}
for j in range(9):
    basis = []
    for c in cyc:
        L = len(c)
        if (j * L) % 9 != 0: continue  # eigenvalue zeta^j occurs on a cycle of length L iff zeta^(jL) = 1
        v = np.zeros(64, complex)
        # want v[P[x]] = zeta^j v[x]  => along cycle c[k+1] = P[c[k]]: v[c[k]] = zeta^(jk)
        for k, x in enumerate(c): v[x] = z ** (j * k)
        basis.append(v / np.linalg.norm(v))
    B = np.array(basis).T
    t = rng.standard_normal(B.shape[1]) + 1j * rng.standard_normal(B.shape[1]); v = B @ t
    assert np.allclose(v[P], z ** j * v)
    spaces[j] = B
res["dims"] = {str(j): spaces[j].shape[1] for j in range(9)}
print("eigenspace dimensions", res["dims"], flush=True)


def restricted(B):
    m = B.shape[1]

    def f(w):
        t = w[:m] + 1j * w[m:]; A = B @ t
        val, gr = fg(np.concatenate([A.real, A.imag]))
        G = gr[:64] + 1j * gr[64:]          # df/dRe + i df/dIm wrt A
        Gt = B.conj().T @ G                 # chain rule for linear map
        return val, np.concatenate([Gt.real, Gt.imag])
    return f, m


t0 = time.time(); res["minima"] = {}
for j in range(9):
    f, m = restricted(spaces[j])
    vals = []
    for _ in range(STARTS):
        r = minimize(f, rng.standard_normal(2 * m), jac=True, method="L-BFGS-B", options=dict(maxiter=20000, gtol=1e-12, ftol=1e-16))
        vals.append((r.fun * 64, r.x))
    vals.sort(key=lambda p: p[0])
    best = vals[0]
    res["minima"][str(j)] = dict(dim=m, best_c=best[0], lowest=[v[0] for v in vals[:5]], gap_to_c8=best[0] - C8)
    print("j", j, "dim", m, "best c", round(best[0], 12), "gap to c8", f"{best[0] - C8:.2e}", round(time.time() - t0), "s", flush=True)
res["attains_c8"] = [j for j in range(9) if abs(res["minima"][str(j)]["best_c"] - C8) < 1e-8]
print("eigenspaces attaining c8:", res["attains_c8"], flush=True)
json.dump(res, open(os.path.join(ROOT, "data", "w33_f8_order9_reduction.json"), "w"), indent=1)
