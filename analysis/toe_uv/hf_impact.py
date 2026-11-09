"""How much did the scalar-field halofit bug (class_halofit_scf_patch.py) move the training chi2?
Per-probe chi2 at the stored Dovekie best fits, original build vs patched build (same parameters, no refit), for every scf model,
with CPL as the control (fluid path: must not change) and LCDM_native (plain Lambda) as the reference for LCDM.
usage: python3 hf_impact.py"""
import json, os, sys
BG = os.path.dirname(os.path.abspath(__file__)); os.chdir(BG); sys.path.insert(0, BG)
sys.argv = ["x", "dovekie", "none"]
src = open("class_growth_fit.py", encoding="utf-8").read().split("F = GF(ds)")[0]
g = dict(__name__="x", __file__=os.path.join(BG, "class_growth_fit.py")); exec(src, g)
C, GF = g["C"], g["GF"]
F = GF("dovekie")
fits = json.load(open("class_fit_dovekie.json"))
klt = json.load(open("klt_fit.json"))["klt_f0.25"]["p"]
H = os.path.expanduser("~/cosmo")
BIN = dict(orig=(H + "/class_fading/class", H + "/class_klt/class"), hf=(H + "/class_fading_hf/class", H + "/class_klt_hf/class"))
models = [(m, dict(fits[m]["p"]), "cpl" if m == "CPL" else "fading") for m in ("LCDM", "LCDM_native", "free_neg", "free_pos", "exp_neg", "CPL")] + [("klt25", dict(klt), "klt")]
out = {}
for m, p, kind in models:
    row = {}
    for lab, (cb, kb) in BIN.items():
        C.CLASSBIN, C.KLTBIN = cb, kb
        if m == "LCDM_native":
            p2 = {k: v for k, v in p.items() if k not in ("c", "cp")}
            r, parts, info = F.resid(p2, "lambda")
        else:
            r, parts, info = F.resid(p, kind)
        row[lab] = dict(total=float(r @ r), **parts)
    row["delta_hf_minus_orig"] = {k: row["hf"][k] - row["orig"][k] for k in row["hf"]}
    out[m] = row
    print(m, "orig %.2f hf %.2f" % (row["orig"]["total"], row["hf"]["total"]), {k: round(v, 3) for k, v in row["delta_hf_minus_orig"].items()}, flush=True)
json.dump(out, open("hf_impact.json", "w"), indent=1)
