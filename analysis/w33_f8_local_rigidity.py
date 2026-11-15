"""Pass 12675: local rigidity of the F_8 regulus minimum set around code-space minimisers.
For each 16-dim code space type (A, B, C: uncovered order-4 Pauli groups) take generic minimisers inside the code space (random
starts, L-BFGS), and compare the null space of the Hessian of f(w) = F(w/|w|) in all of C^64 (128 real dims) with its null space
restricted to the code space (32 real dims).  Equal null dimensions mean every flat direction of the minimum set at that point is
tangent to the code space, i.e. nearby minimisers stay on it (a local form of 'every minimiser has an uncovered order-4 stabiliser').
Also reports negative eigenvalues (should be none at a minimum).   usage: py -3 analysis/w33_f8_local_rigidity.py"""
import json, os
import numpy as np
from scipy.optimize import minimize
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
lsrc = open(os.path.join(HERE, "w33_f8_pauli_stabiliser_ladder.py"), encoding="utf-8").read()
gl = {"__name__": "x", "__file__": os.path.join(HERE, "w33_f8_pauli_stabiliser_ladder.py")}
exec(lsrc[: lsrc.index("res = {}")], gl)
fg, space, C8 = gl["fg"], gl["space"], gl["C8"]
rng = np.random.default_rng(12675)
TYPES = {"A": [((12, 53), -1), ((53, 33), 1)], "B": [((11, 47), 1), ((35, 8), 1)], "C": [((53, 33), 1), ((1, 6), 1)]}
def hess(w, h=1e-5):
    n = len(w); H = np.zeros((n, n))
    for i in range(n):
        wp = w.copy(); wm = w.copy(); wp[i] += h; wm[i] -= h
        H[:, i] = (fg(wp)[1] - fg(wm)[1]) / (2 * h)
    return (H + H.T) / 2
out = {}
for name, gens in TYPES.items():
    B = space(gens); m = B.shape[1]
    def f(x):
        A = B @ (x[:m] + 1j * x[m:]); val, gr = fg(np.concatenate([A.real, A.imag]))
        G = B.conj().T @ (gr[:64] + 1j * gr[64:]); return val, np.concatenate([G.real, G.imag])
    recs = []
    for trial in range(4):
        r = min((minimize(f, rng.standard_normal(2 * m), jac=True, method="L-BFGS-B", options=dict(maxiter=50000, gtol=1e-13, ftol=1e-18)) for _ in range(4)), key=lambda r: r.fun)
        if abs(r.fun * 64 - C8) > 1e-8: continue
        A = B @ (r.x[:m] + 1j * r.x[m:]); A /= np.linalg.norm(A); w = np.concatenate([A.real, A.imag])
        H = hess(w); E = np.linalg.eigvalsh(H); scale = np.abs(E).max()
        null_full = int((np.abs(E) < 1e-6 * scale).sum()); neg_full = int((E < -1e-6 * scale).sum())
        # restricted Hessian: J^T H J with J the real embedding of B
        J = np.block([[B.real, -B.imag], [B.imag, B.real]])
        Hr = J.T @ H @ J; Er = np.linalg.eigvalsh((Hr + Hr.T) / 2)
        null_code = int((np.abs(Er) < 1e-6 * scale).sum())
        gap_full = float(np.sort(np.abs(E))[null_full]) / scale
        recs.append(dict(null_full=null_full, null_code=null_code, negative_full=neg_full, smallest_nonzero_rel=gap_full))
        print(name, recs[-1], flush=True)
    out[name] = recs
out["rigid_all"] = all(r["null_full"] == r["null_code"] and r["negative_full"] == 0 for k in TYPES for r in out[k])
print("local rigidity (full null space = code-space null space, no negative directions) at every sample:", out["rigid_all"], flush=True)
json.dump(out, open(os.path.join(ROOT, "data", "w33_f8_local_rigidity.json"), "w"), indent=1)
