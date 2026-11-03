"""Fading dark sector against full Planck spectra + DESI + SNe, through class_fading_patch.py and class_cmb.py.  LCDM is the scf run with lambda = c' = 0, so every model shares the numerics.
Fits per sample: LCDM; CPL (native fluid with PPF); exponential c' = 0 on c < 0 and c > 0; free c' on each branch at fixed start from fading_ds_*.json; a c' profile at free c on the c < 0 branch; the Casimir line c = 4 c'.
Everything is a local optimum (Levenberg-Marquardt from the start given): a Delta chi2 is a lower limit on the true gain.
usage: python3 class_fits.py dataset [dataset...]"""
import json
import os
import sys
import numpy as np
import class_cmb as C

BG = os.path.dirname(os.path.abspath(__file__))
for ds in sys.argv[1:]:
    F = C.Fitter(ds)
    path = os.path.join(BG, f"class_fit_{ds}.json")
    out = json.load(open(path)) if os.path.exists(path) else dict(dataset=ds)
    prev = json.load(open(os.path.join(BG, f"fading_ds_{ds}.json")))
    base = C.NAMES

    def go(name, x0, free, kind="fading", fixed=None, tie=None):
        if name in out:
            return out[name]
        print(ds, name, flush=True)
        try:
            r = F.fit(x0, free, fixed=fixed, kind=kind, tie=tie)
        except Exception as e:
            print("FAILED", name, str(e)[-200:], flush=True)
            r = dict(failed=str(e)[-300:])
        out[name] = r
        if "chi2" in r:
            print(name, round(r["chi2"], 3), "delta", round(r["chi2"] - out["LCDM"]["chi2"], 3) if "LCDM" in out else "", {k: round(v, 4) for k, v in r["p"].items()}, r["parts"], r["info"], flush=True)
        json.dump(out, open(path, "w"), indent=1)
        return r

    lc = go("LCDM", dict(C.START, c=0.0, cp=0.0), base)
    x = lc["p"]
    go("LCDM_native", dict(x), base, kind="lcdm")  # the reference for CPL, which also runs without the scalar field
    go("CPL", dict(x, w0=-0.85, wa=-0.5, c=0.0, cp=0.0), base + ["w0", "wa"], kind="cpl")
    # phi-side start: omega_cdm at phi = 0 slightly higher than at recombination when c' > 0; the fit finds it
    for lab, c0 in (("exp_neg", -0.8), ("exp_pos", 0.8)):
        go(lab, dict(x, c=c0, cp=0.0), base + ["c"])
    for lab, key in (("free_neg", "free_c_neg"), ("free_pos", "free_c_pos")):
        s = prev[key]
        go(lab, dict(x, c=s["c"], cp=s["cp"]), base + ["c", "cp"])
    fn = out["free_neg"]["p"] if "p" in out["free_neg"] else dict(x, c=-0.9, cp=0.05)
    for cp in (() if os.environ.get("QUICK") else (0.02, 0.03, 0.05, 0.07, 0.1)):
        go(f"prof_neg_{cp}", dict(fn, cp=cp), base + ["c"])
    r4 = prev["ratio_lines"]["4.0"]

    def tie4(p):
        p["c"] = 4 * p["cp"]

    go("casimir", dict(x, cp=max(r4["cp"], 0.05), c=4 * max(r4["cp"], 0.05)), base + ["cp"], tie=tie4)
print("alldone", flush=True)
