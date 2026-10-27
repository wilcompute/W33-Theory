"""Passes 12316-12321: the radius window corrected -- the left-right lineage is tachyonic at every radius (Claude track).

12316 -- correction to 12307.  The torsion phase B(w, e6) = 1/2 multiplies the translation e6 on Witten-twisted states, so it shifts
  their MOMENTUM along e6 by 1/2; a lattice-valued Wilson line is not a freely acting translation, so windings stay integral.  12307
  assigned the parent's tachyons winding 1/2 -- wrong.  With p_{L,R} = (n/R +- w R/alpha') sqrt(alpha'/2):
    n = 1/2, w = 0 :  alpha' m^2 / 4 = -1/6 + alpha'/(16 R^2)  -> tachyonic for R > sqrt(3 alpha'/8) ~ 0.612 sqrt(alpha')
      (the decompactification limit restores the tachyonic parent -- as it must);
    w = 1, n = 0   :  alpha' m^2 / 4 = -1/6 + R^2/(4 alpha') -> tachyonic for R < sqrt(2 alpha'/3) ~ 0.816 sqrt(alpha')
      (odd winding flips the momentum shift -- the standard Scherk-Schwarz rule; the engine cannot compute winding states, so this
      step is an argument, not a computation).
  0.816 > 0.612: the window is EMPTY -- the Scherk-Schwarz brother is tachyonic at every radius of e6.
12317 -- all 15 brothers of the lineage (SM_20260917_810 V0 variants): the verbose TachyonSolver finds the same right-moving vacua
  (m_R^2 = -1/6 twice, -1/2 once) and T_NFIELDS = 0 at zero momentum/winding; the window argument applies to the whole family.
  The -1/6 vacua come from the Witten x theta^2 twist alone (independent of the gauge embedding), so every non-SUSY Z6-II model has
  them; a window needs a parent with no level-matched -1/6 partner at all.
12318-12319 -- radius stabilisation, unification with the full spectrum and the non-SUSY vertex rule for the 48 mass pairings: not
  pursued -- they concern a candidate that the window argument removes.  The 12312 potential proxy (n_F - n_B = -222) and the 12313
  k_Y = 8/3 obstruction stand as recorded but are now secondary.
12320 -- other Scherk-Schwarz three-generation candidates: ordinary Standard-Model parents lose a generation (12180 halving lemma);
  the left-right scan of all 1399 non-SUSY Z6-II models found only the SM_810 family (12310), whose parents carry tachyons; for
  Z2xZ6-I the corpus closed three-generation Scherk-Schwarz models in 12199.  Within the geometries the corpus covers, this route
  yields no three-generation model with a tachyon-free window (an argument built on cited closures, not a new scan).
12321 -- synthesis.
"""

import json
import math
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "w33_pass12316_to_12321_window_empty.json"
A = ROOT / "analysis"


def main():
    checks, res = {}, {}
    R_mom = math.sqrt(3 / 8)       # n = 1/2: tachyonic for R > this
    R_win = math.sqrt(2 / 3)       # w = 1:   tachyonic for R < this
    res["12316"] = dict(R_momentum_bound=R_mom, R_winding_bound=R_win, window_empty=R_win > R_mom)
    checks["12316: momentum bound 0.612, winding bound 0.816 -> window empty"] = abs(R_mom - 0.6124) < 1e-3 and abs(R_win - 0.8165) < 1e-3 and R_win > R_mom
    fam = {}
    for p in sorted((A / "search_drivers_12317").glob("v*_w6odd.txt")):
        t = p.read_text(errors="ignore")
        masses = sorted(round(float(x), 2) for x in re.findall(r"mass M_R\^2 = (-?[\d.]+)", t))
        fam[p.stem] = dict(masses=masses, T=int(re.search(r"T_NFIELDS (\d+)", t).group(1)))
    res["12317"] = fam
    checks["12317: all 15 brothers -- vacua (-0.5, -0.17, -0.17), T_NFIELDS 0"] = (
        len(fam) == 15 and all(v["masses"] == [-0.5, -0.17, -0.17] and v["T"] == 0 for v in fam.values()))
    checks = {k: bool(v) for k, v in checks.items()}
    res["checks"] = checks
    res["all_checks_pass"] = all(checks.values())
    OUT.write_text(json.dumps(res, indent=2, default=str))
    print(json.dumps(checks, indent=1), res["all_checks_pass"])
    return res


if __name__ == "__main__":
    main()
