"""Pass 12679: (a) logical stabiliser fidelity of the 128 F_8 code-space minimisers (effective three-qubit model; code-space Cliffords
preserve stabiliser states, so the value is basis-independent): max over the 1080 three-qubit stabiliser states of |<s|psi>|^2,
identified in Q(cos 2pi/9) and compared with the qutrit E6(a1) eigenstate value (2 + 2cos 2pi/9)/9 (Pass 12677).
(b) code parameters [[6, k, d]] of the stabiliser codes T (rank 3) and the order-4 types A, B, C, in the six physical qubits of the
regulus (Pauli label bits): d = minimum weight of an element of S^perp \ S.
usage: py -3 analysis/w33_f8_minimiser_magic_and_codes.py"""
import collections, contextlib, io, itertools, json, os, sys
import numpy as np
import mpmath as mp
from scipy.optimize import minimize
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
_argv = sys.argv; sys.argv = ["x", "T", "3"]
src = open(os.path.join(HERE, "w33_f8_codespace_effective_sos.py"), encoding="utf-8").read()
G = {"__name__": "x", "__file__": os.path.join(HERE, "w33_f8_codespace_effective_sos.py")}
with contextlib.redirect_stdout(io.StringIO()):
    exec(src[: src.index("rng = np.random.default_rng(1)")], G)
sys.argv = _argv
ceff, N, nq, C8, comm, covered = (G[k] for k in ("ceff", "N", "nq", "C8", "comm", "covered"))
pc = lambda n: bin(n).count("1") & 1
# ---- (a) minimisers and three-qubit stabiliser states
weights = G["weights"]
PW = []
for (x, z), wgt in weights.items():
    Pm = np.zeros((N, N), complex)
    for y in range(N): Pm[y, y ^ x] = (-1) ** (bin(z & (y ^ x)).count("1") & 1)
    PW.append((wgt, Pm))
def f_and_grad(v):
    psi = v[:N] + 1j * v[N:]; nn = np.vdot(psi, psi).real; f = 0.0; g = np.zeros(N, complex)
    for wgt, Pm in PW:
        Pp = Pm @ psi; a = np.vdot(psi, Pp); f += wgt * abs(a) ** 2; g += wgt * (np.conj(a) * Pp + a * (Pm.conj().T @ psi))
    f /= nn * nn; g = g / (nn * nn) - 2 * f * psi / nn
    return f, np.concatenate([2 * g.real, 2 * g.imag])
def polish(v):
    for _ in range(8):
        f, g = f_and_grad(v); h = 1e-6; n2 = len(v); H = np.zeros((n2, n2))
        for i in range(n2):
            vp = v.copy(); vm = v.copy(); vp[i] += h; vm[i] -= h; H[:, i] = (f_and_grad(vp)[1] - f_and_grad(vm)[1]) / (2 * h)
        E, V = np.linalg.eigh((H + H.T) / 2); keep = np.abs(E) > 1e-7 * np.abs(E).max()
        v = v - V[:, keep] @ ((V[:, keep].T @ g) / E[keep]); v = v / np.linalg.norm(v)
    return v
rng = np.random.default_rng(9); mins = []
for _ in range(500):
    r = minimize(lambda w: ceff(w[:N] + 1j * w[N:]), rng.standard_normal(2 * N), method="BFGS", options=dict(gtol=1e-12))
    if abs(r.fun - C8) < 1e-8:
        vv = polish(r.x / np.linalg.norm(r.x)); psi = vv[:N] + 1j * vv[N:]; psi /= np.linalg.norm(psi)
        if all(abs(abs(np.vdot(p, psi)) - 1) > 1e-6 for p in mins): mins.append(psi)
def pauli(x, z):
    M = np.zeros((N, N), complex)
    for y in range(N): M[y, y ^ x] = (-1) ** pc(z & (y ^ x))
    return M
sform = lambda p, r: pc(p[0] & r[1]) ^ pc(p[1] & r[0])
labels = [(x, z) for x in range(N) for z in range(N) if (x, z) != (0, 0)]
lags = set()
for gens in itertools.combinations(labels, nq):
    if any(sform(a, b) for a, b in itertools.combinations(gens, 2)): continue
    span = {(0, 0)}
    for g in gens: span |= {(s[0] ^ g[0], s[1] ^ g[1]) for s in span}
    if len(span) == N: lags.add(frozenset(span))
assert len(lags) == 135
stabs = []
for Lg in lags:
    gens = []; span = {(0, 0)}
    for p in sorted(Lg):
        if p not in span: gens.append(p); span |= {(s[0] ^ p[0], s[1] ^ p[1]) for s in span}
    Mx = sum((0.37 + 0.11 * i) * (pauli(*g) if pc(g[0] & g[1]) == 0 else 1j * pauli(*g)) for i, g in enumerate(gens))
    _, Ub = np.linalg.eigh((Mx + Mx.conj().T) / 2)
    stabs.extend(Ub[:, i] for i in range(N))
S = np.array(stabs); assert len(stabs) == 1080
fids = collections.Counter(round(float(np.max(np.abs(S.conj() @ psi) ** 2)), 13) for psi in mins)
mp.mp.dps = 30; gam = 2 * mp.cos(2 * mp.pi / 9)
s3 = mp.sqrt(3)
fid_rows = [dict(value=k, count=v, pslq_Qg=str(mp.pslq([mp.mpf(k), 1, gam, gam * gam], maxcoeff=3000, tol=mp.mpf(10) ** -12)),
                 pslq_Qg_sqrt3=str(mp.pslq([mp.mpf(k), 1, gam, gam * gam, s3, s3 * gam, s3 * gam * gam], maxcoeff=3000, tol=mp.mpf(10) ** -12)),
                 findpoly=str(mp.findpoly(mp.mpf(k), 6, maxcoeff=10 ** 5, tol=mp.mpf(10) ** -12))) for k, v in sorted(fids.items())]
print("minimisers:", len(mins), "| logical stabiliser fidelities:", fid_rows, "| qutrit E6(a1) value:", float((2 + gam) / 9), flush=True)
# ---- (b) code parameters in the six physical qubits
wt6 = lambda k: sum(1 for i in range(6) if ((k[0] >> i) & 1) or ((k[1] >> i) & 1))
def code_params(gens):
    S_ = [(0, 0)]
    for g in gens: S_ = S_ + [(e[0] ^ g[0], e[1] ^ g[1]) for e in S_]
    Sset = set(S_)
    perp = [(u, v) for u in range(64) for v in range(64) if (u, v) != (0, 0) and all(comm((u, v), s) for s in S_[1:])]
    logical = [k for k in perp if k not in Sset]
    d = min(wt6(k) for k in logical)
    return dict(n=6, k=6 - len(gens), d=d, stabiliser_weights=sorted(wt6(s) for s in S_[1:]),
                n_logical_min_weight=sum(1 for k in logical if wt6(k) == d))
codes = {"T": [(12, 53), (53, 33), (1, 6)], "A": [(12, 53), (53, 33)], "B": [(12, 53), (52, 39)], "C": [(53, 33), (1, 6)]}
cp_ = {name: code_params(g) for name, g in codes.items()}
for name, r in cp_.items(): print(f"code {name}: [[{r['n']},{r['k']},{r['d']}]] stabiliser weights {r['stabiliser_weights']}", flush=True)
json.dump(dict(n_minimisers=len(mins), logical_stabiliser_fidelity=fid_rows, qutrit_E6a1_fidelity=float((2 + gam) / 9), codes=cp_),
          open(os.path.join(ROOT, "data", "w33_f8_minimiser_magic_and_codes.json"), "w"), indent=1)
# ---- (c) 30-digit confirmation of the logical stabiliser fidelity: mp Newton on one minimiser, exact stabiliser projector
mp.mp.dps = 40
psi0 = mins[0]; k_best = int(np.argmax(np.abs(S.conj() @ psi0) ** 2)); Lbest = list(lags)[k_best // N]
PWm = [(wgt, [[mp.mpf(int(round(Pm[i, j].real))) for j in range(N)] for i in range(N)]) for wgt, Pm in PW]
def mp_fg(x):
    psi = [mp.mpc(x[i], x[N + i]) for i in range(N)]; nn = mp.fsum(abs(z) ** 2 for z in psi); f = mp.mpf(0); g = [mp.mpc(0)] * N
    for wgt, Pm in PWm:
        Pp = [mp.fsum(Pm[i][j] * psi[j] for j in range(N)) for i in range(N)]
        a = mp.fsum(mp.conj(psi[i]) * Pp[i] for i in range(N)); f += wgt * abs(a) ** 2
        PHp = [mp.fsum(Pm[j][i] * psi[j] for j in range(N)) for i in range(N)]
        g = [g[i] + wgt * (mp.conj(a) * Pp[i] + a * PHp[i]) for i in range(N)]
    f /= nn * nn; g = [gi / (nn * nn) - 2 * f * psi[i] / nn for i, gi in enumerate(g)]
    return f, [2 * mp.re(z) for z in g] + [2 * mp.im(z) for z in g]
x = [mp.mpf(v) for v in np.concatenate([psi0.real, psi0.imag])]
for it in range(5):
    f, g = mp_fg(x); h = mp.mpf(10) ** -18; n2 = 2 * N; H = mp.matrix(n2, n2)
    for i in range(n2):
        xp = list(x); xm = list(x); xp[i] += h; xm[i] -= h; gp = mp_fg(xp)[1]; gm = mp_fg(xm)[1]
        for j in range(n2): H[j, i] = (gp[j] - gm[j]) / (2 * h)
    E, V = mp.eigsy((H + H.T) / 2); tol = mp.mpf(10) ** -10 * max(abs(e) for e in E); step = [mp.mpf(0)] * n2
    for kk in range(n2):
        if abs(E[kk]) > tol:
            co = mp.fsum(V[j, kk] * g[j] for j in range(n2)) / E[kk]
            for j in range(n2): step[j] += co * V[j, kk]
    x = [a - b for a, b in zip(x, step)]
psi = [mp.mpc(x[i], x[N + i]) for i in range(N)]; nn = mp.sqrt(mp.fsum(abs(z) ** 2 for z in psi)); psi = [z / nn for z in psi]
# exact projector of the best stabiliser state: P = prod over generators (I + s g)/2 with the sign s fixed by the double state
s_vec = S[k_best]; gens = []; span = {(0, 0)}
for p in sorted(Lbest):
    if p not in span: gens.append(p); span |= {(s_[0] ^ p[0], s_[1] ^ p[1]) for s_ in span}
fid = mp.mpf(1)
proj = [[mp.mpf(1) if i == j else mp.mpf(0) for j in range(N)] for i in range(N)]
for g_ in gens:
    Pg = pauli(*g_); herm = 1 if pc(g_[0] & g_[1]) == 0 else 1j; Ph = herm * Pg
    sgn = int(round(float(np.real(np.vdot(s_vec, Ph @ s_vec)))))
    Pm_ = [[mp.mpc((Ph[i, j]).real, (Ph[i, j]).imag) for j in range(N)] for i in range(N)]
    proj = [[mp.fsum(proj[i][k] * ((1 if k == j else 0) + sgn * Pm_[k][j]) / 2 for k in range(N)) for j in range(N)] for i in range(N)]
F_hp = mp.re(mp.fsum(mp.conj(psi[i]) * mp.fsum(proj[i][j] * psi[j] for j in range(N)) for i in range(N)))
closed = (3 + mp.sqrt(3)) * (gam + gam * gam) / 36
print("stabiliser fidelity at 40 digits:", mp.nstr(F_hp, 32), "| (3 + sqrt3)(g + g^2)/36 =", mp.nstr(closed, 32), "| diff", mp.nstr(F_hp - closed, 3), flush=True)
out = json.load(open(os.path.join(ROOT, "data", "w33_f8_minimiser_magic_and_codes.json")))
out.update(fidelity_40_digits=mp.nstr(F_hp, 35), closed_form="(3 + sqrt3)(g + g^2)/36, g = 2cos(2pi/9)", closed_form_diff=mp.nstr(F_hp - closed, 3))
json.dump(out, open(os.path.join(ROOT, "data", "w33_f8_minimiser_magic_and_codes.json"), "w"), indent=1)
