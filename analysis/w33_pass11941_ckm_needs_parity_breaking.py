"""Pass 11941: CKM from theta-null textures -- the central-inversion parity forces an isolated generation; parity-breaking
Wilson lines in the DOWN coupling alone reproduce the whole quark sector, leaving the up Weber law intact.

1. Parity theorem (exact, every Omega). The zero-characteristic level-3 theta null is invariant under the central inversion
   c -> -c of both qutrits: Theta[(-a,-b)](0, Omega) = Theta[(a,b)](0, Omega). Reshaped, Y = P Y P with P: c -> -c, so Y
   is block-diagonal on (P-even: 2) + (P-odd: 1). Two such Yukawas share the P-odd generation: |V| has an isolated
   generation (a row and column with a single unit entry). For near-product homes the P-odd state is the middle one
   (f_1 = (0, x, -x), Pass 11938), so V_us = V_cb = 0 exactly and only V_ub = O(eps^2) survives. Complements Pass 11910
   (V_us = 0 from the localised-Higgs selection rule) and extends the one-qutrit reflection of Pass 11905 to mixing.
   Hence CKM mixing NEEDS Wilson lines with a P-odd part.
2. Existence with the up coupling parity-clean. Keep the up coupling Wilson-line-free (so the Weber law of Pass 11938 and
   the neutrino relation of Passes 11939/11940 are untouched: |f(tau)|^8 = 1.467 = 2 sqrt(R_u)) and put Wilson lines
   only in the down coupling, on near-product homes |eps| <= 0.03: least-squares fits reproduce all eight quark
   observables -- m_c/m_t, m_u/m_c, m_s/m_b, m_d/m_s, |V_us|, |V_cb|, |V_ub| and J -- exactly (cost ~ 1e-17).
   Counting: 12 real parameters for 8 observables, so this is EXISTENCE, not prediction; J in particular is fittable
   (a fit with J included is exact), so no CP prediction is claimed.
3. The regime (search record, frozen from 26 multi-start fits; not re-run here). Every good fit puts the 5-bar (down)
   factor in its cusp regime: Im(-1/tau_d) = 3.5-3.8 across eps caps 0.01/0.03, cutoffs and Wilson configurations, where
   the level-3 Gaussian factor e^(-pi Im/3) ~ 0.02 ~ m_s/m_b. The up hierarchy is entangling (Omega12), the down one
   Gaussian (cusp). With Im tau_d >= 0.15 the best cost is 3.6e-3 (V_us = 0.21): preferred, not strictly forced.
   Without its Wilson lines the fitted down coupling would give R_d = 19.5, m_s/m_b = 0.0096: the down Weber law is
   strongly modified by the Wilson lines, the up one is exact.
"""

import json
import sys
from pathlib import Path

import mpmath as mp
import numpy as np
from scipy.optimize import least_squares

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "analysis"))
from w33_pass11869_11873_siegel_level3_two_qutrits import theta_null_2  # noqa: E402

OUT = ROOT / "data" / "w33_pass11941_ckm_needs_parity_breaking.json"
DATA = dict(mc_mt=0.620 / 168.26, mu_mc=1.23e-3 / 0.620, ms_mb=0.053 / 2.86, md_ms=2.67e-3 / 0.053, Vus=0.2250,
            Vcb=0.0411, Vub=0.00382, J=3.08e-5)
X0 = [0.5851, 0.2951, -0.1261, 0.0886, -0.0018, 0.0005, 0.0239, 0.0097, 0.0097, 0.0126, -0.0557, 0.0098]  # frozen fit
SCAN = dict(exact_fits_up_wilson_free=6, im_minus_inv_tau_d_exact=[3.69, 3.75], best_cost_im_tau_d_ge_015=3.55e-3,
            im_minus_inv_tau_d_all_good_fits=[3.47, 3.81], fits_run=26)
N = 24
n = np.arange(-N, N + 1)
n1, n2 = np.meshgrid(n, n, indexing="ij")


def theta(Om, z=(0, 0)):
    Y = np.zeros((3, 3), complex)
    for a in range(3):
        for b in range(3):
            v1, v2 = n1 + a / 3, n2 + b / 3
            Q = Om[0, 0] * v1 * v1 + 2 * Om[0, 1] * v1 * v2 + Om[1, 1] * v2 * v2
            Y[a, b] = np.exp(3j * np.pi * Q + 6j * np.pi * (v1 * z[0] + v2 * z[1])).sum()
    return Y


def eta(t):
    return complex(mp.exp(2j * mp.pi * t / 24) * mp.qp(mp.exp(2j * mp.pi * t)))


def weber(t):
    return np.exp(-1j * np.pi / 24) * eta((t + 1) / 2) / eta(t)


def observables(x):
    c = np.asarray(x[0::2]) + 1j * np.asarray(x[1::2])
    tau, td, eu, ed, z1, z2 = c
    Yu = theta(np.array([[tau, eu], [eu, tau]]))
    Yd = theta(np.array([[tau, ed], [ed, td]]), (z1, z2))
    Uu, su, _ = np.linalg.svd(Yu)
    Ud, sd, _ = np.linalg.svd(Yd)
    V = (Uu.conj().T @ Ud)[::-1, ::-1]                         # rows (u,c,t), columns (d,s,b)
    J = np.imag(V[0, 0] * V[1, 1] * np.conj(V[0, 1]) * np.conj(V[1, 0]))
    return dict(mc_mt=su[1] / su[0], mu_mc=su[2] / su[1], ms_mb=sd[1] / sd[0], md_ms=sd[2] / sd[1], Vus=abs(V[0, 1]),
                Vcb=abs(V[1, 2]), Vub=abs(V[0, 2]), J=abs(J)), c


def main():
    rng = np.random.default_rng(11941)
    res = dict(pass_id=11941, scan_record=SCAN)
    par, blocks = [], []
    perm = np.array([[1, 0, 0], [0, 0, 1], [0, 1, 0]])          # c -> -c on Z3
    for _ in range(6):
        A = rng.normal(size=(2, 2))
        Om = (lambda X: (X + X.T) / 2)(rng.uniform(-0.5, 0.5, (2, 2))) + 1j * (A @ A.T * 0.3 + np.diag(rng.uniform(0.6, 1.5, 2)))
        Y = theta_null_2(Om, N=30).reshape(3, 3)
        par.append(float(np.abs(perm @ Y @ perm - Y).max() / np.abs(Y).max()))
        Om2 = Om.copy()
        Om2[1, 1] += 0.2 + 0.1j
        Y2 = theta_null_2(Om2, N=30).reshape(3, 3)
        V = np.abs(np.linalg.svd(Y)[0].conj().T @ np.linalg.svd(Y2)[0])
        blocks.append(float(np.sort(V.max(axis=1)).max()))      # some row has a single unit entry
    res["parity_max_violation"] = max(par)
    res["isolated_generation_max_entry"] = max(blocks)
    tau = 1 + 0.874456j
    Yu = theta(np.array([[tau, 1e-3], [1e-3, tau]]))
    Yd = theta(np.array([[tau, 0.02], [0.02, 0.4 + 1.3j]]))
    V = np.abs(np.linalg.svd(Yu)[0].conj().T @ np.linalg.svd(Yd)[0])[::-1, ::-1]
    res["near_product_no_wilson"] = dict(Vus=float(V[0, 1]), Vcb=float(V[1, 2]), Vub=float(V[0, 2]))
    keys = list(DATA)
    fit = least_squares(lambda x: [np.log(observables(x)[0][k] / DATA[k]) for k in keys], X0, method="trf", xtol=1e-15,
                        ftol=1e-15, max_nfev=2000)
    obs, c = observables(fit.x)
    res["fit"] = dict(x=fit.x.tolist(), observables={k: float(v) for k, v in obs.items()},
                      max_log_residual=float(np.max(np.abs(fit.fun))), tau=[c[0].real, c[0].imag], tau_d=[c[1].real, c[1].imag],
                      eps_u=abs(c[2]), eps_d=abs(c[3]), wilson_d=[abs(c[4]), abs(c[5])],
                      weber_f8_tau=abs(weber(c[0])) ** 8, im_minus_inv_tau_d=float((-1 / c[1]).imag))
    sv0 = np.linalg.svd(theta(np.array([[c[0], c[3]], [c[3], c[1]]])), compute_uv=False)
    res["fit"]["down_without_wilson"] = dict(R_d=float(sv0[0] * sv0[2] / sv0[1] ** 2), ms_mb=float(sv0[1] / sv0[0]))
    F = res["fit"]
    res["checks"] = {k: bool(v) for k, v in dict(
        central_inversion_parity_exact=res["parity_max_violation"] < 1e-12,
        isolated_generation=res["isolated_generation_max_entry"] > 1 - 1e-9,
        near_product_vus_vcb_zero=res["near_product_no_wilson"]["Vus"] < 1e-12 and res["near_product_no_wilson"]["Vcb"] < 1e-12
        and res["near_product_no_wilson"]["Vub"] > 1e-7,
        all_eight_quark_observables_fit=F["max_log_residual"] < 1e-6,
        near_product_regime=F["eps_u"] < 0.03 and F["eps_d"] < 0.03,
        up_weber_law_intact=abs(F["weber_f8_tau"] ** 2 / 4 / (DATA["mu_mc"] / DATA["mc_mt"]) - 1) < 0.02,
        down_factor_in_cusp_regime=3.4 < F["im_minus_inv_tau_d"] < 3.9,
        wilson_lines_change_down_weber=F["down_without_wilson"]["R_d"] > 5 * (DATA["md_ms"] / DATA["ms_mb"]),
    ).items()}
    res["all_checks_pass"] = all(res["checks"].values())
    OUT.write_text(json.dumps(res, indent=2, default=float))
    print(json.dumps(res["checks"], indent=1), res["all_checks_pass"])
    print({k: round(v, 6) for k, v in F["observables"].items()}, F["max_log_residual"], F["weber_f8_tau"], F["im_minus_inv_tau_d"],
          F["down_without_wilson"], res["near_product_no_wilson"])


if __name__ == "__main__":
    main()
