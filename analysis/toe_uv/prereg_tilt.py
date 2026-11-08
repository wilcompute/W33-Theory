"""Frozen statement S7 (2026-11-08): the tomographic-tilt signature that separates CPL from the fading coupling in cosmic shear (shear_diag.py, Pass 12631 addendum).
At the frozen full-data Dovekie backgrounds, CPL predicts xi+ in the lowest tomographic pair 3.9-4.4 percent below fading and in the highest pair within -0.3..+1.1 percent of it (KiDS-Legacy and DES Y3 binnings).
usage: py -3 prereg_tilt.py"""
import hashlib
import json

k = json.load(open("shear_diag_kids.json"))["cpl_over_fading_xiplus_minus1_by_pair"]
d = json.load(open("shear_diag_des.json"))["cpl_over_fading_xiplus_minus1_by_pair"]
S = dict(
    written="2026-11-08",
    S7_tomographic_tilt=dict(
        claim="Relative to the fading coupling (c<0), CPL predicts a redder shear tomography: xi+ low-z/high-z ratio lower by ~4-5 percent (lowest pair -3.9 to -4.4 percent, highest pair -0.3 to +1.1 percent). Next shear releases will prefer the fading (or LCDM) tilt over CPL's, i.e. a positive Delta chi2(CPL - fading) driven by the low-z bins.",
        kids_pairs=k, des_pairs=d,
        scored_by="DES Y6, HSC Y3/final, KiDS COSEBIs, Euclid DR1 cosmic shear analysed at the frozen backgrounds (class_fit_dovekie.json) with nuisances refitted",
        falsified_if="Delta chi2(CPL - fading) <= 0, or a positive Delta chi2 that is driven by the high-z bins rather than the low-z bins",
    ),
)
js = json.dumps(S, indent=1, sort_keys=True)
open("prereg_tilt.json", "w", newline="\n").write(js)
h = hashlib.sha256(js.encode()).hexdigest()
open("prereg_tilt.sha256", "w", newline="\n").write(h + "  prereg_tilt.json\n")
print("sha256", h)
