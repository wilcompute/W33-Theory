"""Pass 11948: the axiflavon decay constant is fixed by the up-quark masses -- f_a ~ 5e15 GeV, m_a ~ 1 neV.

Input: Pass 11947 (the phase of the up-sector Omega12 shifts theta-bar by 3 phi at fixed quark data) and the Weber law of
Pass 11938 (m_u m_t / m_c^2 = |f(tau)|^16/4 on the swap-symmetric up home).

1. Normalisation. With the Siegel complex-structure Kahler potential K = -log det Im Omega (the T^4 factor of the
   holomorphic 3-form), K_{Omega12 Omega12bar} = 1/(2 Im tau1 Im tau2) at the product locus (checked by finite
   differences). Writing Omega12 = r e^{i phi}, the canonical field is a = M_P r phi / sqrt(Im tau1 Im tau2), and
   theta-bar = 3 phi gives
        f_a = M_P |Omega12| / (3 sqrt(Im tau1 Im tau2)),
   invariant under the rescaling Omega -> Omega/6 between toy and physical units.
2. Fixed by the up masses. m_c/m_t = kappa(tau) |Omega12| near the product locus, so f_a = M_P (m_c/m_t)/(3 kappa Im tau).
   Along the whole Weber level curve |f(tau)|^8 = 2 sqrt(m_u m_t/m_c^2), the weight-zero combination kappa Im tau varies
   only between 0.584 and 0.591 (1.3%). Hence f_a is fixed by m_c/m_t and m_u m_t/m_c^2 alone:
        f_a = (5.06 - 5.12) x 1e15 GeV   (M_Z-scale ratios; both quark fits give 5.12e15),
   falling to ~3.7e15 GeV if the GUT-scale m_c/m_t (~0.0027) is used.
3. Phenomenology (standard formulae). m_a = 5.69 ueV (1e12 GeV/f_a) = 1.1-1.5 neV (frequency ~270-360 kHz). The anomaly
   sits in the up sector only, so E/N = 2 N_c Q_u^2 = 8/3 and g_agamma = alpha/(2 pi f_a) (E/N - 1.92) ~ 1.7-2.3e-19
   GeV^-1. As all of dark matter via misalignment it needs an initial angle ~0.007 (pre-inflationary PQ breaking, where
   the domain-wall number 3 is harmless). The 1-100 neV window is the GUT-scale-PQ target of ABRACADABRA/DMRadio-GUT and
   of CASPEr-Electric; the predicted mass sits at its lower edge.
Scope: conditional on the axiflavon reading of Pass 11947 (dynamical, flux-flat arg Omega12) and on K = -log det Im Omega
(O(1) changes from other Kahler terms rescale f_a); quality not addressed.
"""

import json
import sys
from pathlib import Path

import mpmath as mp
import numpy as np
from scipy.optimize import brentq

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "analysis"))
import w33_pass11942_hypercharge_wilson_leptons as P42  # noqa: E402

OUT = ROOT / "data" / "w33_pass11948_axiflavon_decay_constant.json"
MP = 2.435e18
MCMT = {"MZ": 0.620 / 168.26, "GUT_approx": 0.0027}
R_UP = 1.23e-3 * 168.26 / 0.620**2
ALPHA = 1 / 137.036


def eta(t):
    return complex(mp.exp(2j * mp.pi * t / 24) * mp.qp(mp.exp(2j * mp.pi * t)))


def weber(t):
    return np.exp(-1j * np.pi / 24) * eta((t + 1) / 2) / eta(t)


def kahler(Om):
    return -np.log(np.linalg.det(Om.imag))


def kappa(tau):
    e = 1e-4
    s = np.linalg.svd(P42.theta(np.array([[tau, e], [e, tau]])), compute_uv=False)
    return s[1] / s[0] / e


def main():
    res = dict(pass_id=11948)
    tau = 1 + 0.874456j
    h = 1e-4
    Om = lambda w: np.array([[tau, w], [w, tau]])
    d = lambda w: kahler(Om(w))
    kcc = (d(h) + d(-h) + d(1j * h) + d(-1j * h) - 4 * d(0)) / (4 * h**2)        # = d2K/dw dwbar
    res["kahler_metric_numeric"] = float(kcc)
    res["kahler_metric_formula"] = float(1 / (2 * tau.imag**2))
    fits = {}
    for k, x in P42.FITS.items():
        c = np.array(x[0::2]) + 1j * np.array(x[1::2])
        fits[k] = dict(tau=[c[0].real, c[0].imag], eps_u=abs(c[2]), f_a=MP * abs(c[2]) / (3 * c[0].imag))
    res["fits"] = fits
    target = 2 * np.sqrt(R_UP)
    ys = np.linspace(0.12, 2.5, 100)
    curve = []
    for re in np.linspace(-1, 1, 21):
        g = [abs(weber(re + 1j * y)) ** 8 - target for y in ys]
        for i in range(len(ys) - 1):
            if g[i] * g[i + 1] < 0:
                y = brentq(lambda y: abs(weber(re + 1j * y)) ** 8 - target, ys[i], ys[i + 1])
                kap = kappa(re + 1j * y)
                curve.append(dict(tau=[re, y], kappa_im=kap * y, f_a_MZ=MP * MCMT["MZ"] / (3 * kap * y)))
    res["weber_curve"] = curve
    kim = [p["kappa_im"] for p in curve]
    fa = [p["f_a_MZ"] for p in curve]
    res["kappa_im_range"] = [min(kim), max(kim)]
    res["f_a_range_MZ"] = [min(fa), max(fa)]
    res["f_a_GUT_approx"] = float(MP * MCMT["GUT_approx"] / (3 * np.mean(kim)))
    fa_band = [res["f_a_GUT_approx"], max(fa)]
    m_a = [5.69e-6 * 1e12 / f for f in fa_band[::-1]]
    res["m_a_eV"] = m_a
    res["frequency_kHz"] = [m / 4.135667e-15 / 1e3 for m in m_a]
    res["E_over_N"] = 8 / 3
    res["g_agamma_per_GeV"] = [ALPHA / (2 * np.pi * f) * (8 / 3 - 1.92) for f in fa_band[::-1]]
    res["misalignment_angle_all_DM"] = [float(np.sqrt(0.12 / (0.12 * (f / 9e11) ** 1.165))) for f in fa_band]
    res["checks"] = {k: bool(v) for k, v in dict(
        kahler_metric_matches=abs(kcc / res["kahler_metric_formula"] - 1) < 1e-3,
        fits_agree=abs(fits["A"]["f_a"] / fits["B"]["f_a"] - 1) < 2e-3,
        kappa_im_nearly_constant=(max(kim) - min(kim)) / np.mean(kim) < 0.02 and len(curve) > 10,
        f_a_gut_scale=3e15 < min(fa_band) and max(fa_band) < 6e15,
        mass_in_neV_window_lower_edge=1e-9 < min(m_a) and max(m_a) < 2e-9,
    ).items()}
    res["all_checks_pass"] = all(res["checks"].values())
    OUT.write_text(json.dumps(res, indent=2, default=float))
    print(json.dumps(res["checks"], indent=1), res["all_checks_pass"])
    print({k: f"{v['f_a']:.4e}" for k, v in fits.items()}, res["kappa_im_range"], [f"{x:.3e}" for x in res["f_a_range_MZ"]],
          f"{res['f_a_GUT_approx']:.3e}", [f"{x:.3e}" for x in m_a], [round(x) for x in res["frequency_kHz"]],
          [f"{x:.2e}" for x in res["g_agamma_per_GeV"]], [round(x, 4) for x in res["misalignment_angle_all_DM"]])


if __name__ == "__main__":
    main()
