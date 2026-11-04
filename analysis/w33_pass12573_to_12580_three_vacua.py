"""Passes 12573-12580 (Claude track).  Not a theory of everything: see PASS12573_12580_THREE_VACUA.md.

12573 -- a particle-mesh N-body of the sparse tower: validated against linear theory and CLASS; no runaway; the coupled species is concentrated in peaks, which retracts the sign of the toy of Pass 12563.
12574 -- weak lensing and RSD in the fit: DES Y6 cuts the c' gain to 4.0, KiDS-Legacy leaves it at 7.7.
12575 -- V_min = 0: dark energy is the radion's height above a zero-energy minimum, with no separate Lambda; acceleration ends in 4 to 7.5 Gyr.
12576 -- V_min > 0 is global along the radion, so TCC needs another decay channel.
12577 -- Scherk-Schwarz gravitini remove AdS3 with no new fields, at any twist tested; the potential stays R^-4, so recollapse returns on that route.
12578 -- the coupled fraction from brane production: control 3.97 GeV against 4 GeV; f of order 0.1 at the natural T_i of 1 GeV.
12579 -- the volume modulus, a scale estimate.
12580 -- three vacua compared.
"""

import json
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
D = ROOT / "analysis" / "toe_uv"
OUT = ROOT / "data" / "w33_pass12573_to_12580_three_vacua.json"
SETS = ("pantheon", "dovekie", "desy5")


def load(n):
    return json.loads((D / n).read_text())


def main():
    checks, res = {}, {}

    # 12573
    nb = {k: load(f"nbody_{k}.json") for k in ("L100_b707", "L25_b707", "L25_b1225")}
    lin = load("nbody_linear_control.json")
    res["nbody"] = {k: dict(k=v["k_common"], P_ratio=v["P_ratio"], amp=v["amp_ratio_coupled"], amp_control=v["amp_ratio_control"], P_over_halofit=v["P_over_halofit_control"], peaks=dict(control=v["control"]["npeaks"], coupled=v["coupled"]["npeaks"]), F_top=[v["coupled"]["F1_top"], v["coupled"]["F2_top"], v["coupled"]["F4_top"]], F_all=[v["coupled"]["F1"], v["coupled"]["F2"], v["coupled"]["F4"]], F_global=v["coupled"]["Fglobal"], class_ratio_0=v["class_ratio_0"]) for k, v in nb.items()}
    res["nbody_linear_control"] = dict(amp=lin["amp_ratio_coupled"][:3], control=lin["amp_ratio_control"][:3], class_ratio_0=lin["class_ratio_0"], ode_coupled=1.0614, ode_control=1.0074)
    checks["12573: linear limit: low-k amplitude ratio within 0.012 of the linear equations (1.0614) and of CLASS (1.0617), control within 0.002 of 1.0074"] = abs(sum(lin["amp_ratio_coupled"][:3]) / 3 - 1.0614) < 0.012 and abs(lin["class_ratio_0"] - 1.0617) < 1e-3 and abs(sum(lin["amp_ratio_control"][:2]) / 2 - 1.0074) < 0.002
    a = nb["L100_b707"]
    i = [j for j, k in enumerate(a["k_common"]) if 0.3 < k < 2.9]
    checks["12573: the control's P(k) agrees with CLASS halofit within 22 percent from k = 0.3 to 2.9 h/Mpc in the 100 Mpc/h box"] = all(abs(a["P_over_halofit_control"][j] - 1) < 0.22 for j in i)
    checks["12573: same seed: peak counts agree within 1 percent in all boxes"] = all(abs(v["control"]["npeaks"] - v["coupled"]["npeaks"]) <= 0.01 * v["control"]["npeaks"] for v in nb.values())
    checks["12573: no runaway: the coupled share in the densest tenth of peaks rises by at most 1.4 at the smallest scale, and control stays within 0.02"] = all(v["coupled"]["F1_top"] < 1.4 and abs(v["control"]["F1_top"] - 1) < 0.02 for v in nb.values())
    checks["12573: retraction: the coupled species is concentrated in peaks, opposite to the toy of Pass 12563, which used a constant positive chi_dot"] = all(v["coupled"]["F1_top"] > 1.1 for v in nb.values())
    checks["12573: total P(k) changes by under 3 percent at all resolved k"] = all(abs(x - 1) < 0.03 for v in nb.values() for x in v["P_ratio"])
    checks["12573: nonlinear phase mixing: low-k amplitude ratio falls from the linear 1.06 to about 1.02 in the full run"] = 1.01 < a["amp_ratio_coupled"][0] < 1.03

    # 12574
    gf = {s: load(f"class_growth_dovekie_{s}.json") for s in ("des", "kids", "none")}
    t = {}
    for s, g in gf.items():
        L0 = g["LCDM"]["chi2"]
        t[s] = {k: dict(delta=g[k]["chi2"] - L0, S8=g[k]["info"]["S8"], S8chi2=g[k]["parts"].get("S8"), fs8chi2=g[k]["parts"]["fs8"], lens=g[k]["parts"]["lens"]) for k in ("LCDM", "exp", "free_neg", "relax")}
        t[s]["cp_gain"] = g["exp"]["chi2"] - g["free_neg"]["chi2"]
    res["growth"] = t
    checks["12574: DES Y6 S8 prior: the c' gain falls to 4.0 (2 sigma); both models stay ahead of LCDM by over 6"] = 3.5 < t["des"]["cp_gain"] < 4.5 and t["des"]["free_neg"]["delta"] < -6 and t["des"]["relax"]["delta"] < -6
    checks["12574: KiDS-Legacy S8 prior: the c' gain stays near 7.7, so the penalty depends on the survey"] = 7 < t["kids"]["cp_gain"] < 8.3
    checks["12574: with no S8 prior the gain is 8.8, about 1 above lensing alone: f sigma8 favours the coupling only mildly, chi2 near 6 on 6 points for every model"] = 8.3 < t["none"]["cp_gain"] < 9.3 and all(5 < t["none"][k]["fs8chi2"] < 7 for k in ("LCDM", "exp", "free_neg", "relax"))
    checks["12574: under DES the S8 prior pulls S8 to about 0.816 in the coupled models, against 0.806 in LCDM"] = abs(t["des"]["free_neg"]["S8"] - 0.816) < 0.004 and abs(t["des"]["LCDM"]["S8"] - 0.806) < 0.003

    # 12575, 12576
    mk = {s: load(f"casimir_mink_{s}.json") for s in SETS}
    res["minkowski"] = mk
    checks["12575: V_min = 0 at x_0 = 0.59 to 0.65 with fits -8.2, -10.4, -17.1, R 9.2 to 10.2 microns, M about 12.7 meV"] = all(0.58 < m["x0"] < 0.66 and 9 < m["R_micron"] < 10.4 and 0.0125 < m["M_eV"] < 0.0130 for m in mk.values()) and abs(mk["pantheon"]["delta"] + 8.23) < 0.05 and abs(mk["dovekie"]["delta"] + 10.42) < 0.05 and abs(mk["desy5"]["delta"] + 17.06) < 0.05
    checks["12575: acceleration ends 4 to 7.5 Gyr from now; slope |V'/V| today is 1.1 to 1.6"] = all(4 < m["future_near_row"]["acceleration_ends_Gyr"] < 7.6 and 1.1 < m["slope_today"] < 1.6 for m in mk.values())
    checks["12576: the minimum is global along the radion; TCC at V_min > 0 limits its life to 2800 to 3100 Gyr, so another channel is needed"] = all(m["global_along_radion"] and 2800 < m["TCC_relax"]["T_max_Gyr"] < 3100 for m in mk.values())

    # 12577
    ss = load("dd_ss_gravitino.json")
    res["gravitino"] = ss
    rows = ss["rows"]
    checks["12577: control: N_eff vanishes as omega goes to 0"] = ss["control_Neff_small_omega"] < 1e-5
    checks["12577: no AdS3 at every twist tested, 0.02 to 0.5, with m1 bound 11 to 14.2 meV"] = all(not r["ads3_at_m1_0"] and 0.011 < r["m1_bound_eV"] < 0.0142 for r in rows)
    checks["12577: at eps = -0.33, omega = 1/2 gives N_eff = 15.5, R = 14.8 microns, gravitino 6.7 meV"] = abs(rows[0]["Neff"] - 15.5) < 1e-6 and abs(rows[0]["R_micron"] - 14.78) < 0.02 and abs(rows[0]["gravitino_eV"] - 0.00667) < 1e-4

    # 12578
    fr = load("dd_fraction.json")
    res["fraction"] = fr
    checks["12578: control: T_i for all dark matter at R = 1 micron is 3.97 GeV, against 4 GeV in arXiv:2209.09249"] = abs(fr["control_Ti_all_DM_GeV"]["1.0"] - 4) < 0.1
    checks["12578: at R = 8.5 microns, f = 0.08 needs T_i = 0.84 GeV, and T_i = 1 GeV gives f = 0.14"] = abs(fr["Ti_GeV"]["8.5"]["0.08"] - 0.84) < 0.01 and abs(fr["f_at_natural"]["8.5"]["1.0"] - 0.136) < 0.002

    # 12579
    mu = 0.1973269804 / 30.0  # eV, range 30 microns
    res["volume_modulus"] = dict(mu_min_eV=mu, scale_eV=math.sqrt(mu * 2.435e27), scale_TeV=math.sqrt(mu * 2.435e27) / 1e12)
    checks["12579: a volume modulus with range below 30 microns has mu above 6.6 meV and a stabiliser scale near 4 TeV, far from the eV scale of the light sector"] = abs(mu - 0.00658) < 1e-4 and 3 < res["volume_modulus"]["scale_TeV"] < 5

    # 12580
    pl = {s: load(f"class_massive_{s}.json") for s in SETS}
    cas = {s: load(f"class_casimir_{s}.json") for s in ("dovekie", "desy5")}
    res["three_vacua"] = dict(relax={s: pl[s]["relax"]["delta"] for s in SETS}, near_knife_edge_x06={s: pl[s]["0.6"]["delta"] for s in SETS}, gravitino_n4={s: cas[s]["b707_neg"]["delta"] for s in cas}, fading={s: pl[s]["free_neg"] - pl[s]["LCDM"] for s in SETS})
    v = res["three_vacua"]
    checks["12580: on full Planck the three vacua and fading tie within 0.7 on each sample"] = all(max(abs(v["relax"][s] - v["fading"][s]), abs(v["near_knife_edge_x06"][s] - v["fading"][s])) < 0.7 for s in SETS) and all(abs(v["gravitino_n4"][s] - v["fading"][s]) < 0.7 for s in cas)

    checks = {k: bool(x) for k, x in checks.items()}
    res["checks"] = checks
    res["all_checks_pass"] = all(checks.values())
    OUT.write_text(json.dumps(res, indent=2, default=float))
    print(json.dumps(checks, indent=1), res["all_checks_pass"])
    print(json.dumps(dict(growth=t, vacua=v), indent=0, default=float)[:1800])


if __name__ == "__main__":
    main()
