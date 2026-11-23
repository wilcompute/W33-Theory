"""Pass 12720 (1): one pseudo-Goldstone mechanism for the Higgs doublets and for Q + U?
 Fields: Sigma (45, complex antisymmetric 10x10), H (16), Hbar (16bar), driver Y.  The 16 is built from the 32-dim Clifford algebra of so(10)
 (gamma matrices from Pauli tensor products, chirality projection); Hbar transforms as -S^T.  Superpotential
     W = (m/2) tr S^2 + (l/4M) tr S^4 + Y (Hbar.H - v^2) + eps Hbar S(Sigma)^2 H
 eps = 0: accidental SO(10)_45 x U(16); eps != 0: the Tavartkiladze-type coupling (arXiv:1803.11164) breaks it.  Vacuum: Sigma along B-L,
 H = Hbar along nu^c (the SU(5) singlet of the 16), solved numerically.  Holomorphic Hessian W'' at the vacuum; zero modes minus the 33
 gauge-orbit directions (complexified broken generators, eaten) = uneaten massless chiral multiplets; their SM content (hypercharge and
 colour/weak Casimirs on the quotient space).
usage: py -3 analysis/explore_pass12720_unified.py"""
import itertools, json, math, os
import numpy as np
from scipy.optimize import least_squares

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
s1 = np.array([[0, 1], [1, 0]], complex); s2 = np.array([[0, -1j], [1j, 0]]); s3 = np.diag([1, -1]).astype(complex); I2 = np.eye(2)


def kron(*a):
    out = np.array([[1.0 + 0j]])
    for x in a: out = np.kron(out, x)
    return out


Gam = []
for k in range(5):
    pre = [s3] * k; post = [I2] * (4 - k)
    Gam.append(kron(*pre, s1, *post)); Gam.append(kron(*pre, s2, *post))
# order: coordinates (x1..x5, y1..y5) of the vector rep -> Gamma index map: x_k -> Gam[2k], y_k -> Gam[2k+1]
gidx = [2 * k for k in range(5)] + [2 * k + 1 for k in range(5)]
G10 = [Gam[i] for i in gidx]
for a in range(10):
    for b in range(10):
        assert np.allclose(G10[a] @ G10[b] + G10[b] @ G10[a], 2 * (a == b) * np.eye(32))
chi = np.eye(32, dtype=complex)
for g in Gam: chi = chi @ g
chi = chi * (1j) ** 5 * (-1) ** 0
ev, U = np.linalg.eigh((chi + chi.conj().T) / 2)
P16 = U[:, ev > 0]; assert P16.shape[1] == 16


def Sv(M):
    """spinor (16) image of a vector-rep generator M (10x10 antisymmetric): S = (1/4) sum M_ab G_a G_b."""
    S32 = 0.25 * sum((M[a, b] * G10[a] @ G10[b] for a in range(10) for b in range(10) if M[a, b] != 0), np.zeros((32, 32), complex))
    return P16.conj().T @ S32 @ P16


basis = []
for i in range(10):
    for j in range(i + 1, 10):
        M = np.zeros((10, 10)); M[i, j], M[j, i] = 1, -1; basis.append(M)
Sb = [Sv(M) for M in basis]
for _ in range(5):
    i, j = np.random.default_rng(_).integers(0, 45, 2)
    C = basis[i] @ basis[j] - basis[j] @ basis[i]
    assert np.allclose(Sv(C), Sb[i] @ Sb[j] - Sb[j] @ Sb[i]), "spinor rep is not a homomorphism"
print("(1) 16 of so(10) built and checked (Clifford algebra, chirality, homomorphism)")
cplx = lambda A: np.block([[A.real, -A.imag], [A.imag, A.real]])
TBL = cplx(1j * np.diag([1, 1, 1, 0, 0])); Yg = cplx(1j * np.diag([-1 / 3] * 3 + [1 / 2] * 2)); Jc = cplx(1j * np.eye(5))
comm = lambda A, B: A @ B - B @ A


def commutant(X, gens):
    Cm = np.array([comm(X, g).ravel() for g in gens]).T
    u, s, vh = np.linalg.svd(Cm); k = int(np.sum(s < 1e-9))
    return [sum(c * gens[i] for i, c in enumerate(v)) for v in vh[-k:]]


u5 = commutant(Jc, basis); Jn = Jc / np.linalg.norm(Jc); su5 = [g - np.sum(g * Jn) * Jn for g in u5]; su5 = [g for g in su5 if np.linalg.norm(g) > 1e-9]
A = np.vstack([Sv(g) for g in su5])
u_, s_, vh_ = np.linalg.svd(A); nuc = vh_[-1].conj(); assert s_[-2] > 1e-6 and s_[-1] < 1e-9
bl = (nuc.conj() @ Sv(TBL) @ nuc) / 1j
print(f"(1) nu^c = SU(5) singlet of the 16; B-L-generator eigenvalue on it: {bl.real:+.3f} (x i)")

# ---------------------------------------------------------------- superpotential on (Sigma 45, H 16, Hbar 16, Y 1) = 78 complex
m_, l_, Mh = 1.0, 1.0, 1.0
nS = 45
def unpack(z):
    S = np.tensordot(z[:nS], np.array(basis), 1); H = z[nS:nS + 16]; Hb = z[nS + 16:nS + 32]; Y = z[-1]
    return S, H, Hb, Y


def W(z, eps, v2=1.0):
    S, H, Hb, Y = unpack(z)
    w = m_ / 2 * np.trace(S @ S) + l_ / (4 * Mh) * np.trace(S @ S @ S @ S) + Y * (Hb @ H - v2)
    if eps:
        SS = Sv(S); w += eps * Hb @ SS @ SS @ H
    return w


def grad(z, eps, h=1e-6):
    return np.array([(W(z + h * e, eps) - W(z - h * e, eps)) / (2 * h) for e in np.eye(len(z))])


def hess(z, eps, h=1e-4):
    n = len(z); Hm = np.zeros((n, n), complex); E = np.eye(n) * h
    for i in range(n):
        for j in range(i, n):
            Hm[i, j] = Hm[j, i] = (W(z + E[i] + E[j], eps) - W(z + E[i] - E[j], eps) - W(z - E[i] + E[j], eps) + W(z - E[i] - E[j], eps)) / (4 * h * h)
    return Hm


a = math.sqrt(m_ * Mh / l_)
S0 = a * TBL
zS = np.array([np.sum(S0 * b) / 2 for b in basis])


def vacuum(eps):
    z0 = np.concatenate([zS, nuc, nuc.conj(), [0.0]]).astype(complex)
    # Hbar such that Hbar.H = 1: Hbar = conj(nu^c) normalised
    z0[nS + 16:nS + 32] = nuc.conj() / (nuc.conj() @ nuc)
    def f(x):
        z = x[:78] + 1j * x[78:]; g = grad(z, eps)
        return np.concatenate([g.real, g.imag])
    x0 = np.concatenate([z0.real, z0.imag])
    r = least_squares(f, x0, xtol=1e-14, ftol=1e-14, gtol=1e-14, max_nfev=200)
    z = r.x[:78] + 1j * r.x[78:]
    return z, float(np.linalg.norm(grad(z, eps)))


def orbit(z):
    S, H, Hb, Y = unpack(z); rows = []
    for g in basis:
        dS = comm(g, S); coeff = np.array([np.sum(dS * b) / 2 for b in basis])
        rows.append(np.concatenate([coeff, Sv(g) @ H, -Sv(g).T @ Hb, [0.0]]))
    return np.array(rows).T                                                  # 78 x 45


def field_action(g, z):
    """linear action of generator g on field fluctuations (78 x 78)."""
    Mx = np.zeros((78, 78), complex)
    for k, b in enumerate(basis):
        dS = comm(g, b); Mx[:nS, k] = [np.sum(dS * bb) / 2 for bb in basis]
    Mx[nS:nS + 16, nS:nS + 16] = Sv(g); Mx[nS + 16:nS + 32, nS + 16:nS + 32] = -Sv(g).T
    return Mx


gm = []
for a_ in range(3):
    for b_ in range(a_ + 1, 3):
        mm = np.zeros((3, 3), complex); mm[a_, b_] = mm[b_, a_] = 1; gm.append(mm)
        mm = np.zeros((3, 3), complex); mm[a_, b_] = -1j; mm[b_, a_] = 1j; gm.append(mm)
gm += [np.diag([1, -1, 0]).astype(complex), np.diag([1, 1, -2]).astype(complex) / math.sqrt(3)]
S3g = [cplx(1j * np.block([[h / 2, np.zeros((3, 2))], [np.zeros((2, 3)), np.zeros((2, 2))]])) for h in gm]
pa = [s1, s2, s3]
S2g = [cplx(1j * np.block([[np.zeros((3, 3)), np.zeros((3, 2))], [np.zeros((2, 3)), h / 2]])) for h in pa]


def analyse(eps):
    z, gn = vacuum(eps)
    Hm = hess(z, eps)
    sv = np.linalg.svd(Hm, compute_uv=False); scale = sv.max()
    u, s, vh = np.linalg.svd(Hm); ker = vh[s < 1e-6 * scale].conj().T               # 78 x nker
    O = orbit(z); uo, so, vo = np.linalg.svd(O); rO = int(np.sum(so > 1e-6 * so.max())); Ob = uo[:, :rO]
    # uneaten: component of ker orthogonal to the orbit space
    Pk = ker @ np.linalg.pinv(ker); Po = Ob @ Ob.conj().T
    Q = (np.eye(78) - Po) @ Pk
    uq, sq, vq = np.linalg.svd(Q); Bq = uq[:, sq > 1e-6]
    def rep_on(Mx):
        return np.linalg.lstsq(Bq, (np.eye(78) - Po) @ Mx @ Bq, rcond=None)[0]
    AY = rep_on(field_action(Yg, z)); C3 = -sum(rep_on(field_action(g, z)) @ rep_on(field_action(g, z)) for g in S3g)
    C2 = -sum(rep_on(field_action(g, z)) @ rep_on(field_action(g, z)) for g in S2g)
    w, V = np.linalg.eig(AY); cont = {}
    for k in range(len(w)):
        vv = V[:, k]; y = round(float((w[k] / 1j).real) * 6) / 6
        c3 = round(float(np.real(vv.conj() @ C3 @ vv / (vv.conj() @ vv))), 2); c2 = round(float(np.real(vv.conj() @ C2 @ vv / (vv.conj() @ vv))), 2)
        key = f"({ {0.0: '1', 1.33: '3', 3.0: '8'}.get(c3, c3)},{ {0.0: '1', 0.75: '2', 2.0: '3'}.get(c2, c2)}){y:+.3f}"
        cont[key] = cont.get(key, 0) + 1
    nz = len(s) - int(np.sum(s >= 1e-6 * scale))
    light = sorted(set(np.round(s[(s > 1e-6 * scale)] / scale, 4)))[:6]
    return dict(eps=eps, grad_norm=gn, zero_modes=int(ker.shape[1]), orbit_rank=rO, uneaten=int(Bq.shape[1]), content=dict(sorted(cont.items())),
                lightest_massive_rel=light)


res = {}
for eps in (0.0, 0.05, 0.2):
    r = analyse(eps); res[str(eps)] = r
    print(f"(1) eps = {eps}: |dW| = {r['grad_norm']:.1e}; zero modes {r['zero_modes']}, eaten (orbit rank) {r['orbit_rank']}, uneaten massless {r['uneaten']}: {r['content']}")
json.dump(res, open(os.path.join(ROOT, "data", "explore_pass12720_unified.json"), "w"), indent=1)
print("wrote data/explore_pass12720_unified.json")
