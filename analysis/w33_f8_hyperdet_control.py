"""Pass 12681: control for a black-hole/qubit (STU) reading of the F_8 code-space minimisers.  The STU dictionary uses the three-qubit
Cayley hyperdeterminant, invariant only under local SL(2)^3.  The effective three-qubit factorisation of the code space is a free choice
(symplectic basis), and the problem's own symmetries include non-local Cliffords.  Test: is |Det| constant over the equivalent
minimisers (all with c = c8)?  If not, the minimiser carries no canonical STU 'entropy'.   usage: py -3 analysis/w33_f8_hyperdet_control.py"""
import collections, contextlib, io, json, os, sys
import numpy as np
from scipy.optimize import minimize
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
_argv = sys.argv; sys.argv = ["x", "T", "3"]
src = open(os.path.join(HERE, "w33_f8_codespace_effective_sos.py"), encoding="utf-8").read()
G = {"__name__": "x", "__file__": os.path.join(HERE, "w33_f8_codespace_effective_sos.py")}
with contextlib.redirect_stdout(io.StringIO()):
    exec(src[: src.index("rng = np.random.default_rng(1)")], G)
sys.argv = _argv
ceff, N, C8 = G["ceff"], G["N"], G["C8"]
def hyperdet(a):   # Cayley hyperdeterminant of a 2x2x2 tensor a[i,j,k], index y = 4i + 2j + k
    a = a.reshape(2, 2, 2)
    return (a[0,0,0]**2*a[1,1,1]**2 + a[0,0,1]**2*a[1,1,0]**2 + a[0,1,0]**2*a[1,0,1]**2 + a[1,0,0]**2*a[0,1,1]**2
            - 2*(a[0,0,0]*a[0,0,1]*a[1,1,0]*a[1,1,1] + a[0,0,0]*a[0,1,0]*a[1,0,1]*a[1,1,1] + a[0,0,0]*a[1,0,0]*a[0,1,1]*a[1,1,1]
                 + a[0,0,1]*a[0,1,0]*a[1,0,1]*a[1,1,0] + a[0,0,1]*a[1,0,0]*a[0,1,1]*a[1,1,0] + a[0,1,0]*a[1,0,0]*a[0,1,1]*a[1,0,1])
            + 4*(a[0,0,0]*a[0,1,1]*a[1,0,1]*a[1,1,0] + a[0,0,1]*a[0,1,0]*a[1,0,0]*a[1,1,1]))
rng = np.random.default_rng(3); vals = []
for _ in range(300):
    r = minimize(lambda w: ceff(w[:N] + 1j * w[N:]), rng.standard_normal(2 * N), method="BFGS", options=dict(gtol=1e-10))
    if abs(r.fun - C8) < 1e-7:
        psi = r.x[:N] + 1j * r.x[N:]; psi /= np.linalg.norm(psi); vals.append(4 * abs(hyperdet(psi)))
hist = collections.Counter(round(v, 6) for v in vals)
print("minimisers:", len(vals), "| distinct 3-tangle values 4|Det|:", sorted(hist.items()))
res = dict(n=len(vals), tangle_values={str(k): v for k, v in sorted(hist.items())}, canonical=len(hist) == 1)
json.dump(res, open(os.path.join(ROOT, "data", "w33_f8_hyperdet_control.json"), "w"), indent=1)
# ---- basis-change control: random three-qubit Clifford words (H, S, CNOT) applied to one minimiser
Hd = np.array([[1, 1], [1, -1]]) / np.sqrt(2); Sg = np.diag([1, 1j]); I2 = np.eye(2)
def on(q, U):
    mats = [I2, I2, I2]; mats[q] = U; return np.kron(np.kron(mats[0], mats[1]), mats[2])
def cnot(c, t):
    M = np.zeros((8, 8))
    for y in range(8):
        b = [(y >> (2 - i)) & 1 for i in range(3)]
        if b[c]: b[t] ^= 1
        M[4 * b[0] + 2 * b[1] + b[2], y] = 1
    return M
gates = [on(q, Hd) for q in range(3)] + [on(q, Sg) for q in range(3)] + [cnot(c, t) for c in range(3) for t in range(3) if c != t]
psi0 = None
for _ in range(50):
    r = minimize(lambda w: ceff(w[:N] + 1j * w[N:]), rng.standard_normal(2 * N), method="BFGS", options=dict(gtol=1e-10))
    if abs(r.fun - C8) < 1e-7: psi0 = r.x[:N] + 1j * r.x[N:]; psi0 /= np.linalg.norm(psi0); break
tang = collections.Counter()
local_only = collections.Counter()
for trial in range(400):
    C = np.eye(8, dtype=complex); Cl = np.eye(8, dtype=complex)
    for _ in range(12):
        g = gates[rng.integers(len(gates))]; C = g @ C
        gl_ = gates[rng.integers(6)]; Cl = gl_ @ Cl            # local gates only (H, S)
    tang[round(4 * abs(hyperdet(C @ psi0)), 6)] += 1; local_only[round(4 * abs(hyperdet(Cl @ psi0)), 6)] += 1
print("random Clifford basis changes -> distinct 3-tangles:", len(tang), "sample", sorted(tang)[:8])
print("local (H, S) changes only -> distinct 3-tangles:", sorted(local_only.items()))
import mpmath as mp
mp.mp.dps = 20; gam = 2 * mp.cos(2 * mp.pi / 9); s3 = mp.sqrt(3)
v = mp.mpf(4 * abs(hyperdet(psi0)))
rel = mp.pslq([v, 1, gam, gam * gam, s3, s3 * gam, s3 * gam * gam], maxcoeff=2000, tol=mp.mpf(10) ** -9)
rel2 = mp.pslq([v * v, 1, gam, gam * gam, s3, s3 * gam, s3 * gam * gam], maxcoeff=2000, tol=mp.mpf(10) ** -9)
print("tangle", mp.nstr(v, 12), "pslq:", rel, "| tangle^2 pslq:", rel2)
res.update(n_distinct_under_clifford=len(tang), local_invariant=len(local_only) == 1, tangle=mp.nstr(v, 12), tangle_pslq=str(rel), tangle_sq_pslq=str(rel2))
json.dump(res, open(os.path.join(ROOT, "data", "w33_f8_hyperdet_control.json"), "w"), indent=1)
