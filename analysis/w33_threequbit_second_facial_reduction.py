"""Pass 12647 item 3 (step 4): second facial-reduction step for the exact three-qubit 1/8 certificate.
After the first step (K0 = 0 forced; G0 = W Y W^H with Y 16x16, W = exact complement of the 20-dim stabiliser kernel) the SDP
{Ar z = br, Y(z) >= 0} has interior margin ~0, so a nonzero Omega >= 0 exists with <Omega, Y(z)> = 0 for every feasible z:
  Omega = sum_t (Ar^T lam)_t H_t^dual,  br^T lam = 0,  Omega >= 0, tr Omega = 1  (H_t the Hermitian basis of Y).
Then Y Omega = 0 on the whole feasible set.  Report rank(Omega) and the eigen-structure, and lift range(Omega) to C^36 kernel vectors.
usage: py -3 analysis/w33_threequbit_second_facial_reduction.py"""
import os, contextlib, io, json
import numpy as np, cvxpy as cp
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
g = {"__name__": "x", "__file__": os.path.join(HERE, "w33_threequbit_exact_one_eighth.py")}
src = open(os.path.join(HERE, "w33_threequbit_exact_one_eighth.py"), encoding="utf-8").read()
with contextlib.redirect_stdout(io.StringIO()):
    exec(src[: src.index("# numerical SDP")], g)
Ar, br, HG, HK, W, rG = g["Ar"], g["br"], g["HG"], g["HK"], g["W"], g["rG"]
assert len(HK) == 0, "K block expected empty"
nvar = Ar.shape[1]; neq = Ar.shape[0]
# <Omega, H_t> (real trace inner product) must equal (Ar^T lam)_t
lam = cp.Variable(neq); Om_r = cp.Variable((rG, rG), symmetric=True); Om_i = cp.Variable((rG, rG))
inner = cp.hstack([cp.trace(Om_r @ H.real.T) + cp.trace(Om_i @ H.imag.T) for H in HG])  # Re tr(Omega^H H)
cons = [inner == Ar.T.astype(float) @ lam, br.astype(float) @ lam == 0, Om_i == -Om_i.T,
        cp.bmat([[Om_r, -Om_i], [Om_i, Om_r]]) >> 0, cp.trace(Om_r) == 1]
pr = cp.Problem(cp.Minimize(0), cons); pr.solve(solver=cp.SCS, eps=1e-10, max_iters=300000)
Om = Om_r.value + 1j * Om_i.value
ev, V = np.linalg.eigh((Om + Om.conj().T) / 2)
rank = int(np.sum(ev > 1e-6))
print("status", pr.status, "| Omega eigenvalues:", np.round(ev[::-1][:8], 6), "| rank", rank, flush=True)
# lift: x in C^36 with W^H x in range(Omega) -> extra kernel directions of G0 (modulo the old 20-dim kernel)
Yker = V[:, ev > 1e-6]
X = np.linalg.lstsq(W.conj().T, Yker, rcond=None)[0]
res = dict(status=pr.status, omega_eigs=[float(x) for x in ev[::-1]], omega_rank=rank, lifted_kernel_vectors=[[[float(c.real), float(c.imag)] for c in col] for col in X.T])
json.dump(res, open(os.path.join(ROOT, "data", "w33_threequbit_second_facial_reduction.json"), "w"), indent=1)
print({k: v for k, v in res.items() if k != "lifted_kernel_vectors"}, flush=True)
