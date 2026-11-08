"""Smoke test of the KLT-family CLASS build: growth likelihood (full Dovekie) at the LCDM best-fit base parameters for their fiducial f = 0.25 M_P, s = 0.01 and a few initial angles; reports chi2 parts, phi0, phi_rec and the DM mass change since recombination.
usage: python3 klt_smoke.py"""
import json, math, os, sys
BG = os.path.dirname(os.path.abspath(__file__)); os.chdir(BG); sys.path.insert(0, BG)
sys.argv = ["x", "dovekie", "sn"]
src = open("class_holdout.py", encoding="utf-8").read().split('if HOLD == "evidence":')[0]
g = dict(__name__="x", __file__=os.path.join(BG, "class_holdout.py")); exec(src, g)
F, BMASK, SN = g["F"], g["BMASK"], g["SN"]; F.sn = SN; BMASK["on"] = True
base = dict(json.load(open("class_fit_dovekie.json"))["LCDM"]["p"])
out = {}
for kf, ks, kth in ((0.25, 0.01, 1.0), (0.25, 0.01, 2.0), (0.25, 0.01, 2.8), (0.25, 0.02, 2.0)):
    q = dict(base, ks=ks, kf=kf, kth=kth)
    try:
        r = F.resid(q, "klt")
        i = r[2]
        mr = lambda ph: (1 + 2 * ks * math.sqrt(1 - 0.98765 * math.sin(ph / (2 * kf)) ** 2))
        dm = mr(i["phi0"]) / mr(i["phi_rec"]) - 1
        out[f"{kf}_{ks}_{kth}"] = dict(chi2=float(r[0] @ r[0]), parts=r[1], phi0=i["phi0"], phi_rec=i["phi_rec"], dm_since_rec=dm, S8=i["S8"])
        print(kf, ks, kth, "chi2 %.2f" % (r[0] @ r[0]), {k: round(v, 2) for k, v in r[1].items()}, "theta0 %.3f theta_rec %.3f dm %.4f S8 %.4f" % (i["phi0"] / kf, i["phi_rec"] / kf, dm, i["S8"]), flush=True)
    except Exception as e:
        print(kf, ks, kth, "FAILED", str(e)[-150:], flush=True)
q = dict(base); r = F.resid(q, "fading"); print("LCDM control chi2 %.2f" % (r[0] @ r[0]), flush=True)
json.dump(out, open("klt_smoke.json", "w"), indent=1, default=float)
