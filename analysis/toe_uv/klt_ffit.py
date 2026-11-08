"""KLT-family fit with the decay constant f free (class_klt2 build, better shooting guess), full Dovekie growth likelihood; start at the f = 0.25 best fit.
In the no-constant-term (v = 0) version, shooting fails for f <~ 0.12 M_P (a heavy field cannot act as dark energy without a separate constant), so f is bounded below in practice (klt2_scan.json).
usage: KLTBIN=~/cosmo/class_klt2/class python3 klt_ffit.py"""
import json, os, sys
BG = os.path.dirname(os.path.abspath(__file__)); os.chdir(BG); sys.path.insert(0, BG)
sys.argv = ["x", "dovekie", "sn"]
src = open("class_holdout.py", encoding="utf-8").read().split('if HOLD == "evidence":')[0]
g = dict(__name__="x", __file__=os.path.join(BG, "class_holdout.py")); exec(src, g)
F, C, BMASK, SN = g["F"], g["C"], g["BMASK"], g["SN"]; F.sn = SN; BMASK["on"] = True
C.STEP.update(ks=0.002, kth=0.05, kf=0.01)
bf = json.load(open("klt_fit.json"))["klt_f0.25"]
r = F.fit(dict(bf["p"]), C.NAMES + ["ks", "kth", "kf"], kind="klt", iters=6, log=lambda *a, **k: None)
out = dict(chi2=r["chi2"], parts=r["parts"], p=r["p"], S8=r["info"].get("S8"))
print("klt free f: chi2 %.2f s %.4f theta_i %.3f f %.3f S8 %.4f" % (r["chi2"], r["p"]["ks"], r["p"]["kth"], r["p"]["kf"], r["info"].get("S8")), flush=True)
json.dump(out, open("klt_ffit.json", "w"), indent=1, default=float)
