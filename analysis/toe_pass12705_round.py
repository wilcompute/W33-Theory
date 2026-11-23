"""Pass 12705 (Claude track): five follow-ups to Pass 12704.
 (1) Real E6: e6 is computed as the 78-dimensional derivation algebra of the cubic norm N = det A + det B + det C - tr(ABC) on
     27 = (3,3b,1)+(1,3,3b)+(3b,1,3).  SM embedding, the 17 SM-invariant 27b.27 mass operators = 1 + 5 (78) + 11 (650), the two 650 cubic
     invariants (tr X^3 and d dbar XXX) and the 78.78.650, 650.650.78 couplings.  F-flat vacua of (a) a 650 alone and (b) 650 + 78 on
     the SM-singlet slice (symmetric criticality); for each: unbroken dimension and whether 27b (M + eta X + eta' A) 27 can leave exactly
     Q + U light with every other block heavy.
 (2) SO(10) 45 + 210 vacuum of Pass 12704: full 255-field gradient (checks symmetric criticality) and superpotential mass matrix; zero
     modes against 45 - dim(unbroken).
 (3) MFV-type tree splitting for A's N: M = M0 [1 + c1 Re(h^dag h) + c2 Re(h^dag Ye Ye^dag h)] at O(1) c_i (lepton MFV,
     Cirigliano-Isidori-Porretti hep-ph/0607068; Branco et al. hep-ph/0609067) plus radiative running.
 (4) Dark-graviton bound verified verbatim from 2307.11048 (eq. 4.14): 30 um > l5_eff > (2/gamma)(delta/0.5)(lambda/0.1)^(2/3) 10 um.
 (5) Cross-track summary addendum (markdown, no computation).
usage: py -3 analysis/toe_pass12705_round.py"""
import itertools, json, math, os
import numpy as np
from scipy.optimize import least_squares

HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
res = {}
K = 1 / (16 * math.pi ** 2)

# ======================================================================= (1) E6 from the cubic norm
d = np.zeros((27, 27, 27))


def addterm(c, i, j, k):
    ps = set(itertools.permutations((i, j, k)))
    for q in ps: d[q] += c / len(ps)


for base in (0, 9, 18):
    for perm in itertools.permutations(range(3)):
        addterm(round(np.linalg.det(np.eye(3)[list(perm)])), base + perm[0], base + 3 + perm[1], base + 6 + perm[2])
for i, j, k in itertools.product(range(3), repeat=3):
    addterm(-1, 3 * i + j, 9 + 3 * j + k, 18 + 3 * k + i)
xt = np.random.default_rng(0).normal(size=27); At, Bt, Ct = xt[:9].reshape(3, 3), xt[9:18].reshape(3, 3), xt[18:].reshape(3, 3)
assert abs(np.einsum("ijk,i,j,k", d, xt, xt, xt) - (np.linalg.det(At) + np.linalg.det(Bt) + np.linalg.det(Ct) - np.trace(At @ Bt @ Ct))) < 1e-9
trip = [(i, j, k) for i in range(27) for j in range(i, 27) for k in range(j, 27)]
rows = np.zeros((len(trip), 729))
for r, (i, j, k) in enumerate(trip):
    for l in range(27):
        rows[r, l * 27 + i] += d[l, j, k]; rows[r, l * 27 + j] += d[i, l, k]; rows[r, l * 27 + k] += d[i, j, l]
ev, evec = np.linalg.eigh(rows.T @ rows)
null = evec[:, ev < 1e-9 * ev.max()].T
assert null.shape[0] == 78
gens = [v.reshape(27, 27).T for v in null]
print("(1) e6 = derivations of the cubic norm: dimension 78")


def op(fA=None, fB=None, fC=None):
    M = np.zeros((27, 27), complex)
    for k in range(27):
        e = np.zeros(27); e[k] = 1; A, B, C = e[:9].reshape(3, 3), e[9:18].reshape(3, 3), e[18:].reshape(3, 3)
        M[:, k] = np.concatenate([np.ravel(fA(A) if fA else 0 * A), np.ravel(fB(B) if fB else 0 * B), np.ravel(fC(C) if fC else 0 * C)])
    return M


def gellmann():
    L = []
    for i in range(3):
        for j in range(i + 1, 3):
            m = np.zeros((3, 3), complex); m[i, j] = m[j, i] = 1; L.append(m)
            m = np.zeros((3, 3), complex); m[i, j] = -1j; m[j, i] = 1j; L.append(m)
    return L + [np.diag([1, -1, 0]).astype(complex), np.diag([1, 1, -2]).astype(complex) / math.sqrt(3)]


span = np.array([g.ravel() for g in gens])
in_e6 = lambda M: np.linalg.norm(span.T @ np.linalg.lstsq(span.T.astype(complex), M.ravel(), rcond=None)[0] - M.ravel()) < 1e-8
Gc = [op(fA=lambda A, g=g: g @ A, fC=lambda C, g=g: -C @ g) for g in gellmann()]
GL = [op(fA=lambda A, g=g: -A @ g, fB=lambda B, g=g: g @ B) for g in gellmann()]
GR = [op(fB=lambda B, g=g: -B @ g, fC=lambda C, g=g: g @ C) for g in gellmann()]
assert all(in_e6(g) for g in Gc + GL + GR)
D8 = np.diag([1, 1, -2]) / 6; D3 = np.diag([1, -1, 0]) / 2
Yop = -op(fA=lambda A: -A @ D8, fB=lambda B: D8 @ B) - op(fB=lambda B: -B @ D3, fC=lambda C: D3 @ C) - op(fB=lambda B: -B @ D8, fC=lambda C: D8 @ C)
assert in_e6(Yop)
Y = np.real(np.diag(Yop))
SMg = Gc + [GL[i] for i in (0, 1, 6)] + [Yop]


def nullsp(R, tol=1e-9):
    u, s, vh = np.linalg.svd(R); return vh[int(np.sum(s > tol)):].conj()


def herm_basis(V, tol=1e-9):
    u, s, vh = np.linalg.svd(np.hstack([V.real, V.imag]), full_matrices=False)
    return [(b[:729] + 1j * b[729:]).reshape(27, 27) for b in vh[:int(np.sum(s > tol))]]


comm = [v.reshape(27, 27) for v in nullsp(np.vstack([np.kron(g, np.eye(27)) - np.kron(np.eye(27), g.T) for g in SMg]))]
Hc = herm_basis(np.array([h.ravel() for X in comm for h in ((X + X.conj().T) / 2, (X - X.conj().T) / 2j)]))
Eb = herm_basis(np.array([e.ravel() for g in gens for e in ((g + g.T) / 2, 1j * (g - g.T) / 2)]))
M_ = np.hstack([np.array([h.ravel() for h in Hc]).T, -np.array([e.ravel() for e in Eb]).T])
nA = nullsp(np.vstack([M_.real, M_.imag])).real
A7 = herm_basis(np.array([sum(v[i] * Hc[i] for i in range(len(Hc))).ravel() for v in nA]))
cons = np.array([[np.trace(p.conj().T @ h).real for h in Hc] for p in Eb + [np.eye(27)]])
X6 = herm_basis(np.array([sum(v[i] * Hc[i] for i in range(len(Hc))).ravel() for v in nullsp(cons).real]))
assert (len(Hc), len(Eb), len(A7), len(X6)) == (17, 78, 5, 11)
print(f"(1) SM-invariant 27b.27 operators: {len(Hc)} = 1 + {len(A7)} (78) + {len(X6)} (650)")
n6, n7 = 11, 5


def sym3(Ls, f):
    n = len(Ls); T = np.zeros((n, n, n))
    for c in itertools.combinations_with_replacement(range(n), 3):
        ps = set(itertools.permutations(c)); val = sum(f(*[Ls[q] for q in p]) for p in ps) / len(ps)
        for p in ps: T[p] = val
    return T


trf = lambda a, b, c: np.real(np.trace(a @ b @ c))


def jf(a, b, c):
    t = np.einsum("def,ad->aef", d, a); t = np.einsum("aef,be->abf", t, b); t = np.einsum("abf,cf->abc", t, c)
    return np.real(np.einsum("abc,abc", d, t))


Tall = sym3(X6 + A7, trf); T3 = Tall[:n6, :n6, :n6]; J3 = sym3(X6, jf); AAX = Tall[n6:, n6:, :n6]; XXA = Tall[:n6, :n6, n6:]
assert abs(Tall[n6:, n6:, n6:]).max() < 1e-10                                   # tr A^3 = 0: no cubic Casimir for E6
assert np.linalg.matrix_rank(np.array([T3.ravel(), J3.ravel()]), tol=1e-8) == 2  # two independent 650^3 invariants
coords = lambda blk, cond: [k for k in range(27) if k // 9 == blk and cond((k % 9) // 3, k % 3, round(Y[k] * 6))]
BL = {"Q": coords(0, lambda i, j, y: i == 0 and j == 0), "D": coords(0, lambda i, j, y: i == 0 and j == 2),
      "u^c": coords(2, lambda i, j, y: j == 0 and y == -4), "d^c/D^c": coords(2, lambda i, j, y: j == 0 and y == 2),
      "L/Hd": coords(1, lambda i, j, y: i == 0 and y == -3), "Hu": coords(1, lambda i, j, y: i == 0 and y == 3),
      "e^c": coords(1, lambda i, j, y: i == 2 and y == 6), "nu^c/S": coords(1, lambda i, j, y: i == 2 and y == 0)}
assert [len(v) for v in BL.values()] == [1, 1, 1, 2, 2, 1, 1, 2]


def grad(z, p):
    x, y = z[:n6], z[n6:]; m1, l1, l2, m2, k1, k2 = p
    gx = 2 * m1 * x + 3 * l1 * np.einsum("ijk,j,k", T3, x, x) + 3 * l2 * np.einsum("ijk,j,k", J3, x, x) + k1 * np.einsum("ijk,i,j", AAX, y, y) \
        + 2 * k2 * np.einsum("ijk,j,k", XXA, x, y)
    gy = 2 * m2 * y + 2 * k1 * np.einsum("ijk,j,k", AAX, y, x) + k2 * np.einsum("ijk,i,j", XXA, x, x)
    return np.concatenate([gx, gy])


opx = lambda x: sum(x[i] * X6[i] for i in range(n6)); opa = lambda y: sum(y[i] * A7[i] for i in range(n7))
blocks = lambda O: {k: O[np.ix_(v, v)] for k, v in BL.items()}


def qu_test(x, y, use78):
    BX, BA = blocks(opx(x)), blocks(opa(y))
    if not use78:
        if abs(BX["Q"][0, 0] - BX["u^c"][0, 0]) > 1e-7: return None
        mats = {k: -BX["Q"][0, 0] * np.eye(len(v)) + BX[k] for k, v in BL.items()}
    else:
        Am = np.array([[1, BA["Q"][0, 0]], [1, BA["u^c"][0, 0]]])
        if abs(np.linalg.det(Am)) < 1e-9: return None
        M, e = np.linalg.solve(Am, -np.array([BX["Q"][0, 0], BX["u^c"][0, 0]]))
        mats = {k: M * np.eye(len(v)) + BX[k] + e * BA[k] for k, v in BL.items()}
    sv = {k: float(np.linalg.svd(m, compute_uv=False).min()) for k, m in mats.items()}
    sc = max(sv.values())
    return sv if all(v > 1e-3 * sc for k, v in sv.items() if k not in ("Q", "u^c")) else None


HgB = np.array([e.ravel() for e in Eb])


def unbroken(x, y):
    Ox, Oa = opx(x), opa(y)
    R = np.array([np.concatenate([(h @ Ox - Ox @ h).ravel(), (h @ Oa - Oa @ h).ravel()]) for h in Eb]).T
    s = np.linalg.svd(np.vstack([R.real, R.imag]), compute_uv=False); return 78 - int(np.sum(s > 1e-7 * s.max()))


rng = np.random.default_rng(12705); e6res = {}
for system in ("650 alone", "650+78"):
    for trial in range(3):
        p = [1.0, rng.uniform(.5, 2), rng.uniform(-2, 2)] + ([0.0, 0.0, 0.0] if system == "650 alone" else [rng.uniform(.5, 2), rng.uniform(-2, 2), rng.uniform(-2, 2)])
        nv = n6 if system == "650 alone" else n6 + n7
        f = (lambda z: grad(np.concatenate([z, np.zeros(n7)]), p)[:n6]) if nv == n6 else (lambda z: grad(z, p))
        sols = []
        for _ in range(300):
            r = least_squares(f, rng.normal(size=nv) * rng.uniform(0.2, 3), xtol=1e-15, ftol=1e-15, gtol=1e-15)
            if np.linalg.norm(r.fun) < 1e-10 and np.linalg.norm(r.x) > 1e-6:
                z = np.concatenate([r.x, np.zeros(n7)]) if nv == n6 else r.x
                key = tuple(np.round(sorted(np.linalg.eigvalsh(opx(z[:n6]) + opa(z[n6:]))), 5))
                if key not in [q[0] for q in sols]: sols.append((key, z))
        dims, okd = [], []
        for _, z in sols:
            dm = unbroken(z[:n6], z[n6:]); dims.append(dm)
            if qu_test(z[:n6], z[n6:], system == "650+78") is not None: okd.append(dm)
        e6res[f"{system}|{trial}"] = dict(params=p, n_vacua=len(sols), unbroken_dims=sorted(set(dims)), n_QU_only=len(okd), QU_unbroken_dims=sorted(okd))
        print(f"(1) {system} {np.round(p, 2)}: {len(sols)} vacua, unbroken dims {sorted(set(dims))}; Q+U only light: {len(okd)} (unbroken dims {sorted(okd)})")
assert all(v["n_QU_only"] == 0 for k, v in e6res.items() if k.startswith("650 alone"))
assert all(v["n_QU_only"] > 0 and max(v["QU_unbroken_dims"]) <= 16 for k, v in e6res.items() if k.startswith("650+78"))
res["e6_650_78"] = dict(vacua=e6res, dims={"comm": 17, "78": 5, "650": 11},
                        note="Regular subgroups seen as unbroken dims 46 (SO(10)xU(1)), 38 (SU(6)xSU(2)), 24 (SU(3)^3), 22 (SU(3)xG2), cf. Babu-Bajc-Susic. "
                             "650 alone: no vacuum leaves exactly Q+U light (needs X_Q = X_U at an isolated point). 650+78: generic SM x U(1) (dim 13) or "
                             "SM x U(1)^2 (dim 14) vacua do (one dim-16 case), at two tuned couplings (M and eta_78).")

# ======================================================================= (2) SO(10) 45+210 vacuum: full gradient and mass matrix
d12704 = json.load(open(os.path.join(ROOT, "data", "toe_pass12704_round.json"), encoding="utf-8"))
v0 = next(r for r in d12704["so10_light_QU"]["vacua_45_210"] if r["QU_only"])
F4 = list(itertools.combinations(range(10), 4)); F2 = list(itertools.combinations(range(10), 2))


def full_form(ind):
    T = np.zeros((10,) * len(ind))
    for perm in itertools.permutations(range(len(ind))):
        T[tuple(ind[q] for q in perm)] = round(np.linalg.det(np.eye(len(ind))[list(perm)]))
    return T


E = np.array([full_form(f).reshape(100, 100) for f in F4]); Fv = np.array([full_form(f).reshape(100) for f in F2])
J6 = [(0, 1), (2, 3), (4, 5)]; S4 = [(6, 7), (8, 9)]
comp4 = {f: 0.0 for f in F4}; comp2 = {f: 0.0 for f in F2}
vv = v0["vev"]
comp4[(6, 7, 8, 9)] += vv["p"]
for c1, c2 in itertools.combinations(J6, 2): comp4[c1 + c2] += vv["a"]
for c in J6:
    for s_ in S4: comp4[c + s_] += vv["w"]
for c in J6: comp2[c] += vv["A"]
for s_ in S4: comp2[s_] += vv["B"]
x0 = np.array([comp4[f] for f in F4]); y0 = np.array([comp2[f] for f in F2])
Phi = np.tensordot(x0, E, 1); avec = y0 @ Fv
m1, m2, lam, kap = (float(eval(s)) if "/" not in s else float(eval(s)) for s in v0["params"])
gx = m2 * 2 * np.einsum("kij,ij->k", E, Phi) + lam * 3 * np.einsum("kij,ji->k", E, Phi @ Phi) + kap * np.einsum("i,kij,j->k", avec, E, avec)
gy = m1 * 2 * Fv @ avec + kap * Fv @ ((Phi + Phi.T) @ avec)
gnorm = float(np.linalg.norm(np.concatenate([gx, gy])) / np.linalg.norm(np.concatenate([x0, y0])))
assert gnorm < 1e-10, gnorm
EP = E @ Phi
Hxx = m2 * 2 * np.einsum("kij,lij->kl", E, E) + lam * 3 * (np.einsum("kij,lji->kl", E, EP) + np.einsum("lij,kji->kl", E, EP))
Hyy = m1 * 2 * Fv @ Fv.T + kap * Fv @ (Phi + Phi.T) @ Fv.T
Hxy = kap * np.einsum("kij,j,li->kl", E + E.transpose(0, 2, 1), avec, Fv)
H = np.block([[Hxx, Hxy], [Hxy.T, Hyy]])
Kn = np.concatenate([np.full(210, 24.0), np.full(45, 2.0)])
Hp = H / np.sqrt(np.outer(Kn, Kn)); evh = np.linalg.eigvalsh(Hp); aev = np.abs(evh)
nzero = int(np.sum(aev < 1e-8 * aev.max()))
gen = [full_form(f) for f in F2]


def act2(Xg, A): return Xg @ A - A @ Xg


def act4(Xg, T): return (np.einsum("ae,ebcd->abcd", Xg, T) + np.einsum("be,aecd->abcd", Xg, T) + np.einsum("ce,abed->abcd", Xg, T) + np.einsum("de,abce->abcd", Xg, T))


A0 = np.tensordot(y0, np.array([full_form(f) for f in F2]), 1); P0 = np.tensordot(x0, np.array([full_form(f) for f in F4]), 1)
Rm = np.array([np.concatenate([act4(g, P0).ravel(), act2(g, A0).ravel()]) for g in gen])
unb = 45 - np.linalg.matrix_rank(Rm, tol=1e-8)
print(f"(2) SO(10) vacuum {vv}: full 255-field gradient |dW|/|v| = {gnorm:.1e} (symmetric criticality holds)")
Ks = np.sqrt(Kn)


def coord_action(Gm):
    Mc = np.zeros((255, 255))
    for k, f in enumerate(F4):
        T = act4(Gm, full_form(f)); Mc[:210, k] = [T[q] for q in F4]
    for k, f in enumerate(F2):
        A = full_form(f); T = Gm @ A - A @ Gm; Mc[210:, 210 + k] = [T[q] for q in F2]
    return Mc


Rk = []
for k in range(5):
    R_ = np.zeros((10, 10)); R_[2 * k, 2 * k + 1] = -1; R_[2 * k + 1, 2 * k] = 1; Rk.append(np.diag(Ks) @ (1j * coord_action(R_)) @ np.diag(1 / Ks))


def analyse(r):
    vv_, (pm1, pm2, plam, pkap) = r["vev"], [float(eval(s)) for s in r["params"]]
    c4 = {f: 0.0 for f in F4}; c2 = {f: 0.0 for f in F2}
    c4[(6, 7, 8, 9)] += vv_["p"]
    for c1_, c2_ in itertools.combinations(J6, 2): c4[c1_ + c2_] += vv_["a"]
    for c in J6:
        for s_ in S4: c4[c + s_] += vv_["w"]
    for c in J6: c2[c] += vv_["A"]
    for s_ in S4: c2[s_] += vv_["B"]
    xv = np.array([c4[f] for f in F4]); yv = np.array([c2[f] for f in F2]); Ph = np.tensordot(xv, E, 1); av = yv @ Fv; EPh = E @ Ph
    Hm = np.block([[pm2 * 2 * np.einsum("kij,lij->kl", E, E) + plam * 3 * (np.einsum("kij,lji->kl", E, EPh) + np.einsum("lij,kji->kl", E, EPh)),
                    pkap * np.einsum("kij,j,li->kl", E + E.transpose(0, 2, 1), av, Fv)],
                   [pkap * np.einsum("kij,j,li->kl", E + E.transpose(0, 2, 1), av, Fv).T, pm1 * 2 * Fv @ Fv.T + pkap * Fv @ (Ph + Ph.T) @ Fv.T]]) / np.outer(Ks, Ks)
    ev_, Uv = np.linalg.eigh(Hm); zmask = np.abs(ev_) < 1e-8 * np.abs(ev_).max(); Z = Uv[:, zmask]
    vfull = np.r_[xv, yv]
    Gs = np.array([Ks * (GA_ @ vfull) for GA_ in GACT]).T; ug, sg, _ = np.linalg.svd(Gs, full_matrices=False); Gs = ug[:, sg > 1e-8 * sg.max()]
    wx, Vx = np.linalg.eigh(Z @ Z.T - Gs @ Gs.T); Bx = Vx[:, wx > 0.5]
    out = dict(zero_modes=int(zmask.sum()), goldstones=Gs.shape[1], extra=Bx.shape[1], heavy_ratio=float(np.abs(ev_[~zmask]).max() / np.abs(ev_[~zmask]).min()))
    if Bx.shape[1]:
        Qr = [Bx.conj().T @ q @ Bx for q in Rk]
        _, W_ = np.linalg.eig(sum(c * q for c, q in zip(np.random.default_rng(3).normal(size=5), Qr)))
        ws = [[np.real((W_[:, j].conj() @ q @ W_[:, j]) / (W_[:, j].conj() @ W_[:, j])) for q in Qr] for j in range(W_.shape[1])]
        out["Y_T3L_hist"] = {f"{round((w[0] + w[1] + w[2]) / 3 + (w[3] + w[4]) / 2, 3) + 0.0},{round((w[3] - w[4]) / 2, 3) + 0.0}": 0 for w in ws}
        for w in ws: out["Y_T3L_hist"][f"{round((w[0] + w[1] + w[2]) / 3 + (w[3] + w[4]) / 2, 3) + 0.0},{round((w[3] - w[4]) / 2, 3) + 0.0}"] += 1
        out["color_roots"] = int(sum(1 for w in ws if sorted(np.round(np.abs(w[:3]), 3)) == [0, 1, 1] and abs(sum(w[:3])) < 1e-6))
    return out


GACT = [coord_action(Gm) for Gm in gen]
so10rows = []
for r in d12704["so10_light_QU"]["vacua_45_210"]:
    a_ = analyse(r); a_.update(vev={k: round(v, 4) for k, v in r["vev"].items()}, QU_only=r["QU_only"], params=r["params"]); so10rows.append(a_)
    print(f"(2) 45+210 vacuum {a_['vev']} (Q+U only: {r['QU_only']}): zero modes {a_['zero_modes']} = {a_['goldstones']} Goldstones + {a_['extra']} extra"
          + (f"; extra (Y,T3L) {a_['Y_T3L_hist']}, colour roots {a_['color_roots']}" if a_["extra"] else ""))
assert any(r["extra"] == 0 for r in so10rows if not r["QU_only"])
assert all(r["extra"] > 0 for r in so10rows if r["QU_only"])
w_ne0 = [r for r in so10rows if r["QU_only"] and abs(r["vev"]["w"]) > 1e-6]
assert w_ne0 and all(r["extra"] == 11 and r["color_roots"] == 6 and r["Y_T3L_hist"] == {"0.0,0.0": 9, "0.0,1.0": 1, "0.0,-1.0": 1} for r in w_ne0)
res["so10_vacuum_mass_matrix"] = dict(rows=so10rows,
                                      note="Every 45+210 vacuum with Q+U-only light has extra massless chiral states beyond the Goldstones: (8,1,0)+(1,3,0) when "
                                           "omega != 0; (3,2,-5/6)+(3,2,1/6)+c.c. (and sometimes 8+3+1) when omega = 0. Most vacua without the Q+U pattern have none (the p, B-only family has 30).")

# ---- (2b) unification with the light octet + triplet (hybrid, M_VL = 1.74 TeV): Weyl below M_SS, chiral superfield (x1.5) above
G3_ = {"__file__": os.path.join(HERE, "toe_pass12703_round.py")}
exec(open(os.path.join(HERE, "toe_pass12703_round.py"), encoding="utf-8").read().split("# ======================================================================= (2)")[0], G3_)
weyl, BIJ, B1, DU, CU, YC, AINV, MZ, tau_p, content = (G3_[k] for k in ("weyl", "BIJ", "B1", "DU", "CU", "YC", "AINV", "MZ", "tau_p", "content"))
from scipy.integrate import solve_ivp


def adj_piece(d3, d2):
    S = np.array([0.0, {1: 0, 2: 0.5, 3: 2.0}[d2] * d3 if d2 == 3 else 0.0, 3.0 if d3 == 8 else 0.0])
    if d2 == 3: S = np.array([0.0, 2.0, 0.0])
    C2 = np.array([0.0, 2.0 if d2 == 3 else 0.0, 3.0 if d3 == 8 else 0.0])
    CG = np.array([0.0, 2.0, 3.0])
    return 2 / 3 * S, 0.5 * (4 * np.outer(S, C2) + 20 / 3 * np.diag(CG * S))


bO, BO = adj_piece(8, 1); bT, BT = adj_piece(1, 3)
assert np.allclose(bO, [0, 0, 2]) and np.allclose(bT, [0, 4 / 3, 0])           # Weyl octet / triplet one-loop shifts


def unify_adj(Madj, yp=0.464, MSS=1e10, MVL=1740.0):
    dbVL, dBVL = content(["Q", "U"])
    events = sorted([(MVL, "vl"), (MSS, "susy"), (Madj, "adj")])
    g = list(np.sqrt(4 * math.pi / AINV)); y = 0.97; mu = MZ; on = set()
    pts = [(MZ, None)] + events
    for i in range(len(pts)):
        if pts[i][1]: on.add(pts[i][1])
        if pts[i][1] == "susy": y = y / math.sin(math.atan(1.0))
        th = "MSSM" if "susy" in on else "SM"; f15 = 1.5 if th == "MSSM" else 1.0
        bb = B1[th] + (dbVL * f15 if "vl" in on else 0) + ((bO + bT) * f15 if "adj" in on else 0)
        Bm = BIJ[th] + (dBVL * f15 if "vl" in on else 0) + ((BO + BT) * f15 if "adj" in on else 0)
        ypp = yp if "vl" in on else 0.0
        mend = pts[i + 1][0] if i + 1 < len(pts) else 1e19

        def fn(t, z, bb=bb, Bm=Bm, th=th, ypp=ypp):
            gg, yy = z[:3], z[3]; g2 = gg ** 2
            return list(K * gg ** 3 * bb + K * K * gg ** 3 * (Bm @ g2 - DU[th] * (yy ** 2 + ypp ** 2))) + [K * yy * (YC[th] * yy ** 2 - CU[th] @ g2)]
        evn = lambda t, z: z[0] - z[1]; evn.terminal = True
        s = solve_ivp(fn, (math.log(mu), math.log(mend)), g + [y], events=evn, rtol=1e-9, atol=1e-12, dense_output=True)
        if s.t_events[0].size:
            z = s.sol(s.t_events[0][0]); ai = 4 * math.pi / z[:3] ** 2
            return math.exp(s.t_events[0][0]), float(ai[0]), float(ai[2] - ai[0])
        g = list(s.y[:3, -1]); y = s.y[3, -1]; mu = mend
    return float("nan"), float("nan"), float("nan")


ref = unify_adj(1e30)
assert abs(ref[2] - 0.26) < 0.03, ref                                          # Pass 12702/12703 hybrid
adj = []
for Ma in (1e12, 1e13, 1e14, 1e15):
    M12, ai, dl = unify_adj(Ma); adj.append(dict(M_adj=Ma, M12=M12, alpha_inv=ai, delta=dl))
    print(f"(2b) hybrid + light (8,1,0)+(1,3,0) at {Ma:.0e}: M12 = {M12:.2e}, delta = {dl:+.2f}")
res["octet_triplet_unification"] = dict(reference_no_adjoint=ref, rows=adj, note="nan = alpha1 and alpha2 do not meet below 1e19 GeV")

# ======================================================================= (3) MFV tree splitting
src03 = open(os.path.join(HERE, "toe_pass12703_round.py"), encoding="utf-8").read()
G3 = {"math": math, "np": np}
exec(src03.split("V, MSTAR, ETA_OBS")[1].split("def lepto")[0].join(["V, MSTAR, ETA_OBS", ""]), G3)
V, MSTAR, ETA_OBS, m2n, m3n, pmns, kappa = (G3[k] for k in ("V", "MSTAR", "ETA_OBS", "m2", "m3", "pmns", "kappa"))
K = 1 / (16 * math.pi ** 2)


def lepto_mfv(M0, Lam, z, delta, alpha, xi, ytau, c1, c2):
    U = pmns(delta, alpha)
    Rm_ = np.array([[0, 0], [np.cos(z), -xi * np.sin(z)], [np.sin(z), xi * np.cos(z)]])
    h0 = (1 / V) * np.conj(U) @ np.diag([0, math.sqrt(m2n), math.sqrt(m3n)]) @ Rm_ * math.sqrt(M0)
    L = math.log(Lam / M0); c = 1.5 * K * ytau ** 2
    wv = np.array([L, L, (1 - math.exp(-2 * c * L)) / (2 * c) if c > 0 else L])
    Pt = np.diag([0, 0, ytau ** 2])
    S = -K * 2 * np.real(h0.conj().T @ np.diag(wv) @ h0) + c1 * np.real(h0.conj().T @ h0) + c2 * np.real(h0.conj().T @ Pt @ h0)
    sv, O = np.linalg.eigh(S); h = h0 @ O; Mi = M0 * (1 + sv); dM = M0 * (sv - sv[::-1])
    hh = h.conj().T @ h; Gam = np.real(np.diag(hh)) * Mi / (8 * math.pi); eps = np.zeros((2, 3))
    for i in range(2):
        j = 1 - i; d2 = dM[i] * (Mi[i] + Mi[j]); fr = d2 * Mi[i] * Gam[j] / (d2 ** 2 + (Mi[i] * Gam[j]) ** 2)
        for al in range(3):
            num = np.imag(np.conj(h[al, i]) * h[al, j] * hh[i, j]) + Mi[i] / Mi[j] * np.imag(np.conj(h[al, i]) * h[al, j] * hh[j, i])
            eps[i, al] = num / np.real(hh[i, i] * hh[j, j]) * fr
    Ka = (np.abs(h) ** 2 * V ** 2 / (Mi[None, :] * MSTAR)).sum(axis=1)
    return 0.96e-2 * abs(sum(kappa(Ka[al]) * eps[:, al].sum() for al in range(3))), abs(dM[0]) / Gam.mean()


M0, YT = 1.24e7, 0.0095
rnd = lambda: (complex(rng.uniform(0, math.pi), rng.uniform(-1.5, 1.5)), rng.uniform(0, 2 * math.pi), rng.uniform(0, 2 * math.pi), rng.choice([-1, 1]))
mfv = {}
for name, c1r, c2r in (("control y_tau = 0", 3.0, 1.0), ("c2 = 0 (c1 only)", 3.0, 0.0), ("|c2| in [0.3, 3]", 3.0, 1.0), ("|c2| in [0.1, 1]", 1.0, -0.5)):
    out = []
    for _ in range(2000):
        c1 = rng.uniform(-c1r, c1r)
        c2 = 0.0 if c2r == 0.0 else rng.choice([-1, 1]) * 10 ** rng.uniform(c2r - 1.0 if c2r == -0.5 else -0.5, c2r if c2r != 1.0 else 0.5)
        out.append(lepto_mfv(M0, 2e16, *rnd(), 0.0 if name.startswith('control') else YT, c1, c2))
    et = np.array([o[0] for o in out]); rat = np.median([o[1] for o in out])
    mfv[name] = dict(frac_ge_obs=float(np.mean(et >= ETA_OBS)), eta_max=float(et.max()), eta_median=float(np.median(et)), dM_over_Gamma_median=float(rat))
    print(f"(3) MFV {name:26s}: eta_B max {et.max():.2e}, median {np.median(et):.1e}, fraction >= obs {np.mean(et >= ETA_OBS):.3f}, median dM/Gamma {rat:.1f}")
assert mfv["control y_tau = 0"]["eta_max"] < 1e-12 and mfv["|c2| in [0.3, 3]"]["frac_ge_obs"] > mfv["c2 = 0 (c1 only)"]["frac_ge_obs"]
res["mfv_tree_splitting"] = dict(scan=mfv, ytau=YT, M0=M0,
                                 note="Tree-level MFV term c2 Re(h^dag Ye Ye^dag h) misaligns at O(y_tau^2 |h|^2) ~ 1e-12 without the loop factor ln/16pi^2.")

# ======================================================================= (4) dark-graviton band, verified bound
band = {r["R_um"]: r["yprime"] for r in d12704["B_dark_graviton_band"]["rows"]}
res["dark_graviton_verified"] = dict(eq_4_14="30 um > l5_eff > (2/gamma)(delta/0.5)(lambda/0.1)^(2/3) x 10 um (2307.11048 v3, verbatim from the PDF)",
                                     natural="gamma ~ 2, delta ~ 0.5, lambda ~ 0.1 -> l5_eff in [10, 30] um",
                                     yprime_natural=[band[10.0], band[30.0]], yprime_O1=[band[1.0], band[30.0]],
                                     correction="Pass 12704 quoted eqs. (42)-(43) and l5 >~ 20 um from a summary; the verbatim equations are (4.13)-(4.14): "
                                                "l5 > 20 um and l5_eff > 10 um at natural parameters.")
print(f"(4) dark-graviton (verbatim eq. 4.14): natural l5_eff 10-30 um -> y'_B = {band[10.0]:.3f}-{band[30.0]:.3f}; O(1) range 1-30 um -> {band[1.0]:.3f}-{band[30.0]:.3f}")

json.dump(res, open(os.path.join(ROOT, "data", "toe_pass12705_round.json"), "w"), indent=1, default=float)
print("wrote data/toe_pass12705_round.json")
