"""Pass 12653: does the three-qubit conditioning route (Pass 12649 Lemmas A, B + Pass 12652 moment bound) extend to the five-qubit
size-9 set?  For an uncovered P0, psi = c psi_+ + s psi_- (P0 eigenspaces, 16-dim each), t = c^2 - s^2.
  Commuting uncovered Paulis (cosets {b, b+P0} of P0^perp/<P0>, image Pauli Q on each eigenspace, <b> = c^2 alpha +- s^2 beta):
    coset with both members uncovered: exactly 2(c^4 alpha^2 + s^4 beta^2) <= 2(c^2 alpha^2 + s^2 beta^2);
    coset with one member uncovered: (c^2 alpha +- s^2 beta)^2 <= c^2 alpha^2 + s^2 beta^2 (Cauchy-Schwarz, c^2 + s^2 = 1).
    Hence Sigma_B <= c^2 lam_B + s^2 lam_B = lam_B, lam_B = max over unit 16-vectors of sum_Q w_Q <Q>^2 (w_Q in {1, 2}).
  Anticommuting uncovered: pair {a, a+P0} both uncovered contributes (1-t^2)|<psi_+|a|psi_->|^2 exactly (Lemma B); a single member
    contributes 4c^2 s^2 (Re z)^2 <= (1-t^2)|z|^2.  Hence Sigma_A <= (1-t^2) kappa_A, kappa_A = max sum_reps |<x|M_a y>|^2.
  So Sigma_U <= t^2 + lam_B + (1-t^2) kappa_A <= max(1 + lam_B, lam_B + kappa_A); the route proves 1/32 at P0 iff this is <= 30.
Also the two-moment upper bound for kappa_A.  Control: at n = 3 the same code at the distinguished P0 must give lam_B = 3, kappa_A = 3
(Pass 12649/12652: 1 + 3 + ... -> Sigma_U <= 6).  usage: py -3 analysis/w33_five_qubit_conditioning_scan.py [n_points]"""
import json, os, sys, time, itertools
import numpy as np
from scipy.optimize import minimize

HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
g = {"__name__": "x", "__file__": os.path.join(HERE, "w33_selfdual_pauli_lp.py")}
src = open(os.path.join(HERE, "w33_selfdual_pauli_lp.py"), encoding="utf-8").read()
exec(src[: src.index("t0 = time.time()")], g)
lags_from_codes = g["lags_from_codes"]
X1 = np.array([[0, 1], [1, 0]], complex); Z1 = np.diag([1, -1]).astype(complex)


def pauli(n, v):
    M = np.eye(1)
    for i in range(n):
        xi, zi = v >> i & 1, v >> (n + i) & 1
        M = np.kron(M, (1j) ** (xi * zi) * np.linalg.matrix_power(X1, xi) @ np.linalg.matrix_power(Z1, zi))
    return M


def omega(n):
    lo = (1 << n) - 1
    return lambda a, b: (bin((a & lo) & (b >> n)).count("1") + bin((a >> n) & (b & lo)).count("1")) % 2


def max_weighted(Qs, wts, dim, starts, rng):
    def fg(z):
        v = z[:dim] + 1j * z[dim:]; nv = np.vdot(v, v).real; e = np.einsum("i,kij,j->k", v.conj(), Qs, v).real
        f = (wts * e ** 2).sum() / nv ** 2
        gr = 4 * np.einsum("k,kij,j->i", wts * e, Qs, v) / nv ** 2 - 4 * f * v / nv
        return -f, -np.concatenate([gr.real, gr.imag])
    return max(-minimize(fg, rng.standard_normal(2 * dim), jac=True, method="L-BFGS-B").fun for _ in range(starts))


def kappa(Ms, starts, rng):
    best = 0; d = Ms.shape[1]
    for _ in range(starts):
        y = rng.standard_normal(d) + 1j * rng.standard_normal(d); y /= np.linalg.norm(y)
        for _ in range(200):
            W = np.einsum("kij,j->ik", Ms, y); x = np.linalg.eigh(W @ W.conj().T)[1][:, -1]
            W2 = np.einsum("kji,j->ik", Ms.conj(), x); y = np.linalg.eigh(W2 @ W2.conj().T)[1][:, -1]
        best = max(best, float((np.abs(np.einsum("i,kij,j->k", x.conj(), Ms, y)) ** 2).sum()))
    return best


def moment_bound(Ms, rng, trials=50):
    """two-moment bound max over sampled y (not a proof; diagnostic) of (k + sqrt((r-1)(r T2 - k^2)))/r"""
    k, d = Ms.shape[0], Ms.shape[1]; r = min(d, k); best = 0
    for _ in range(trials):
        y = rng.standard_normal(d) + 1j * rng.standard_normal(d); y /= np.linalg.norm(y)
        W = np.einsum("kij,j->ik", Ms, y); G = W.conj().T @ W; T2 = np.trace(G @ G).real
        best = max(best, (k + np.sqrt(max(0, (r - 1) * (r * T2 - k * k)))) / r)
    return best


def analyse(n, lags, p0, rng, starts=12):
    d = 1 << n; N = d * d; w = omega(n)
    C = set().union(*lags) - {0}; U = set(range(1, N)) - C
    P0 = pauli(n, p0); ev, V = np.linalg.eigh(P0); Vp, Vm = V[:, ev > 0], V[:, ev < 0]
    comm = [b for b in range(1, N) if b != p0 and w(b, p0) == 0]
    cosets = {}
    for b in comm:
        cosets.setdefault(min(b, b ^ p0), []).append(b)
    Qs, wts, mult = [], [], {0: 0, 1: 0, 2: 0}
    for rep, mem in cosets.items():
        k = sum(1 for b in mem if b in U); mult[k] += 1
        if k:
            Qs.append(Vp.conj().T @ pauli(n, rep) @ Vp); wts.append(float(k))
    anti = [a for a in U if w(a, p0) == 1]
    reps = sorted({min(a, a ^ p0) for a in anti})
    pair_both = sum(1 for r_ in reps if r_ in U and (r_ ^ p0) in U)
    Ms = np.array([Vp.conj().T @ pauli(n, r_) @ Vm for r_ in reps])
    lamB = max_weighted(np.array(Qs), np.array(wts), d // 2, starts, rng)
    kA = kappa(Ms, starts, rng)
    return dict(p0=int(p0), coset_multiplicities=mult, n_anti_reps=len(reps), anti_pairs_both_uncovered=pair_both,
                lam_B=lamB, kappa_A=kA, moment_bound_kappa_sampled=moment_bound(Ms, rng),
                route_bound=max(1 + lamB, lamB + kA), proves_target=bool(max(1 + lamB, lamB + kA) <= d - 2 + 1e-6))


rng = np.random.default_rng(0); t0 = time.time(); res = {}
# control n = 3: the distinguished P0 = coherent-closure singleton; try all uncovered points, the best must reach 6
lags3 = lags_from_codes(3, [41, 14, 53]); C3 = set().union(*lags3) - {0}
ctrl = [analyse(3, lags3, p, rng, starts=8) for p in range(1, 64) if p not in C3]
best3 = min(ctrl, key=lambda r: r["route_bound"])
print("control n=3 best route bound", best3["route_bound"], best3, flush=True)
assert abs(best3["route_bound"] - 6) < 1e-6
res["control_n3_best"] = best3; res["control_n3_route_bounds"] = sorted({round(r["route_bound"], 4) for r in ctrl})
lags5 = lags_from_codes(5, json.load(open(os.path.join(ROOT, "data", "w33_five_qubit_size9_verify.json")))["example"])
C5 = set().union(*lags5) - {0}; U5 = sorted(set(range(1, 1024)) - C5)
npts = int(sys.argv[1]) if len(sys.argv) > 1 else 40
sel = [U5[i] for i in np.random.default_rng(1).choice(len(U5), npts, replace=False)]
rows = []
for p in sel:
    r = analyse(5, lags5, p, rng, starts=6); rows.append(r)
    print({k: (round(v, 4) if isinstance(v, float) else v) for k, v in r.items()}, round(time.time() - t0), "s", flush=True)
res["n5_rows"] = rows; res["n5_best_route_bound"] = min(r["route_bound"] for r in rows)
res["seconds"] = round(time.time() - t0, 1)
json.dump(res, open(os.path.join(ROOT, "data", "w33_five_qubit_conditioning_scan.json"), "w"), indent=1)
