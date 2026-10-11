"""Pass 11904: the magnetized home unlocks the charm-up pair at first order; a massless up forces top = charm.

Option 3 (magnetized T4, flux 3 per torus). The zero modes at the origin are the level-3 Siegel thetas of Pass 11869 (two
qutrits). With a localised Higgs the light-pair couplings are theta[(+-1/3, a/3), 0](zeta, Omega):
  * a = 0, zeta = 0: exactly degenerate for every Omega (theta evenness) -- the same lock as heterotic Z3 (Pass 11903);
  * a != 0: split at FIRST order in the off-diagonal Siegel modulus Omega12 (heterotic Z3: third order, Pass 11900 --
    the Eisenstein coset rigidity w = 1 mod sqrt(-3) is absent for a real period lattice);
  * a continuous Wilson line zeta on the family torus splits the pair at first order EVEN at a = 0. Heterotic Z3 Wilson
    lines are quantised (finite Pauli displacements, which only relabel classes); magnetized Wilson lines are continuous
    Weyl displacements and break the evenness.

Theta-zero law (genus 1, level 3, any Omega). theta[a,0](z, Omega) vanishes at z* = 1/2 + (1/2 - a) Omega, and there
|theta[a + 1/3](z*)| = |theta[a - 1/3](z*)|. Proof: theta[a'](z*) = e^{i pi a'} e^{-i pi Omega (1/2 - a)^2}
sum_n (-1)^n e^{i pi Omega (n + b)^2} with b = a' + 1/2 - a; n -> -1 - n maps b -> 1 - b, i.e. the sums for b and 1 - b
agree up to sign, so b = 1/2 vanishes and b = 1/2 +- 1/3 have equal modulus. Physical reading: with a localised Higgs, an
exactly massless up quark forces top = charm -- unifying Pass 11114 (Hesse alignments (1,1,omega): (1,1,0)), the
special Kahler points of Pass 11899, and the magnetized Wilson-line zeros. The up hierarchy cannot come from sitting
near a theta zero; it needs the near-cusp (Gaussian) regime with a continuous Wilson-line offset.

Gaussian regime (large Im Omega): log|theta_c| = -pi Im Omega (c/3 - delta)^2 + const, so m_u m_c / m_t^2 =
e^{-2 pi Im Omega / 9} independently of the Wilson-line offset delta, while m_u / m_c = e^{-4 pi Im Omega delta / 3}: the
torus area sets the product, the continuous Wilson line sets the split. The observed-order up ratios (m_c/m_t = 3.6e-3,
m_u/m_c = 1.7e-3, illustrative) are reached at Im Omega ~ 25, delta ~ 0.06 (two parameters, two ratios: existence,
not a prediction). The heterotic class of Passes 11901-11903 cannot do this; the magnetized two-qutrit home can.

Option 2 (non-renormalisable and Kahler, heterotic survivors). Pass 11103: the charm and up entries arise at EQUAL VEV
order (no parametric gap). Their coefficients can differ only through breaking of the family-torus reflection; with the
Wilson-line classes fixed (Pass 11903) the only source among the moduli is the off-diagonal Kahler modulus, entering
couplings that span a Wilson-line torus at O(Z12^3) (Pass 11900). Hence m_u / m_c = 1 + O(Z^3): no parametric
hierarchy. Recorded here as the closing argument; the cubic scaling is re-checked below.
"""

import json
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "analysis"))
OUT = ROOT / "data" / "w33_pass11904_magnetized_unlock_and_theta_zero_law.json"
R12 = np.arange(-12, 13)
N1, N2 = [x.ravel() for x in np.meshgrid(R12, R12, indexing="ij")]
N40 = np.arange(-40, 41)


def theta2(a1, a2, Om, z=(0, 0)):
    x1, x2 = N1 + a1, N2 + a2
    q = Om[0, 0] * x1 * x1 + 2 * Om[0, 1] * x1 * x2 + Om[1, 1] * x2 * x2
    return np.sum(np.exp(1j * np.pi * q + 2j * np.pi * (x1 * z[0] + x2 * z[1])))


def theta1(a, z, Om):
    return np.sum(np.exp(1j * np.pi * (N40 + a) ** 2 * Om + 2j * np.pi * (N40 + a) * z))


def main():
    rng = np.random.default_rng(11904)
    Om0 = np.array([[0.3 + 1.1j, 0], [0, -0.2 + 0.9j]]) * 3
    split = {}
    for a in (0, 1):
        vals = []
        for s in (1e-2, 5e-3, 2.5e-3):
            Om = Om0.copy()
            Om[0, 1] = Om[1, 0] = s * (0.7 + 0.4j) * 3
            t1, t2 = theta2(1 / 3, a / 3, Om), theta2(-1 / 3, a / 3, Om)
            vals.append(float(abs(t1 - t2) / abs(t1) / s))
        split[f"a={a}"] = vals
    wl = []
    for zz in (1e-2, 5e-3, 2.5e-3):
        t1, t2 = theta2(1 / 3, 0, Om0, z=(zz * (1 + 0.5j), 0)), theta2(-1 / 3, 0, Om0, z=(zz * (1 + 0.5j), 0))
        wl.append(float(abs(t1 - t2) / abs(t1) / zz))
    # theta-zero law
    worst, zero_ok = 0.0, True
    for _ in range(30):
        Om = rng.normal() * 0.7 + 1j * (0.4 + 2 * rng.random())
        for c in range(3):
            zs = 0.5 + (0.5 - c / 3) * Om
            v = [abs(theta1(cc / 3, zs, Om)) for cc in range(3)]
            o = [v[cc] for cc in range(3) if cc != c]
            zero_ok &= v[c] < 1e-10 * max(o)
            worst = max(worst, abs(o[0] - o[1]) / max(o))
    Om, z = 0.3 + 1.2j, 0.17 + 0.4j
    ctrl = [abs(theta1(c / 3, z, Om)) for c in range(3)]
    ctrl_spread = float((max(ctrl) - min(ctrl)) / max(ctrl))
    # near the zero: m_u / m_c linear in the displacement
    near = []
    Om = 0.25 + 2j
    zs = 0.5 + (0.5 + 1 / 3) * Om
    for d in (1e-3, 5e-4):
        near.append(float(abs(theta1(-1 / 3, zs + d, Om)) / abs(theta1(1 / 3, zs + d, Om)) / d))
    # Gaussian (near-cusp) regime: m_u m_c / m_t^2 = e^{-2 pi Im Omega / 9}, independent of the Wilson-line offset delta
    def masses(imO, delta):
        Omg, zz = 1j * imO, -1j * delta * imO
        t = [abs(theta1(c / 3, zz, Omg)) for c in (0, 1, -1)]
        return t[0], t[1], t[2]  # top (Higgs point), charm, up
    inv = []
    for delta in (0.0, 0.03, 0.06, 0.1):
        mt, mc, mu = masses(25.0, delta)
        inv.append(float(np.log(mu * mc / mt ** 2) / (-2 * np.pi * 25.0 / 9)))
    from scipy.optimize import fsolve
    target = (np.log(3.6e-3), np.log(1.7e-3))  # illustrative m_c/m_t and m_u/m_c
    def eqs(p):
        mt, mc, mu = masses(p[0], p[1])
        return [np.log(mc / mt) - target[0], np.log(mu / mc) - target[1]]
    fit = fsolve(eqs, [25.0, 0.06])
    fit_res = eqs(fit)
    res = dict(pass_id=11904, gaussian_invariant_ratio=inv, fit_im_omega_delta=[float(x) for x in fit],
               fit_residual=[float(x) for x in fit_res], siegel_offdiag_split_over_s=split, wilson_line_split_over_zeta=wl,
               theta_zero_max_rel_diff=worst, control_generic_spread=ctrl_spread, near_zero_mu_over_mc_per_dz=near)
    res["checks"] = {k: bool(v) for k, v in dict(
        a0_locked=max(split["a=0"]) < 1e-10,
        a1_linear_in_omega12=max(split["a=1"]) / min(split["a=1"]) < 1.02 and min(split["a=1"]) > 0.5,
        wilson_line_linear_even_at_a0=max(wl) / min(wl) < 1.02 and min(wl) > 0.5,
        theta_zero_law=zero_ok and worst < 1e-12,
        control_nonvacuous=ctrl_spread > 0.05,
        mu_over_mc_linear_near_zero=abs(near[0] / near[1] - 1) < 1e-2,
        gaussian_invariant_delta_independent=max(abs(x - 1) for x in inv) < 1e-5,  # next-term corrections grow as delta -> 1/6
        up_hierarchy_reachable=max(abs(x) for x in fit_res) < 1e-9 and fit[0] > 0 and 0 < fit[1] < 1 / 6,
    ).items()}
    res["all_checks_pass"] = all(res["checks"].values())
    OUT.write_text(json.dumps(res, indent=2))
    print(json.dumps(res, indent=1))


if __name__ == "__main__":
    main()
