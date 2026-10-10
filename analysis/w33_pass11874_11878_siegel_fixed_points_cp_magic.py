"""Passes 11874-11878: the five follow-ups to the level-3 Siegel reading of W(3,3) (Passes 11869-11873).

psi(Omega)_c = theta[c/3, 0](0, 3 Omega) is the two-qutrit theta-null state of a genus-2 modulus Omega; the theta group
Gamma_theta (stabiliser of the characteristic 0) acts on it through the two-qutrit Clifford group.

  * 11874 FIXED POINTS. The isolated fixed points of Sp(4, Z) on the Siegel half-space (Gottschling's list) are
    recomputed from cyclotomic symplectic matrices; their stabilisers are computed exactly as automorphism groups of
    the polarised lattice (orders 10, 24, 24, 32, 48, 72) and reduced mod 3 (injective, Gamma(3) is torsion-free), with
    their orbit structure on the 40 points of W(3,3). Every fixed point is isomorphic to its CP image -conj(Omega)
    (exact lattice isomorphisms, as many as the stabiliser): all isolated fixed points are CP-conserving. The three product points (E_i^2, E_rho^2, E_i x E_rho) give a
    product theta-null state: a rank-one 3x3 Yukawa texture, one heavy generation.
  * 11875 WEIL 5 + 4. The theta-nulls span the even Weil module (5, "Rac"), the z-gradients of the odd thetas the odd
    one (4, "Di"); both are irreducible under the Clifford generators, and S acts on the gradients as
    sqrt(det(-i Omega)) (F x F) G (-Omega): Rac is a scalar weight-1/2 form, Di a vector-valued det^{1/2} x std form
    carrying the holomorphic cotangent index of T^4.
  * 11876 HIERARCHY. Near a factorised torus the Schmidt values of psi are (1, eps, eps^2) with the exact leading law
    s1 s3 / s2^2 = r(tau1) r(tau2) / 2, r(tau) = |g0 ^ g2| / |g1|^2 (g_k the k-th moment theta vectors), r invariant
    under the theta group, ranging over (0, inf) (0 at the cusp 1, inf at i inf; r(1+i) = sqrt2, r(1+i/2) = 3-2sqrt2).
    With ONE modulus and one characteristic the shape invariant and the first ratio are sector-universal; measured
    u, d, e values differ by factors 33 and 16, so one (modulus, characteristic) for all sectors is excluded.
  * 11877 MAGIC. The stabiliser 2-Renyi magic of psi(Omega) is a modular function (theta-group invariant, CP-even).
    It vanishes at the cusp i inf (|00>) and has no interior maximum: its supremum, log 2 per factor, is reached only at
    the cusp tau -> 1, where the one-qutrit theta-null tends to the maximal-magic state (2 e^{-i pi/3}, 1, 1)/sqrt6.
    Magic alone does not stabilise the modulus; the isolated fixed points are interior critical values.
  * 11878 GENUS-2 CP. Ratios of Burkhardt-group invariants (degrees 12, 16, 20, 24) of the Coble point of psi(Omega)
    are invariant under the full Sp(4, Z) (level-one Siegel modular functions), go to their complex conjugates under Omega -> -conj(Omega), are real on CP-conserving
    moduli and complex otherwise: the genus-2 arrow. Two tori with opposite one-qutrit arrows, diag(tau, -conj tau),
    compose to a CP-conserving surface; equal arrows do not.
"""

import itertools
import json
import math
import sys
from pathlib import Path

import numpy as np
from scipy.optimize import least_squares

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "analysis"))
import w33_pass11651_n_qutrit_hesse_space as H  # noqa: E402
from w33_pass11869_11873_siegel_level3_two_qutrits import IDX, rand_Om, theta_null_2  # noqa: E402

OUT = ROOT / "data" / "w33_pass11874_11878_siegel_fixed_points_cp_magic.json"
W = np.exp(2j * np.pi / 3)
C2 = [(a, b) for a in range(3) for b in range(3)]
JSTD = np.block([[np.zeros((2, 2), int), np.eye(2, dtype=int)], [-np.eye(2, dtype=int), np.zeros((2, 2), int)]])
NEG = [IDX[((-a) % 3, (-b) % 3)] for a, b in C2]


# ------------------------------------------------------------------ Siegel action, reduction, stabilisers
def act(g, Om):
    A, B, C, D = g[:2, :2], g[:2, 2:], g[2:, :2], g[2:, 2:]
    return (A @ Om + B) @ np.linalg.inv(C @ Om + D)


def companion(a):
    Cm = np.zeros((4, 4), int)
    Cm[1:, :3] = np.eye(3, dtype=int)
    Cm[:, 3] = [-x for x in a]
    return Cm


def invariant_unimodular_forms(M, rng=range(-2, 3)):
    """All alternating integer forms with Pfaffian +-1 preserved by M (small coefficients on a nullspace basis)."""
    import sympy as sp
    syms = sp.symbols("j0:6")
    pos = [(0, 1), (0, 2), (0, 3), (1, 2), (1, 3), (2, 3)]
    J = sp.zeros(4, 4)
    for s, (i, k) in zip(syms, pos):
        J[i, k], J[k, i] = s, -s
    A, _ = sp.linear_eq_to_matrix(list(sp.Matrix(M).T * J * sp.Matrix(M) - J), syms)
    basis = []
    for v in A.nullspace():
        v = v * sp.ilcm(*[x.q for x in v])
        Jv = np.zeros((4, 4), int)
        for x, (i, k) in zip(v, pos):
            Jv[i, k], Jv[k, i] = int(x), -int(x)
        basis.append(Jv)
    for co in itertools.product(rng, repeat=len(basis)):
        Jc = sum(c * b for c, b in zip(co, basis))
        if abs(Jc[0, 1] * Jc[2, 3] - Jc[0, 2] * Jc[1, 3] + Jc[0, 3] * Jc[1, 2]) == 1:
            yield Jc


def symplectic_basis(J):
    vecs = [np.array(v) for v in itertools.product(range(-2, 3), repeat=4) if any(v)]
    e1 = f1 = None
    for a in vecs:
        f = next((b for b in vecs if a @ J @ b == 1), None)
        if f is not None:
            e1, f1 = a, f
            break

    def proj(v):
        return v + (v @ J @ e1) * f1 - (v @ J @ f1) * e1
    imgs = [proj(np.eye(4, dtype=int)[i]) for i in range(4)]
    for a, b in itertools.product(vecs, vecs):
        pa, pb = proj(a), proj(b)
        if pa @ J @ pb != 1:
            continue
        Bm = np.array([pa, pb]).T.astype(float)
        ok = True
        for im in imgs:
            c = np.linalg.lstsq(Bm, im, rcond=None)[0]
            if not (np.allclose(c, np.round(c)) and np.allclose(Bm @ np.round(c), im)):
                ok = False
                break
        if ok:
            P = np.array([e1, pa, f1, pb]).T
            if (P.T @ J @ P == JSTD).all():
                return P
    return None


def fixed_points(g, starts, seed):
    rng = np.random.default_rng(seed)

    def unpack(p):
        X = np.array([[p[0], p[1]], [p[1], p[2]]])
        L = np.array([[p[3], 0], [p[4], p[5]]])
        return X + 1j * (L @ L.T + 1e-6 * np.eye(2))

    def res(p):
        d = act(g, unpack(p)) - unpack(p)
        return np.concatenate([d.real.ravel(), d.imag.ravel()])
    sols = []
    for _ in range(starts):
        r = least_squares(res, np.concatenate([rng.uniform(-1, 1, 3), rng.uniform(0.3, 1.5, 3)]),
                          xtol=1e-15, ftol=1e-15, gtol=1e-15)
        if np.linalg.norm(res(r.x)) < 1e-11:
            sols.append(unpack(r.x))
    return sols


def siegel_reduce(Om, it_max=300):
    for _ in range(it_max):
        Y = Om.imag
        best = None
        for U in itertools.product(range(-3, 4), repeat=4):
            U = np.array(U).reshape(2, 2)
            if abs(round(np.linalg.det(U))) != 1:
                continue
            Y2 = U @ Y @ U.T
            key = (round(Y2[0, 0], 12), round(Y2[1, 1], 12), -abs(round(Y2[0, 1], 12)))
            if best is None or key < best[0]:
                best = (key, U)
        U = best[1]
        Om = U @ Om @ U.T
        Om = Om - np.round(Om.real)
        if abs(Om[0, 0]) < 1 - 1e-12:
            s = np.zeros((4, 4), int)
            s[0, 2], s[2, 0], s[1, 1], s[3, 3] = -1, 1, 1, 1
            Om = act(s, Om)
        else:
            return Om
    return Om


def lattice_data(Om):
    X, Y = Om.real, Om.imag
    PiR = np.block([[np.eye(2), X], [np.zeros((2, 2)), Y]])
    Yi = np.linalg.inv(Y)
    S = PiR.T @ np.block([[Yi, np.zeros((2, 2))], [np.zeros((2, 2)), Yi]]) @ PiR
    Jc = np.linalg.inv(PiR) @ np.block([[np.zeros((2, 2)), -np.eye(2)], [np.eye(2), np.zeros((2, 2))]]) @ PiR
    E = PiR.T @ np.block([[np.zeros((2, 2)), Yi], [-Yi, np.zeros((2, 2))]]) @ PiR  # Im h, the Weil pairing
    return S, Jc, E


def stabiliser(Om):
    return isomorphisms(Om, Om)


def isomorphisms(Om1, Om2):
    """Integer M in GL4(Z) with M^T S2 M = S1 and M J1 = J2 M: isomorphisms of polarised lattices Om1 -> Om2."""
    S, Jc, _ = lattice_data(Om1)
    S2, Jc2, _ = lattice_data(Om2)
    Si = np.linalg.inv(S2)
    cands = []
    for i in range(4):
        b = int(np.ceil(np.sqrt(S[i, i] * Si.diagonal().max()))) + 1
        cands.append([np.array(v) for v in itertools.product(range(-b, b + 1), repeat=4)
                      if abs(np.array(v) @ S2 @ np.array(v) - S[i, i]) < 1e-7])
    out = []

    def rec(cols):
        k = len(cols)
        if k == 4:
            M = np.array(cols).T
            if abs(round(np.linalg.det(M))) == 1 and np.allclose(M @ Jc, Jc2 @ M, atol=1e-7):
                out.append(M)
            return
        for v in cands[k]:
            if all(abs(v @ S2 @ cols[j] - S[k, j]) < 1e-7 for j in range(k)):
                rec(cols + [v])
    rec([])
    return out


def orbits_on_w33(mats):
    pts = [v for v in itertools.product(range(3), repeat=4) if any(v) and next(x for x in v if x) == 1]
    pidx = {p: i for i, p in enumerate(pts)}

    def norm(v):
        v = tuple(int(x) % 3 for x in v)
        s = next(x for x in v if x)
        return tuple((x * s) % 3 for x in v)
    perms = [[pidx[norm(M @ np.array(p))] for p in pts] for M in mats]
    seen, orbs = set(), []
    for i in range(40):
        if i in seen:
            continue
        orb, fr = {i}, [i]
        while fr:
            j = fr.pop()
            for p in perms:
                if p[j] not in orb:
                    orb.add(p[j])
                    fr.append(p[j])
        seen |= orb
        orbs.append(len(orb))
    return sorted(orbs)


# ------------------------------------------------------------------ Hesse / Burkhardt machinery (Passes 11651/11657)
_, _PTS, _, _B, _WG = H.setup(2)
GCUB = np.array(H.closure([H.R_of(_B, g) for g in _WG.values()]))
TCUB = _B.T.reshape(5, 9, 9, 9)
L1 = np.random.default_rng(3).normal(size=5)  # real linear forms: Reynolds invariants commute with conjugation
L2 = np.random.default_rng(8).normal(size=5)


def coble(x):
    Gm = 3 * np.einsum("iabc,b,c->ai", TCUB, x, x)
    _, s, Vh = np.linalg.svd(Gm)
    return Vh[-1].conj(), s[-1] / s[0]


def reynolds(d, v, lv):
    return np.mean(((GCUB @ v) @ lv) ** d)


def cp_invariants(Om):
    x = theta_null_2(Om)
    k, _ = coble(x / np.linalg.norm(x))
    a12 = reynolds(12, k, L1)
    return np.array([a12 / reynolds(12, k, L2), reynolds(24, k, L1) / a12**2,
                     reynolds(16, k, L1) ** 2 / (a12 * reynolds(20, k, L1))])


def im_ratio(J):
    return float(np.max(abs(J.imag) / abs(J)))


# ------------------------------------------------------------------ magic
X1 = np.roll(np.eye(3), 1, axis=0)
Z1 = np.diag([1, W, W * W])
WEYL1 = np.array([np.linalg.matrix_power(X1, a) @ np.linalg.matrix_power(Z1, b) for a in range(3) for b in range(3)])
WEYL2 = np.array([np.kron(WEYL1[i], WEYL1[j]) for i in range(9) for j in range(9)])


def magic(p, weyl):
    p = p / np.linalg.norm(p)
    ex = np.einsum("i,kij,j->k", p.conj(), weyl, p)
    return float(-np.log(np.sum(abs(ex) ** 4) / len(p)))


def theta_null_1(tau, N=200):
    n = np.arange(-N, N + 1)
    return np.array([np.sum(np.exp(3j * np.pi * tau * (n + c / 3) ** 2)) for c in range(3)])


# ------------------------------------------------------------------ 11874
CYCLOTOMIC = {"Phi5": [1, 1, 1, 1], "Phi8": [1, 0, 0, 0], "Phi12": [1, 0, -1, 0], "Phi3Phi6": [1, 0, 1, 0],
              "Phi3Phi4": [1, 1, 2, 1], "Phi4Phi6": [1, -1, 2, -1]}


def gottschling_points():
    """Closed forms of the six isolated fixed points (Gottschling 1961), as located by the cyclotomic search
    (companion matrices of Phi5, Phi8, Phi12 with their invariant unimodular forms; scratch provenance in the note)."""
    s2, s3 = math.sqrt(2), math.sqrt(3)
    c72, s72, t36 = math.cos(2 * math.pi / 5), math.sin(2 * math.pi / 5), math.tan(math.pi / 5)
    rho = complex(0.5, s3 / 2)
    return {
        "y2=x5-1 (C10)": np.array([[complex(-c72, s72), complex(0.5, -t36 / 2)], [complex(0.5, -t36 / 2), complex(c72, s72)]]),
        "y2=x6-1": 1j / s3 * np.array([[2, 1], [1, 2]]),
        "E_i x E_rho": np.diag([1j, rho]),
        "E_i x E_i": 1j * np.eye(2),
        "Bolza y2=x5-x": np.array([[complex(1 / 3, 2 * s2 / 3), complex(-1 / 3, s2 / 3)], [complex(-1 / 3, s2 / 3), complex(1 / 3, 2 * s2 / 3)]]),
        "E_rho x E_rho": rho * np.eye(2),
    }


def part_fixed_points():
    rows = []
    for name, Om in gottschling_points().items():
        st = stabiliser(Om)
        mod3 = {tuple((m % 3).ravel()) for m in st}
        x = theta_null_2(Om)
        sv = np.linalg.svd(x.reshape(3, 3), compute_uv=False)
        rows.append(dict(
            point=name, Omega=[[str(np.round(z, 6)) for z in r] for r in Om], stabiliser_order=len(st),
            injective_mod3=len(mod3) == len(st), orbits_on_40_points=orbits_on_w33(st),
            schmidt_sv=[float(s / sv[0]) for s in sv], product_state=bool(sv[1] / sv[0] < 1e-10),
            cp_conserving_lattice_isomorphisms=len(isomorphisms(Om, -Om.conj())),
            magic=magic(x, WEYL2)))
    return rows


# ------------------------------------------------------------------ 11875
def theta_and_gradients(Om, N=16):
    n = np.arange(-N, N + 1)
    n1, n2 = np.meshgrid(n, n, indexing="ij")
    val, gr = [], []
    for c1, c2 in C2:
        v1, v2 = n1 + c1 / 3, n2 + c2 / 3
        e = np.exp(3j * np.pi * (Om[0, 0] * v1 * v1 + 2 * Om[0, 1] * v1 * v2 + Om[1, 1] * v2 * v2))
        val.append(e.sum())
        gr.append([6j * np.pi * (v1 * e).sum(), 6j * np.pi * (v2 * e).sum()])
    return np.array(val), np.array(gr)


def part_weil(rng):
    Pm = np.zeros((9, 9))
    for i in range(9):
        Pm[NEG[i], i] = 1
    ev, V = np.linalg.eigh((np.eye(9) + Pm) / 2)
    Ve, Vo = V[:, ev > 0.5], V[:, ev < 0.5]
    F = np.array([[W ** (a * b) for b in range(3)] for a in range(3)]) / np.sqrt(3)
    FF = np.kron(F, F)
    worst = dict(values_even=0.0, gradients_odd=0.0, S_law=0.0, X_equals_minus_Omega=0.0)
    for _ in range(6):
        Om = rand_Om(rng)
        v, G = theta_and_gradients(Om)
        _, G2 = theta_and_gradients(-np.linalg.inv(Om))
        Gl = np.sqrt(np.linalg.det(-1j * Om)) * (FF @ G)
        Xs = np.linalg.lstsq(Gl, G2, rcond=None)[0]
        worst["values_even"] = max(worst["values_even"], float(np.max(abs(Vo.conj().T @ v))))
        worst["gradients_odd"] = max(worst["gradients_odd"], float(np.max(abs(Ve.conj().T @ G))))
        worst["S_law"] = max(worst["S_law"], float(np.max(abs(Gl @ Xs - G2))))
        worst["X_equals_minus_Omega"] = max(worst["X_equals_minus_Omega"], float(np.max(abs(Xs + Om))))
    D1 = np.diag([1, 1, W])
    I3 = np.eye(3)
    gens = [np.kron(F, I3), np.kron(I3, F), np.kron(D1, I3), np.kron(I3, D1), np.diag([W ** (a * b) for a, b in C2])]
    comm = {}
    for name, Vs in (("even", Ve), ("odd", Vo)):
        d = Vs.shape[1]
        A = np.vstack([np.kron(np.eye(d), r) - np.kron(r.T, np.eye(d)) for r in (Vs.conj().T @ g @ Vs for g in gens)])
        comm[name] = int(np.sum(np.linalg.svd(A, compute_uv=False) < 1e-9))
    return dict(dims=dict(even=Ve.shape[1], odd=Vo.shape[1]), max_errors=worst, commutant_dims=comm)


# ------------------------------------------------------------------ 11876
def g_moment(k, tau, N=60):
    n = np.arange(-N, N + 1)
    return np.array([np.sum((n + c / 3) ** k * np.exp(3j * np.pi * tau * (n + c / 3) ** 2)) for c in range(3)])


def wedge(a, b):
    return float(np.sqrt(max(np.linalg.norm(a) ** 2 * np.linalg.norm(b) ** 2 - abs(np.vdot(a, b)) ** 2, 0)))


def r_of(tau):
    return wedge(g_moment(0, tau), g_moment(2, tau)) / np.linalg.norm(g_moment(1, tau)) ** 2


MASSES_MZ = dict(  # running masses at M_Z (Xing, Zhang, Zhou 2008), GeV
    u=(1.27e-3, 0.619, 171.7), d=(2.90e-3, 0.055, 2.89), e=(0.48657e-3, 0.10272, 1.74624))


def part_hierarchy(rng):
    law = []
    for _ in range(3):
        t1, t2 = (complex(rng.uniform(-0.5, 0.5), rng.uniform(0.8, 1.6)) for _ in range(2))
        O = np.diag([t1, t2]).astype(complex)
        O[0, 1] = O[1, 0] = 1e-4 * np.exp(0.4j)
        s = np.linalg.svd(theta_null_2(O, N=20).reshape(3, 3), compute_uv=False)
        law.append(abs(s[0] * s[2] / s[1] ** 2 - r_of(t1) * r_of(t2) / 2) / (r_of(t1) * r_of(t2) / 2))
    t = 0.21 + 1.13j
    inv = dict(r=r_of(t), r_S=r_of(-1 / t), r_T2=r_of(t + 2), r_T=r_of(t + 1))
    cusp1 = {f"1+i/{Y}": r_of(1 + 1j / Y) for Y in (1, 2, 4, 8)}
    cuspinf = {f"0.3+{Y}i": r_of(0.3 + 1j * Y) for Y in (1, 2, 4, 8)}
    data = {}
    for k, (m1, m2, m3) in MASSES_MZ.items():
        data[k] = dict(R=m1 * m3 / m2**2, eps=m2 / m3)
    Rs = [v["R"] for v in data.values()]
    es = [v["eps"] for v in data.values()]
    return dict(law_rel_err_max=float(max(law)), invariance=inv, near_cusp_1=cusp1, near_cusp_inf=cuspinf,
                exact_values=dict(r_1_plus_i=r_of(1 + 1j), sqrt2=math.sqrt(2), r_1_plus_i_over_2=r_of(1 + 0.5j),
                                  three_minus_2sqrt2=3 - 2 * math.sqrt(2)),
                measured=data, R_spread=max(Rs) / min(Rs), eps_spread=max(es) / min(es))


# ------------------------------------------------------------------ 11877
def part_magic(rng):
    Om = rand_Om(rng)
    x = theta_null_2(Om)
    O2 = Om.copy()
    O2[0, 1] += 1
    O2[1, 0] += 1
    inv = dict(S=abs(magic(theta_null_2(-np.linalg.inv(Om)), WEYL2) - magic(x, WEYL2)),
               shear=abs(magic(theta_null_2(O2), WEYL2) - magic(x, WEYL2)),
               CP=abs(magic(theta_null_2(-Om.conj()), WEYL2) - magic(x, WEYL2)))
    cusp_inf = magic(theta_null_2(5j * np.eye(2)), WEYL2)
    one = {}
    for Y in (1, 2, 4, 8, 16):
        p = theta_null_1(1 + 1j / Y)
        one[f"1+i/{Y}"] = magic(p, WEYL1)
    p = theta_null_1(1 + 1j / 16)
    p = p / np.linalg.norm(p)
    p = p / np.exp(1j * np.angle(p[1]))
    target = np.array([2 * np.exp(-1j * np.pi / 3), 1, 1]) / np.sqrt(6)
    grid = [complex(x0, y0) for x0 in np.linspace(-1, 1, 81) for y0 in np.linspace(0.08, 3, 80) if abs(complex(x0, y0)) >= 1]
    vals = [magic(theta_null_1(t, N=60), WEYL1) for t in grid]
    return dict(invariance=inv, cusp_inf=cusp_inf, one_qutrit_near_cusp_1=one, log2=math.log(2),
                limit_state_err=float(np.max(abs(p - target))), one_qutrit_grid_sup=float(max(vals)),
                one_qutrit_at_i=magic(theta_null_1(1j), WEYL1),
                one_qutrit_at_rho=magic(theta_null_1(np.exp(1j * np.pi / 3)), WEYL1))


# ------------------------------------------------------------------ 11878
def part_cp(rng):
    Om = np.array([[0.31 + 1.1j, 0.17 + 0.2j], [0.17 + 0.2j, -0.22 + 0.9j]])
    J0 = cp_invariants(Om)
    O2 = Om.copy()
    O2[0, 1] += 1
    O2[1, 0] += 1
    O3 = Om.copy()
    O3[0, 0] += 2

    def rel(J):
        return float(np.max(abs(J - J0) / abs(J0)))
    O4 = Om.copy()
    O4[0, 0] += 1  # outside the theta group
    s1 = np.zeros((4, 4), int)
    s1[0, 2], s1[2, 0], s1[1, 1], s1[3, 3] = -1, 1, 1, 1
    t = 0.23 + 1.17j
    off = 0.2j * np.array([[0, 1], [1, 0]])
    return dict(
        invariance=dict(S=rel(cp_invariants(-np.linalg.inv(Om))), shear=rel(cp_invariants(O2)),
                        diag_shift=rel(cp_invariants(O3)), swap=rel(cp_invariants(Om[::-1, ::-1])),
                        T1_outside_theta_group=rel(cp_invariants(O4)), S1_genus1=rel(cp_invariants(act(s1, Om)))),
        cp_conjugates=float(np.max(abs(cp_invariants(-Om.conj()) - J0.conj()) / abs(J0))),
        im_ratio=dict(pure_imaginary=im_ratio(cp_invariants(1j * np.array([[1.3, 0.4], [0.4, 1.1]]))),
                      integer_real_part=im_ratio(cp_invariants(np.array([[1 + 1.2j, 1 + 0.3j], [1 + 0.3j, -1 + 1.4j]]))),
                      generic=im_ratio(J0),
                      opposite_arrows=im_ratio(cp_invariants(np.diag([t, -t.conjugate()]) + off)),
                      equal_arrows=im_ratio(cp_invariants(np.diag([t, t]) + off)),
                      one_cp_even_factor=im_ratio(cp_invariants(np.diag([t, 1j]) + off))))


def main():
    rng = np.random.default_rng(11874)
    res = dict(pass_ids=[11874, 11875, 11876, 11877, 11878])
    res["11875_weil_5_plus_4"] = part_weil(rng)
    res["11876_hierarchy"] = part_hierarchy(rng)
    res["11877_magic"] = part_magic(rng)
    res["11878_genus2_cp"] = part_cp(rng)
    res["11874_fixed_points"] = part_fixed_points()
    w, h, m, c, f = (res[k] for k in ("11875_weil_5_plus_4", "11876_hierarchy", "11877_magic", "11878_genus2_cp",
                                      "11874_fixed_points"))
    orders = sorted(r["stabiliser_order"] for r in f)
    res["checks"] = {k: bool(v) for k, v in dict(
        fixed_point_stabilisers_are_gottschling=orders == [10, 24, 24, 32, 48, 72],
        stabilisers_inject_mod3=all(r["injective_mod3"] for r in f),
        fixed_points_cp_conserving=all(r["cp_conserving_lattice_isomorphisms"] == r["stabiliser_order"] for r in f),
        product_points_rank_one=sum(r["product_state"] for r in f) == 3,
        weil_even5_odd4=w["dims"] == dict(even=5, odd=4) and max(w["max_errors"].values()) < 1e-10,
        weil_irreducible=w["commutant_dims"] == dict(even=1, odd=1),
        hierarchy_law=h["law_rel_err_max"] < 1e-5,
        r_theta_group_invariant=abs(h["invariance"]["r"] - h["invariance"]["r_S"]) < 1e-10
        and abs(h["invariance"]["r"] - h["invariance"]["r_T2"]) < 1e-10,
        r_exact_values=abs(h["exact_values"]["r_1_plus_i"] - math.sqrt(2)) < 1e-10
        and abs(h["exact_values"]["r_1_plus_i_over_2"] - (3 - 2 * math.sqrt(2))) < 1e-10,
        one_modulus_excluded=h["R_spread"] > 10 and h["eps_spread"] > 10,
        magic_modular=max(m["invariance"].values()) < 1e-10 and m["cusp_inf"] < 1e-2,
        magic_sup_at_cusp_1=abs(m["one_qutrit_near_cusp_1"]["1+i/16"] - math.log(2)) < 1e-9
        and m["one_qutrit_grid_sup"] <= math.log(2) + 1e-9 and m["limit_state_err"] < 1e-4,
        cp_invariant_modular=max(c["invariance"].values()) < 1e-5 and c["cp_conjugates"] < 1e-5,
        cp_real_on_cp_loci=c["im_ratio"]["pure_imaginary"] < 1e-10 and c["im_ratio"]["integer_real_part"] < 1e-10
        and c["im_ratio"]["generic"] > 1e-3,
        opposite_arrows_cancel=c["im_ratio"]["opposite_arrows"] < 1e-10 < 1e-3 < c["im_ratio"]["equal_arrows"],
    ).items()}
    res["all_checks_pass"] = all(res["checks"].values())
    OUT.parent.mkdir(exist_ok=True)
    OUT.write_text(json.dumps(res, indent=2, default=str))
    print(json.dumps(res["checks"], indent=1))
    print(json.dumps(f, indent=1, default=str))
    print("all", res["all_checks_pass"])


if __name__ == "__main__":
    main()
