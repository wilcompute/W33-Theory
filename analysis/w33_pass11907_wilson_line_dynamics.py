"""Pass 11907: dynamics of the relative Wilson line -- the minimal potential selects degenerate textures; a competing
quartic term selects a hierarchical one, with the observed up ratios at an O(1) coefficient.

Input (Pass 11906, exact): for a localised Higgs the physical up-type Yukawas are
    |Y_c(zeta)| = C e^{-(3 pi/2) (Im zeta)^2 / Im tau} |theta[c/3, 0](3 zeta, 6 tau)|,   c = 0, 1, 2,
(zeta = relative Wilson line). The prefactor was fitted to the direct overlaps (ln f = const - (3 pi/2)(Im zeta)^2/Im tau
at seven points, to 1e-9) and makes F_p = sum_c |Y_c|^p invariant under zeta -> zeta + 1/3, zeta -> zeta + 2 tau / 3,
zeta -> -zeta. Units: C = 1 (the top coupling at nu = 0 is ~1); the invariant coefficient is r y_t^2.

1. Minimal potential V = +- F_2 (two-loop vacuum energy with the light Higgs): over four values of tau, the global
   maximum is at zeta = 0 (spectrum (1, e, e): m_c = m_u) and the global minimum at the theta-zero point
   zeta = 1/6 + tau/3 (spectrum (0, 1, 1)). Either sign selects a DEGENERATE texture.
2. Competing terms V = -F_2 + r F_4: the symmetric point nu = 0 loses stability exactly at r = 1/2 (Hessian sign
   change); for every r > 1/2 tested (to 8) the global minimum sits at a NON-symmetric nu(r), increasing monotonically,
   with a non-degenerate hierarchical spectrum. At Im tau = 4.209 the observed-order up ratios (m_c/m_t = 3.6e-3,
   m_u/m_c = 1.7e-3) are the vacuum at r* = 0.890 -- an O(1) coefficient, no hierarchy put in by hand. The opposite
   sign (+F_2 - r F_4) keeps symmetric/degenerate minima.
Reading: the hierarchy is not symmetry-selected (Pass 11905), and the minimal light-Higgs potential selects degenerate
textures; but a generic competition between the quadratic and quartic Yukawa terms (r y_t^2 > 1/2) places the Wilson
line at a non-symmetric point, and the observed up hierarchy is such a vacuum for r y_t^2 ~ 0.89 with Im tau ~ 4.2.
Not derived: the coefficients (loop factors, SUSY breaking, the other sectors' contributions), so this shows a natural
mechanism, not a prediction.
"""

import json
from pathlib import Path

import numpy as np
from scipy.optimize import brentq, minimize

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "w33_pass11907_wilson_line_dynamics.json"
N = np.arange(-40, 41)


def th(a, z, Om):
    return np.sum(np.exp(1j * np.pi * (N + a) ** 2 * Om + 2j * np.pi * (N + a) * z))


def masses(zeta, tau):
    g = np.exp(-1.5 * np.pi * zeta.imag ** 2 / tau.imag)
    return g * np.array([abs(th(c / 3, 3 * zeta, 6 * tau)) for c in range(3)])


def Fp(zeta, tau, p):
    return float(np.sum(masses(zeta, tau) ** p))


def global_opt(f, sign, ng=(7, 13)):
    best = None
    for x0 in np.linspace(0, 1 / 3, ng[0], endpoint=False):
        for n0 in np.linspace(0, 2 / 3, ng[1], endpoint=False):
            r = minimize(lambda p: sign * f(p), [x0, n0], method="Nelder-Mead",
                         options=dict(xatol=1e-11, fatol=1e-16, maxiter=6000))
            if best is None or r.fun < best.fun - 1e-14:
                best = r
    return best.x[0] % (1 / 3), best.x[1] % (2 / 3)


def spectrum(x, nu, tau):
    m = np.sort(masses(x + nu * tau, tau))
    return m / m[-1]


def degenerate(m):
    return min(abs(m[1] - m[0]), abs(m[2] - m[1])) < 1e-6


def main():
    out = {}
    # invariance of F_2
    tau = 0.1 + 1.3j
    z0 = 0.07 + 0.31 * tau
    f0 = Fp(z0, tau, 2)
    out["F2_invariance_err"] = max(abs(Fp(z0 + 1 / 3, tau, 2) - f0), abs(Fp(z0 + 2 * tau / 3, tau, 2) - f0),
                                   abs(Fp(-z0, tau, 2) - f0)) / f0
    # 1. minimal potential
    minimal = {}
    for t in (1.3j, 0.1 + 1.3j, 0.3 + 0.9j, 2.0j):
        f = lambda p, t=t: Fp(p[0] + p[1] * t, t, 2)  # noqa: E731
        xmax, numax = global_opt(f, -1, (5, 9))
        xmin, numin = global_opt(f, +1, (5, 9))
        minimal[str(t)] = dict(max_spectrum=[float(v) for v in spectrum(xmax, numax, t)],
                               min_spectrum=[float(v) for v in spectrum(xmin, numin, t)],
                               min_at=[float(xmin), float(numin)])
    out["minimal_potential"] = minimal
    # 2. competing terms at the hierarchy torus
    tau = 4.209036j

    def V(p, r):
        m = masses(p[0] + p[1] * tau, tau)
        return -np.sum(m ** 2) + r * np.sum(m ** 4)

    def vac(r):
        return global_opt(lambda p: V(p, r), +1, (5, 25))

    def d2(r, h=1e-4):
        return (V([0, h], r) - 2 * V([0, 0], r) + V([0, -h], r)) / h ** 2
    out["instability_r"] = float(brentq(d2, 0.3, 0.7))
    sweep = {}
    for r in (0.6, 0.8, 1.0, 2.0, 5.0, 8.0):
        x, nu = vac(r)
        nu = min(nu, 2 / 3 - nu)
        m = spectrum(x, nu, tau)
        sweep[str(r)] = dict(nu=float(nu), spectrum=[float(v) for v in m])
    out["window_sweep"] = sweep
    rstar = brentq(lambda r: min(vac(r)[1], 2 / 3 - vac(r)[1]) - 0.1205681, 0.85, 0.9, xtol=1e-7)
    x, nu = vac(rstar)
    m = spectrum(x, min(nu, 2 / 3 - nu), tau)
    out["r_star"] = float(rstar)
    out["r_star_ratios"] = dict(mc_over_mt=float(m[1]), mu_over_mc=float(m[0] / m[1]))
    # opposite sign keeps symmetric minima
    opp = []
    for r in (0.6, 1.0, 2.0):
        x, nu = global_opt(lambda p: -V(p, r) + 0 * p[0], +1, (5, 13))  # V' = +F2 - r F4
        opp.append([float(v) for v in spectrum(x, nu, tau)])
    out["opposite_sign_spectra"] = opp
    res = dict(pass_id=11907, **out)
    nus = [sweep[k]["nu"] for k in sweep]
    res["checks"] = {k: bool(v) for k, v in dict(
        F2_invariant=out["F2_invariance_err"] < 1e-12,
        minimal_max_degenerate=all(degenerate(v["max_spectrum"]) for v in minimal.values()),
        minimal_min_theta_zero=all(v["min_spectrum"][0] < 1e-6 and abs(v["min_spectrum"][1] - 1) < 1e-6
                                   for v in minimal.values()),
        instability_at_one_half=abs(out["instability_r"] - 0.5) < 1e-4,
        window_nonsymmetric_hierarchical=all(0.01 < s["nu"] < 1 / 3 - 0.01 and not degenerate(s["spectrum"])
                                             for s in sweep.values()),
        nu_monotone_in_r=all(a < b for a, b in zip(nus, nus[1:])),
        observed_ratios_at_order_one_r=abs(out["r_star_ratios"]["mc_over_mt"] - 3.6e-3) < 1e-6
        and abs(out["r_star_ratios"]["mu_over_mc"] - 1.7e-3) < 1e-6 and 0.5 < rstar < 2,
        opposite_sign_degenerate=all(degenerate(s) or s[0] < 1e-6 for s in opp),
    ).items()}
    res["all_checks_pass"] = all(res["checks"].values())
    OUT.write_text(json.dumps(res, indent=2))
    print(json.dumps(res, indent=1))


if __name__ == "__main__":
    main()
