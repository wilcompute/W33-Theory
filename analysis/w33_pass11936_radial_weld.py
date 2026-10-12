"""Pass 11936: the radial weld -- the E8 displacement off a Witting ray is the top/charm hierarchy parameter, with
universal Schmidt exponents (0, 1, 1).

Inputs: the Cartan -> Siegel inversion of Passes 11879/11891 (V.invert: Coble/Maschke matching), the level-3 theta
two-qutrit Yukawa of Passes 11869/11872 (theta_null_2(Omega) reshaped 3 x 3), the selected tangent direction of Pass
11935 (the log(8/5) Clifford orbit) and the essential scaling of the parallel packet 8407e70cf
(log t* = -kappa/(32 r) - 1/2 - C_G/16, kappa = 7.211, C_G = 3.693 on that orbit).

Result: displace the Cartan vev to c = (1, t u), invert to Omega(t) (residuals <= 1e-13), and take the singular values of
the theta Yukawa:
* along the selected log(8/5) direction: (1, 0.465 t, 0.370 t) -- both light states exactly linear in t (log-slopes 1.00),
  while Im Omega_max grows like (3/pi) ln(1/t);
* the same exponents (0,1,1) along a generic mixed direction and along directions approaching the stabiliser state, where the two
  coefficients merge (the charm-up lock);
* the strange direction leaves Omega fixed (degenerate Maschke direction); the stabiliser direction and some directions with
  no e1 component run into a deeper cusp (Im Omega ~ 20-30) with a locked, numerically degenerate pair.
Reading: the essential scaling t ~ exp(-kappa/32r) is the top/charm hierarchy parameter: m_c/m_t = 0.465 t fits the data
(3.6e-3) at t ~ 7.8e-3, i.e. r ~ 0.055 -- a modest soft-supertrace ratio. But near a Witting ray the degeneration is a
one-dimensional cusp, so m_u/m_c = b/a is fixed by the direction (0.796 on the selected orbit): the up/charm hierarchy
needs a second small parameter.
"""

import json
import sys
from pathlib import Path

import numpy as np
from scipy.optimize import minimize

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "analysis"))
import w33_20261011_soft_supertrace_hierarchy as SS  # noqa: E402
import w33_pass11874_11878_siegel_fixed_points_cp_magic as S  # noqa: E402
import w33_pass11890_11892_vacuum_phase_diagram as V  # noqa: E402
import w33_pass11923_stabiliser_higgs_lock as H23  # noqa: E402
import w33_pass11926_g25_tangent_vacua as G26  # noqa: E402
from w33_pass11869_11873_siegel_level3_two_qutrits import theta_null_2  # noqa: E402

OUT = ROOT / "data" / "w33_pass11936_radial_weld.json"
TS = [0.02, 0.01, 0.005, 0.0025]


def run(u, rng):
    guess, rows = None, []
    for t in TS:
        c = np.r_[1, t * u]
        c = c / np.linalg.norm(c)
        Om, res, guess = V.invert(c, rng, guess)
        Om = S.siegel_reduce(Om)
        sv = np.linalg.svd(theta_null_2(Om, N=40).reshape(3, 3), compute_uv=False)
        sv = sv / sv[0]
        rows.append((t, res, float(np.linalg.eigvalsh(Om.imag).max()), float(sv[1]), float(sv[2])))
    o = np.array(rows)
    return dict(rows=o.tolist(), max_residual=float(o[:, 1].max()),
                slope2=float(np.polyfit(np.log(o[:, 0]), np.log(o[:, 3]), 1)[0]),
                slope3=float(np.polyfit(np.log(o[:, 0]), np.log(o[:, 4]), 1)[0]),
                a=float(o[-1, 3] / o[-1, 0]), b=float(o[-1, 4] / o[-1, 0]),
                imom_slope_vs_ln_inv_t=float(np.polyfit(np.log(1 / o[:, 0]), o[:, 2], 1)[0]))


def main():
    rng = np.random.default_rng(11936)
    r = minimize(lambda x: SS.local_coefficients((x[:3] + 1j * x[3:]) / np.linalg.norm(x[:3] + 1j * x[3:]), 2e-4)[1],
                 rng.normal(size=6), method="Nelder-Mead", options=dict(maxiter=800, xatol=1e-7, fatol=1e-9))
    u = r.x[:3] + 1j * r.x[3:]
    ustar, stab = G26.polish(u / np.linalg.norm(u), G26.clifford())
    stabvec = np.array([1, 0, 0], complex)
    gen = rng.normal(size=3) + 1j * rng.normal(size=3)
    gen -= np.vdot(stabvec, gen) * stabvec
    gen /= np.linalg.norm(gen)
    res = dict(pass_id=11936, selected_M2=float(H23.magic(ustar)), selected_stabiliser=int(stab))
    res["log85"] = run(ustar, rng)
    mixed = np.cos(0.3) * stabvec + np.sin(0.3) * gen      # generic direction (a direction exactly orthogonal to e1
    res["random"] = run(mixed / np.linalg.norm(mixed), rng)  # can run into the deeper stabiliser-type cusp)
    near = np.cos(0.03) * stabvec + np.sin(0.03) * gen
    res["near_stabiliser"] = run(near / np.linalg.norm(near), rng)
    kappa, cg = 7.211, SS.local_coefficients(ustar, 2e-4)[1]
    t_fit = 3.61e-3 / res["log85"]["a"]
    res["fit"] = dict(t_for_mc_mt=float(t_fit), r=float(kappa / (32 * (-np.log(t_fit) - 0.5 - cg / 16))),
                      predicted_mu_mc=float(res["log85"]["b"] / res["log85"]["a"]), C_G=float(cg))
    res["checks"] = {k: bool(v) for k, v in dict(
        selected_direction_is_log85=abs(res["selected_M2"] - np.log(8 / 5)) < 1e-9 and stab == 4,
        inversions_converged=max(res[k]["max_residual"] for k in ("log85", "random", "near_stabiliser")) < 1e-10,
        exponents_011_everywhere=all(abs(res[k]["slope2"] - 1) < 0.03 and abs(res[k]["slope3"] - 1) < 0.03 for k in ("log85", "random", "near_stabiliser")),
        im_omega_logarithmic=abs(res["log85"]["imom_slope_vs_ln_inv_t"] - 3 / np.pi) < 0.05,
        near_stabiliser_pair_merges=abs(res["near_stabiliser"]["b"] / res["near_stabiliser"]["a"] - 1) < abs(res["random"]["b"] / res["random"]["a"] - 1),
        modest_r=0.02 < res["fit"]["r"] < 0.1,
    ).items()}
    res["all_checks_pass"] = all(res["checks"].values())
    OUT.write_text(json.dumps(res, indent=2))
    print(json.dumps({k: res[k] for k in ("fit", "checks", "all_checks_pass")}, indent=1),
          {k: (round(res[k]["a"], 4), round(res[k]["b"], 4), round(res[k]["slope2"], 3), round(res[k]["slope3"], 3)) for k in ("log85", "random", "near_stabiliser")})


if __name__ == "__main__":
    main()
