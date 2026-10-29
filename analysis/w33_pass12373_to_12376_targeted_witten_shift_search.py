"""Passes 12373-12376: a targeted Witten-shift search for three-generation non-SUSY Z6-II models that are tachyon-free at large radius
(Claude track).  Follows the closure of the 99-parent sample (12368): new models, not new tests.

12373 -- for the SUSY parents of the five three-doublet lineages (SM_2913, 2618, 2503, 574, 1105; W6 = 0) ALL admissible Witten shifts
  V0 = (a; b) in (1/2){norm-4 E8 vectors}^2 with V0 . V, V0 . W_i integral were enumerated: 111108 (the 12180 construction tried <= 400 per
  parent).  A seeded sample of 3000 per parent (15000): 7391 pass the strict engine, 2141 are tachyon-free at the orbifold point, 202
  carry three net (3,2) doublets (all five parents) -- versus 17 in the whole 99-parent sample.
12374 -- radius filters on the 202 (6D theories of both fixed tori with Wilson lines off; odd e5 winding; e3 winding classes 1, 2):
  clean at large and small radius 27, large only 75, small only 47, neither 53.  The 102 large-radius-safe ones: full strict spectra;
  43 carry chiral states charged under the SM group and a hidden non-abelian factor (fatal for every hypercharge).
12375 -- hypercharge (exact MILP of 12364) for the 59 others (27 of them clean at every tested radius): no solution in the base search,
  none for any of the 65 SU(3) x SU(2) pairings with three net doublets, none in the relaxed search so far (coverage recorded in the
  certificate; the run continues).  Mechanism, diagnosed on SM_574_c420: the gauge group is SU(3) x SU(2) x SU(3)' x SU(2)' and the second
  pair carries its own chiral (3,2)-type matter ('twin' sector); the quark and colour conditions can be met only by giving that twin
  matter visible hypercharge -- with a Y-neutral hidden sector the problem is infeasible (as for SM_574, 12364).
12376 -- synthesis: the radius obstruction of 12363-12368 is NOT generic -- 27 three-doublet models pass every tested radius channel --
  but in this family a hypercharge with exactly three SM generations does not exist: the hidden sector is a chiral twin that the
  visible hypercharge cannot avoid.  Open: Y with two U(1)s (visible Y plus a twin Y'), i.e. a twin-Standard-Model reading; untwisted
  winding channels; the 96108 unsampled shifts.
"""

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "w33_pass12373_to_12376_targeted_witten_shift_search.json"
A = ROOT / "analysis"


def main():
    checks, res = {}, {}
    s = json.loads((A / "search_drivers_12373" / "summary.json").read_text())
    res["summary"] = s
    checks["12373: 15000 sampled shifts; 7391 strict, 2141 tachyon-free, 202 with three net (3,2) across all five parents"] = (
        s["sampled"] == 15000 and s["strict"] == 7391 and s["tachyon_free"] == 2141 and s["three_doublet"] == 202
        and len(s["three_doublet_by_parent"]) == 5)
    checks["12374: radius classes 27 / 75 / 47 / 53; 102 large-radius safe; 43 with hypercharge-independent exotics"] = (
        s["radius_classes"] == {"large-T,small-clean": 47, "large-clean,small-clean": 27, "large-clean,small-T": 75, "large-T,small-T": 53}
        and s["large_safe"] == 102 and s["y_independent_exotics"] == 43 and s["all_radius_exotic_free"] == 27)
    checks["12375: no three-generation hypercharge -- base (59), all 65 pairings, relaxed (coverage as recorded)"] = (
        s["base_hypercharge_found"] == 0 and s["pairing_hypercharge_found"] == 0 and s["pairings_tested"] == 65
        and s["relaxed_found"] == 0 and s["relaxed_done"] >= 18)
    checks = {k: bool(v) for k, v in checks.items()}
    res["checks"] = checks
    res["all_checks_pass"] = all(checks.values())
    OUT.write_text(json.dumps(res, indent=2, default=str))
    print(json.dumps(checks, indent=1), res["all_checks_pass"])
    return res


if __name__ == "__main__":
    main()
