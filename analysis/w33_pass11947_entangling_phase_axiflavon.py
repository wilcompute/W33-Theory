"""Pass 11947: the phase of the up-sector entangling modulus is an anomalous Froggatt-Nielsen rephasing -- it moves
theta-bar by 3 arg Omega12 while every quark observable stays fixed; a dynamical phase would be an axiflavon.

1. Exact structure. Near a product home the up Yukawa is Y_u = sum_k c_k f_k f_k^T with c_k = (6 pi i eps)^k / k!
   (Pass 11938). By Cauchy-Binet, det Y_u = sum_{k1<k2<k3} c_k1 c_k2 c_k3 det[f_k1 f_k2 f_k3]^2, and by the central-
   inversion parity (Passes 11941/11944) only triples with exactly one odd k survive (the odd vectors span one
   dimension). The leading triple is (0,1,2); the next ones, (0,2,3) and (0,1,4), are suppressed by |eps|^2. Hence
        arg det Y_u = 3 arg eps_u + const(tau) + O(|eps_u|^2),
   i.e. the heat-kernel texture is a Froggatt-Nielsen texture with charges (0,1,2) on both chiralities, arg eps is the
   FN U(1) rotation, and its QCD anomaly coefficient is 0+1+2 = 3.
2. In the quark fits of Pass 11942 (all eight quark observables reproduced), rotating arg eps_u by phi shifts
   theta-bar = arg det(Y_u Y_d) by 3 phi (to 1e-4 rad) while the masses, |V| and J change by at most 3e-3 relative
   (largest for J); the deviation of arg det from 3 phi scales as |eps|^2.00 (exponent measured). arg eps_d is NOT such a direction: the down Wilson lines (Pass 11941) make it physical (observables move by
   9-30% for phi = 0.3-2).
3. Reading. The fitted vacua have theta-bar = O(1) (0.19 and -1.41 rad at the two fits): taken alone, the framework has a
   strong-CP problem. But the up-sector Omega12 is precisely the modulus that, per Pass 11913, stays flat under fluxes
   within the tadpole bound. If its phase is a dynamical field, the QCD potential relaxes theta-bar to zero along a
   direction that leaves the CKM untouched: the entangling modulus is the flavon and its phase the QCD axion -- the
   "axiflavon"/"flaxion" mechanism (Calibbi-Goertz-Redigolo-Ziegler-Zupan 2016; Ema-Hamaguchi-Moroi-Nakayama 2016),
   here with the FN charges supplied by the theta heat-kernel. Open: the decay constant (Kahler normalisation of Omega12
   in physical units), the quality requirement (other potentials for arg Omega12 below ~1e-10 of the QCD one), and the
   domain-wall number 3.
"""

import json
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "analysis"))
import w33_pass11942_hypercharge_wilson_leptons as P42  # noqa: E402

OUT = ROOT / "data" / "w33_pass11947_entangling_phase_axiflavon.json"
KEYS = ("mc_mt", "mu_mc", "ms_mb", "md_ms", "Vus", "Vcb", "Vub", "J")


def observables(tau, td, eu, ed, zd):
    Yu = P42.theta(np.array([[tau, eu], [eu, tau]]))
    Yd = P42.normalised(np.array([[tau, ed], [ed, td]]), (0, zd))
    Uu, su, _ = np.linalg.svd(Yu)
    Ud, sd, _ = np.linalg.svd(Yd)
    V = (Uu.conj().T @ Ud)[::-1, ::-1]
    J = np.imag(V[0, 0] * V[1, 1] * np.conj(V[0, 1]) * np.conj(V[1, 0]))
    o = dict(mc_mt=su[1] / su[0], mu_mc=su[2] / su[1], ms_mb=sd[1] / sd[0], md_ms=sd[2] / sd[1], Vus=abs(V[0, 1]),
             Vcb=abs(V[1, 2]), Vub=abs(V[0, 2]), J=J)
    return {k: float(v) for k, v in o.items()}, float(np.angle(np.linalg.det(Yu) * np.linalg.det(Yd)))


def wrap(x):
    return float((x + np.pi) % (2 * np.pi) - np.pi)


def main():
    res = dict(pass_id=11947)
    tau = 1 + 0.874456j
    scaling = []
    for e in (1e-3, 3e-3, 1e-2, 3e-2):
        d0 = np.linalg.det(P42.theta(np.array([[tau, e], [e, tau]])))
        devs = []
        for phi in (0.4, 1.3, 2.2):
            ee = e * np.exp(1j * phi)
            devs.append(abs(wrap(np.angle(np.linalg.det(P42.theta(np.array([[tau, ee], [ee, tau]])))) - np.angle(d0) - 3 * phi)))
        scaling.append(dict(eps=e, max_dev_from_3phi=max(devs)))
    res["arg_det_scaling"] = scaling
    sl = np.polyfit(np.log([s["eps"] for s in scaling]), np.log([s["max_dev_from_3phi"] for s in scaling]), 1)[0]
    res["deviation_slope_in_eps"] = float(sl)
    res["fits"] = {}
    for k, x in P42.FITS.items():
        x = np.array(x)
        c = x[0::2] + 1j * x[1::2]
        tau_f, td, eu, ed, zd = c
        base, tb = observables(tau_f, td, eu, ed, zd)
        rows = []
        for which in ("u", "d"):
            for phi in (0.3, 1.0, 2.0):
                e2 = eu * np.exp(1j * phi) if which == "u" else eu
                d2 = ed * np.exp(1j * phi) if which == "d" else ed
                o, t = observables(tau_f, td, e2, d2, zd)
                rows.append(dict(sector=which, phi=phi, theta_bar_shift=wrap(t - tb),
                                 max_rel_change=max(abs(o[q] / base[q] - 1) for q in KEYS), Vus_rel_change=abs(o["Vus"] / base["Vus"] - 1)))
        res["fits"][k] = dict(theta_bar=tb, base=base, rotations=rows)
    F = res["fits"]
    up = [r for f in F.values() for r in f["rotations"] if r["sector"] == "u"]
    dn = [r for f in F.values() for r in f["rotations"] if r["sector"] == "d"]
    res["checks"] = {k: bool(v) for k, v in dict(
        arg_det_is_3_arg_eps=all(s["max_dev_from_3phi"] < 1e-2 for s in scaling[:3]),
        correction_is_order_eps_squared=1.7 < sl < 2.3,
        up_phase_shifts_theta_bar_by_3phi=all(abs(wrap(r["theta_bar_shift"] - 3 * r["phi"])) < 1e-3 for r in up),
        up_phase_leaves_quark_observables=all(r["max_rel_change"] < 5e-3 for r in up),
        down_phase_is_physical=any(r["Vus_rel_change"] > 0.02 for r in dn),
        fitted_vacua_have_order_one_theta_bar=all(abs(f["theta_bar"]) > 0.1 for f in F.values()),
    ).items()}
    res["all_checks_pass"] = all(res["checks"].values())
    OUT.write_text(json.dumps(res, indent=2, default=float))
    print(json.dumps(res["checks"], indent=1), res["all_checks_pass"], sl, [round(s["max_dev_from_3phi"], 8) for s in scaling])
    for k, f in F.items():
        print(k, round(f["theta_bar"], 4), [(r["sector"], r["phi"], round(r["theta_bar_shift"], 4), f"{r['max_rel_change']:.1e}") for r in f["rotations"]])


if __name__ == "__main__":
    main()
