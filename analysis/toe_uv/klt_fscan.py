"""KLT-family profile in f (class_klt2 build): at fixed f, refit the 7 base parameters + s + theta_i, starting with the same initial field value phi_ini = theta_i f = 0.561 M_P as the f = 0.25 best fit (breaks the f-theta_i degeneracy that stalled klt_ffit.py).
f in {0.18, 0.35, 0.5}; f = 0.25 is the existing fit (2253.30).  Smaller f has a lower quality cost (Pass 12630: N >~ 276.5/ln(sqrt2 M_P/f)).
usage: KLTBIN=~/cosmo/class_klt2/class python3 klt_fscan.py"""
import json, os, sys
BG = os.path.dirname(os.path.abspath(__file__)); os.chdir(BG); sys.path.insert(0, BG)
sys.argv = ["x", "dovekie", "sn"]
src = open("class_holdout.py", encoding="utf-8").read().split('if HOLD == "evidence":')[0]
g = dict(__name__="x", __file__=os.path.join(BG, "class_holdout.py")); exec(src, g)
F, C, BMASK, SN = g["F"], g["C"], g["BMASK"], g["SN"]; F.sn = SN; BMASK["on"] = True
C.STEP.update(ks=0.002, kth=0.05)
bf = json.load(open("klt_fit.json"))["klt_f0.25"]["p"]
phi0 = bf["kth"] * bf["kf"]
path = "klt_fscan.json"
out = json.load(open(path)) if os.path.exists(path) else {}
for f in (0.18, 0.35, 0.5):
    key = f"f{f}"
    if key in out:
        continue
    x0 = dict(bf, kf=f, kth=phi0 / f)
    try:
        r = F.fit(x0, C.NAMES + ["ks", "kth"], kind="klt", iters=6, log=lambda *a, **k: None)
        out[key] = dict(chi2=r["chi2"], p=r["p"], S8=r["info"].get("S8"))
        print(key, "chi2 %.2f s %.4f theta_i %.3f S8 %.4f" % (r["chi2"], r["p"]["ks"], r["p"]["kth"], r["info"].get("S8")), flush=True)
    except Exception as e:
        out[key] = dict(error=str(e)[-160:]); print(key, "FAILED", str(e)[-120:], flush=True)
    json.dump(out, open(path, "w"), indent=1, default=float)
