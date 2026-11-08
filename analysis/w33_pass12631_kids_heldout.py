"""Pass 12631 producer (claude track): KiDS-Legacy held-out shear and the combined out-of-sample scorecard; KLT-family f boundary.
Reads analysis/toe_uv/{shear_ppd,shear_ppd_desy5,shear_ppd_kids_dovekie,scorecard,klt2_check,klt2_scan,klt_fit}.json; writes data/w33_pass12631_kids_heldout.json.
usage: py -3 analysis/w33_pass12631_kids_heldout.py"""
import json
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
UV = os.path.join(ROOT, "analysis", "toe_uv")


def L(n):
    return json.load(open(os.path.join(UV, n), encoding="utf-8"))


d1, d5, kk, sc, k2, ks, kf = (L(n) for n in ("shear_ppd.json", "shear_ppd_desy5.json", "shear_ppd_kids_dovekie.json", "scorecard.json", "klt2_check.json", "klt2_scan.json", "klt_fit.json"))
rel = lambda d: {m: d[m]["elpd_shear"] - d["LCDM"]["elpd_shear"] for m in d}  # noqa: E731
R = dict(des_dovekie=rel(d1), des_desy5=rel(d5), kids_dovekie=rel(kk))
checks = dict(
    cpl_worst_on_all_three=all(r["CPL"] < min(r["LCDM"], r["free_neg"], r["free_pos"]) for r in R.values()),
    kids_cpl_penalty_vs_fading_above_2=kk["free_neg"]["elpd_shear"] - kk["CPL"]["elpd_shear"] > 2,
    lcdm_within_0p6_of_best_on_all=all(max(r.values()) - r["LCDM"] < 0.6 for r in R.values()),
    combined_fading_beats_cpl_by_3=sc["fading_cneg"]["oos_gain_dovekie_plus_des_kids_shear"] - sc["CPL"]["oos_gain_dovekie_plus_des_kids_shear"] > 3,
    combined_cpl_near_lcdm=abs(sc["CPL"]["oos_gain_dovekie_plus_des_kids_shear"]) < 1.5,
    klt2_control_reproduces_fit=abs(k2["control_f0.25"]["chi2"] - kf["klt_f0.25"]["chi2"]) < 1e-2,
    klt_small_f_no_dark_energy=("error" in k2["f0.1"]) and ("error" in ks["f0.12"]) and ("chi2" in ks["f0.2"]),
)
out = dict(pass_number=12631, track="claude", heldout_shear_rel_lcdm=R, combined=dict(fading=sc["fading_cneg"]["oos_gain_dovekie_plus_des_kids_shear"], CPL=sc["CPL"]["oos_gain_dovekie_plus_des_kids_shear"]), klt_boundary=dict(check=k2, scan=ks), checks=checks, all_checks_pass=all(checks.values()))
json.dump(out, open(os.path.join(ROOT, "data", "w33_pass12631_kids_heldout.json"), "w"), indent=1, default=float)
for k, v in checks.items():
    print(k, v)
print({k: {m: round(x, 2) for m, x in v.items()} for k, v in R.items()})
print("all_checks_pass", out["all_checks_pass"])
