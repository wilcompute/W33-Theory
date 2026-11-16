"""Pass 12678: numerical facial reduction of the degree-8 SOS on the T code space AT C = c8 exactly.
At C = c8 every certificate must vanish on the minimisers, so each PSD block M (Fourier block (chi, xi) of shift-orbit reps O) has
the kernel vectors y_O = F_{O,xi}(psi*)/|stab_O|, F_{O,xi}(psi) = sum_s (-1)^{xi.s} m_{s.o}(psi), for every minimiser psi* (derived from
sum conj(m) G m = (1/N) sum_xi sum conj(F~) M F~).  Steps: (1) all minimisers of the effective three-qubit objective (random starts,
deduplicated up to phase); (2) kernel spans per block; (3) SDP at C = c8 (float) with M y = 0 imposed and margin s on the complement:
M - s P_perp >= 0, maximise s.  A margin clearly above solver noise means the SDP is strictly feasible on the face, the condition for
an exact (rounded-on-the-face) certificate at c8 over Q(cos 2pi/9).   usage: py -3 analysis/w33_f8_facial_reduction.py"""
import collections, contextlib, io, json, math, os, sys, time
import numpy as np
import scipy.sparse as sps
from scipy.optimize import minimize
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
_argv = sys.argv; sys.argv = ["x", "T", "4"]
src = open(os.path.join(HERE, "w33_f8_codespace_effective_sos.py"), encoding="utf-8").read()
G = {"__name__": "x", "__file__": os.path.join(HERE, "w33_f8_codespace_effective_sos.py")}
with contextlib.redirect_stdout(io.StringIO()):
    exec(src[: src.index("# ---------------- SCS")], G)
sys.argv = _argv
VARS, var_rows, cones, psd_entries, CONE_META, classes, cidx, NK, ceff, N, shiftm, C8 = (G[k] for k in
    ("VARS", "var_rows", "cones", "psd_entries", "CONE_META", "classes", "cidx", "NK", "ceff", "N", "shiftm", "C8"))
t00 = time.time(); log = lambda *a: print(*a, f"[{time.time() - t00:.0f}s]", flush=True)
# ---- (1) minimisers (BFGS, then Newton polish with an analytic gradient so the states are accurate to ~1e-13)
weights = G["weights"]
PW = []
for (x, z), wgt in weights.items():
    Pm = np.zeros((N, N), complex)
    for y in range(N): Pm[y, y ^ x] = (-1) ** (bin(z & (y ^ x)).count("1") & 1)
    PW.append((wgt, Pm))
def f_and_grad(v):
    psi = v[:N] + 1j * v[N:]; nn = np.vdot(psi, psi).real; f = 0.0; g = np.zeros(N, complex)
    for wgt, Pm in PW:
        Pp = Pm @ psi; a = np.vdot(psi, Pp); f += wgt * abs(a) ** 2
        g += wgt * (np.conj(a) * Pp + a * (Pm.conj().T @ psi))
    f /= nn * nn; g = g / (nn * nn) - 2 * f * psi / nn
    return f, np.concatenate([2 * g.real, 2 * g.imag])
def polish(v):
    for _ in range(8):
        f, g = f_and_grad(v); h = 1e-6; n2 = len(v); H = np.zeros((n2, n2))
        for i in range(n2):
            vp = v.copy(); vm = v.copy(); vp[i] += h; vm[i] -= h
            H[:, i] = (f_and_grad(vp)[1] - f_and_grad(vm)[1]) / (2 * h)
        E, V = np.linalg.eigh((H + H.T) / 2); keep = np.abs(E) > 1e-7 * np.abs(E).max()
        v = v - V[:, keep] @ ((V[:, keep].T @ g) / E[keep]); v = v / np.linalg.norm(v)
    return v
rng = np.random.default_rng(5)
mins = []
for trial in range(1500):
    r = minimize(lambda w: ceff(w[:N] + 1j * w[N:]), rng.standard_normal(2 * N), method="BFGS", options=dict(gtol=1e-11))
    if abs(r.fun - C8) > 1e-7: continue
    vv = polish(r.x / np.linalg.norm(r.x)); psi = vv[:N] + 1j * vv[N:]; psi /= np.linalg.norm(psi)
    if all(abs(abs(np.vdot(p, psi)) - 1) > 1e-6 for p in mins): mins.append(psi)
    if trial % 300 == 299: log(f"after {trial + 1} starts: {len(mins)} distinct minimisers")
log(f"distinct minimisers (up to phase): {len(mins)}; max gradient after polish {max(np.linalg.norm(f_and_grad(np.concatenate([p.real, p.imag]))[1]) for p in mins):.2e}")
# ---- (2) kernel vectors per block
def mono(m, psi):
    U, B = m; v = 1.0 + 0j
    for u in U: v *= psi[u]
    for b in B: v *= np.conj(psi[b])
    return v
pc = lambda n: bin(n).count("1") & 1
kernels = []
for ci, (kind, xi, mem, stab) in enumerate(CONE_META):
    Y = []
    for psi in mins:
        if kind == "even":
            y = np.array([sum((-1) ** pc(xi & s_) * mono(shiftm(o, s_), psi) for s_ in range(N)) / st for o, st in zip(mem, stab)])
        else:
            y = np.array([mono(o, psi) for o in mem])
        Y.append(y)
    Y = np.array(Y).T                     # L x M
    u, sv, vh = np.linalg.svd(Y, full_matrices=True)
    rank = int((sv > 1e-6 * max(sv.max(), 1e-300)).sum())
    kernels.append(u[:, :rank])           # orthonormal basis of the kernel span (complex L x rank)
kdims = [k.shape[1] for k in kernels]
log(f"kernel span dimensions: total {sum(kdims)} (complex) over {len(kdims)} blocks; histogram {dict(collections.Counter(kdims))}")
# ---- (3) SDP at C = c8 with M K = 0 and margin on the complement
nV = len(VARS); NV = 1 + 2 * nV; col = lambda v, part: 1 + 2 * v + part
rows, cols_, vals = [], [], []
TA = np.array([G["orbit_size"](mu) * G["tcoef"](mu)[0] for mu in classes]); TB = np.array([G["orbit_size"](mu) * G["tcoef"](mu)[1] for mu in classes])
for kap, lst in var_rows.items():
    rr = cidx[kap]
    for (v, w, cj) in lst:
        rows.append(rr); cols_.append(col(v, 0)); vals.append(w)
        rows.append(NK + rr); cols_.append(col(v, 1)); vals.append(-w if cj else w)
nrow = 2 * NK; beq = list(TA - C8 * TB) + [0.0] * NK
# M as linear map: entries per cone
entry = collections.defaultdict(dict)
for (ci, i, j, terms) in psd_entries:
    acc = collections.defaultdict(complex)
    for (v, cf, cj) in terms:
        acc[col(v, 0)] += cf; acc[col(v, 1)] += (-1j if cj else 1j) * cf
    entry[ci][(i, j)] = dict(acc)
def Mcoef(ci, i, j):   # coefficients of M[i,j] (Hermitian) as dict col -> complex
    if (i, j) in entry[ci]: return entry[ci][(i, j)]
    return {c_: np.conj(z) if (c_ - 1) % 2 == 0 else np.conj(z) for c_, z in entry[ci][(j, i)].items()} if False else \
           {c_: (z.conjugate() if (c_ - 1) % 2 == 0 else z.conjugate()) for c_, z in entry[ci][(j, i)].items()}
# kernel constraints: (M K)[i, r] = sum_j M[i,j] K[j,r] = 0  (real and imaginary parts)
for ci, K in enumerate(kernels):
    if K.shape[1] == 0: continue
    L = cones[ci]
    for i in range(L):
        for rr_ in range(K.shape[1]):
            accr = collections.defaultdict(float); acci = collections.defaultdict(float)
            for j in range(L):
                kz = K[j, rr_]
                if abs(kz) < 1e-14: continue
                for c_, z in Mcoef(ci, i, j).items():
                    # M[i,j] = sum_c z_c x_c with x_c real; contribution z * kz * x_c
                    zz = z * kz; accr[c_] += zz.real; acci[c_] += zz.imag
            for c_, v_ in accr.items():
                if abs(v_) > 1e-13: rows.append(nrow); cols_.append(c_); vals.append(v_)
            nrow += 1; beq.append(0.0)
            for c_, v_ in acci.items():
                if abs(v_) > 1e-13: rows.append(nrow); cols_.append(c_); vals.append(v_)
            nrow += 1; beq.append(0.0)
Aeq = sps.csr_matrix((vals, (rows, cols_)), shape=(nrow, NV))
def sidx(i, j_, n_):
    if i < j_: i, j_ = j_, i
    return j_ * n_ - j_ * (j_ - 1) // 2 + (i - j_), (1.0 if i == j_ else 1 / math.sqrt(2))
offs = []; o = 0
for L in cones: offs.append(o); o += (2 * L) * (2 * L + 1) // 2
prow, pcol, pval = [], [], []
for (ci, i, j, terms) in psd_entries:
    L = cones[ci]; N2 = 2 * L
    for c_, z in entry[ci][(i, j)].items():
        ents = [(i, j, z.real), (L + i, L + j, z.real), (L + i, j, z.imag)]
        if i != j: ents.append((L + j, i, -z.imag))
        for (ii, jj, val) in ents:
            if abs(val) < 1e-14: continue
            k_, sc = sidx(ii, jj, N2); prow.append(offs[ci] + k_); pcol.append(c_); pval.append(-val * (math.sqrt(2) if ii != jj else 1.0))
for ci, K in enumerate(kernels):               # + s * P_perp (real embedding)
    L = cones[ci]; P = np.eye(L) - K @ K.conj().T
    Pr = np.block([[P.real, -P.imag], [P.imag, P.real]])
    for ii in range(2 * L):
        for jj in range(ii + 1):
            v_ = Pr[ii, jj]
            if abs(v_) < 1e-13: continue
            k_, sc = sidx(ii, jj, 2 * L); prow.append(offs[ci] + k_); pcol.append(0); pval.append(v_ * (math.sqrt(2) if ii != jj else 1.0))
Apsd = sps.csr_matrix((pval, (prow, pcol)), shape=(o, NV))
A = sps.vstack([Aeq, Apsd]).tocsc(); bb = np.concatenate([beq, np.zeros(o)]); qv = np.zeros(NV); qv[0] = -1.0
log(f"face SDP: {NV} variables, {nrow} equalities ({nrow - 2 * NK} kernel), nnz {A.nnz}")
import scs
sol = scs.SCS(dict(A=A, b=bb, c=qv), dict(z=nrow, s=[2 * L for L in cones]), eps_abs=1e-9, eps_rel=1e-9, max_iters=200000, verbose=False).solve()
s_val = float(sol["x"][0])
log(f"AT C = c8 exactly: SCS status {sol['info']['status']}, margin on the complement of the face s = {s_val:.4e}")
res = dict(n_minimisers=len(mins), kernel_total=sum(kdims), kernel_hist={str(k): v for k, v in collections.Counter(kdims).items()},
           status=sol["info"]["status"], margin_at_c8=s_val, strictly_feasible_on_face=s_val > 1e-6)
json.dump(res, open(os.path.join(ROOT, "data", "w33_f8_facial_reduction.json"), "w"), indent=1)
