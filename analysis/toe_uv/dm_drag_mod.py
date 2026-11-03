"""Stabilising chi: what mass does it take?  chi starts at rest on the valley, V = (1/2) mu^2 chi^2 about it, and dark matter with m = m0 exp(-b chi) kicks it until H falls to mu.  Then it oscillates and redshifts as extra cold matter.
Integrated directly with radiation and coupled dust, stopping at H = mu/30 (or today), where the oscillation energy and the cycle-averaged shift of ln m are read off.  This replaces the full fits above mu ~ 100 H0 in dm_drag.py, where the shooting fails: those failures are solver failures, not exclusions.
Reported: f = rho_chi/rho_c after the kick; the redshift z_mu with H = mu; the range 1/mu, in kpc; the Yukawa strength alpha = 2 b^2; and the implied stabiliser scale (mu M_Pl)^(1/2) with its tuning against Lambda, if chi has a Planckian range.
Control: mu = 0 limit must reproduce chi_N -> 2 b Omega_c.  Control: the ratio mu/H0 at z_mu must follow H(z).  usage: py -3 dm_drag_mod.py"""
import json
import math
import numpy as np
from scipy.integrate import solve_ivp

h = 0.68
Om, Orad = 0.31, 4.15e-5 / (h * h) * (1 + 0.0)
H0_eV = 100 * h * 1e3 / 3.0857e22 * 6.582e-16
MPL_eV = 2.435e27
KPC_INV_eV = 1.97327e-7 / 3.0857e19  # eV per (1/kpc)
out = dict(H0_eV=H0_eV)
Ol = 1 - Om - Orad


def run(b, mu):
    NI = -14.0

    def rhs(N, s):
        chi, x = s
        ea = math.exp(-3 * N)
        rc = Om * ea * math.exp(-b * chi)
        rr = Orad * ea * math.exp(-N)
        V = 0.5 * mu * mu * chi * chi / 3.0 + Ol
        E2 = (rc + rr + V) / (1 - x * x / 6)
        dl = -0.5 * (x * x + 3 * (rc + 4 / 3 * rr) / E2)
        return [x, -(3 + dl) * x + 3 * (b * rc - mu * mu * chi / 3.0) / E2]

    def stop(N, s):
        chi, x = s
        ea = math.exp(-3 * N)
        rc = Om * ea * math.exp(-b * chi)
        rr = Orad * ea * math.exp(-N)
        V = 0.5 * mu * mu * chi * chi / 3.0 + Ol
        E2 = (rc + rr + V) / (1 - x * x / 6)
        return math.sqrt(E2) - mu / 30.0

    stop.terminal = True
    stop.direction = -1

    def blow(N, s):
        return 5.9 - s[1] * s[1]

    blow.terminal = True
    s = solve_ivp(rhs, (NI, 0), [0.0, 0.0], rtol=1e-7, atol=1e-11, method="LSODA", events=[stop, blow], dense_output=True)
    Nf = s.t[-1]
    # cycle average over the last e-fold fraction
    Ns = np.linspace(Nf - min(0.3, 0.2 * abs(Nf)), Nf, 400)
    y = s.sol(Ns)
    chi, x = y
    ea = np.exp(-3 * Ns)
    rc = Om * ea * np.exp(-b * chi)
    rr = Orad * ea * np.exp(-Ns)
    V = 0.5 * mu * mu * chi * chi / 3.0
    E2 = (rc + rr + V + Ol) / (1 - x * x / 6)
    rho_chi = E2 * x * x / 6 + V
    return dict(Nf=float(Nf), f=float(np.mean(rho_chi / rc)), chi_mean=float(np.mean(chi)), chi_amp=float(0.5 * (chi.max() - chi.min())), z_end=float(math.exp(-Nf) - 1), steps=len(s.t))


for b in (0.7071, 1.2247):
    rows = {}
    for lmu in (2, 3, 4, 4.5, 5, 5.5, 6, 6.5, 7, 8, 9, 10):
        mu = 10.0 ** lmu
        r = run(b, mu)
        r["mu_over_H0"] = mu
        r["mu_eV"] = mu * H0_eV
        r["range_kpc"] = KPC_INV_eV / (mu * H0_eV)
        r["stabiliser_scale_eV"] = math.sqrt(mu * H0_eV * MPL_eV)
        r["tuning_vs_Lambda"] = mu * mu / (3 * Ol)
        rows[str(lmu)] = r
        print(b, lmu, {k: (round(v, 5) if isinstance(v, float) and abs(v) < 1e4 else v) for k, v in r.items() if k in ("f", "chi_mean", "chi_amp", "z_end", "range_kpc", "steps")}, flush=True)
    out[str(b)] = dict(alpha=2 * b * b, rows=rows)
# control: no mass, matter domination only
b = 0.3


def rhs0(N, s):
    x = s[0]
    o = 1 - x * x / 6
    d = -0.5 * (x * x + 3 * o)
    return [-(3 + d) * x + 3 * b * o]


r0 = solve_ivp(rhs0, (0, 40), [0.0], rtol=1e-10, atol=1e-12, method="LSODA")
out["control_light_chiN"] = dict(num=float(r0.y[0, -1]), exact=2 * b)
assert abs(r0.y[0, -1] - 2 * b) < 1e-6
json.dump(out, open("dm_drag_mod.json", "w"), indent=1)
print("done", out["control_light_chiN"], flush=True)
