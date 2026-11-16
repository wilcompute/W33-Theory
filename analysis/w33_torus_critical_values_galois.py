"""Pass 12678: are the Galois conjugates of the torus level tau_q critical values of F inside the torus eigenspaces?
At q = 8 the eigenspaces are 1-dim and the conjugates of c8 are the other eigenstates' values (Pass 12672/12673).  For q = 4, 16 the
eigenspaces are larger, and tau_q's conjugates do not occur as eigenspace minima.  Here: in every eigenspace of the equal-trace
torus Clifford, solve grad F = 0 (restricted, Riemannian) by least squares from many random starts, collect critical values, and
check which conjugates of tau_q (w33_q{q}_torus_level_eigenspace_newton.json) occur.  By symmetric criticality each critical point in
an eigenspace is a critical point of F on C^{q^2}.   usage: REG_K=k py -3 analysis/w33_torus_critical_values_galois.py [starts]"""
import collections, json, os, sys
import numpy as np
from scipy.optimize import least_squares
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
STARTS = int(sys.argv[1]) if len(sys.argv) > 1 else 40
tsrc = open(os.path.join(HERE, "w33_regulus_torus_clifford_eigenspaces.py"), encoding="utf-8").read()
_argv = sys.argv; sys.argv = ["x", os.environ.get("REG_K", "4"), "1", "1", "1"]
gt = {"__name__": "x", "__file__": os.path.join(HERE, "w33_regulus_torus_clifford_eigenspaces.py")}
exec(tsrc[: tsrc.index("t0 = time.time(); tor")], gt); sys.argv = _argv
q, d, fg, clifford, torus_elements, rng = (gt[k] for k in ("q", "d", "fg", "clifford", "torus_elements", "rng"))
conj = [float(c) for c in json.load(open(os.path.join(ROOT, "data", f"w33_q{q}_torus_level_eigenspace_newton.json")))["conjugates"]]
tor = torus_elements(); W = clifford(tor[0], tor[0]); ev, U = np.linalg.eig(W)
groups = []
for i in np.argsort(np.angle(ev)):
    if groups and abs(ev[groups[-1][0]] - ev[i]) < 1e-6: groups[-1].append(i)
    else: groups.append([i])
crit = collections.Counter(); per_space = []
for gi, idx in enumerate(groups):
    Q, _ = np.linalg.qr(U[:, idx]); m = Q.shape[1]
    def grad(x):
        A = Q @ (x[:m] + 1j * x[m:]); nrm = np.linalg.norm(A)
        val, gr = fg(np.concatenate([A.real, A.imag]) / nrm)
        G = Q.conj().T @ (gr[:d] + 1j * gr[d:]); return np.concatenate([G.real, G.imag, [nrm - 1.0]])
    vals = set()
    for _ in range(STARTS):
        r = least_squares(grad, rng.standard_normal(2 * m), xtol=1e-15, ftol=1e-15, gtol=1e-15, max_nfev=4000)
        if np.linalg.norm(r.fun[:-1]) < 1e-9:
            A = Q @ (r.x[:m] + 1j * r.x[m:]); A /= np.linalg.norm(A)
            v = fg(np.concatenate([A.real, A.imag]))[0] * d; vals.add(round(v, 7)); crit[round(v, 7)] += 1
    per_space.append(sorted(vals))
found = {c: [i for i, vs in enumerate(per_space) if any(abs(v - c) < 1e-5 for v in vs)] for c in conj}
print(f"q = {q}: conjugates of tau_q found as critical values (eigenspace indices):")
for c in conj: print(f"   {c:.10f}: {found[c]}")
res = dict(q=q, conjugates=conj, found_in_eigenspaces={f"{c:.10f}": v for c, v in found.items()}, n_eigenspaces=len(groups),
           all_conjugates_critical=all(found[c] for c in conj), critical_values_sample=sorted(crit)[:40])
print("all conjugates are critical values:", res["all_conjugates_critical"])
json.dump(res, open(os.path.join(ROOT, "data", f"w33_q{q}_torus_critical_values_galois.json"), "w"), indent=1)
