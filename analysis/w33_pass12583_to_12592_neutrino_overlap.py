"""Passes 12583-12592 (Claude track).  Not a theory of everything: see PASS12583_12592_NEUTRINO_OVERLAP.md.

12583 -- shear-equivalent S8: a LCDM analysis of coupled-model shear returns an S8 lower by about 0.012, because the growth is late.
12584 -- DES Y6 with that shift: the c' gain is 6.7, not the 4.0 of Pass 12574.  A Limber equivalence, not a 3x2pt likelihood.
12585 -- N-body to 31 kpc/h: the coupled share in peaks converges; no runaway.
12586 -- Lyman-alpha compressed in the fit: LCDM misses it and the coupling neither helps nor hurts.
12587 -- growth fits on DES-SN5YR repeat the Dovekie pattern.
12588 -- massive hypermultiplets give the gravitino route a minimum: same fit, in compressed CMB.
12589 -- no AdS3 at the four fitted points tested, with m_1 <= 11 meV for Dirac neutrinos in normal ordering.
12590 -- omega = 1/2 is a true joint minimum in radius and twist, but of mass about H0 for kappa = 1.
12591 -- cluster gas fraction: a 0.6 percent baryon-fraction signal, smaller than the distance term.
12592 -- neutrino mass: the pull to low mass falls by a factor of 5 to 6, and the c' gain depends on the mass.
"""

import json
import math
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
D = ROOT / "analysis" / "toe_uv"
OUT = ROOT / "data" / "w33_pass12583_to_12592_neutrino_overlap.json"


def load(n):
    return json.loads((D / n).read_text())


def vertex(rows):
    ms = sorted(rows, key=float)
    x = np.array([float(k) for k in ms])
    y = np.array([rows[k]["chi2"] for k in ms])
    a, b, c = np.polyfit(x, y, 2)
    return dict(vertex=float(-b / (2 * a)), sigma=float(1 / math.sqrt(a)), n_sigma_from_006=float((0.06 + b / (2 * a)) * math.sqrt(a)))


def main():
    checks, res = {}, {}

    # 12583
    sh = {s: load(f"class_shear_{s}.json") for s in ("dovekie", "desy5")}
    res["shear"] = {s: dict(control=v["control_LCDM"], shift={k: r["S8_equiv"] - r["S8_true"] for k, r in v["rows"].items()}, resid={k: r["resid_chi2"] for k, r in v["rows"].items()}) for s, v in sh.items()}
    checks["12583: control: a LCDM model returns its own S8 within 0.0002"] = all(abs(v["control_LCDM"]["S8_true"] - v["control_LCDM"]["S8_equiv"]) < 2e-4 for v in sh.values())
    checks["12583: coupled models shift by -0.011 to -0.017 and the exponential by under -0.007"] = all(-0.017 < v["rows"][k]["S8_equiv"] - v["rows"][k]["S8_true"] < -0.011 for v in sh.values() for k in ("free_neg", "free_pos", "relax")) and all(-0.007 < v["rows"]["exp_neg"]["S8_equiv"] - v["rows"]["exp_neg"]["S8_true"] < 0 for v in sh.values())
    checks["12583: the LCDM family absorbs the shape: residual chi2 under 0.6 on the mock covariance"] = all(r["resid_chi2"] < 0.6 for v in sh.values() for r in v["rows"].values())

    # 12584, 12587
    t = {}
    for ds in ("dovekie", "desy5"):
        t[ds] = {}
        for s in ("none", "des", "desq"):
            g = load(f"class_growth_{ds}_{s}.json")
            t[ds][s] = {k: g[k]["chi2"] - g["LCDM"]["chi2"] for k in ("exp", "free_neg", "relax")}
            t[ds][s]["LCDM"] = g["LCDM"]["chi2"]
            t[ds][s]["S8_chi2_fading"] = g["free_neg"]["parts"].get("S8")
    res["growth"] = t
    gain = lambda ds, s: t[ds][s]["exp"] - t[ds][s]["free_neg"]
    res["c_prime_gain"] = {ds: {s: gain(ds, s) for s in ("none", "des", "desq")} for ds in t}
    checks["12584: on Dovekie the c' gain with DES is 4.0 uncorrected and 6.7 with the shift; no S8 prior 8.8"] = abs(gain("dovekie", "des") - 3.96) < 0.1 and abs(gain("dovekie", "desq") - 6.72) < 0.1 and abs(gain("dovekie", "none") - 8.78) < 0.1
    checks["12587: DES-SN5YR repeats the order: none > desq > des"] = gain("desy5", "none") > gain("desy5", "desq") > gain("desy5", "des")
    checks["12587: fading and the relaxing radion stay within 0.5 of each other under every prior on both samples"] = all(abs(t[ds][s]["free_neg"] - t[ds][s]["relax"]) < 0.5 for ds in t for s in t[ds])

    # 12585
    nb = {k: load(f"nbody_{k}.json") for k in ("L6_b707", "L6_b1225", "L25_b707", "L25_b707_seed77", "L25_b1225", "L100_b707")}
    res["nbody"] = {k: dict(F1_top=v["coupled"]["F1_top"], control=v["control"]["F1_top"], peaks=[v["control"]["npeaks"], v["coupled"]["npeaks"]], P_max=max(abs(x - 1) for x in v["P_ratio"]), cell_kpc=1000 * v["L"] / v["Ng"]) for k, v in nb.items()}
    checks["12585: converged: b = 1/sqrt 2 peak share 1.18 to 1.24 across 100, 25 (two seeds) and 6 Mpc/h"] = all(1.15 < nb[k]["coupled"]["F1_top"] < 1.25 for k in ("L6_b707", "L25_b707", "L25_b707_seed77", "L100_b707"))
    checks["12585: no runaway at b = sqrt(3/2) down to a 31 kpc/h cell: share under 1.4"] = all(nb[k]["coupled"]["F1_top"] < 1.4 for k in ("L6_b1225", "L25_b1225"))
    checks["12585: peak counts change by under 1.5 percent and the control's share stays near 1"] = all(abs(v["control"]["npeaks"] - v["coupled"]["npeaks"]) <= 0.015 * v["control"]["npeaks"] and abs(v["control"]["F1_top"] - 1) < 0.03 for v in nb.values())

    # 12586
    ly = load("class_growth_dovekie_lya.json")
    res["lya"] = {k: dict(delta=ly[k]["chi2"] - ly["LCDM"]["chi2"], lya=ly[k]["parts"]["lya"], D2=ly[k]["info"]["lya"]["D2"], n=ly[k]["info"]["lya"]["n"]) for k in ("LCDM", "exp", "free_neg", "relax")}
    checks["12586: LCDM misses Lyman-alpha at chi2 about 18.7, an existing tension"] = 17 < ly["LCDM"]["parts"]["lya"] < 20
    checks["12586: the coupling neither helps nor hurts within 2: slope n unchanged within 0.002"] = all(abs(ly[k]["parts"]["lya"] - ly["LCDM"]["parts"]["lya"]) < 2 and abs(ly[k]["info"]["lya"]["n"] - ly["LCDM"]["info"]["lya"]["n"]) < 0.002 for k in ("exp", "free_neg", "relax"))
    checks["12586: the gain survives: fading -11.4, radion -10.0"] = abs(res["lya"]["free_neg"]["delta"] + 11.41) < 0.1 and abs(res["lya"]["relax"]["delta"] + 10.04) < 0.1

    # 12588
    su = {s: load(f"casimir_sugra_{s}.json") for s in ("dovekie", "desy5")}
    res["sugra"] = {s: {nh: {k: {a: r.get(a) for a in ("delta", "x0", "R_micron", "M_eV", "V_min", "turnaround_Gyr")} for k, r in b["rows"].items()} for nh, b in v.items()} for s, v in su.items()}
    checks["12588: every N_H and x_i gives at least the fading fit on the same compressed likelihood"] = all(r["delta"] < b["fading"] for v in su.values() for b in v.values() for r in b["rows"].values())
    checks["12588: V_min is positive at the minimum, turning negative only by x_i/x_min = 1.35 or below 1.2 for large N_H"] = all(b["rows"]["1.0"]["V_min"] > 0 and b["rows"]["1.35"]["V_min"] < 0 for v in su.values() for b in v.values())
    checks["12588: R is 10 to 15 microns and M 8 to 37 meV across the grid"] = all(10 < r["R_micron"] < 15.5 and 0.008 < r["M_eV"] < 0.038 for v in su.values() for b in v.values() for r in b["rows"].values())

    # 12589
    ad = load("dd_sugra_ads3.json")
    res["ads3"] = ad["rows"]
    D21, D31 = 7.49e-5, 2.513e-3
    summ = lambda m: m + math.sqrt(m * m + D21) + math.sqrt(m * m + D31)
    res["sum_mnu_window_eV"] = [summ(0.0), summ(max(r["m1_bound_eV"] for r in ad["rows"]))]
    checks["12589: no AdS3 at all four rows"] = len(ad["rows"]) == 4 and all(not r["ads3"] for r in ad["rows"])
    checks["12589: m_1 bound 9.9 to 10.9 meV, so sum m_nu 0.059 to 0.076 eV in normal ordering"] = all(0.0098 < r["m1_bound_eV"] < 0.011 for r in ad["rows"]) and abs(res["sum_mnu_window_eV"][1] - 0.076) < 0.001

    # 12590
    tw = load("dd_twist_joint.json")
    res["twist"] = dict(joint=tw, mass=ad["twist"])
    checks["12590: control: gravity alone has omega = 1/2 at every radius"] = all(c == 0.5 for c in tw["control_NH0_omega_min"])
    checks["12590: for each N_H omega = 1/2 is a joint minimum: both Hessian eigenvalues positive, and the only local minimum on the grid"] = all(min(r["eig"]) > 0 and len(r["local_minima"]) == 1 and r["local_minima"][0]["omega"] == 0.5 for r in tw["rows"].values())
    checks["12590: at small radius omega = 0 wins for N_H >= 4, so the vacuum has a basin, not a global attractor"] = all(tw["rows"][n]["omega_scan"]["0.3"]["omega"] == 0.0 for n in ("4", "6", "8"))
    checks["12590: twist mass about 3.4 H0 at the stand-in kappa = 1"] = 3 < ad["twist"]["mu_over_H0_kappa1"] < 4

    # 12591
    fg = load("class_fgas_dovekie.json")
    res["fgas"] = fg
    checks["12591: control: LCDM returns 1 at all z"] = all(abs(x - 1) < 1e-9 for x in fg["control_LCDM_A"])
    checks["12591: baryon fraction moves 0.5 to 0.7 percent between z = 0.1 and 1.1 and the apparent signal is about 2.3 percent, mostly distance"] = all(0.004 < fg["rows"][k]["A_fb"][-1] - 1 < 0.007 and 0.02 < fg["rows"][k]["A"][-1] - 1 < 0.025 and fg["rows"][k]["A_dist"][-1] - 1 > fg["rows"][k]["A_fb"][-1] - 1 for k in ("free_neg", "relax"))

    # 12592
    P = {k: load(f"class_mnu_dovekie_{k}.json")["rows"] for k in ("LCDM", "free_neg")}
    E = load("class_mnu_dovekie_exp.json")["rows"]
    R = load("class_mnu_dovekie_relax.json")["rows"]
    gn = load("class_growth_dovekie_none.json")
    gd = load("class_growth_desy5_none.json")
    chi = dict(LCDM={k: v["chi2"] for k, v in P["LCDM"].items()}, fading={k: v["chi2"] for k, v in P["free_neg"].items()}, exp=dict({k: v["chi2"] for k, v in E.items()}, **{"0.06": gn["exp"]["chi2"]}), relax=dict({k: v["chi2"] for k, v in R.items()}, **{"0.06": gn["relax"]["chi2"]}))
    res["mnu_chi2_dovekie"] = chi
    res["c_prime_gain_vs_mass"] = {m: chi["exp"][m] - chi["fading"][m] for m in ("0.01", "0.06", "0.12")}
    res["c_vs_mass"] = {m: P["free_neg"][m]["p"]["cp"] for m in P["free_neg"]}
    res["vertex"] = {k: vertex(P[k]) for k in P}
    pull = {m: (chi["LCDM"][m] - chi["LCDM"]["0.01"]) / (chi["fading"][m] - chi["fading"]["0.01"]) for m in ("0.06", "0.12", "0.25")}
    res["pull_ratio"] = pull
    L5 = load("class_mnu_desy5_LCDM.json")["rows"]
    F5 = load("class_mnu_desy5_free_neg.json")["rows"]
    res["mnu_chi2_desy5"] = dict(LCDM={"0.01": L5["0.01"]["chi2"], "0.06": gd["LCDM"]["chi2"], "0.12": L5["0.12"]["chi2"]}, fading={"0.01": F5["0.01"]["chi2"], "0.06": gd["free_neg"]["chi2"], "0.12": F5["0.12"]["chi2"]})
    q5 = res["mnu_chi2_desy5"]
    Fq = load("class_mnu_dovekie_free_neg_desq.json")["rows"]
    Lq = load("class_mnu_dovekie_LCDM_desq.json")["rows"]
    gq = load("class_growth_dovekie_desq.json")
    res["mnu_desq_dovekie"] = dict(LCDM={"0.01": Lq["0.01"]["chi2"], "0.06": gq["LCDM"]["chi2"], "0.12": Lq["0.12"]["chi2"]}, fading={"0.06": gq["free_neg"]["chi2"], "0.12": Fq["0.12"]["chi2"], "0.25": Fq["0.25"]["chi2"]})
    mq = res["mnu_desq_dovekie"]
    checks["12592: control: the 0.06 rows return the earlier fits within 0.01"] = abs(chi["LCDM"]["0.06"] - gn["LCDM"]["chi2"]) < 0.01 and abs(chi["fading"]["0.06"] - gn["free_neg"]["chi2"]) < 0.01
    checks["12592: control: LCDM effective mass is negative, -0.073 +- 0.052, about 2.6 sigma from 0.06, matching arXiv:2603.13208's 2.59 sigma"] = abs(res["vertex"]["LCDM"]["vertex"] + 0.0734) < 0.002 and 2.4 < res["vertex"]["LCDM"]["n_sigma_from_006"] < 2.8
    checks["12592: the pull to low mass falls by a factor of 5 to 6 in fading"] = all(5 < v < 6.5 for v in pull.values())
    checks["12592: DES-SN5YR agrees: same mass range, pull smaller by over 3"] = (q5["LCDM"]["0.12"] - q5["LCDM"]["0.01"]) / (q5["fading"]["0.12"] - q5["fading"]["0.01"]) > 3
    checks["12592: the c' gain depends on the mass: 4.2, 8.8, 16.2 at 0.01, 0.06, 0.12 eV"] = abs(res["c_prime_gain_vs_mass"]["0.01"] - 4.25) < 0.05 and abs(res["c_prime_gain_vs_mass"]["0.06"] - 8.78) < 0.05 and abs(res["c_prime_gain_vs_mass"]["0.12"] - 16.23) < 0.05
    checks["12592: c' rises with mass from 0.047 to 0.076: a degeneracy"] = res["c_vs_mass"]["0.01"] < res["c_vs_mass"]["0.06"] < res["c_vs_mass"]["0.12"] < res["c_vs_mass"]["0.25"]
    checks["12592: the relaxing radion has the same profile within 0.2"] = all(abs(chi["relax"][m] - chi["fading"][m]) < 0.2 for m in ("0.01", "0.06", "0.12"))
    checks["12592: BAO in fading stays flat, 9.0 to 9.2, while LCDM goes 12 to 22"] = all(8.9 < P["free_neg"][m]["parts"]["bao"] < 9.2 for m in P["free_neg"]) and P["LCDM"]["0.25"]["parts"]["bao"] - P["LCDM"]["0.01"]["parts"]["bao"] > 10
    checks["12592: with the shifted DES prior fading is flat to 0.12 eV while LCDM worsens by 5.5"] = abs(mq["fading"]["0.12"] - mq["fading"]["0.06"]) < 0.2 and mq["LCDM"]["0.12"] - mq["LCDM"]["0.06"] > 5

    res["checks"] = checks
    res["all_checks_pass"] = all(checks.values())
    OUT.write_text(json.dumps(res, indent=1, default=float), encoding="utf-8")
    for k, v in checks.items():
        print(("PASS" if v else "FAIL"), k.encode("ascii", "replace").decode())
    print("all_checks_pass", res["all_checks_pass"])
    print(json.dumps(dict(gain=res["c_prime_gain"], gain_mass=res["c_prime_gain_vs_mass"], pull=pull, vertex=res["vertex"], win=res["sum_mnu_window_eV"], des=mq, d5=q5, lya=res["lya"]), default=float))


if __name__ == "__main__":
    main()
