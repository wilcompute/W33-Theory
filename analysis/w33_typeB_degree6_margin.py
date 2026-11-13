"""Pass 12660: a validated (floating-point, with explicit margin) degree-6 SOS bound for type B: fix delta0 < delta* = 0.04516 and
maximise the smallest eigenvalue t of both Gram blocks, so the certificate is strictly interior; then measure the equality residual
r = M(K, G) - (cF - delta0 cN) and the Frobenius norm of the least-norm Gram correction (dK, dG) that removes it exactly (lsqr).
If ||dK||_F, ||dG||_F < t the corrected Gram matrices are still PSD and the identity F|v|^2 - delta0 |v|^6 = SOS holds exactly in
real arithmetic up to the lsqr tolerance: F >= delta0.  This is validated numerics, not an exact rational certificate.
usage: py -3 analysis/w33_typeB_degree6_margin.py [delta0]"""
import json, os, sys, time
import numpy as np, cvxpy as cp, scipy.sparse as sps
from scipy.sparse.linalg import lsqr
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
src = open(os.path.join(HERE, "w33_typeB_degree6_sos.py"), encoding="utf-8").read()
g = {"__name__": "x", "__file__": os.path.join(HERE, "w33_typeB_degree6_sos.py")}
exec(src[: src.index("def solve(")], g)
MK, MG, cN, nK, nG = g["MK"], g["MG"], g["cN"], g["nK"], g["nG"]
delta0 = float(sys.argv[1]) if len(sys.argv) > 1 else 0.044
cF = g["coefF"](g["bases"]([0, 1, 2, 3])); rhs = cF - delta0 * cN
K0r = cp.Variable((nK, nK), symmetric=True); K0i = cp.Variable((nK, nK)); G0r = cp.Variable((nG, nG), symmetric=True); G0i = cp.Variable((nG, nG)); t = cp.Variable()
I2K = np.eye(2 * nK); I2G = np.eye(2 * nG)
cons = [cp.bmat([[K0r, -K0i], [K0i, K0r]]) >> t * I2K, cp.bmat([[G0r, -G0i], [G0i, G0r]]) >> t * I2G, K0i == -K0i.T, G0i == -G0i.T,
        MK @ cp.vec(K0r, order="C") + MG @ cp.vec(G0r, order="C") == rhs, MK @ cp.vec(K0i, order="C") + MG @ cp.vec(G0i, order="C") == 0]
pr = cp.Problem(cp.Maximize(t), cons); t0 = time.time(); pr.solve(solver=cp.SCS, eps=1e-8, max_iters=200000)
Kr, Ki, Gr, Gi = K0r.value, K0i.value, G0r.value, G0i.value
Kr = (Kr + Kr.T) / 2; Gr = (Gr + Gr.T) / 2; Ki = (Ki - Ki.T) / 2; Gi = (Gi - Gi.T) / 2
res_r = MK @ Kr.reshape(-1) + MG @ Gr.reshape(-1) - rhs; res_i = MK @ Ki.reshape(-1) + MG @ Gi.reshape(-1)
M = sps.hstack([MK, MG]).tocsr()
dr = lsqr(M, res_r, atol=1e-14, btol=1e-14, iter_lim=20000)[0]; di = lsqr(M, res_i, atol=1e-14, btol=1e-14, iter_lim=20000)[0]
Kr2 = Kr - dr[: nK * nK].reshape(nK, nK); Gr2 = Gr - dr[nK * nK:].reshape(nG, nG); Ki2 = Ki - di[: nK * nK].reshape(nK, nK); Gi2 = Gi - di[nK * nK:].reshape(nG, nG)
# re-symmetrise (the correction of a symmetric system need not be symmetric): symmetrising keeps M-image only if M is symmetric-invariant; measure the final residual
Kr2 = (Kr2 + Kr2.T) / 2; Gr2 = (Gr2 + Gr2.T) / 2; Ki2 = (Ki2 - Ki2.T) / 2; Gi2 = (Gi2 - Gi2.T) / 2
fr = np.abs(MK @ Kr2.reshape(-1) + MG @ Gr2.reshape(-1) - rhs).max(); fi = np.abs(MK @ Ki2.reshape(-1) + MG @ Gi2.reshape(-1)).max()
eK = np.linalg.eigvalsh(Kr2 + 1j * Ki2)[0]; eG = np.linalg.eigvalsh(Gr2 + 1j * Gi2)[0]
out = dict(delta0=delta0, t=float(t.value), status=pr.status, seconds=round(time.time() - t0, 1), residual_before=float(max(np.abs(res_r).max(), np.abs(res_i).max())),
           correction_frobenius=float(np.sqrt((dr ** 2).sum() + (di ** 2).sum())), residual_after=float(max(fr, fi)), min_eig_K_after=float(eK), min_eig_G_after=float(eG),
           validated=bool(eK > 0 and eG > 0 and max(fr, fi) < 1e-10 * max(1.0, abs(eK), abs(eG)) * 1e3))
print(out); json.dump(out, open(os.path.join(ROOT, "data", "w33_typeB_degree6_margin.json"), "w"), indent=1)
np.savez(os.path.join(ROOT, "data", "w33_typeB_degree6_margin_solution.npz"), K0=Kr2 + 1j * Ki2, G0=Gr2 + 1j * Gi2)
