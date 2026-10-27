"""Passes 12292-12297: the candidate's fractional states can be lifted (gauge level); the candidate is unique in the census; the
R rule is validated and two Z2xZ6-I lineages have a rank-1 cubic top; the torsion rule refined on Z4 (prediction partly refuted)
(Claude track).

12292 -- lifting.  The left-right candidate (12286) has 48 left-handed Weyl fermions of fractional electric charge (the '96' of
  12286 counted each with its CPT conjugate), all vector-like.  A mass term chi_a chi_b S_1...S_n needs conjugate representations,
  opposite Y, and q_a + q_b an INTEGER combination of the charge vectors of the 50 SM-singlet scalars (lattice rank 4; Hermite normal
  form).  134 pairs allowed; maximum matching 24 pairs: all 48 liftable.  Gauge level only: discrete (space-group / H-momentum)
  selection rules are not imposed and the vacuum (singlet vevs) is not constructed -- an upper bound.
12293 -- radius dependence: not determined.  The engine's spectra contain only states with zero compact momentum and winding; in the
  Scherk-Schwarz brother the parent's tachyonic states carry half-integer winding along e6 and are invisible to it, so 'tachyon-free'
  holds for the zero-winding sector at the orbifold point only.  An attempt to compute the parent tachyons' level from the engine data
  (P^2/2 + N - 1 + dc) FAILED its control (massless states came out at -1/3, -1/6, -1/2, not 0), so no critical radius is quoted.
12294 -- census-wide left-right scan (Y = T3R + Y', both SU(2) assignments, exact): of 299 Scherk-Schwarz brothers, 86 have an
  SU(3) x SU(2) x SU(2) visible factor; exactly 2 give three chiral generations with no chiral fractional charge -- the SM_810 v9 and
  v4 brothers (the 12286 candidate).  The ansatz covers only hypercharges of left-right form.
12295 -- R rule: synthetic control passes (U1 U2 U3 allowed; U1^3, U2^3, U3^3 forbidden), and all 284 engine-allowed QLd/udd couplings
  of 12287 have plane sums exactly (-1, -1, -1) -- the rule holds non-vacuously, so the 12287 counts are gauge + space group + R.
  Cubic Yukawas of the three lineages without renormalisable QLd: SM_128 none (no tree-level top); SM_808 and SM_2579 (parents and
  brothers alike): three up-type couplings q_i bu_1 Hu_k, all through the same bu_1 -- a rank-1 cubic up sector (one heavy up quark),
  no cubic down Yukawa, four lepton couplings.
12296 -- Z4 (SUSY, Geometry_Z4_1_1, standard embedding + random order-2 lines; 12 models, 100 consistent brothers).  The pre-registered
  prediction 'no torsion (k = 2 even)' was REFUTED: 16 brothers changed.  Cause: the fixed-point term -- for a theta^2 sector at fixed
  point f, B(e5, (theta^2, f)) = V.lam + (1/2) sum_b f_b W_b.lam, and the order-2 lines W1, W3 on the theta^2-rotated tori make the
  second term a half-integer when W_b.lam is odd.  Post-hoc rule 'changed iff W1.lam or W3.lam odd' fits 100/100; the V.lam part
  of the prediction held (48/48 brothers with V.lam odd and even W-parities identical).  The corrected rule is fitted, not yet
  independently tested.
12297 -- synthesis.
"""

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "w33_pass12292_to_12297_lifting_census_yukawas_z4.json"
A = ROOT / "analysis"


def main():
    checks, res = {}, {}
    li = json.loads((A / "search_drivers_12292" / "lift_int.json").read_text())
    res["12292"] = li
    checks["12292: 48 fractional Weyl fermions, all liftable by integer singlet monomials (gauge level)"] = (
        li["fractional_fermions"] == 48 and li["liftable_fields_integer"] == 48 and li["lattice_rank"] == 4)
    lv = json.loads((A / "search_drivers_12293" / "levels.json").read_text())
    ctrl_fail = any(k.startswith("('massless-type'") and not k.endswith("'0')") for k in lv["levels"])
    res["12293_level_control_failed"] = ctrl_fail
    checks["12293: the level computation fails its massless control (no critical radius quoted)"] = ctrl_fail
    lc = json.loads((A / "search_drivers_12294" / "lr_census.json").read_text())
    res["12294"] = lc["table"]
    hits = sorted(k for k, v in lc["results"].items() if k.endswith("__w6odd") and any(x.get("sm_values") for x in v))
    res["12294_hits"] = hits
    checks["12294: the only Scherk-Schwarz brothers with three LR chiral generations are SM_810 v9 and v4"] = hits == [
        "Z6II_60_SM_20260917_810_v4__w6odd", "Z6II_60_SM_20260917_810_v9__w6odd"] and lc["table"].get(
        "('w6odd', 'LR-type', 'three generations found')") == 2
    rc = json.loads((A / "search_drivers_12295" / "rcontrol.json").read_text())
    yk = json.loads((A / "search_drivers_12295" / "yuk.json").read_text())
    res["12295"] = dict(rcontrol=rc, yukawas=yk)
    checks["12295: R-rule control passes and all 284 allowed couplings have plane sums (-1,-1,-1)"] = (
        rc["synthetic"] == {"U1 U2 U3": True, "U2 U2 U2": False, "U1 U1 U1": False, "U3 U3 U3": False}
        and rc["plane_sums"] == {"('-1', '-1', '-1')": 284})
    checks["12295: SM_808 and SM_2579 have three up couplings through one bu (rank 1), SM_128 none"] = all(
        yk[m]["allowed"].get("up") == 3 and "down" not in yk[m]["allowed"] for m in yk if not m.startswith("SM_20260926_128"))
    z = json.loads((A / "search_drivers_12296" / "z4cmp.json").read_text())
    ph = json.loads((A / "search_drivers_12296" / "z4_posthoc.json").read_text())
    res["12296"] = dict(table=z["table"], posthoc=ph)
    checks["12296: prediction refuted (16/100 changed); post-hoc fixed-point rule fits 100/100; V.lam alone never matters"] = (
        z["table"].get("changed") == 16 and z["table"].get("identical") == 84
        and all(("pred=changed" in k) == ("obs=changed" in k) for k in ph)
        and ph.get("('V.lam odd=True', 'pred=identical', 'obs=identical')") == 48)
    checks = {k: bool(v) for k, v in checks.items()}
    res["checks"] = checks
    res["all_checks_pass"] = all(checks.values())
    OUT.write_text(json.dumps(res, indent=2, default=str))
    print(json.dumps(checks, indent=1), res["all_checks_pass"])
    return res


if __name__ == "__main__":
    main()
