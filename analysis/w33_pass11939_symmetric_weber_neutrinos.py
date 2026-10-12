"""Pass 11939: the symmetric-channel Weber law -- normal ordering, and a quark-lepton relation m1 m3/m2^2 = m_u m_t/m_c^2.

Inputs: the Weber law of Pass 11938 (near a product torus diag(tau1, tau2) with small Omega12 the level-3 theta Yukawa has
geometric exponents (0,1,2) and m_light m_heavy / m_mid^2 = |f(tau1) f(tau2)|^8/4, f the Weber function).

1. Symmetric channels. A flavour-symmetric coupling (the Weinberg operator L_a L_b H H, and the SU(5) up coupling
   10_a 10_b H) realised as the reshaped theta null Y_ab = Theta[(a,b)](Omega) needs Y = Y^T, i.e. a swap-symmetric home
   Omega = [[tau, eps], [eps, tau]] (checked: Y symmetric to 1e-15). Then
        m_light m_heavy / m_mid^2 = |f(tau)|^16 / 4.
   The CM values are 4 (tau = i, the square torus selected in Pass 11937), 2^(2/3) (tau = w) and 1 (tau = 1+i).
2. Ordering lemma. With the oscillation data, an inverted spectrum has m3 m2/m1^2 < 1 for every m3 (sup 0.9988), and a
   normal spectrum has m1 m3/m2^2 <= 2.952. Hence a geometric neutrino texture with R >= 1 -- every CM point -- is
   NORMAL ordered, and the square torus (R = 4) is excluded by oscillation data alone.
3. CM spectra (hierarchical branch): tau = 1+i: m = (1.53, 8.75, 50.12) meV, Sigma = 0.0604 eV; tau = w: (2.55, 8.98, 50.16) meV,
   Sigma = 0.0617 eV (its quasi-degenerate branch, Sigma = 0.138 eV, is cosmologically disfavoured); m_bb <= 5.5 meV.
4. Shared torus. If the up coupling and the Weinberg operator are theta nulls of the same swap-symmetric home, they share
   |f(tau)|^16/4 and
        m1 m3 / m2^2 = m_u m_t / m_c^2  (= 0.54 at M_Z, 0.45-0.65 with the m_u error and running),
   which fixes the neutrino spectrum without a free parameter: normal ordering (the IO branch has Sigma ~ 0.15 eV),
   m1 = 0.80 meV (0.67-0.97), Sigma = 0.0596 eV, m_bb in [0.95, 4.3] meV, m_beta = 8.8 meV. The home is then non-CM,
   |f(tau)|^8 = 1.47 (tau = 1 + i y*).
5. The Pass 11933 alternative (inverted, m3 ~ 1.3 meV) has Sigma = 0.1006 eV (0.100-0.103), above the DESI DR2 (BAO+CMB, LCDM) bound
   of about 0.064 eV; it survives only outside LCDM (w0wa: about 0.16 eV). The two readings are distinguished by the mass
   ordering (JUNO + long-baseline, 3 sigma expected within about five years) and by Sigma.
Assumptions (all stated, none derived here): the symmetric channels are theta nulls of one swap-symmetric home near the
reducible locus; leading order in Omega12; the light neutrino mass matrix is the Weinberg coefficient itself (no
seesaw distortion); MZ-scale quark ratios.
"""

import json
import sys
from pathlib import Path

import mpmath as mp
import numpy as np
from scipy.optimize import brentq

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "analysis"))
from w33_pass11869_11873_siegel_level3_two_qutrits import theta_null_2  # noqa: E402

OUT = ROOT / "data" / "w33_pass11939_symmetric_weber_neutrinos.json"
W = np.exp(2j * np.pi / 3)
D21, D31_NO, D32_IO = 7.42e-5, 2.511e-3, 2.498e-3          # eV^2 (NuFIT 5.x/6.0 central values)
S12, S13 = 0.307, 0.0220                                     # sin^2
R_UP = {"MZ": 1.23e-3 * 168.26 / 0.620**2, "low": 0.45, "high": 0.65}
SIGMA_DESI_LCDM = 0.064


def eta(t):
    return complex(mp.exp(2j * mp.pi * t / 24) * mp.qp(mp.exp(2j * mp.pi * t)))


def weber(t):
    return np.exp(-1j * np.pi / 24) * eta((t + 1) / 2) / eta(t)


def sym_theta(tau, eps):
    Y = theta_null_2(np.array([[tau, eps], [eps, tau]]), N=60).reshape(3, 3)
    sv = np.linalg.svd(Y, compute_uv=False)
    return Y, float(sv[0] * sv[2] / sv[1] ** 2)


def no_ratio(m1):
    return m1 * np.sqrt(m1**2 + D31_NO) / (m1**2 + D21)


def io_ratio(m3):
    m1, m2 = np.sqrt(m3**2 + D32_IO - D21), np.sqrt(m3**2 + D32_IO)
    return m3 * m2 / m1**2


def observables(m):
    m1, m2, m3 = m
    c12, c13 = 1 - S12, 1 - S13
    a, b, c = c12 * c13 * m1, S12 * c13 * m2, S13 * m3
    mx = max(a, b, c)
    return dict(masses_meV=[1e3 * x for x in m], sigma_eV=float(sum(m)), mbb_meV=[1e3 * max(0, 2 * mx - (a + b + c)), 1e3 * (a + b + c)],
                mbeta_meV=float(1e3 * np.sqrt(c12 * c13 * m1**2 + S12 * c13 * m2**2 + S13 * m3**2)))


def spectra(R):
    x = np.logspace(-6, 0, 60001)
    out = []
    for fn, kind in ((no_ratio, "NO"), (io_ratio, "IO")):
        G = fn(x) - R
        for k in np.nonzero(G[:-1] * G[1:] < 0)[0]:
            r = brentq(lambda m: fn(m) - R, x[k], x[k + 1])
            if kind == "NO":
                m = (r, np.sqrt(r**2 + D21), np.sqrt(r**2 + D31_NO))
            else:
                m = (np.sqrt(r**2 + D32_IO - D21), np.sqrt(r**2 + D32_IO), r)
            out.append(dict(ordering=kind, **observables(m)))
    return out


def main():
    rng = np.random.default_rng(11939)
    res = dict(pass_id=11939, R_up=R_UP)
    sym, law = [], []
    for _ in range(6):
        tau = rng.uniform(-1, 1) + 1j * rng.uniform(0.6, 1.8)
        Y, R = sym_theta(tau, 1e-4 * np.exp(1j * rng.uniform(0, 2 * np.pi)))
        sym.append(float(np.abs(Y - Y.T).max() / np.abs(Y).max()))
        law.append(abs(R / (abs(weber(tau)) ** 16 / 4) - 1))
    res.update(max_asymmetry=max(sym), weber16_max_rel_err=float(max(law)))
    res["cm_values"] = {k: sym_theta(t, 1e-4)[1] for k, t in (("i", 1j), ("w", W), ("1+i", 1 + 1j))}
    xs = np.logspace(-6, 0, 200001)
    res["sup_io_ratio"] = float(io_ratio(xs).max())
    res["max_no_ratio"] = float(no_ratio(xs).max())
    res["spectra"] = {k: spectra(R) for k, R in (("1+i", 1.0), ("w", 2 ** (2 / 3)), ("i", 4.0), ("up_MZ", R_UP["MZ"]),
                                                 ("up_low", R_UP["low"]), ("up_high", R_UP["high"]))}
    ystar = brentq(lambda y: abs(weber(1 + 1j * y)) ** 8 - 2 * np.sqrt(R_UP["MZ"]), 0.3, 1.0)
    res["shared_home_tau"] = [1.0, float(ystar)]
    res["shared_home_R_check"] = sym_theta(1 + 1j * ystar, 1e-4)[1]
    m3q = json.loads((ROOT / "data" / "w33_pass11933_radiative_neutrino_relation.json").read_text())["m3_meV_quantiles"]
    io11933 = [observables((np.sqrt((1e-3 * m3) ** 2 + D32_IO - D21), np.sqrt((1e-3 * m3) ** 2 + D32_IO), 1e-3 * m3)) for m3 in m3q]
    res["pass11933_io"] = io11933
    sp = res["spectra"]
    hier = lambda k: [s for s in sp[k] if s["ordering"] == "NO" and s["sigma_eV"] < SIGMA_DESI_LCDM]
    res["checks"] = {k: bool(v) for k, v in dict(
        symmetric_home_symmetric_yukawa=res["max_asymmetry"] < 1e-12,
        weber16_law=res["weber16_max_rel_err"] < 1e-6,
        cm_values=abs(res["cm_values"]["i"] - 4) < 1e-6 and abs(res["cm_values"]["w"] - 2 ** (2 / 3)) < 1e-6
        and abs(res["cm_values"]["1+i"] - 1) < 1e-6,
        io_ratio_below_one=res["sup_io_ratio"] < 1,
        square_torus_excluded=res["max_no_ratio"] < 4 and sp["i"] == [],
        cm_forces_normal_ordering=all(s["ordering"] == "NO" for k in ("1+i", "w", "i") for s in sp[k]),
        cm_hierarchical_inside_desi=len(hier("1+i")) == 1 and len(hier("w")) == 1,
        shared_home_normal_and_light=len(hier("up_MZ")) == 1 and 0.5 < hier("up_MZ")[0]["masses_meV"][0] < 1.2
        and all(s["sigma_eV"] > 0.12 for s in sp["up_MZ"] if s["ordering"] == "IO"),
        shared_home_is_non_cm=abs(res["shared_home_R_check"] / R_UP["MZ"] - 1) < 1e-5,
        pass11933_above_desi_lcdm=io11933[1]["sigma_eV"] > 0.1 > SIGMA_DESI_LCDM,
    ).items()}
    res["all_checks_pass"] = all(res["checks"].values())
    OUT.write_text(json.dumps(res, indent=2, default=float))
    print(json.dumps(res["checks"], indent=1), res["all_checks_pass"])
    for k, v in sp.items():
        for s in v:
            print(k, s["ordering"], [round(x, 2) for x in s["masses_meV"]], round(s["sigma_eV"], 4), [round(x, 2) for x in s["mbb_meV"]], round(s["mbeta_meV"], 2))
    print("tau*", res["shared_home_tau"], "11933 IO sigma", [round(x["sigma_eV"], 4) for x in io11933], res["sup_io_ratio"], res["max_no_ratio"])


if __name__ == "__main__":
    main()
