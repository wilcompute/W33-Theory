"""Control and test for class_klt_guess_patch.py: the f = 0.25 best fit (klt_fit.json) must give the same chi2 with the new build (only the shooting guess changed); then f = 0.1, 0.05 at the same s, theta_i, and with theta_i scanned, to see whether shooting now succeeds.
usage: KLTBIN=~/cosmo/class_klt2/class python3 klt2_check.py"""
import json, os, sys
BG = os.path.dirname(os.path.abspath(__file__)); os.chdir(BG); sys.path.insert(0, BG)
sys.argv = ["x", "dovekie", "sn"]
src = open("class_holdout.py", encoding="utf-8").read().split('if HOLD == "evidence":')[0]
g = dict(__name__="x", __file__=os.path.join(BG, "class_holdout.py")); exec(src, g)
F, BMASK, SN = g["F"], g["BMASK"], g["SN"]; F.sn = SN; BMASK["on"] = True
bf = json.load(open("klt_fit.json"))["klt_f0.25"]
out = {}
import os as _os
LABS = (("control_f0.25", {}), ("f0.1", dict(kf=0.1)), ("f0.1_th1.5", dict(kf=0.1, kth=1.5)), ("f0.1_th3.0", dict(kf=0.1, kth=3.0)), ("f0.05", dict(kf=0.05)), ("f0.5", dict(kf=0.5))) if not _os.environ.get("KLTSCAN") else tuple((f"f{x}", dict(kf=x)) for x in (0.12, 0.15, 0.2))
for lab, upd in LABS:
    q = dict(bf["p"], **upd)
    try:
        r = F.resid(q, "klt")
        out[lab] = dict(chi2=float(r[0] @ r[0]), S8=r[2]["S8"])
        print(lab, "chi2 %.3f S8 %.4f" % (out[lab]["chi2"], r[2]["S8"]), "(fit value %.3f)" % bf["chi2"] if lab.startswith("control") else "", flush=True)
    except Exception as e:
        out[lab] = dict(error=str(e)[-120:]); print(lab, "FAILED", str(e)[-100:], flush=True)
json.dump(out, open("klt2_check.json" if not _os.environ.get("KLTSCAN") else "klt2_scan.json", "w"), indent=1, default=float)
