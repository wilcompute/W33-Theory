"""Pass 11906: magnetized normalisation audit by direct overlap integrals -- the level-3 texture of 11904/11905 is exact.

Normalised zero modes on T^2 (z = x + tau y, unit-area convention, mean |psi|^2 = 1 over the unit cell):
    psi^{j,M}(z; zeta) ~ exp(i pi M w Im(w)/Im tau) theta[j/M, 0](M w, M tau),  w = z + zeta,
fluxes 3 (left), 3 (right), 6 (Higgs), with zeta_3 = (3 zeta_1 + 3 zeta_2)/6. Yukawas Y_{ijk} = <psi_i psi_j conj(psi_k)>
are computed as overlap integrals on a grid (spectrally accurate for these smooth periodic integrands). The relative
Wilson line is zeta = zeta_1 - zeta_2 (zeta_1 = zeta/2, zeta_2 = -zeta/2); nu = Im zeta / Im tau.

Results:
  * Cross-check with the parallel track (TOE46 front 4, equal backgrounds, tau = 1.45 i): lowest allowed overlap
    0.0031126747 reproduced; selection rule k = i + j mod 3 (forbidden overlaps at round-off).
  * EXACT DICTIONARY: for a localised Higgs the normalised physical masses equal |theta[c/3, 0](3 zeta, 6 tau)|,
    c = 0, 1, 2, up to a permutation (random tau and zeta, to 1e-14). The level-3 texture of Passes 11904-11905 is
    therefore the physical magnetized texture with z = 3 zeta (relative Wilson line times the flux), Omega = 6 tau.
  * Hence both results hold in true normalisation:
      - theta-zero law: at zeta with 3 zeta = z* (Re zeta = 1/6, e.g. Im zeta / Im tau = 1/3, 1, 5/3) one mass vanishes
        exactly and the other two are equal (massless up forces top = charm);
      - symmetric points zeta = m/6 + k tau/3 (z = m/2 + k Omega/6): two masses coincide exactly; at the non-fixed
        points Im zeta / Im tau = 1/6, 1/2, 5/6 (Re zeta = 0) nothing coincides.
    The Re-zeta dependence is real (O(1) near zeros at small Im tau), not a pure phase.
  * Gaussian invariant m_1 m_2 / m_0^2 = e^{-(4 pi/3) Im tau} = e^{-2 pi Im Omega / 9} for generic nu; the observed-order
    up ratios are reached by the physical overlaps at Im tau = 4.209, nu = Im zeta / Im tau = 0.1206 -- exactly the
    11904 point (Im Omega = 25.25, delta = nu/2 = 0.0603), found here independently.
Drafting note: an intermediate draft of this pass claimed that Re zeta enters only as a phase and that the physical
masses never vanish; both came from scanning only Re zeta = 0, nu in [0, 1). The direct test at Re zeta = 1/6 refuted
them before commit.
"""

import json
from pathlib import Path

import numpy as np
from scipy.optimize import fsolve

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "w33_pass11906_magnetized_normalisation_audit.json"
NN = np.arange(-25, 26)


def theta(a, nu, T):
    return np.sum(np.exp(1j * np.pi * (NN + a) ** 2 * T + 2j * np.pi * np.multiply.outer(nu, NN + a)), axis=-1)


class Torus:
    def __init__(self, tau, G):
        self.tau = tau
        xs = (np.arange(G) + 0.5) / G
        X, Yg = np.meshgrid(xs, xs, indexing="ij")
        self.Z = X + tau * Yg

    def psi(self, j, M, zeta):
        w = self.Z + zeta
        p = np.exp(1j * np.pi * M * w * w.imag / self.tau.imag) * theta(j / M, M * w, M * self.tau)
        return p / np.sqrt(np.mean(abs(p) ** 2))

    def yuk(self, z1, z2, ks=range(6)):
        z3 = (3 * z1 + 3 * z2) / 6
        L = [self.psi(i, 3, z1) for i in range(3)]
        R = [self.psi(j, 3, z2) for j in range(3)]
        Y = {}
        for k in ks:
            H = np.conj(self.psi(k, 6, z3))
            for i in range(3):
                for j in range(3):
                    Y[(i, j, k)] = np.mean(L[i] * R[j] * H)
        return Y

    def masses(self, zeta, k=0):
        Y = self.yuk(zeta / 2, -zeta / 2, ks=[k])
        return np.array([abs(Y[(i, (k - i) % 3, k)]) for i in range(3)])


def main():
    out = {}
    # cross-check with TOE46 (equal backgrounds, tau = 1.45 i)
    T0 = Torus(1.45j, 144)
    Y = T0.yuk(0, 0)
    allowed = [abs(v) for (i, j, k), v in Y.items() if (i + j - k) % 3 == 0]
    forbidden = [abs(v) for (i, j, k), v in Y.items() if (i + j - k) % 3 != 0]
    out["toe46_lowest_allowed"] = float(min(allowed))
    out["max_forbidden"] = float(max(forbidden))
    # exact dictionary to the level-3 texture
    rng = np.random.default_rng(11906)
    dict_err = 0.0
    import itertools
    for _ in range(6):
        tau = rng.normal() * 0.4 + 1j * (0.8 + 1.5 * rng.random())
        Tq = Torus(tau, 200)
        zeta = rng.random() + rng.random() * 2 * tau
        m = Tq.masses(zeta)
        m = m / m.max()
        t = np.array([abs(theta(c / 3, np.array([3 * zeta]), 6 * tau)[0]) for c in range(3)])
        best = min(np.max(abs(t[list(pp)] / t.max() - m)) for pp in itertools.permutations(range(3)))
        dict_err = max(dict_err, best)
    out["dictionary_max_err"] = float(dict_err)
    T = Torus(0.2 + 2.5j, 220)
    # theta-zero law in true normalisation (Im tau = 1.2)
    Tz = Torus(1.2j, 200)
    zl = []
    for nu in (1 / 3, 1.0, 5 / 3):
        m = Tz.masses(1 / 6 + nu * Tz.tau)
        m = np.sort(m / m.max())
        zl.append([float(x) for x in m])
    out["theta_zero_points"] = zl
    # symmetric points
    sym = {}
    for nu in (0, 1 / 6, 1 / 3, 1 / 2, 2 / 3, 5 / 6):
        m = T.masses(nu * T.tau)
        m = m / m.max()
        d = {f"{a},{b}": float(abs(m[a] - m[b])) for a, b in ((0, 1), (0, 2), (1, 2))}
        sym[f"{nu:.4f}"] = dict(masses=[float(x) for x in m], gaps=d)
    out["symmetric_scan"] = sym
    # no zeros, Gaussian invariant
    grid = np.linspace(0, 1, 61, endpoint=False)
    invs = []
    for nu in grid:
        m = np.sort(T.masses(nu * T.tau))[::-1]
        invs.append(m[1] * m[2] / m[0] ** 2)
    pred = float(np.exp(-4 * np.pi / 3 * T.tau.imag))
    generic = [x for x, nu in zip(invs, grid) if min(abs(nu - c) for c in (1 / 3, 2 / 3, 1.0, 0.0)) > 0.12]
    out["invariant_predicted"] = pred
    out["invariant_generic_range"] = [float(min(generic)), float(max(generic))]
    # physical fit for observed-order up ratios
    target = (np.log(3.6e-3), np.log(1.7e-3))

    def eqs(p):
        Tp = Torus(1j * p[0], 260)
        m = np.sort(Tp.masses(p[1] * Tp.tau))[::-1]
        return [np.log(m[1] / m[0]) - target[0], np.log(m[2] / m[1]) - target[1]]
    fit = fsolve(eqs, [4.2, 0.12], xtol=1e-10)
    out["fit_im_tau_nu"] = [float(x) for x in fit]
    out["fit_residual"] = [float(x) for x in eqs(fit)]
    gp = lambda nu: min(sym[f"{nu:.4f}"]["gaps"].values())  # noqa: E731
    res = dict(pass_id=11906, **out)
    res["checks"] = {k: bool(v) for k, v in dict(
        reproduces_toe46=abs(out["toe46_lowest_allowed"] - 0.0031126747) < 1e-8 and out["max_forbidden"] < 1e-12,
        exact_dictionary_z_3zeta_omega_6tau=out["dictionary_max_err"] < 1e-12,
        theta_zero_law_physical=all(z[0] < 1e-10 and abs(z[1] - z[2]) < 1e-10 for z in out["theta_zero_points"]),
        coincide_at_0_third_two_thirds=gp(0) < 1e-10 and gp(1 / 3) < 1e-10 and gp(2 / 3) < 1e-10,
        no_coincidence_at_sixths=min(gp(1 / 6), gp(1 / 2), gp(5 / 6)) > 1e-4,
        gaussian_invariant=abs(np.log(out["invariant_generic_range"][0] / pred)) < 0.02
        and abs(np.log(out["invariant_generic_range"][1] / pred)) < 0.02,
        fit_reached_at_nonsymmetric_nu=max(abs(x) for x in out["fit_residual"]) < 1e-8
        and min(abs(fit[1] - c) for c in (0, 1 / 3, 2 / 3, 1)) > 0.03,
        fit_equals_pass11904_point=abs(6 * fit[0] - 25.254) < 0.01 and abs(fit[1] / 2 - 0.0603) < 1e-3,
    ).items()}
    res["all_checks_pass"] = all(res["checks"].values())
    OUT.write_text(json.dumps(res, indent=2))
    print(json.dumps({k: v for k, v in res.items() if k != "symmetric_scan"}, indent=1))


if __name__ == "__main__":
    main()
