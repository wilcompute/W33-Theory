"""Pass 11645: time reversal of the Hesse shadow is complex conjugation of a j-invariant; the CP sign is sign Im j.

Every qutrit state psi (off the nine base points) lies on exactly one member of the Hesse pencil,
    E_psi :  x^3 + y^3 + z^3 = 3 mu x y z ,     mu(psi) = (psi0^3 + psi1^3 + psi2^3) / (3 psi0 psi1 psi2) = sqrt2 u0/u1,
an elliptic curve with  j(E_psi) = 27 mu^3 (mu^3 + 8)^3 / (mu^3 - 1)^3   (j - 1728 is 27 x a square / (mu^3 - 1)^3, checked).
  * j is a Clifford invariant (the Clifford group acts on the pencil through A4 and A4 preserves j), and
    j(conj psi) = conj j(psi): TIME REVERSAL ACTS AS COMPLEX CONJUGATION OF j.
  * THEOREM: sign W(psi) = sign Im j(E_psi), with W the CP-odd discriminant of Passes 11600/11614 in Pass 11600's axes.
    Proof: j: P^1 -> P^1 has degree 12 and is ramified only over 0 (the 4 equianharmonic = T-magic vertices, order 3),
    1728 (the 6 edge midpoints, order 2) and infinity (the 4 MUB vertices, order 3).  So j^-1(real line) is a graph with
    vertices only there, of valences 6, 4, 6; the 6 mirror great circles of T_d already map into the real line (they are
    fixed by antiunitary Cliffords, so their curves are real) and have exactly these valences, hence j^-1(R u oo) = the 6
    mirrors, and the 24 open chambers map alternately onto the upper and lower half planes.  Adjacent chambers have
    opposite sign W, so sign Im j = epsilon sign W globally; epsilon = +1 (checked).
  * The moduli are explicit in the four MUB triple products (Pass 11641), sigma = sum Pi_b:
        |j|        = C1 [ prod_b (sigma - 2 Pi_b) / prod_b Pi_b ]^(3/2),
        |j - 1728| = C2 (rho^2 - x^2)(rho^2 - y^2)(rho^2 - z^2) / [prod_b Pi_b]^(3/2),
    and Im j has the sign of W: j is determined by four measured numbers.
  * The 24 vacua of Pass 11600 are the 24 curves with j = j_vac or conj(j_vac); j_vac is computed exactly.
"""

from __future__ import annotations

import itertools
import json
from pathlib import Path

import numpy as np
import sympy as sp

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "w33_pass11645_time_reversal_is_conjugation_of_j.json"
C11600 = ROOT / "data" / "w33_pass11600_dynamical_hesse_flavor.json"

w = np.exp(2j * np.pi / 3)
LABELS = ["Z", "X", "XZ", "XZ2"]
MB = {"Z": (1, 1, 1), "X": (1, -1, -1), "XZ": (-1, 1, -1), "XZ2": (-1, -1, 1)}       # Pass 11641, unit after /sqrt3


def jmu(m):
    return 27 * m ** 3 * (m ** 3 + 8) ** 3 / (m ** 3 - 1) ** 3


def exact_part():
    mu = sp.symbols("mu")
    j = 27 * mu ** 3 * (mu ** 3 + 8) ** 3 / (mu ** 3 - 1) ** 3
    f = sp.factor(sp.together(j - 1728))
    num = sp.Poly(sp.numer(f), mu)
    const, facs = num.factor_list()
    is_square = const == 27 and all(e % 2 == 0 for _, e in facs)
    # Pass 11600 canonical vacuum ray (1,2,3)/sqrt14 -> exact mu and j
    T = sp.Matrix([[sp.sympify(x) for x in row] for row in json.load(open(C11600))["tensor"]["Bloch_axes"]])
    n = sp.Matrix([1, 2, 3]) / sp.sqrt(14)
    r = T * n                                                 # n = T^T r  (columns are the axes)
    zeta = (r[0] + sp.I * r[1]) / (1 + r[2])                  # u1/u0 for a unit Bloch vector
    m = sp.radsimp(sp.sqrt(2) / zeta)
    m_closed = -sp.sqrt(42) / 2 - 3 + sp.I * (sp.sqrt(3) + sp.sqrt(14) / 2)
    assert abs(complex(sp.N(m - m_closed, 40))) < 1e-30
    X = sp.symbols("X")
    jv = jmu(m_closed)
    jnum = complex(sp.N(jv, 30))
    mp = sp.minimal_polynomial(jv, X)
    mre = sp.minimal_polynomial(sp.re(sp.expand_complex(jv)), X)
    return dict(j_minus_1728_is_27_square_over_cube=bool(is_square), j_minus_1728=str(f),
                vacuum_mu=str(m_closed), vacuum_j_numeric=[jnum.real, jnum.imag],
                vacuum_j_minimal_polynomial_over_Q=str(mp), vacuum_Re_j_minimal_polynomial=str(mre),
                leading_coefficient_factorisation=str(sp.factorint(sp.Poly(mp, X).LC())))


def state_tools():
    T = np.array([[float(sp.sympify(x)) for x in row] for row in json.load(open(C11600))["tensor"]["Bloch_axes"]])
    Xm = np.roll(np.eye(3), 1, axis=0)
    Zm = np.diag([1, w, w * w])
    bases = [np.eye(3)] + [np.linalg.eig(Xm @ np.linalg.matrix_power(Zm, a))[1] for a in range(3)]

    def n_of(psi):
        u0 = (psi ** 3).sum() / np.sqrt(3)
        u1 = np.sqrt(6) * psi.prod()
        c = np.conj(u0) * u1
        return T.T @ np.array([2 * c.real, 2 * c.imag, abs(u0) ** 2 - abs(u1) ** 2]), abs(u0) ** 2 + abs(u1) ** 2

    def Pis(psi):
        return np.array([np.prod(np.abs(B.conj().T @ psi) ** 2) for B in bases])

    def jpsi(psi):
        return jmu((psi ** 3).sum() / (3 * psi.prod()))
    return n_of, Pis, jpsi


def numeric_part(N=20000):
    n_of, Pis, jpsi = state_tools()
    rng = np.random.default_rng(11645)
    F = np.array([[w ** (a * b) for b in range(3)] for a in range(3)]) / np.sqrt(3)
    P = np.diag([1, 1, w])
    sign_agree = 0
    clif = conj = 0
    r1, r2, r3 = [], [], []
    for _ in range(N):
        psi = rng.normal(size=3) + 1j * rng.normal(size=3)
        psi /= np.linalg.norm(psi)
        n, rho = n_of(psi)
        x, y, z = n
        W = (x * x - y * y) * (y * y - z * z) * (z * z - x * x)
        j = jpsi(psi)
        sign_agree += np.sign(j.imag) == np.sign(W)
        clif += np.isclose(jpsi(F @ psi), j, rtol=1e-8) and np.isclose(jpsi(P @ psi), j, rtol=1e-8)
        conj += np.isclose(jpsi(np.conj(psi)), np.conj(j), rtol=1e-8)
        Pi = Pis(psi)
        s = Pi.sum()
        r1.append(abs(j) / (np.prod(s - 2 * Pi) / np.prod(Pi)) ** 1.5)
        r2.append(abs(j - 1728) / ((rho ** 2 - x * x) * (rho ** 2 - y * y) * (rho ** 2 - z * z) / np.prod(Pi) ** 1.5))
        a, b, c, d = Pi
        pair = (6 * (a + b) * (c + d) - s * s) * (6 * (a + c) * (b + d) - s * s) * (6 * (a + d) * (b + c) - s * s)
        r3.append(abs(j - 1728) / (pair / np.prod(Pi) ** 1.5))
    r1, r2 = np.array(r1), np.array(r2)
    C1 = sp.nsimplify(float(np.median(r1)), tolerance=1e-9, rational=False)
    C2 = sp.nsimplify(float(np.median(r2)), tolerance=1e-9, rational=False)
    r3 = np.array(r3)
    out = dict(C3_pairings=str(sp.nsimplify(float(np.median(r3)), tolerance=1e-9, rational=False)),
               C3_spread=float(r3.max() - r3.min()), states=N, sign_Im_j_equals_sign_W=int(sign_agree), j_Clifford_invariant=int(clif),
               j_of_conjugate_is_conjugate=int(conj),
               C1=str(C1), C1_spread=float(r1.max() - r1.min()), C2=str(C2), C2_spread=float(r2.max() - r2.min()))
    # special points
    z9 = np.exp(2j * np.pi / 9)
    out["j_T_plus_state"] = abs(jpsi(np.array([1, z9, 1 / z9]) / np.sqrt(3)))
    out["CP_symmetric_states_have_real_j"] = bool(abs(jpsi(np.array([1, 2, 3.5]) / np.linalg.norm([1, 2, 3.5])).imag) < 1e-9)
    return out


def main():
    res = dict(pass_id=11645)
    res["exact"] = exact_part()
    print(res["exact"], flush=True)
    res["numeric"] = numeric_part()
    print(res["numeric"], flush=True)
    json.dump(res, open(OUT, "w"), indent=1, default=str)


if __name__ == "__main__":
    main()
