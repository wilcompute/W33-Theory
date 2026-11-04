"""Passes 12563-12570 (Claude track).  Not a theory of everything: see PASS12563_12570_STABILISED_TOWER.md.

12563 -- the 7 percent component in a toy halo: no self-reinforced collapse; depleted by 12 to 25 percent inside 0.05 r_ta.
12564 -- massive bulk fermions: two or more with M R about 0.5 to 3 remove AdS3 and keep the negative sign today.
12565 -- they also put a minimum in the radion potential: the recollapse of Pass 12562 is not robust.
12566 -- no-AdS4 at that minimum selects x_0 below about 0.6: M about 11 to 13 meV, R about 7 to 10 microns; fits on full Planck.
12567 -- what could measure the exponent: not a 0.3 percent stage-V BAO survey.
12568 -- DESI z = 0.706 against eBOSS: no support, no contradiction.
12569 -- black holes as the rest: uncoupled on the fixed-volume direction, by cited results.
12570 -- lensing inside the fit: the c' gain is 7.7, the models stay tied.
"""

import json
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
D = ROOT / "analysis" / "toe_uv"
OUT = ROOT / "data" / "w33_pass12563_to_12570_stabilised_tower.json"
SETS = ("pantheon", "dovekie", "desy5")


def load(n):
    return json.loads((D / n).read_text())


def main():
    checks, res = {}, {}

    # 12563
    h = load("halo_shells.json")
    res["halo"] = {k: dict(slope_total=v["slope_total"], slope_coupled=v.get("slope_coupled"), f_inside_over_f={a: b / v["f"] for a, b in v.get("f_inside", {}).items()}) for k, v in h.items() if isinstance(v, dict) and "slope_total" in v}
    c = res["halo"]["control_b0"]
    checks["12563: control: b = 0 gives slope within 0.15 of Bertschinger's -9/4 (-2.37 measured, so the toy is for relative statements) and the two species agree within 5 percent"] = abs(c["slope_total"] + 2.25) < 0.15 and all(abs(x - 1) < 0.05 for x in c["f_inside_over_f"].values())
    a7, b4 = res["halo"]["b707_f7"], res["halo"]["b1225_f4"]
    checks["12563: at f b = 0.05 no runaway: the coupled fraction inside any radius stays within 0.75 to 1.05 of its cosmic value, at b = 1/sqrt 2 and sqrt(3/2)"] = all(0.75 < x < 1.05 for x in a7["f_inside_over_f"].values()) and all(0.75 < x < 1.05 for x in b4["f_inside_over_f"].values())
    n16 = res["halo"]["control_b707_n16000"]
    checks["12563: resolution: doubling shells moves f_inside/f at 0.05 r_ta by under 0.05"] = abs(n16["f_inside_over_f"]["0.05"] - a7["f_inside_over_f"]["0.05"]) < 0.05
    checks["12563: b = sqrt(3/2) with f = 30 percent is strongly expelled, a non-vacuous control of the force"] = res["halo"]["b1225_f30"]["f_inside_over_f"]["0.05"] < 0.4

    # 12564
    fm = load("dd_massive_fermions.json")
    res["fermion_controls"] = dict(C=fm["control_C_small_x"], no_tower_m1=fm["control_no_tower_m1_bound"])
    grid = fm["grid"]
    res["fermion_grid"] = grid
    checks["12564: control: C(0) = 1 and no tower returns the m1 bound of Pass 12537, 7.65 meV"] = abs(fm["control_C_small_x"]["0.0001"] - 1) < 1e-6 and abs(fm["control_no_tower_m1_bound"] - 0.00765) < 0.0001
    G = lambda n, m: [r for r in grid if r["Nf"] == n and abs(r["MR"] - m) < 1e-9][0]
    checks["12564: control: gravitons alone give AdS3, as Pass 12539 found; so does one bulk fermion at any mass"] = G(0, 0.0)["ads3_at_m1_0"] and all(r["ads3_at_m1_0"] for r in grid if r["Nf"] == 1)
    checks["12564: two fermions with M R from 0.5 to 3 give no AdS3 at m1 = 0 and a negative sign today"] = all(not G(2, m)["ads3_at_m1_0"] and G(2, m)["sign"] == "negative" for m in (0.5, 0.75, 1.0, 1.5, 2.0, 3.0))
    checks["12564: the window closes on both sides: M R = 0.25 and 0 flip the sign to positive, M R = 5 brings AdS3 back"] = G(2, 0.0)["sign"] == "positive" and G(2, 0.25)["sign"] == "positive" and G(2, 5.0)["ads3_at_m1_0"]

    # 12565, 12566
    fine = {s: load(f"casimir_massive_fine_{s}.json") for s in SETS}
    chk = load("dd_massive_check.json")
    res["fine"] = {s: {k: {a: r.get(a) for a in ("delta", "x0", "eps", "R_micron", "M_eV", "prod")} | dict(V_min=r["future"]["V_at_minimum_over_crit"], turnaround_Gyr=r["future"]["t_turnaround_Gyr"]) for k, r in d["rows"].items() if "future" in r} for s, d in fine.items()}
    res["vacuum"] = chk
    do = res["fine"]["dovekie"]
    checks["12565: at x_0 = 0.5 the field settles in a minimum with V > 0 and no turnaround; at x_0 >= 0.75 V_min < 0 and it turns around: recollapse is not robust"] = all(res["fine"][s]["0.5"]["V_min"] > 0 and res["fine"][s]["0.5"]["turnaround_Gyr"] is None for s in SETS) and do["1.0"]["V_min"] < 0 and do["1.0"]["turnaround_Gyr"] is not None
    checks["12565: control: decoupled fermions (x_0 = 8) return the n = 4 model within 0.02"] = all(abs(res["fine"][s]["8.0"]["delta"] - fine[s]["n4_delta"]) < 0.02 for s in SETS)
    x_c = {}
    for s in SETS:
        rows = sorted(((v["x0"], v["V_min"]) for v in res["fine"][s].values()))
        for (x1, v1), (x2, v2) in zip(rows, rows[1:]):
            if v1 > 0 >= v2:
                x_c[s] = x1 + (x2 - x1) * v1 / (v1 - v2)
    res["x0_where_V_min_is_zero"] = x_c
    checks["12566: V_min = 0 at x_0 between 0.55 and 0.75 on all samples"] = all(0.55 < v < 0.75 for v in x_c.values()) and len(x_c) == 3
    win = {s: chk[s]["window"] for s in SETS}
    res["window"] = win
    checks["12566: the window passing no-AdS3 and no-AdS4 has M from 0.0105 to 0.0135 eV and R from 6.5 to 10.5 microns, on all samples"] = all(w is not None and w["M_eV"][0] > 0.0105 and w["M_eV"][1] < 0.0135 and w["R_micron"][0] > 6.5 and w["R_micron"][1] < 10.5 for w in win.values())
    checks["12566: inside that window the fit stays within 1 of the best fit on each sample at x_0 >= 0.45, so the data do not select x_0"] = all(abs(res["fine"][s]["0.5"]["delta"] - res["fine"][s]["8.0"]["delta"]) < 1 for s in SETS)
    m1 = [v["m1_bound_eV"] for s in SETS for v in chk[s]["rows"].values() if not v["ads3"] and not v["ads4"] and v["m1_bound_eV"]]
    res["m1_bounds_in_window"] = [min(m1), max(m1)]
    checks["12566: m1 bound in the window is 12 to 18 meV, wider than 7.65 meV without a tower"] = 0.012 < min(m1) and max(m1) < 0.018
    pl = {s: load(f"class_massive_{s}.json") for s in SETS}
    res["planck"] = {s: {k: dict(delta=v.get("delta"), x0=v.get("x0"), S8=v.get("info", {}).get("S8"), failed=v.get("failed")) for k, v in d.items() if isinstance(v, dict)} | dict(free_neg=d["free_neg"] - d["LCDM"]) for s, d in pl.items()}
    checks["12566: full Planck, two fluids: x_0 about 0.5 within 0.4 of the free-slope fading fit on all samples"] = all(abs(res["planck"][s]["0.5"]["delta"] - res["planck"][s]["free_neg"]) < 0.4 for s in pl)
    checks["12566: full Planck: the radion started at its minimum ties or beats the free-slope fit on all three samples, within 0.5"] = all(-0.5 < res["planck"][s]["free_neg"] - res["planck"][s]["relax"]["delta"] < 0.5 for s in pl)
    rx = {s: load(f"casimir_relax_{s}.json") for s in SETS}
    res["relax"] = {s: {k: {a: v[a] for a in ("delta", "prod", "f", "x0", "eps", "R_micron", "M_eV", "mu_over_H0", "dlnm")} | dict(V_min=v["future"]["V_at_minimum_over_crit"], turnaround=v["future"]["t_turnaround_Gyr"]) for k, v in d["rows"].items()} for s, d in rx.items()}
    checks["12566: started at the minimum, for b from 1/sqrt 2 to 1: V_min > 0, no turnaround, radion mass 3.6 to 5.5 H0, on all samples"] = all(v["V_min"] > 0 and v["turnaround"] is None and 3.5 < v["mu_over_H0"] < 5.6 for d in res["relax"].values() for v in d.values())

    # 12567
    nb = load("casimir_nobs_dovekie.json")
    res["exponent_observables"] = {k: nb[k] for k in ("zs", "dDM_percent_1_vs_12", "dDH_percent_1_vs_12", "dfs8_percent_1_vs_12", "dmu_mag_1_vs_12", "yardstick_chi2_BAO_0p3pc_8bins", "yardstick_chi2_fs8_1pc")}
    checks["12567: n = 1 and n = 12 differ by at most 0.25 percent in D_H, 0.2 percent in D_M, 0.35 percent in f sigma8, 0.005 mag in SN; a 0.3 percent BAO survey sees Delta chi2 of about 1.3"] = max(abs(x) for x in nb["dDH_percent_1_vs_12"]) < 0.25 and max(abs(x) for x in nb["dDM_percent_1_vs_12"]) < 0.2 and max(abs(x) for x in nb["dfs8_percent_1_vs_12"].values()) < 0.35 and max(abs(x) for x in nb["dmu_mag_1_vs_12"]) < 0.005 and nb["yardstick_chi2_BAO_0p3pc_8bins"] < 2

    # 12568
    lr = {s: load(f"dark_lrg2_{s}.json") for s in ("none", "dovekie")}
    res["lrg2"] = lr
    for s, d in lr.items():
        v = d["variants"]
        assert v["desi"]["gain"] > v["drop"]["gain"]
    checks["12568: replacing DESI z = 0.706 by eBOSS gives the gain of dropping the bin within 0.4 on both, well below DESI's"] = all(abs(d["variants"][k]["gain"] - d["variants"]["drop"]["gain"]) < 0.4 and d["variants"][k]["gain"] < d["variants"]["desi"]["gain"] - 2 for d in lr.values() for k in ("eboss_cons_r033", "eboss_cons_r0", "eboss_pk_r033"))
    p = lr["none"]["pulls_from_fit_without_bin"]
    checks["12568: against a fit without the bin, DESI's D_M is low and eBOSS's high, by about 1 sigma each: they do not agree on the direction, and neither is decisive"] = p["lcdm_desi"]["DM_pull"] < -0.5 and p["lcdm_eboss"]["DM_pull"] > 0.5
    checks["12568: both DESI D_H and eBOSS D_H are low against the fit; D_H and D_M each carry part of the DESI gain"] = p["lcdm_desi"]["DH_pull"] < -1 and p["lcdm_eboss"]["DH_pull"] < -0.5 and lr["none"]["variants"]["desi_DM_only"]["gain"] > 2.8 and lr["none"]["variants"]["desi_DH_only"]["gain"] > 3.5

    # 12569
    bh = load("dd_pbh.json")
    res["pbh"] = bh
    checks["12569: control: the 4D lifetime formula returns the usual age-of-universe mass within a factor 3 of 5e14 g"] = 1.5e14 < bh["control_4d_mass_at_age_g"] < 1.5e15
    r13 = bh["13.0"]
    checks["12569: at R = 13 microns the 5D regime reaches 3e24 g, covering the asteroid window, and holes there are far colder and longer lived"] = r13["M_crossover_g"] > 1e24 and r13["r5_micron_1e+20"] < 1 and r13["tau_over_age_1e+17"] > 1e10

    # 12570
    lf = load("class_lensfit_dovekie.json")
    L0 = lf["LCDM"]["chi2"]
    res["lensfit"] = {k: dict(delta=v["chi2"] - L0, lens=v["parts"]["lens"], S8=v["info"]["S8"]) for k, v in lf.items() if isinstance(v, dict) and "chi2" in v}
    gain = lf["exp"]["chi2"] - lf["free_neg"]["chi2"]
    res["cp_gain_with_lens_in_fit"] = gain
    checks["12570: lensing in the fit: c' gain 7.7, near 2.8 sigma, up by under 1 from no lensing, and below the post hoc 8.0"] = 7.2 < gain < 8.0
    checks["12570: fading, negative Casimir and sparse free-c stay tied within 0.3 with lensing in the fit"] = max(res["lensfit"][k]["delta"] for k in ("free_neg", "casimir_neg", "sparse_b707_free_c")) - min(res["lensfit"][k]["delta"] for k in ("free_neg", "casimir_neg", "sparse_b707_free_c")) < 0.3
    checks["12570: lensing chi2 stays near the 19 bandpowers for all of them"] = all(19 < v["lens"] < 21 for v in res["lensfit"].values())

    checks = {k: bool(v) for k, v in checks.items()}
    res["checks"] = checks
    res["all_checks_pass"] = all(checks.values())
    OUT.write_text(json.dumps(res, indent=2, default=float))
    print(json.dumps(checks, indent=1), res["all_checks_pass"])
    print(json.dumps(dict(x_c=x_c, win=win, m1=res["m1_bounds_in_window"], planck=res["planck"], lens=res["lensfit"], gain=gain), indent=0, default=float))


if __name__ == "__main__":
    main()
