"""Frozen statement S6 (2026-11-08), written BEFORE mono_fit.py results: the natural (periodic, axion-monodromy) completion of the fading coupling predicts a running coupling with a floor.
For m_DM^2 ~ cos(theta0 + phi/F):  c'(phi) = tan(theta)/(2F)  and  dc'/dphi = 1/(2F^2) + 2 c'^2 >= 2 c'^2, for every F.
So between recombination and today c' grows by at least ~2 c' Delta_phi: ~3% (c<0 mode, Delta_phi ~0.28) and ~8-9% (c>0 mode, Delta_phi ~0.8), independent of F; the constant-c' (exponential-mass) model used in Passes 12597-12628 is NOT a limit of the natural model.
usage: py -3 prereg_mono.py"""
import hashlib
import json

S = dict(
    written="2026-11-08",
    S6_running_floor=dict(
        claim="In the periodic (axion-monodromy) completion, the coupling c' = -d ln m_DM/dphi obeys dc'/dphi >= 2 c'^2, so c' grows toward today by at least 2 c' Delta_phi (about 3 percent for the c<0 mode, 8-9 percent for c>0) between recombination and today, for any F.",
        scored_by="a fit with c'(phi) free to run (e.g. c'(phi) = c'_0 + c'_1 phi) to Planck/ACT + DESI + SN + lensing + shear, and the mono_fit.py refits",
        falsified_if="data prefer a decreasing c' (c'_1 < 0) at more than 2 sigma, or the minimal-running monodromy model (F -> infinity) fits worse than constant c' by Delta chi2 > 4 after refitting",
    ),
)
js = json.dumps(S, indent=1, sort_keys=True)
open("prereg_mono.json", "w", newline="\n").write(js)
h = hashlib.sha256(js.encode()).hexdigest()
open("prereg_mono.sha256", "w", newline="\n").write(h + "  prereg_mono.json\n")
print("sha256", h)
