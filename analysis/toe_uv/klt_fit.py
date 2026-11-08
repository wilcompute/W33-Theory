"""Fit the KLT-family model (class_klt_patch.py) and LCDM with the same fitter and likelihood (full Dovekie growth likelihood: plik-lite + tau + DESI + SN + lensing + f sigma8).
Free: 7 base parameters + s (ks) + initial angle theta_i (kth); f fixed at 0.25 M_P (their Model 1) and 0.1 M_P.  Starts from the LCDM best fit with theta_i = 2.8, s = 0.01 (the smoke-test point that runs).
usage: python3 klt_fit.py"""
import json, os, sys
BG = os.path.dirname(os.path.abspath(__file__)); os.chdir(BG); sys.path.insert(0, BG)
sys.argv = ["x", "dovekie", "sn"]
src = open("class_holdout.py", encoding="utf-8").read().split('if HOLD == "evidence":')[0]
g = dict(__name__="x", __file__=os.path.join(BG, "class_holdout.py")); exec(src, g)
F, C, BMASK, SN = g["F"], g["C"], g["BMASK"], g["SN"]; F.sn = SN; BMASK["on"] = True
C.STEP.update(ks=0.002, kth=0.05)
base = dict(json.load(open("class_fit_dovekie.json"))["LCDM"]["p"])
path = "klt_fit.json"
out = json.load(open(path)) if os.path.exists(path) else {}
if "LCDM" not in out:
    r = F.fit(dict(base), C.NAMES, kind="fading", iters=6, log=lambda *a, **k: None)
    out["LCDM"] = dict(chi2=r["chi2"], parts=r["parts"], p=r["p"])
    print("LCDM chi2 %.2f" % r["chi2"], flush=True); json.dump(out, open(path, "w"), indent=1, default=float)
for kf in (0.25, 0.1):
    key = f"klt_f{kf}"
    if key in out:
        continue
    x0 = dict(out["LCDM"]["p"], ks=0.01, kf=kf, kth=2.8)
    try:
        r = F.fit(x0, C.NAMES + ["ks", "kth"], kind="klt", iters=6, log=lambda *a, **k: None)
        out[key] = dict(chi2=r["chi2"], parts=r["parts"], p=r["p"], S8=r["info"].get("S8"))
        print(key, "chi2 %.2f" % r["chi2"], "s %.4f theta_i %.3f S8 %.4f" % (r["p"]["ks"], r["p"]["kth"], r["info"].get("S8")), {k: round(v, 2) for k, v in r["parts"].items()}, flush=True)
    except Exception as e:
        out[key] = dict(error=str(e)[-200:])
        print(key, "FAILED", str(e)[-200:], flush=True)
    json.dump(out, open(path, "w"), indent=1, default=float)
