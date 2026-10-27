"""Passes 12304-12309: the engine's excited tachyons are genuine (12299's suspicion retracted); the candidate's tachyon-freedom and
its radius window; the left-right census over all 1399 models (Claude track).

12304 -- the non-SUSY engine's TachyonSolver run verbosely (chalfstate.cpp verbose = true; ~/orb/nsoverb/nsodump_verbose).  In
  SM_20260917_810_v9 (parent) it finds right-moving tachyonic vacua q = (0, +-1/3, -+1/3, 0) with m_R^2 = -1/6 in the Witten-twisted
  theta^2 and theta^4 sectors (and the untwisted-Witten -1/2, projected out); the 16 'excited tachyon' states are left-movers level-
  matched to -1/6 with an oscillator.  They ARE tachyons.  12299 had re-derived their levels from the W/R lines nsoq prints, which for
  these states are not the solver's tachyonic configuration; the controls (massless states) could not detect that.  RETRACTED: the
  'tachyon-free' statements of 12281/12286/12292 stand as stated.  The Scherk-Schwarz brother: the same right-moving tachyonic vacua,
  no surviving left partner, T_NFIELDS = 0.
12305 -- the left-right candidate re-ranked (Z6II_60_SM_810_v9/v4, Scherk-Schwarz brother): tachyon-free in the zero-winding sector
  (engine solver); three chiral generations, no chiral fractional charge, Higgs candidates, Tr Y = 0 (12286); 48 vector-like fractional
  fermions liftable under gauge + point-group + Witten rules (12292/12300).  Against: k_Y = 8/3; the translation selection rule and the
  singlet vacuum are not built; the one-loop potential is not computed; the radius window below.
12307 -- radius window.  In the brother the parent's tachyons carry winding 1/2 along e6, so (alpha' m^2/4 levels, p_L,R =
  (n/R +- w R/alpha') sqrt(alpha'/2)) alpha' m^2/4 = -1/6 + R^2/(16 alpha'): tachyon-free iff R_6 >= 4 sqrt(alpha'/6) ~ 1.63 sqrt(alpha').
  Below that radius the tachyon returns.  (Convention-dependent normalisation of R; the -1/6 is the engine's.)
12306 -- the left-right scan over all 1399 non-SUSY Z6-II models (2198 dumps): see search_drivers_12294/lr_census_all.json.
12308 -- texture degrees with the sector rule: not computed, and not needed -- the sector rule only adds constraints, so it can only
  raise the 12301 lower bounds, which already exclude SM_2579 and push SM_808's bottom and charm to degree >= 7.
12309 -- synthesis.

CORRECTED in 12316: the parent's tachyons return with half-integer MOMENTUM (not winding) along e6 -> tachyonic for
R_6 > 0.612 sqrt(alpha'); odd-winding states are tachyonic for R_6 < 0.816 sqrt(alpha'); the window is empty.  Statements here about
R_6 >= 1.63 sqrt(alpha') and the radius running into the tachyonic region are superseded.
"""

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "w33_pass12304_to_12309_tachyons_confirmed_and_radius_window.json"
A = ROOT / "analysis"


def solver(path):
    t = (A / "search_drivers_12293" / path).read_text(errors="ignore")
    sols = re.findall(r"potential tachyons in sector \((\d+), (\d+), (\d+)\).*?mass M_R\^2 = (-?[\d.]+)", t, re.S)
    nT = int(re.search(r"T_NFIELDS (\d+)", t).group(1))
    return [(s[0], s[1], s[2], float(s[3])) for s in sols], nT


def main():
    checks, res = {}, {}
    pc, nc = solver("verbose_810_ctrl.txt")
    pb, nb = solver("verbose_810_w6odd.txt")
    res["12304"] = dict(parent_solutions=pc, parent_T=nc, brother_solutions=pb, brother_T=nb)
    checks["12304: solver finds m_R^2 = -1/6 vacua in Witten theta^2, theta^4 (both models); parent 16 tachyons, brother 0"] = (
        sorted((s[1], round(s[3], 2)) for s in pc) == [("0", -0.5), ("2", -0.17), ("4", -0.17)] and pb == pc and nc == 16 and nb == 0)
    import math
    Rc = 4 * math.sqrt(1 / 6)
    res["12307_Rc_over_sqrt_alpha"] = Rc
    checks["12307: R_c = 4 sqrt(1/6) ~ 1.633 sqrt(alpha')"] = abs(Rc - 1.633) < 1e-3
    lc = A / "search_drivers_12294" / "lr_census_all.json"
    if lc.exists():
        d = json.loads(lc.read_text())
        hits = sorted(k for k, v in d["results"].items() if k.endswith("__w6odd") and any(x.get("sm_values") for x in v))
        res["12306"] = dict(table=d["table"], hits=hits)
        checks["12306: left-right hits over all models recorded"] = len(d["results"]) > 2000
    checks = {k: bool(v) for k, v in checks.items()}
    res["checks"] = checks
    res["all_checks_pass"] = all(checks.values())
    OUT.write_text(json.dumps(res, indent=2, default=str))
    print(json.dumps(checks, indent=1), res["all_checks_pass"])
    return res


if __name__ == "__main__":
    main()
