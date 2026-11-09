"""Refit the Dovekie full-data (Planck + DESI + SN) best fits with the halofit-patched build (class_halofit_scf_patch.py),
starting from the stored original-build optima (class_fit_dovekie.json), so the change is the bug alone.
Models: LCDM (scf path), exp_neg, free_neg, free_pos; LCDM_native and CPL are on the Lambda/fluid paths and are copied unchanged.
Writes hf_refit_dovekie.json with chi2, parts and Delta chi2 vs LCDM (patched) and vs LCDM_native.
usage: CLASSBIN=~/cosmo/class_fading_hf/class python3 hf_refit.py"""
import json, os, sys
BG = os.path.dirname(os.path.abspath(__file__)); os.chdir(BG); sys.path.insert(0, BG)
import class_cmb as C
assert C.CLASSBIN.endswith("_hf/class"), "run with the patched CLASSBIN"
F = C.Fitter("dovekie")
old = json.load(open("class_fit_dovekie.json"))
path = "hf_refit_dovekie.json"
out = json.load(open(path)) if os.path.exists(path) else dict(classbin=C.CLASSBIN)
FREE = dict(LCDM=[], exp_neg=["c"], free_neg=["c", "cp"], free_pos=["c", "cp"])
for m, fr in FREE.items():
    if m in out:
        continue
    r = F.fit(dict(old[m]["p"]), C.NAMES + fr, kind="fading")
    out[m] = dict(chi2=r["chi2"], p=r["p"], parts=r["parts"], chi2_orig=old[m]["chi2"])
    print(m, "orig %.3f patched refit %.3f" % (old[m]["chi2"], r["chi2"]), flush=True)
    json.dump(out, open(path, "w"), indent=1)
for m in ("LCDM_native", "CPL"):
    out[m] = dict(chi2=old[m]["chi2"], p=old[m]["p"], unchanged="Lambda/fluid path, not affected")
out["delta_vs_LCDM"] = {m: out[m]["chi2"] - out["LCDM"]["chi2"] for m in list(FREE) + ["LCDM_native", "CPL"]}
out["delta_vs_LCDM_orig"] = {m: old[m]["chi2"] - old["LCDM"]["chi2"] for m in list(FREE) + ["LCDM_native", "CPL"]}
json.dump(out, open(path, "w"), indent=1)
print(json.dumps({k: {m: round(v, 2) for m, v in out[k].items()} for k in ("delta_vs_LCDM", "delta_vs_LCDM_orig")}))
