"""Item 4: frozen point predictions for future BAO (DESI DR3) from the full-data best fits, written BEFORE any DR3 release (none as of 2026-11-06).
Models: LCDM, CPL, fading (free_neg) and fading c>0 (free_pos), fitted on Dovekie and on DES-SN5YR (class_fit_*.json).
Quantities: D_M/r_d, D_H/r_d at the DESI DR2 effective redshifts (0.51, 0.706, 0.934, 1.321, 1.484, 2.33), D_V/r_d at 0.295, plus a higher-z grid (2.8, 3.2, 3.5) for the DR3 extension quoted in arXiv:2603.09973.
The output JSON is hashed (sha256) so that a later scoring can verify it was not edited.  Point predictions only; a posterior band is added from the MCMC chains when they exist.
usage: python3 dr3_prereg.py"""
import hashlib
import json
import os
import sys
import numpy as np

BG = os.path.dirname(os.path.abspath(__file__))
os.chdir(BG)
sys.path.insert(0, BG)
import class_cmb as C  # noqa: E402

ZA = [0.51, 0.706, 0.934, 1.321, 1.484, 2.33, 2.8, 3.2, 3.5]
out = dict(written="2026-11-06", note="frozen before DESI DR3; point predictions from full-data best fits", z_aniso=ZA, z_iso=[0.295], fits={})
KIND = dict(LCDM="fading", CPL="cpl", free_neg="fading", free_pos="fading")
for ds in ("dovekie", "desy5"):
    fits = json.load(open(f"class_fit_{ds}.json"))
    for m in ("LCDM", "CPL", "free_neg", "free_pos"):
        p = dict(fits[m]["p"])
        cl, z, H, dc, info = C.run_class(p, KIND[m])
        rd = info["rd"]
        DM = [float(np.interp(zz, z, dc)) / rd for zz in ZA]
        DH = [1 / float(np.interp(zz, z, H)) / rd for zz in ZA]
        zv = 0.295
        dm, dh = float(np.interp(zv, z, dc)) / rd, 1 / float(np.interp(zv, z, H)) / rd
        DV = (zv * dm ** 2 * dh) ** (1 / 3)
        out["fits"][f"{ds}_{m}"] = dict(params=p, rd=rd, DM_rd=DM, DH_rd=DH, DV_rd_0295=DV, chi2=fits[m]["chi2"])
        print(ds, m, "rd %.2f" % rd, "DV(0.295) %.3f" % DV, "DM", np.round(DM, 3).tolist(), flush=True)
js = json.dumps(out, indent=1, sort_keys=True, default=float)
open("dr3_prereg.json", "w").write(js)
h = hashlib.sha256(js.encode()).hexdigest()
open("dr3_prereg.sha256", "w").write(h + "  dr3_prereg.json\n")
print("sha256", h, flush=True)
