"""Pass 12048: canonical modular-invariant moduli potentials do not select the flavour moduli. They repel the product
locus where the hierarchy lives, and their minima carry no hierarchy (Claude track).

Potentials: N = 1 supergravity, V = e^K (K^{i jbar} D_i W conj(D_j W) - 3 |W|^2).
  genus 1: K = -3 log(2 Im tau), W = eta(tau)^-6  (Font-Ibanez-Lust-Quevedo 1990; Cvetic et al. 1991).
  genus 2: K = -3 log det(2 Im Omega), W = chi10(Omega)^(-3/10). This is the unique power of the Igusa cusp form that
           makes e^K |W|^2 Sp(4,Z)-invariant. chi10 = -2^-14 prod of the ten even theta constants squared, evaluated
           branch-free (d log W = -0.3 d chi10/chi10, |W|^2 = |chi10|^-0.6).
Results.
 1. Genus 1: the minimum is at tau = 1.2346 i (control: the classic 1.23 i). Its SL(2,Z) orbit meets the CP line
    Re tau = 1 at y = 1.2346 and y = 0.810. With eps_u refitted to m_c/m_t at each, m_u m_t/m_c^2 is far from the data
    0.534 +- 3.3% at both. The fitted up modulus sits at 1.1435 i in the fundamental domain.
 2. Genus 2, near the product locus Omega_12 = eps -> 0 (where the up hierarchy (1, eps, eps^2) lives, Pass 11872):
    chi10 -> pi^2 eps^2 Delta(tau1) Delta(tau2) (checked to 1e-5, an exact control of the chi10 evaluation), so the eps F-term dominates and
    V ~ |eps|^(-16/5) -> +infinity (measured log slope 3.20). The canonical potential REPELS the hierarchy locus; at the
    fitted eps_u = 0.0055 it is large, positive and steep.
 3. Genus 2, symmetric CP-locus home [[tau, eps], [eps, tau]]: the minimum is at Im eps/Im tau = 1/2 (to 2e-6),
    Im tau = 1.2721, V = -83.39 (an equivalent image sits at 1.0482). So Im Omega is proportional to the Gram matrix of
    the A2 (Eisenstein) lattice, a point with enhanced stabiliser. The canonical potential selects the A2-symmetric
    abelian surface -- the lattice native to the qutrit structure -- but that point has no hierarchy: m_2/m_1 = 0.18-0.31
    against m_c/m_t = 0.0037.
Reading. The canonical invariant potentials stabilise the moduli at symmetric points, away from the near-product region
that the flavour hierarchy requires. The up hierarchy therefore needs a non-canonical stabilisation (matter or
threshold factors H(j)-like, fluxes, or a different mechanism). This makes the "moduli are free" problem of
12004-12047 concrete: the natural potentials point the wrong way.
Scope: two canonical potentials (no dilaton dynamics, no H-factors); the genus-2 minimum is on the symmetric CP-locus
slice only. Not new: the genus-1 minimum (FILQ 1990, CFILQ 1991); chi10 as the genus-2 analogue of Delta; Siegel
modular flavour (Ding-Feruglio-Liu arXiv:2010.07952); hierarchies near fixed points (Novichkov-Penedo-Petcov,
Feruglio et al.); Codex 11950 uses chi10 as a divisor in the gauge kinetic function (different use).
"""

import itertools
import json
import sys
from pathlib import Path

import numpy as np
from scipy.optimize import brentq, minimize

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "analysis"))
from w33_pass11942_hypercharge_wilson_leptons import DATA, theta  # noqa: E402

OUT = ROOT / "data" / "w33_pass12048_canonical_moduli_potentials.json"
UP_Y = 0.8744698731421595
W_DATA, W_ERR = 1.967e-3 / DATA["mc_mt"], 0.0334


def eta(t, N=80):
    q = np.exp(2j * np.pi * t)
    return np.exp(2j * np.pi * t / 24) * np.prod([1 - q ** n for n in range(1, N)])


def E2(t, N=200):
    q = np.exp(2j * np.pi * t)
    return 1 - 24 * sum(n * q ** n / (1 - q ** n) for n in range(1, N))


def V1(t):
    y = t.imag
    return float(((2 * y) ** -3 * abs(eta(t)) ** -12 * ((y * y * np.pi ** 2 / 3) * abs(E2(t) - 3 / (np.pi * y)) ** 2 - 3)).real)


def theta2(Om, a, b, N=8):
    n = np.arange(-N, N + 1)
    X, Y = np.meshgrid(n + a[0] / 2, n + a[1] / 2, indexing="ij")
    return np.exp(1j * np.pi * (Om[0, 0] * X * X + 2 * Om[0, 1] * X * Y + Om[1, 1] * Y * Y) + 2j * np.pi * (X * b[0] + Y * b[1]) / 2).sum()


EVEN = [(a, b) for a in itertools.product((0, 1), repeat=2) for b in itertools.product((0, 1), repeat=2) if (a[0] * b[0] + a[1] * b[1]) % 2 == 0]


def chi10(Om):
    return -2.0 ** -14 * np.prod([theta2(Om, a, b) ** 2 for a, b in EVEN])


def om(p):
    return np.array([[p[0], p[2]], [p[2], p[1]]])


def V2(p, h=1e-6, s=1e-4):
    if np.linalg.eigvalsh(om(p).imag).min() <= 0:
        return np.inf
    K = lambda q: -3 * np.log(np.linalg.det(2 * om(q).imag))  # noqa: E731
    c0 = chi10(om(p))
    F = []
    for i in range(3):
        e = np.zeros(3, complex)
        e[i] = h
        dlogW = -0.3 * (chi10(om(p + e)) - chi10(om(p - e))) / (2 * h) / c0
        dK = (K(p + e) - K(p - e)) / (4 * h) - 1j * (K(p + 1j * e) - K(p - 1j * e)) / (4 * h)
        F.append(dlogW + dK)
    G = np.zeros((3, 3), complex)
    for i in range(3):
        for j in range(3):
            ei, ej = np.zeros(3, complex), np.zeros(3, complex)
            ei[i] = ej[j] = s
            f = lambda a, b: K(p + a * ei + b * ej)  # noqa: E731
            Kxx = (f(1, 1) - f(1, -1) - f(-1, 1) + f(-1, -1)) / (4 * s * s)
            Kyy = (f(1j, 1j) - f(1j, -1j) - f(-1j, 1j) + f(-1j, -1j)) / (4 * s * s)
            Kxy = (f(1, 1j) - f(1, -1j) - f(-1, 1j) + f(-1, -1j)) / (4 * s * s)
            Kyx = (f(1j, 1) - f(1j, -1) - f(-1j, 1) + f(-1j, -1)) / (4 * s * s)
            G[i, j] = 0.25 * (Kxx + Kyy + 1j * (Kxy - Kyx))
    F = np.array(F)
    return float(np.exp(K(p)) * abs(c0) ** -0.6 * ((F @ np.linalg.inv(G).T @ F.conj()).real - 3))


def up_W(y):
    def rat(e):
        s = np.linalg.svd(theta(np.array([[1 + 1j * y, 1j * e], [1j * e, 1 + 1j * y]])), compute_uv=False)
        return s[1] / s[0], s[2] / s[1]
    e = brentq(lambda e: rat(e)[0] - DATA["mc_mt"], 1e-6, 0.4)
    r = rat(e)
    return r[1] / r[0]


def main():
    checks, res = {}, {}
    r1 = minimize(lambda p: V1(p[0] + 1j * p[1]), [0.0, 1.2], method="Nelder-Mead", options=dict(xatol=1e-10, fatol=1e-14))
    t1 = r1.x[0] + 1j * r1.x[1]
    Ws = {"y=1.2346": up_W(t1.imag), "y=0.810": up_W(1 / t1.imag)}
    res["genus1"] = dict(min_tau=[float(t1.real), float(t1.imag)], V=float(r1.fun), fitted_up_in_fd=1 / UP_Y,
                         W_on_CP_line=Ws, W_data=W_DATA, pulls={k: float(np.log(v / W_DATA) / W_ERR) for k, v in Ws.items()})
    checks["genus 1: minimum 1.2346 i (classic); its CP-line images miss m_u m_t/m_c^2 by > 5 sigma"] = bool(
        abs(t1.imag - 1.2346) < 1e-3 and abs(t1.real) < 1e-6 and min(abs(v) for v in res["genus1"]["pulls"].values()) > 5)

    tau = 1 + 1j * UP_Y
    D = eta(tau) ** 24
    ratio = [complex(chi10(np.array([[tau, 1j * d], [1j * d, tau]])) / ((1j * d) ** 2 * D * D)) for d in (1e-2, 1e-3, 1e-4)]
    res["chi10_product_limit"] = [[r.real, r.imag] for r in ratio]
    checks["control: chi10 / (eps^2 Delta(tau1) Delta(tau2)) -> pi^2 on the product locus"] = bool(
        abs(ratio[2] / np.pi ** 2 - 1) < 1e-5 and abs(ratio[2].imag) < 1e-10)

    vs = {d: V2(np.array([tau, tau, 1j * d])) for d in (0.002, 0.001, 0.0055, 0.3)}
    slope = np.log(vs[0.001] / vs[0.002]) / np.log(2)
    res["genus2_product_locus"] = dict(V=vs, log_slope=float(slope))
    checks["genus 2: V ~ |eps|^(-16/5) near the product locus (repelled); V > 0 at eps_u = 0.0055"] = bool(
        abs(slope - 3.2) < 0.02 and vs[0.0055] > 1e6 and vs[0.3] < 0)

    r2 = minimize(lambda q: V2(np.array([1 + 1j * q[0], 1 + 1j * q[0], 1j * q[1]])) if 0 < q[1] < 0.95 * q[0] else 1e9,
                  [1.27, 0.63], method="Nelder-Mead", options=dict(xatol=1e-8, fatol=1e-11))
    y2, d2 = r2.x
    s = np.linalg.svd(theta(np.array([[1 + 1j * y2, 1j * d2], [1j * d2, 1 + 1j * y2]])), compute_uv=False)
    res["genus2_symmetric_min"] = dict(tau=[1.0, float(y2)], eps=float(d2), eps_over_tau=float(d2 / y2), V=float(r2.fun),
                                       m2_m1=float(s[1] / s[0]), m3_m2=float(s[2] / s[1]))
    checks["genus 2 symmetric-home minimum at Im Omega ~ A2 Gram matrix (Im eps/Im tau = 1/2), no hierarchy (m2/m1 > 0.1)"] = bool(
        abs(d2 / y2 - 0.5) < 1e-4 and abs(r2.fun + 83.39) < 0.05 and s[1] / s[0] > 0.1)

    res["checks"] = checks
    res["all_checks_pass"] = all(checks.values())
    OUT.write_text(json.dumps(res, indent=2, default=float))
    print(json.dumps(checks, indent=1), res["all_checks_pass"])
    return res


if __name__ == "__main__":
    main()
