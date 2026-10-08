"""Pass 11699: the E8 structure tensor produces Codex's Maschke-to-Burkhardt map -- the Coble covariant of the trivector
Cartan is, coefficient for coefficient, -2 times Pass 11663's Pfaffian quartic.

Construction (intrinsic: uses only the epsilon tensor that defines the E8 bracket [x, y] = *(x ^ y), Pass 11681).  For
a trivector x in Lambda^3 V (V = C^9, two qutrits) define the cubic form on V*
        P_x(y) = < (i_y x)^3 ^ x , vol >  =  6 sum_{|I| = 6} Pf((i_y x)[I, I]) sgn(I, J) x_J,     J = complement of I.
P_x is an SL(9)-covariant of degree 4 (Sym^4(Lambda^3 V) -> Sym^3 V*), hence equivariant for every unitary gate of
determinant 1 and Pauli-invariant whenever x is.  This is the Gruson-Sam-Weyman construction of the Coble cubic from a
trivector (pass to i_y x in Lambda^2 C^8), cited as prior art (Gruson-Sam-Weyman 2013; Rains-Sam 2018; already cited for
Lambda^3 C^9 <-> Coble cubics in Pass 11680).

FOUND, with x = sum_u c_u h_u on the Pauli-singlet Cartan (Pass 11681 basis, DIRS order) and P_x expanded in the five
Pauli-invariant cubics (c0 = sum y^3/6, c_d = parallel-line products; Pass 11663's basis):
    beta_0 = 24 abcd, beta_1 = -4a(b^3+c^3+d^3), beta_2 = 4b(a^3+c^3-d^3), beta_3 = 4c(a^3-b^3+d^3), beta_4 = 4d(a^3+b^3-c^3)
i.e. beta(c) = -2 Q(c) EXACTLY, where Q is Pass 11663's signed Pfaffian vector (the classical Maschke parametrisation,
Bruin-Filatov 2207.04393 sec. 3.1), in the committed coordinates with c = f.
  * The image is the hypersurface y1y2y3y4 + (1/6) y0 (y1^3+y2^3+y3^3+y4^3) + (1/48) y0^4 = 0: the BURKHARDT QUARTIC
    (t^4 - t sum y^3 + 3 y1y2y3y4 with y0 = -2t); it is the only quartic vanishing on the image.
  * The base locus contains all 40 Witting rays (the E8 root rays, Pass 11690).
  * Uniqueness: the space of quartic maps odd(4) -> even(5) equivariant for Pass 11663's determinant-one Weil generators
    is ONE-dimensional (and zero into the dual or conjugate of the even sector).
So the Maschke map is not an extra choice: it is the unique equivariant quartic, and it is the GSW Coble covariant of the
two-qutrit E8 Cartan.  New here: the coefficient identity on the committed two-qutrit E8 and the uniqueness count; the
covariant, the Maschke parametrisation and the Burkhardt quartic are classical.
"""

from __future__ import annotations

import itertools
import json
import sys
from pathlib import Path

import numpy as np
import sympy as s

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "analysis"))
import w33_pass11663_odd_weil_normal_map as C  # noqa: E402
import w33_pass11681_e8_from_two_qutrits as E  # noqa: E402

OUT = ROOT / "data" / "w33_pass11699_coble_covariant_is_maschke_map.json"


def sgn(seq):
    sg, seq = 1, list(seq)
    for i in range(len(seq)):
        for j in range(i + 1, len(seq)):
            if seq[i] > seq[j]:
                sg = -sg
    return sg


def _matchings(L):
    if not L:
        yield []
        return
    for k in range(1, len(L)):
        for m in _matchings(L[1:k] + L[k + 1:]):
            yield [(L[0], L[k])] + m


MATCH = [(m, sgn([i for p in m for i in p])) for m in _matchings(list(range(6)))]
COMP = []
for I in itertools.combinations(range(9), 6):
    J = tuple(sorted(set(range(9)) - set(I)))
    COMP.append((list(I), J, sgn(I + J)))


def pf6(Wm):
    return sum(sg * Wm[..., m[0][0], m[0][1]] * Wm[..., m[1][0], m[1][1]] * Wm[..., m[2][0], m[2][1]] for m, sg in MATCH)


def coble_cubic(x, ys):
    """P_x(y) for a batch of covectors y (up to the overall factor 6)."""
    X = E.full(x)
    Om = np.einsum("ka,aij->kij", ys, X)
    return sum(sg * x[E.TI[J]] * pf6(Om[:, I][:, :, I]) for I, J, sg in COMP)


def cubic_basis(ys):
    pts = E.PTS
    cs = [sum(ys[:, 3 * a[0] + a[1]] ** 3 for a in pts) / 6]
    for d in E.DIRS:
        lines = {tuple(sorted((a, tuple((a[i] + d[i]) % 3 for i in range(2)), tuple((a[i] - d[i]) % 3 for i in range(2)))))
                 for a in pts}
        cs.append(sum(ys[:, 3 * l[0][0] + l[0][1]] * ys[:, 3 * l[1][0] + l[1][1]] * ys[:, 3 * l[2][0] + l[2][1]] for l in lines))
    return np.array(cs).T


MONS = [m for m in itertools.product(range(5), repeat=4) if sum(m) == 4]


def mon(c):
    return np.array([np.prod(c ** np.array(m)) for m in MONS])


def main():
    rng = np.random.default_rng(11699)
    H = E.cartan_trivectors()
    ys = rng.normal(size=(60, 9)) + 1j * rng.normal(size=(60, 9))
    CB = cubic_basis(ys)

    def beta(c):
        P = coble_cubic(c @ H, ys)
        b = np.linalg.lstsq(CB, P, rcond=None)[0]
        return b, float(np.linalg.norm(CB @ b - P) / np.linalg.norm(P))

    cs = rng.normal(size=(80, 4)) + 1j * rng.normal(size=(80, 4))
    B, pauli_res = zip(*[beta(c) for c in cs])
    B = np.array(B)
    coef = np.linalg.lstsq(np.array([mon(c) for c in cs]), B, rcond=None)[0]
    fit_res = float(np.linalg.norm(np.array([mon(c) for c in cs]) @ coef - B) / np.linalg.norm(B))
    # compare with -2 * Pass 11663 quartic
    cmp = max(float(np.linalg.norm(beta(c)[0] + 2 * C.quartic(c))) for c in cs[:10])
    terms = {f"beta_{k}": {"".join(f"{'abcd'[i]}^{e}" for i, e in enumerate(m) if e): round(float(coef[j, k].real), 6)
                           for j, m in enumerate(MONS) if abs(coef[j, k]) > 1e-8} for k in range(5)}
    # image hypersurface
    m5 = [m for m in itertools.product(range(5), repeat=5) if sum(m) == 4]
    img = [mon(c) @ coef for c in rng.normal(size=(300, 4)) + 1j * rng.normal(size=(300, 4))]
    A = np.array([[np.prod(p ** np.array(m)) for m in m5] for p in img])
    sv = np.linalg.svd(A, compute_uv=False)
    ns = np.linalg.svd(A)[2][-1].conj()
    ns /= ns[np.argmax(np.abs(ns))]
    quartic = {str(m5[i]): round(float(ns[i].real), 6) for i in range(len(m5)) if abs(ns[i]) > 1e-8}
    # Witting base locus
    W = np.exp(2j * np.pi / 3)
    rays = [np.eye(4)[i] for i in range(4)]
    for i, j in itertools.product(range(3), repeat=2):
        rays += [np.array([0, 1, W ** i, W ** j]), np.array([1, 0, W ** i, -W ** j]),
                 np.array([1, -W ** i, 0, W ** j]), np.array([1, W ** i, -W ** j, 0])]
    base = max(float(np.linalg.norm(beta(r)[0])) for r in rays)
    # uniqueness of the equivariant quartic
    E9, O9 = C.parity_bases()
    num = lambda M: np.array(M.subs(C.W, s.Rational(-1, 2) + s.sqrt(3) * s.I / 2).evalf(), dtype=complex)  # noqa: E731
    F = rng.normal(size=(20, 4)) + 1j * rng.normal(size=(20, 4))
    dims = {}
    for label, tgt in (("even", lambda g: g), ("dual_even", lambda g: np.linalg.inv(g).T), ("conjugate_even", np.conj)):
        rows = []
        for g in C.canonical_generators().values():
            ge, go = tgt(num(C.G.inv() * E9.T * g * E9)), num(O9.T * g * O9 / 2)
            rows += [np.kron(np.eye(5), mon(go @ f)[None, :]) - np.kron(ge, mon(f)[None, :]) for f in F]
        sv2 = np.linalg.svd(np.vstack(rows), compute_uv=False)
        dims[label] = int(np.sum(sv2 < 1e-9 * sv2[0]))
    res = dict(pass_id=11699, pauli_invariance_residual=max(pauli_res), quartic_fit_residual=fit_res, coefficients=terms,
               max_norm_beta_plus_2Q=cmp, image_quartics=int(np.sum(sv < 1e-9 * sv[0])), image_quartic=quartic,
               burkhardt_form_check="y0=-2t gives (1/3)(t^4 - t sum y^3 + 3 y1y2y3y4)",
               max_norm_on_40_witting_rays=base, equivariant_quartic_dimensions=dims)
    print(json.dumps(res, indent=1))
    json.dump(res, open(OUT, "w"), indent=1)


if __name__ == "__main__":
    main()
