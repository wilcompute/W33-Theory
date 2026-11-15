"""Pass 12674: EXACT degree-8 SOS certificate 64F >= C on the 8-dim code space of T, in the effective three-qubit model
(w33_f8_codespace_effective_sos.py builds the structure: integer weights n(x,z), pair-orbit variables gamma, Fourier PSD blocks).
Steps: (1) SCS at fixed C maximising s with every block Y - s I PSD; (2) round gamma to Gaussian rationals (2^-40); (3) exact
orthogonal projection onto the coefficient equations (each variable enters one class and its conjugate; per conjugate-class pair
one real and one imaginary equation, solved in closed form); (4) exact PSD proof of every block: Y - delta I = L L^T + E with dyadic
L, exact residual E, ||E||_F < delta.   usage: py -3 analysis/w33_f8_codespace_effective_certify.py C   (e.g. 49985/20006)"""
import collections, json, math, os, sys, time
from fractions import Fraction as Fr
import numpy as np
import scipy.sparse as sps
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
CC = Fr(sys.argv[1]) if len(sys.argv) > 1 else Fr(24985, 10000)
_argv = sys.argv; sys.argv = ["x", "T", "4"]
src = open(os.path.join(HERE, "w33_f8_codespace_effective_sos.py"), encoding="utf-8").read()
G = {"__name__": "x", "__file__": os.path.join(HERE, "w33_f8_codespace_effective_sos.py")}
exec(src[: src.index("# ---------------- SCS")], G); sys.argv = _argv
VARS, var_rows, cones, psd_entries, classes, cidx, NK = (G[k] for k in ("VARS", "var_rows", "cones", "psd_entries", "classes", "cidx", "NK"))
log = G["log"]; C8 = G["C8"]
# exact targets (integers): recompute TA, TB exactly
TAe, TBe = [], []
for mu in classes:
    sz = G["orbit_size"](mu); A_, B_ = G["tcoef"](mu); TAe.append(Fr(sz) * Fr(A_).limit_denominator(1)); TBe.append(Fr(sz) * Fr(B_).limit_denominator(1))
    assert abs(float(TAe[-1]) - sz * A_) < 1e-9 and abs(float(TBe[-1]) - sz * B_) < 1e-9
rhs = [TAe[i] - CC * TBe[i] for i in range(NK)]
nV = len(VARS); NV = 1 + 2 * nV; col = lambda v, part: 1 + 2 * v + part
rows, cols_, vals = [], [], []
for kap, lst in var_rows.items():
    rr = cidx[kap]
    for (v, w, cj) in lst:
        rows.append(rr); cols_.append(col(v, 0)); vals.append(w)
        rows.append(NK + rr); cols_.append(col(v, 1)); vals.append(-w if cj else w)
Aeq = sps.csr_matrix((vals, (rows, cols_)), shape=(2 * NK, NV)); beq = np.concatenate([[float(x) for x in rhs], np.zeros(NK)])
SOLVER = os.environ.get("SOLVER", "scs")
def sidx(i, j_, n_):   # SCS: lower triangle column-major; Clarabel: upper triangle column-major (both scale off-diagonals by sqrt2)
    if SOLVER == "clarabel":
        if i > j_: i, j_ = j_, i
        return j_ * (j_ + 1) // 2 + i, (1.0 if i == j_ else 1 / math.sqrt(2))
    if i < j_: i, j_ = j_, i
    return j_ * n_ - j_ * (j_ - 1) // 2 + (i - j_), (1.0 if i == j_ else 1 / math.sqrt(2))
offs = []; o = 0
for L in cones: offs.append(o); o += (2 * L) * (2 * L + 1) // 2
prow, pcol, pval = [], [], []
entry_terms = []                                   # exact description of block entries
for (ci, i, j, terms) in psd_entries:
    L = cones[ci]; N2 = 2 * L
    acc = collections.defaultdict(complex)
    for (v, cf, cj) in terms:
        acc[col(v, 0)] += cf; acc[col(v, 1)] += (-1j if cj else 1j) * cf
    entry_terms.append((ci, i, j, dict(acc)))
    for c_, z in acc.items():
        ents = [(i, j, z.real), (L + i, L + j, z.real), (L + i, j, z.imag)]
        if i != j: ents.append((L + j, i, -z.imag))
        for (ii, jj, val) in ents:
            if abs(val) < 1e-14: continue
            k_, sc = sidx(ii, jj, N2)
            prow.append(offs[ci] + k_); pcol.append(c_); pval.append(-val * (math.sqrt(2) if ii != jj else 1.0))
for ci, L in enumerate(cones):                       # + s on diagonal entries:  cone = Y - s I
    for d_ in range(2 * L):
        k_, _ = sidx(d_, d_, 2 * L); prow.append(offs[ci] + k_); pcol.append(0); pval.append(1.0)
Apsd = sps.csr_matrix((pval, (prow, pcol)), shape=(o, NV))
A = sps.vstack([Aeq, Apsd]).tocsc(); bb = np.concatenate([beq, np.zeros(o)]); qv = np.zeros(NV); qv[0] = -1.0
t0 = time.time()
if SOLVER == "clarabel":
    import clarabel
    st = clarabel.DefaultSettings(); st.verbose = False; st.max_iter = 500
    st.tol_gap_abs = st.tol_gap_rel = st.tol_feas = st.tol_ktratio = 1e-14
    cl = [clarabel.ZeroConeT(2 * NK)] + [clarabel.PSDTriangleConeT(2 * L) for L in cones]
    so = clarabel.DefaultSolver(sps.csc_matrix((NV, NV)), qv, A, bb, cl, st).solve()
    x = np.array(so.x); s_val = float(x[0]); sol = {"info": {"status": str(so.status)}}
else:
    import scs
    sol = scs.SCS(dict(A=A, b=bb, c=qv), dict(z=2 * NK, s=[2 * L for L in cones]), eps_abs=1e-10, eps_rel=1e-10, max_iters=400000, verbose=False).solve()
    s_val = float(sol["x"][0]); x = sol["x"]
log(f"SCS at C = {CC}: status {sol['info']['status']}, margin s = {s_val:.3e} ({time.time() - t0:.0f}s)")
# ---- rounding and exact projection
R = 1 << int(os.environ.get("RBITS", "40"))
gam = [[Fr(int(round(x[col(v, 0)] * R)), R), Fr(int(round(x[col(v, 1)] * R)), R)] for v in range(nV)]
# group rows: each class with its conjugate; collect variable incidences
conjc = lambda mu: (mu[1], mu[0])
canon = G["canon"]
done = set(); maxres = Fr(0)
for kap, lst in var_rows.items():
    if kap in done: continue
    kb = canon(conjc(kap)); grp = [kap] + ([kb] if kb != kap and kb in var_rows else [])
    done |= set(grp)
    # Re equation for class kap: sum w Re(v) = rhs ; Im: sum (+-) w Im(v) = 0.  The conj class gives the same equations.
    re_terms = collections.defaultdict(Fr); im_terms = collections.defaultdict(Fr)
    for (v, w, cj) in var_rows[kap]:
        re_terms[v] += w; im_terms[v] += (-w if cj else w)
    target = rhs[cidx[kap]]
    res_re = sum(c_ * gam[v][0] for v, c_ in re_terms.items()) - target
    nrm = sum(c_ * c_ for c_ in re_terms.values())
    for v, c_ in re_terms.items(): gam[v][0] -= res_re * c_ / nrm
    res_im = sum(c_ * gam[v][1] for v, c_ in im_terms.items())
    nrm = sum(c_ * c_ for c_ in im_terms.values() if c_)
    if nrm:
        for v, c_ in im_terms.items(): gam[v][1] -= res_im * c_ / nrm
    maxres = max(maxres, abs(res_re), abs(res_im))
# verify all equations exactly
for kap, lst in var_rows.items():
    re_ = sum(w * gam[v][0] for (v, w, cj) in lst); im_ = sum((-w if cj else w) * gam[v][1] for (v, w, cj) in lst)
    assert re_ == rhs[cidx[kap]] and im_ == 0, "exact equation failed"
log(f"exact projection done (max pre-projection residual {float(maxres):.2e}); all {NK} coefficient equations hold exactly")
# ---- exact blocks and PSD proof
blocks = [[[None] * (2 * L) for _ in range(2 * L)] for L in cones]
for (ci, i, j, acc) in entry_terms:
    L = cones[ci]
    re_ = Fr(0); im_ = Fr(0)
    for c_, z in acc.items():
        v = (c_ - 1) // 2; part = (c_ - 1) % 2
        zr, zi = Fr(z.real).limit_denominator(1), Fr(z.imag).limit_denominator(1)
        g_ = gam[v][part]
        re_ += zr * g_; im_ += zi * g_
    for (ii, jj, val) in ((i, j, re_), (L + i, L + j, re_), (L + i, j, im_), (j, L + i, im_)):
        blocks[ci][ii][jj] = val; blocks[ci][jj][ii] = val
    if i != j:
        blocks[ci][L + j][i] = -im_; blocks[ci][i][L + j] = -im_
all_ok = True; worst = 1.0
for ci, Y in enumerate(blocks):
    n2 = len(Y)
    for a in range(n2):
        for b in range(n2):
            if Y[a][b] is None: Y[a][b] = Fr(0)
    Yf = np.array([[float(Y[a][b]) for b in range(n2)] for a in range(n2)])
    lam = np.linalg.eigvalsh(Yf)[0]
    if lam <= 0: all_ok = False; log(f"block {ci}: float lambda_min {lam:.3e} <= 0"); break
    delta = Fr(lam / 4).limit_denominator(1 << 50)
    Cf = np.linalg.cholesky(Yf - float(delta) * np.eye(n2)); SC = 1 << int(os.environ.get("SCBITS", "40"))
    Li = [[int(round(Cf[a, b] * SC)) for b in range(n2)] for a in range(n2)]
    E2 = Fr(0)
    for a in range(n2):
        for b in range(n2):
            llt = sum(Li[a][k] * Li[b][k] for k in range(min(a, b) + 1))
            e_ = Y[a][b] - (delta if a == b else 0) - Fr(llt, SC * SC); E2 += e_ * e_
    ratio = float(E2 / (delta * delta)); worst = min(worst, 1 - ratio)
    if not E2 < delta * delta: all_ok = False; log(f"block {ci}: residual too large ({ratio:.3e})"); break
log(f"CERTIFIED 64F >= {CC} = {float(CC):.10f} on the T code space (degree 8): {all_ok}   (c8 = {C8:.10f})")
json.dump(dict(C=str(CC), C_float=float(CC), certified=all_ok, scs_margin=s_val, blocks=len(cones), max_block=max(cones), n_classes=NK,
               n_vars=nV, c8=C8, gap=C8 - float(CC)), open(os.path.join(ROOT, "data", f"w33_f8_codespace_deg8_certificate_{str(CC).replace('/', '_')}.json"), "w"), indent=1)
