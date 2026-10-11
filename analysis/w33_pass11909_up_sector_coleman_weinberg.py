"""Pass 11909: deriving r -- the up-sector Coleman-Weinberg potential for the relative Wilson line.

Setting: the exact magnetized up texture of Passes 11906-11907 at the hierarchy torus Im tau = 4.209 (fixed by the
Gaussian invariant m_u m_c / m_t^2), Yukawas y_c(zeta) = y0 t_c(zeta) with y0 = 0.94, quark masses m_c = y_c v/sqrt2,
v = 246 GeV. At fixed v (the tree potential is zeta-independent) the Wilson-line potential is the zeta-dependent part of
the up-sector one-loop potential (N_c = 3, Dirac fermions):
  * SM with hard cutoff Lambda:  V = -(3/16 pi^2) sum_c [2 Lambda^2 m_c^2 + m_c^4 (ln(m_c^2/Lambda^2) - 1/2)];
  * supersymmetric completion (up squarks of soft mass m~, no mixing; MS-bar at the matching/mediation scale Q):
    V = (3/16 pi^2) sum_c [S_c^2 (ln(S_c/Q^2) - 3/2) - m_c^4 (ln(m_c^2/Q^2) - 3/2)],  S_c = m_c^2 + m~^2.
Expanding in m_c^2: the quadratic coefficient (of sum m_c^2) is set by 2 Lambda^2 (SM) or 2 m~^2 (1 + ln(Q^2/m~^2))
(SUSY; the finite threshold survives at Q = m~), the quartic by ln(m~^2/m_c^2) + O(1); in the units of Pass 11907
r ~ y0^2 v^2 [ln(m~^2/m_t^2) + ...] / (4 m~^2 (1 + ln(Q^2/m~^2))).

Results:
  * SM, Lambda = 0.2 - 5 TeV: the vacuum is the symmetric point nu = 0 (m_c = m_u).
  * SUSY with Q >= m~ (standard mediation, m~ = 0.3 - 3 TeV, Q/m~ = 1.01 - 10): nu = 0 (m_c = m_u).
  * The hierarchical phase exists only in the band e^{-1/2} < Q/m~ < q_hi(m~), where the quadratic coefficient nearly
    cancels; the band width above e^{-1/2} is 0.253 (m~ = 300 GeV), 0.039 (1 TeV), 0.0062 (3 TeV), i.e.
    ~ c (v/m~)^2 with c growing logarithmically (0.38, 0.64, 0.92). The observed up ratios (m_c/m_t = 3.6e-3,
    m_u/m_c = 1.7e-3) are the vacuum at Q/m~ = 0.7706, 0.6307, 0.6103 respectively.
Reading: in the minimal completions the up sector's own loops put the Wilson line at the symmetric point (m_c = m_u).
The hierarchical vacuum of Pass 11907 requires the top sector's Wilson-line-dependent Higgs-mass term to cancel to
O(v^2/m~^2) -- in the MSSM parametrisation only below standard mediation (Q < m~). The up-quark hierarchy is thereby
tied to the naturalness of the top-sector Higgs mass: a little-hierarchy-sized cancellation, growing as (m~/v)^2.
"""

import json
from pathlib import Path

import numpy as np
from scipy.optimize import brentq, minimize

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "w33_pass11909_up_sector_coleman_weinberg.json"
N = np.arange(-40, 41)
TAU, V0, Y0 = 4.209036j, 246.0, 0.94


def th(a, z, Om):
    return np.sum(np.exp(1j * np.pi * (N + a) ** 2 * Om + 2j * np.pi * (N + a) * z))


def masses(x, nu):
    zeta = x + nu * TAU
    g = np.exp(-1.5 * np.pi * zeta.imag ** 2 / TAU.imag)
    return Y0 * g * np.array([abs(th(c / 3, 3 * zeta, 6 * TAU)) for c in range(3)]) * V0 / np.sqrt(2)


def V_SM(p, lam):
    m2 = masses(*p) ** 2
    return -3 / (16 * np.pi ** 2) * np.sum(2 * lam ** 2 * m2 + m2 ** 2 * (np.log(m2 / lam ** 2) - 0.5))


def V_SUSY(p, mt, Q):
    m2 = masses(*p) ** 2
    S = m2 + mt ** 2
    return 3 / (16 * np.pi ** 2) * np.sum(S ** 2 * (np.log(S / Q ** 2) - 1.5) - m2 ** 2 * (np.log(m2 / Q ** 2) - 1.5))


def vac(f):
    best = None
    for x0 in (0.0, 1 / 6):
        for n0 in np.linspace(0, 1 / 3, 13):
            r = minimize(f, [x0, n0], method="Nelder-Mead", options=dict(xatol=1e-10, fatol=1e-14, maxiter=4000))
            if best is None or r.fun < best.fun:
                best = r
    x, nu = best.x[0] % (1 / 3), best.x[1] % (2 / 3)
    nu = min(nu, 2 / 3 - nu)
    return float(nu), np.sort(masses(x, nu))


def main():
    sm = {str(L): vac(lambda p, L=L: V_SM(p, L))[0] for L in (200.0, 500.0, 1000.0, 5000.0)}
    susy_std = {}
    for mt in (300.0, 1000.0, 3000.0):
        for q in (1.01, 1.1, 2.0, 10.0):
            susy_std[f"{mt}|{q}"] = vac(lambda p, mt=mt, q=q: V_SUSY(p, mt, q * mt))[0]
    band = {}
    for mt in (300.0, 1000.0, 3000.0):
        def hess(q, h=1e-4):
            f = lambda nu: V_SUSY([0, nu], mt, q * mt)  # noqa: E731
            return (f(h) - 2 * f(0) + f(-h)) / h ** 2
        q_hi = brentq(hess, 0.607, 0.99)
        q_star = brentq(lambda q: vac(lambda p: V_SUSY(p, mt, q * mt))[0] - 0.1205681, 0.6066, q_hi - 1e-6, xtol=1e-8)
        nu, m = vac(lambda p: V_SUSY(p, mt, q_star * mt))
        w = q_hi - np.exp(-0.5)
        band[str(mt)] = dict(q_hi=float(q_hi), width_above_e_minus_half=float(w), width_times_mt_over_v_sq=float(w * (mt / V0) ** 2),
                             q_star=float(q_star), mc_over_mt=float(m[1] / m[2]), mu_over_mc=float(m[0] / m[1]))
    res = dict(pass_id=11909, sm_vacuum_nu=sm, susy_standard_mediation_nu=susy_std, hierarchical_band=band)
    ws = [band[k]["width_above_e_minus_half"] for k in ("300.0", "1000.0", "3000.0")]
    res["checks"] = {k: bool(v) for k, v in dict(
        sm_always_symmetric=all(v < 1e-6 for v in sm.values()),
        susy_standard_mediation_symmetric=all(v < 1e-6 for v in susy_std.values()),
        band_above_e_minus_half=all(b["q_hi"] > np.exp(-0.5) for b in band.values()),
        band_shrinks_like_v_over_m_squared=ws[0] > ws[1] > ws[2] and 0.2 < band["1000.0"]["width_times_mt_over_v_sq"] < 2,
        observed_ratios_inside_band=all(abs(b["mc_over_mt"] - 3.6e-3) < 1e-6 and abs(b["mu_over_mc"] - 1.7e-3) < 1e-6
                                        for b in band.values()),
    ).items()}
    res["all_checks_pass"] = all(res["checks"].values())
    OUT.write_text(json.dumps(res, indent=2))
    print(json.dumps(res, indent=1))


if __name__ == "__main__":
    main()
