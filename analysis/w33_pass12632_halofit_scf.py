"""Pass 12632 producer (claude track): the CLASS halofit scalar-field bug, its fix, and the corrected shear comparison.
Reads analysis/toe_uv/{halofit_check_orig,halofit_check_hf,hf_impact,hf_matched_fluid,sign_des[_orig],sign_des_kids[_orig],
shear_hybrid_{des,kids}[_orig]}.json and, when present, the corrected held-out shear files (shear_ppd*.json with *_orig.json).
Writes data/w33_pass12632_halofit_scf.json.
usage: py -3 analysis/w33_pass12632_halofit_scf.py"""
import json
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
UV = os.path.join(ROOT, "analysis", "toe_uv")


def L(n):
    return json.load(open(os.path.join(UV, n), encoding="utf-8"))


ho, hh, imp, mf = L("halofit_check_orig.json")["rows"], L("halofit_check_hf.json")["rows"], L("hf_impact.json"), L("hf_matched_fluid.json")


def maxdev(a, b):
    return max(abs(a[z][k] / b[z][k] - 1) for z in a for k in a[z])


def rel(d, key="des"):
    return {m: d[m][key] - d["LCDM"][key] for m in d}


shear_fixed = {s: dict(patched=rel(L(f"sign_des{x}.json")), original=rel(L(f"sign_des{x}_orig.json"))) for s, x in (("des", ""), ("kids", "_kids"))}
hyb = {s: dict(patched=L(f"shear_hybrid_{s}.json")["split"]["all"], original=L(f"shear_hybrid_{s}_orig.json")["split"]["all"]) for s in ("des", "kids")}
checks = dict(
    patched_scf_equals_lambda=maxdev(hh["lcdm_scf"], hh["lcdm_lambda"]) < 1e-5,  # measured 2.0e-6: the numerical Omega_scf tuning (shooting) precision; original build 0.58
    fluid_equals_lambda_both_builds=maxdev(hh["lcdm_fluid"], hh["lcdm_lambda"]) < 1e-9 and maxdev(ho["lcdm_fluid"], ho["lcdm_lambda"]) < 1e-9,
    original_scf_wrong_by_25pct=maxdev(ho["lcdm_scf"], ho["lcdm_lambda"]) > 0.25,
    cpl_untouched_by_patch=maxdev(hh["cpl_fit"], ho["cpl_fit"]) < 1e-9,
    training_controls_zero=abs(imp["CPL"]["delta_hf_minus_orig"]["total"]) < 1e-9 and abs(imp["LCDM_native"]["delta_hf_minus_orig"]["total"]) < 1e-9,
    training_shift_below_1=all(abs(v["delta_hf_minus_orig"]["total"]) < 1.0 for v in imp.values()),
    matched_fluid_uncoupled_agrees_0p1pct=mf["exp_neg"]["max_frac_dev_vs_fluid"]["patched"] < 1e-3,
    matched_fluid_all_patched_within_5pct=all(v["max_frac_dev_vs_fluid"]["patched"] < 0.05 for v in mf.values()),
    matched_fluid_original_off_by_50pct=all(v["max_frac_dev_vs_fluid"]["original"] > 0.5 for v in mf.values()),
    cpl_fixed_background_shear_unchanged=all(abs(L(f"sign_des{x}.json")["CPL"]["des"] - L(f"sign_des{x}_orig.json")["CPL"]["des"]) < 0.05 for x in ("", "_kids")),
    corrected_cpl_minus_fading_below_1=all(abs(shear_fixed[s]["patched"]["CPL"] - shear_fixed[s]["patched"]["free_neg"]) < 1.0 for s in shear_fixed),
    original_cpl_minus_fading_above_2p5=all(shear_fixed[s]["original"]["CPL"] - shear_fixed[s]["original"]["free_neg"] > 2.5 for s in shear_fixed),
)
heldout = {}
for f in ("shear_ppd.json", "shear_ppd_kids_dovekie.json", "shear_ppd_desy5.json"):
    p = os.path.join(UV, f)
    d = json.load(open(p))
    if "LCDM" in d and "free_neg" in d:
        o = L(f.replace(".json", "_orig.json"))
        heldout[f] = dict(patched={m: d[m]["elpd_shear"] - d["LCDM"]["elpd_shear"] for m in d}, original={m: o[m]["elpd_shear"] - o["LCDM"]["elpd_shear"] for m in o}, cpl_raw_unchanged=abs(d["CPL"]["elpd_shear"] - o["CPL"]["elpd_shear"]) < 1e-9)
if heldout:
    checks["heldout_cpl_rows_untouched"] = all(v["cpl_raw_unchanged"] for v in heldout.values())
out = dict(pass_number=12632, track="claude", halofit_rows=dict(original=ho, patched=hh), training_impact={m: v["delta_hf_minus_orig"] for m, v in imp.items()}, matched_fluid={m: dict(w0=v["w0"], wa=v["wa"], dev=v["max_frac_dev_vs_fluid"]) for m, v in mf.items()}, shear_fixed_background_rel_lcdm=shear_fixed, hybrid_all=hyb, heldout_shear_rel_lcdm=heldout, checks=checks, all_checks_pass=all(checks.values()))
json.dump(out, open(os.path.join(ROOT, "data", "w33_pass12632_halofit_scf.json"), "w"), indent=1, default=float)
for k, v in checks.items():
    print(k, v)
print({s: {k: {m: round(x, 2) for m, x in v.items()} for k, v in d.items()} for s, d in shear_fixed.items()})
print("all_checks_pass", out["all_checks_pass"])
