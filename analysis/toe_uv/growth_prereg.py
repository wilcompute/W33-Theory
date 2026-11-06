"""Frozen growth predictions for future weak-lensing / RSD data (Euclid, LSST, DESI DR3 RSD), written 2026-11-06 from existing runs, no refit:
S8, sigma8 and f sigma8 at z = 0.07, 0.38, 0.51, 0.70, 0.85, 1.48 for LCDM, CPL, fading c<0 and c>0 at the full-data Dovekie and DES-SN5YR fits (sign_growth.json), plus the DES Y3 fixed-background shear chi2 (sign_desdovekie, sign_des.json).
Discriminators recorded: S8(c<0) - S8(c>0) = 0.011-0.015; S8(fading c<0) - S8(LCDM) = 0.026-0.028.  Hashed; score only against data released after this date.
usage: py -3 growth_prereg.py"""
import hashlib
import json

sg = json.load(open("sign_growth.json"))
sd = json.load(open("sign_des.json"))
out = dict(written="2026-11-06", note="frozen growth predictions from full-data best fits; no refit", models={k: dict(S8=v["S8"], sigma8=v["s8"], fs8=v["fs8"], c=v["c"], cp=v["cp"]) for k, v in sg.items()}, des_y3_fixed_background={k: dict(des=v["des"], desp=v["desp"]) for k, v in sd.items()})
js = json.dumps(out, indent=1, sort_keys=True)
open("growth_prereg.json", "w", newline="\n").write(js)
h = hashlib.sha256(js.encode()).hexdigest()
open("growth_prereg.sha256", "w", newline="\n").write(h + "  growth_prereg.json\n")
print("sha256", h)
