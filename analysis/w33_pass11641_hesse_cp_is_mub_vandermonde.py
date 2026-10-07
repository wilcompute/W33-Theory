"""Pass 11641: the Hesse CP order parameter of a qutrit state is the Vandermonde of its four MUB triple products.

THE MAP.  For a qutrit state psi, project psi^(x3) onto the Hesse pencil inside Sym^3(C^3), spanned by the diagonal
tensor d (norm^2 3) and the all-distinct tensor s (norm^2 6) -- exactly the basis B of Pass 11600:
    u(psi) = B^T psi^(x3) = ( (psi0^3 + psi1^3 + psi2^3)/sqrt3 ,  sqrt6 psi0 psi1 psi2 ).
For every one-qutrit Clifford g, g^(x3) B = B R(g), so u(g psi) = R(g) u(psi), and u(conj psi) = conj u(psi).
CHECKED HERE: R(Fourier) and R(phase) are EXACTLY Pass 11600's normalized_F and normalized_P, and R(X) = R(Z) = 1.
So the Hesse doublet of Passes 11600-11614 is the Clifford quotient of a qutrit state (classical: the Hesse pencil
map P^2 --> P^1, Artebani-Dolgachev; Hughston 2007), with Pass 11600's coefficient CP = complex conjugation of psi.

THE THEOREM (exact, symbolic).  Let Pi_b = prod_{s in MUB b} |<s|psi>|^2 be the triple product of MUB b (4 MUBs), and
let m_b be the unit Bloch vector of the image of MUB b.  Then, with rho = |u|^2 and r the Bloch vector of u,
    rho = 3 sum_b Pi_b ,      r = -9 sum_b Pi_b m_b .
Consequences:
  (a) (sum_b Pi_b)^2 = 3 sum_b Pi_b^2 for every pure qutrit state (it is |r| = rho);
  (b) rho = M3 - M1^3, with M_k = sum_s |<s|psi>|^(2k) the stabiliser moments of Pass 11534; rho = 1/3 exactly on
      stabiliser states and rho = 0 exactly on the nine Hesse SIC (strange) states;
  (c) Pass 11600's CP-odd discriminant W = (x^2-y^2)(y^2-z^2)(z^2-x^2), in Pass 11600's own tetrahedral axes, is
      W = c * prod_{a<b} (Pi_a - Pi_b)   (exact constant c computed below);
  (d) so sign W = parity of the ordering of the four MUBs by their triple products; Pass 11614's 24 Weyl chambers are
      the 24 orderings, its walls are the ties Pi_a = Pi_b, and CP (complex conjugation) swaps two MUBs.
"""

from __future__ import annotations

import itertools
import json
import sys
from pathlib import Path

import numpy as np
import sympy as sp

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "w33_pass11641_hesse_cp_is_mub_vandermonde.json"
C11600 = ROOT / "data" / "w33_pass11600_dynamical_hesse_flavor.json"

# ---------------------------------------------------------------- exact objects
W_ = sp.Rational(-1, 2) + sp.sqrt(3) * sp.I / 2                       # omega
F_ = sp.Matrix(3, 3, lambda j, k: W_ ** (j * k)) / sp.sqrt(3)
P_ = sp.diag(1, 1, W_)
X_ = sp.Matrix(3, 3, lambda j, k: 1 if j == (k + 1) % 3 else 0)
Z_ = sp.diag(1, W_, W_ ** 2)


def pencil_basis():
    d = sp.zeros(27, 1)
    s = sp.zeros(27, 1)
    for i in range(3):
        d[9 * i + 3 * i + i] = 1
    for p in itertools.permutations(range(3)):
        s[9 * p[0] + 3 * p[1] + p[2]] = 1
    return sp.Matrix.hstack(d / sp.sqrt(3), s / sp.sqrt(6))


def R_exact(g):
    B = pencil_basis()
    g3 = sp.kronecker_product(g, g, g)
    return sp.simplify(B.T * g3 * B)


def mub_states():
    """the 12 stabiliser states, grouped by MUB: eigenbases of Z, X, XZ, XZ^2 (exact)"""
    out = {}
    out["Z"] = [sp.Matrix([1 if j == k else 0 for j in range(3)]) for k in range(3)]
    for lab, a in (("X", 0), ("XZ", 1), ("XZ2", 2)):
        # eigenvectors of X Z^a: components omega^(-(k j + a j(j-1)/2))... built numerically-exact by search
        Mx = X_ * Z_ ** a
        vecs = []
        for k in range(3):
            for ph in itertools.product(range(3), repeat=2):
                v = sp.Matrix([1, W_ ** ph[0], W_ ** ph[1]]) / sp.sqrt(3)
                lam = (Mx * v)[0] / v[0]
                if sp.simplify(Mx * v - lam * v) == sp.zeros(3, 1) and all(
                        sp.simplify((v.H * u)[0]) == 0 for u in vecs):
                    vecs.append(v)
                    break
        assert len(vecs) == 3, lab
        out[lab] = vecs
    return out


def u_of(psi):
    return (psi[0] ** 3 + psi[1] ** 3 + psi[2] ** 3) / sp.sqrt(3), sp.sqrt(6) * psi[0] * psi[1] * psi[2]


def bloch(u0, u1):
    c = sp.conjugate(u0) * u1
    return sp.Matrix([2 * sp.re(c), 2 * sp.im(c), sp.Abs(u0) ** 2 - sp.Abs(u1) ** 2])


def load_11600():
    d = json.load(open(C11600))["tensor"]
    T = sp.Matrix([[sp.sympify(x) for x in row] for row in d["Bloch_axes"]]).T      # stored axes are COLUMNS: n = T^T r
    nF = sp.Matrix([[sp.sympify(x) for x in row] for row in d["normalized_F"]])
    nP = sp.Matrix([[sp.sympify(x) for x in row] for row in d["normalized_P"]])
    return T, nF, nP, d


# ---------------------------------------------------------------- part 1: the doublet is the pencil quotient
def part_equivariance():
    T, nF, nP, raw = load_11600()
    RF, RP, RX, RZ = (R_exact(g) for g in (F_, P_, X_, Z_))
    res = dict(
        R_Fourier_equals_11600_normalized_F=sp.simplify(RF - nF) == sp.zeros(2, 2),
        R_phase_equals_11600_normalized_P=sp.simplify(RP - nP) == sp.zeros(2, 2),
        R_X_is_identity=sp.simplify(RX - sp.eye(2)) == sp.zeros(2, 2),
        R_Z_is_identity=sp.simplify(RZ - sp.eye(2)) == sp.zeros(2, 2),
        B_is_real="conj(u(psi)) = u(conj psi): complex conjugation of the state is Pass 11600's coefficient CP",
    )
    # Bloch actions in Pass 11600's tetrahedral axes, n = T r
    BF = sp.Matrix([[sp.sympify(x) for x in row] for row in raw["Bloch_F"]])
    BP = sp.Matrix([[sp.sympify(x) for x in row] for row in raw["Bloch_P"]])
    rng = np.random.default_rng(1)
    ok = 0
    for _ in range(5):
        u = sp.Matrix([sp.Rational(int(a), 7) + sp.I * sp.Rational(int(b), 7) for a, b in rng.integers(-6, 7, (2, 2))])
        for Rg, Bg in ((RF, BF), (RP, BP)):
            v = Rg * u
            lhs = T * bloch(v[0], v[1])
            rhs = Bg * T * bloch(u[0], u[1])
            ok += sp.simplify(lhs - rhs) == sp.zeros(3, 1)
    res["Bloch_actions_match_11600_(10_checks)"] = ok
    return res, T


# ---------------------------------------------------------------- part 2: the theorem, symbolically
def part_theorem(T):
    a = sp.symbols("a0:3", real=True)
    b = sp.symbols("b0:3", real=True)
    psi = sp.Matrix([a[j] + sp.I * b[j] for j in range(3)])
    mubs = mub_states()
    labels = ["Z", "X", "XZ", "XZ2"]

    def prob(s):
        z = sp.expand((s.H * psi)[0])
        return sp.expand(sp.re(z) ** 2 + sp.im(z) ** 2)
    p = {lab: [prob(s) for s in mubs[lab]] for lab in labels}
    Pi = {lab: sp.expand(p[lab][0] * p[lab][1] * p[lab][2]) for lab in labels}
    u0, u1 = (sp.expand(x) for x in u_of(psi))
    rho = sp.expand(sp.re(u0) ** 2 + sp.im(u0) ** 2 + sp.re(u1) ** 2 + sp.im(u1) ** 2)
    c = sp.expand(sp.conjugate(u0) * u1)
    r = sp.Matrix([2 * sp.re(c), 2 * sp.im(c), sp.re(u0) ** 2 + sp.im(u0) ** 2 - sp.re(u1) ** 2 - sp.im(u1) ** 2])
    n = (T * r).applyfunc(sp.expand)

    # images of the MUBs (unit vectors m_b, Pass 11600 axes)
    m = {}
    for lab in labels:
        imgs = []
        for s in mubs[lab]:
            uu = u_of(s)
            imgs.append((T * bloch(*uu)).applyfunc(sp.nsimplify).applyfunc(sp.simplify))
        assert all(sp.simplify(x - imgs[0]) == sp.zeros(3, 1) for x in imgs), lab     # one point per MUB
        rr = sp.sqrt(sum(x ** 2 for x in imgs[0]))
        assert sp.simplify(rr - sp.Rational(1, 3)) == 0
        m[lab] = (imgs[0] / rr).applyfunc(sp.simplify)

    sumPi = sum(Pi.values())
    thm_rho = sp.expand(rho - 3 * sumPi) == 0
    thm_r = all(sp.expand(n[i] + 9 * sum(Pi[lab] * m[lab][i] for lab in labels)) == 0 for i in range(3))

    # (a) cone identity
    cone = sp.expand(sumPi ** 2 - 3 * sum(x ** 2 for x in Pi.values())) == 0
    # (b) rho = M3 - M1^3
    allp = [x for lab in labels for x in p[lab]]
    M1 = sp.expand(sum(p["Z"]))
    M3 = sp.expand(sum(x ** 3 for x in allp))
    rho_is_M3 = sp.expand(rho - (M3 - M1 ** 3)) == 0

    # (c) W = c * Vandermonde, via the linear relation (symbolic in Pi)
    q = sp.symbols("q0:4")
    nq = -9 * sum((q[i] * m[lab] for i, lab in enumerate(labels)), sp.zeros(3, 1))
    x, y, z = nq
    Wq = sp.expand((x ** 2 - y ** 2) * (y ** 2 - z ** 2) * (z ** 2 - x ** 2))
    V = sp.expand(sp.prod([q[i] - q[j] for i, j in itertools.combinations(range(4), 2)]))
    cW = sp.nsimplify(sp.simplify(Wq / V))
    W_is_cV = sp.expand(Wq - cW * V) == 0
    xyz = sp.factor(sp.expand(x * y * z))
    p4 = sp.expand(x ** 4 + y ** 4 + z ** 4)

    # tetrahedron check and which side the MUBs sit on
    gram = [[sp.simplify(m[a_].dot(m[b_])) for b_ in labels] for a_ in labels]
    mub_xyz_sign = [int(sp.sign(sp.simplify(m[lab][0] * m[lab][1] * m[lab][2]))) for lab in labels]
    return dict(
        labels=labels,
        mub_unit_vectors_11600_axes={lab: [str(sp.nsimplify(v)) for v in m[lab]] for lab in labels},
        mub_gram=[[str(g) for g in row] for row in gram],
        theorem_rho_equals_3_sum_Pi=thm_rho,
        theorem_r_equals_minus9_sum_Pi_m=thm_r,
        cone_identity_sumPi2_eq_3sumPi2sq=cone,
        rho_equals_M3_minus_M1cubed=rho_is_M3,
        W_equals_c_times_Vandermonde=W_is_cV,
        c=str(cW),
        xyz_in_Pi=str(xyz),
        p4_in_Pi=str(sp.factor(p4)),
        sign_of_xyz_at_the_four_MUB_vertices=mub_xyz_sign,
    ), m


# ---------------------------------------------------------------- part 3: numerics, CP, special states
def part_numeric(m):
    w = np.exp(2j * np.pi / 3)
    labels = ["Z", "X", "XZ", "XZ2"]
    F = np.array([[w ** (j * k) for k in range(3)] for j in range(3)]) / np.sqrt(3)
    Xm = np.roll(np.eye(3), 1, axis=0)
    Zm = np.diag([1, w, w * w])
    bases = {"Z": np.eye(3)}
    for lab, a in (("X", 0), ("XZ", 1), ("XZ2", 2)):
        _, V = np.linalg.eig(Xm @ np.linalg.matrix_power(Zm, a))
        bases[lab] = V
    T = np.array(json.load(open(C11600))["tensor"]["Bloch_axes"], dtype=object)
    T = np.array([[float(sp.sympify(x)) for x in row] for row in T]).T
    M = {lab: np.array([float(v) for v in m[lab]]) for lab in labels}

    def Pis(psi):
        return np.array([np.prod(np.abs(bases[lab].conj().T @ psi) ** 2) for lab in labels])

    def n_of(psi):
        u0 = (psi[0] ** 3 + psi[1] ** 3 + psi[2] ** 3) / np.sqrt(3)
        u1 = np.sqrt(6) * psi[0] * psi[1] * psi[2]
        c = np.conj(u0) * u1
        return T @ np.array([2 * c.real, 2 * c.imag, abs(u0) ** 2 - abs(u1) ** 2])

    def Wn(n):
        x, y, z = n
        return (x * x - y * y) * (y * y - z * z) * (z * z - x * x)

    # CP: complex conjugation permutes the MUBs
    def mub_perm(g, anti=False):
        out = []
        for lab in labels:
            v = bases[lab][:, 0]
            v = g @ (np.conj(v) if anti else v)
            for lab2 in labels:
                if np.isclose(np.abs(bases[lab2].conj().T @ v).max(), 1):
                    out.append(lab2)
        return out
    rng = np.random.default_rng(11641)
    flips = 0
    for _ in range(2000):
        psi = rng.normal(size=3) + 1j * rng.normal(size=3)
        psi /= np.linalg.norm(psi)
        Wv = Wn(n_of(psi))
        flips += np.sign(Wn(n_of(np.conj(psi)))) == -np.sign(Wv)
    # special states
    zeta = np.exp(2j * np.pi / 9)
    tplus = np.array([1, zeta, zeta ** -1]) / np.sqrt(3)
    sic = np.array([0, 1, -1]) / np.sqrt(2)
    out = dict(
        mub_permutation_Fourier=mub_perm(F), mub_permutation_phase=mub_perm(np.diag([1, 1, w])),
        mub_permutation_conjugation=mub_perm(np.eye(3), anti=True),
        random_states=2000, CP_flips_sign_W=int(flips),
        T_plus_state=dict(Pi=[round(x * 81, 10) for x in Pis(tplus)], Pi_units="1/81",
                          rho=round(float(np.linalg.norm(n_of(tplus))), 12),
                          direction_dot_minus_mZ=round(float(-M["Z"] @ n_of(tplus) / np.linalg.norm(n_of(tplus))), 12)),
        strange_state_rho=float(np.linalg.norm(n_of(sic))),
    )
    # Pass 11600's canonical vacuum ray (1,2,3)/sqrt14 (unit rho): triple products and MUB order
    nv = np.array([1, 2, 3]) / np.sqrt(14)
    Pi_v = np.array([(1 - M[lab] @ nv) / 12 for lab in labels])        # rho = 1 units: Pi_b = rho (1 - m_b.n)/12
    order = [labels[i] for i in np.argsort(-Pi_v)]
    out["vacuum_11600_(1,2,3)/sqrt14"] = dict(Pi_over_rho=[float(x) for x in Pi_v], MUB_order_by_Pi=order,
                                              W=float(Wn(nv)))
    # a qutrit state realising that ray: the fibre is the Hesse cubic u1*f0 - u0*f1 = 0; on psi = (1, 1, t) it reads
    # u1 t^3 - 3 sqrt2 u0 t + 2 u1 = 0 (u = the doublet ray, from r = T n, any phase)
    r = T.T @ nv                                                       # n = T r, T orthogonal
    th = np.arccos(np.clip(r[2], -1, 1))
    ph = np.arctan2(r[1], r[0])
    u0, u1 = np.cos(th / 2), np.sin(th / 2) * np.exp(1j * ph)        # r = (2Re(u0* u1), 2Im(u0* u1), |u0|^2-|u1|^2)
    sols = []
    for tt in np.roots([u1, 0, -3 * np.sqrt(2) * u0, 2 * u1]):
        psi = np.array([1, 1, tt]) / np.linalg.norm([1, 1, tt])
        n = n_of(psi)
        sols.append(dict(t=[float(tt.real), float(tt.imag)], rho=float(np.linalg.norm(n)),
                         direction_error=float(np.linalg.norm(n / np.linalg.norm(n) - nv)),
                         Pi_times_81=[float(81 * x) for x in Pis(psi)],
                         MUB_order_by_Pi=[labels[i] for i in np.argsort(-Pis(psi))]))
    out["vacuum_11600_realised_by_states_(1,1,t)"] = sols
    return out


def main():
    res = dict(pass_id=11641)
    eq, T = part_equivariance()
    res["equivariance"] = eq
    print(eq, flush=True)
    th, m = part_theorem(T)
    res["theorem"] = th
    print(th, flush=True)
    res["numeric"] = part_numeric(m)
    print(res["numeric"], flush=True)
    json.dump(res, open(OUT, "w"), indent=1, default=str)


if __name__ == "__main__":
    main()
