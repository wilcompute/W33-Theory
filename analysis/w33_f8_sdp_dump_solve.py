"""Pass 12683: re-solve an SDP dumped by w33_f8_symmetric_sos8.py (DUMP=<prefix>) without redoing the 20-minute setup.
Standard form (SCS convention): minimise c.x subject to b - A x in K = {0}^nz x PSD_lower-svec(cones).  The bound is -objective = x[-1].
Solvers: SOLVER = clarabel (rows permuted to Clarabel's upper-triangle svec order; equality rows normalised) | scs (SCS_EPS, SCS_ITERS).
usage: py -3 analysis/w33_f8_sdp_dump_solve.py <prefix>"""
import os, sys, time
import numpy as np
import scipy.sparse as sps

pre = sys.argv[1]
A = sps.load_npz(pre + "_A.npz").tocsc(); d = np.load(pre + "_bc.npz"); b, c, cones, nz = d["b"], d["c"], [int(t) for t in d["cones"]], int(d["nz"])
rn = np.sqrt(np.asarray(A[:nz].multiply(A[:nz]).sum(axis=1)).ravel())
D = sps.diags(np.concatenate([1 / rn, np.ones(A.shape[0] - nz)]))
A = (D @ A).tocsc(); b = D @ b
print(f"{A.shape[1]} variables, {nz} equalities, {len(cones)} cones (max {max(cones)}), nnz {A.nnz}", flush=True)
t0 = time.time()


def sidx(i, j, n):
    if i < j: i, j = j, i
    return j * n - j * (j - 1) // 2 + (i - j)


if os.environ.get("SOLVER", "clarabel") == "clarabel":
    import clarabel
    perm = np.arange(A.shape[0]); base = nz
    for n_ in cones:
        for i_ in range(n_):
            for j_ in range(i_ + 1):
                perm[base + i_ * (i_ + 1) // 2 + j_] = base + sidx(i_, j_, n_)
        base += n_ * (n_ + 1) // 2
    Acl = A.tocsr()[perm].tocsc(); bcl = b[perm]
    st = clarabel.DefaultSettings(); st.verbose = True; st.max_iter = int(os.environ.get("CL_ITERS", "300"))
    st.tol_gap_abs = st.tol_gap_rel = st.tol_feas = float(os.environ.get("EPS", "1e-8"))
    if os.environ.get("STATREG"): st.static_regularization_constant = float(os.environ["STATREG"])
    if os.environ.get("NOEQ"): st.equilibrate_enable = False
    s = clarabel.DefaultSolver(sps.csc_matrix((A.shape[1], A.shape[1])), c, Acl, bcl, [clarabel.ZeroConeT(nz)] + [clarabel.PSDTriangleConeT(n_) for n_ in cones], st).solve()
    x = np.array(s.x); status = str(s.status)
else:
    import scs
    s = scs.SCS(dict(A=A, b=b, c=c), dict(z=nz, s=cones), eps_abs=float(os.environ.get("EPS", "1e-8")), eps_rel=float(os.environ.get("EPS", "1e-8")),
                max_iters=int(os.environ.get("SCS_ITERS", "200000")), verbose=True, acceleration_lookback=int(os.environ.get("AA", "10"))).solve()
    x = s["x"]; status = s["info"]["status"]
# feasibility of the returned point: equality residual and minimum eigenvalue per cone
res_eq = float(np.abs(A[:nz] @ x - b[:nz]).max())
slack = b[nz:] - A[nz:] @ x; off = 0; mineig = np.inf
for n_ in cones:
    v = slack[off: off + n_ * (n_ + 1) // 2]; M = np.zeros((n_, n_))
    for j_ in range(n_):
        for i_ in range(j_, n_):
            M[i_, j_] = M[j_, i_] = v[sidx(i_, j_, n_)] / (1 if i_ == j_ else np.sqrt(2))
    mineig = min(mineig, np.linalg.eigvalsh(M)[0]); off += n_ * (n_ + 1) // 2
print(f"status {status}; bound x[-1] = {x[-1]:.10f}; max equality residual {res_eq:.2e}; min cone eigenvalue {mineig:.2e}; {time.time() - t0:.0f}s", flush=True)
if os.environ.get("OUT"):
    import json
    rec = dict(prefix=os.path.basename(pre), solver=os.environ.get("SOLVER", "clarabel"), statreg=os.environ.get("STATREG"), eps=os.environ.get("EPS", "1e-8"),
               status=status, bound=float(x[-1]), max_equality_residual=res_eq, min_cone_eigenvalue=float(mineig), variables=int(A.shape[1]), equalities=nz,
               cones=len(cones), max_cone=max(cones))
    rows = json.load(open(os.environ["OUT"])) if os.path.exists(os.environ["OUT"]) else []
    rows.append(rec); json.dump(rows, open(os.environ["OUT"], "w"), indent=1)
