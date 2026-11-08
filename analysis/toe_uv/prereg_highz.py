"""Frozen statement S8 (2026-11-08), replacing the mis-specified mechanism clause of S7 (prereg_tilt.json stays as written).
Based on shear_diag.py block chi2 and shear_hybrid.py growth/geometry split (Pass 12631 correction and addenda).
usage: py -3 prereg_highz.py"""
import hashlib, json
hk = json.load(open("shear_hybrid_kids.json"))["split"]
hd = json.load(open("shear_hybrid_des.json"))["split"]
S = dict(
    written="2026-11-08",
    supersedes="mechanism clause of S7 (prereg_tilt.json, sha a05a56e8), contradicted by DES Y3 and KiDS-Legacy",
    S8_highz_shear=dict(
        claim="At the frozen full-data Dovekie backgrounds (class_fit_dovekie.json), the next cosmic-shear releases will give Delta chi2(CPL - fading c<0) > 0, with the excess carried by the high-z tomographic block (both bins in the upper half) and/or the mixed block, not by the low-z block; both the matter power history P(k,z) and the geometry contribute (current split: KiDS power +3.2, geometry +2.0; DES power +2.2, geometry +1.9).",
        current_values=dict(kids=hk, des=hd),
        scored_by="DES Y6, HSC final, KiDS COSEBIs, Euclid DR1 shear analysed with class_des_fit.py-style block chi2 at the frozen backgrounds, nuisances refitted",
        falsified_if="Delta chi2(CPL - fading) <= 0, or a positive total dominated (> 60 percent) by the low-z block",
    ),
)
js = json.dumps(S, indent=1, sort_keys=True)
open("prereg_highz.json", "w", newline="\n").write(js)
h = hashlib.sha256(js.encode()).hexdigest()
open("prereg_highz.sha256", "w", newline="\n").write(h + "  prereg_highz.json\n")
print("sha256", h)
