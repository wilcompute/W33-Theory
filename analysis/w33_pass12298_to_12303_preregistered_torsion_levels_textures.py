"""Passes 12298-12303: the corrected torsion bicharacter passes a pre-registered test; the engine's 'excited tachyons' are level-matched
massless states (suspected labelling); the candidate's fractional states stay liftable under point-group rules; the Z2xZ6-I
lineages fail the texture test; the left-right census extended (Claude track).

12298 -- pre-registered test.  Fresh SUSY Z4_1_1 models (seed 12298), the shifted line W1 = W2 (on a theta^2-rotated torus, unlike
  12296), B evaluated with fixed-point labels on every commuting pair (theta = diag(R90, R90, -1)); predictions.json committed and
  pushed (e570f4b1f) before any engine run.  Score: 124/124 (32/32 changed, 92/92 identical; 12 controls load).
12299 -- mass levels.  Left level P^2/2 + N - 1 + dc(n) and right level R^2/2 - 1/2 + dc(n), dc = (1/2) sum w(1-w), w = frac(n v),
  calibrated on the engine's data: two parsing errors fixed (oscillator frequencies are printed signed; the O-line N= is the number
  operator value, two decimals) -- controls: 518/518 massless-type states of SM_810's parent at (0, 0), 13632/13632 over 20 parents.
  The engine's 'excited tachyon' states (m = 23/24; the T lines of nsodump) come out at (0, 0) as well: 16/16 in SM_810's parent,
  120/120 over 20 parents.  No state of type 21/22 (genuine tachyon label) occurs in any of the 12281 dumps (ctrl, even, odd, W6-odd).
  Suspected (not confirmed against the engine's internal tachyon mass): the 'excited tachyonic' branch yields level-matched massless
  states, so the 'tachyon-free' statements of 12281/12286/12292 mean 'free of excited-tachyon-labelled states'; the parent of the
  left-right candidate is then not tachyonic either at this level.  No critical radius is computed.
12300 -- the candidate's 48 fractional Weyl fermions under gauge + point-group (sum of Z6 powers = 0 mod 6) + Witten (sum of labels
  = 0 mod 2) selection: still 134 allowed pairs, all 48 liftable.  Control: unit Z6 and Witten residuals are not in the lattice (the
  rules are live).  The fixed-point translation rule is still not imposed.
12301 -- textures (exact MILP over 31 / 21 singlets; U(1) + R rule; the probe's idx is an internal sector enumeration, so the sector
  rule is dropped after a first version failed the positive control -> degrees are LOWER bounds; control: all six engine cubic
  couplings at degree 0).  SM_808: up column of the top at degree 0-1, the other two up columns >= 7; down >= 7; tau at degree 0,
  other leptons >= 8.  SM_2579: no down Yukawa up to degree 12; two up columns forbidden to degree 12.  So SM_2579 is excluded and
  SM_808 needs epsilon ~ 0.5 for m_b/m_t ~ 1e-2: the Z2xZ6-I lineages that passed the proton test fail the texture test.
12302 -- the Scherk-Schwarz census extended to all 1399 non-SUSY Z6-II models with an order-2 W5 (1099 new), with the left-right
  hypercharge scan on every completed pair; see search_drivers_12294/lr_census_all.json.
12303 -- synthesis.
"""

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "w33_pass12298_to_12303_preregistered_torsion_levels_textures.json"
A = ROOT / "analysis"


def main():
    checks, res = {}, {}
    s = json.loads((A / "search_drivers_12298" / "score.json").read_text())
    res["12298"] = s
    checks["12298: pre-registered predictions 124/124 (32 changed, 92 identical)"] = (
        s.get("('changed', 'changed')") == 32 and s.get("('identical', 'identical')") == 92 and s.get("('control', 'loaded')") == 12
        and not any(k.startswith("('changed', 'identical'") or k.startswith("('identical', 'changed'") for k in s))
    lv = json.loads((A / "search_drivers_12293" / "levels.json").read_text())["levels"]
    rl = json.loads((A / "search_drivers_12293" / "rlevels.json").read_text())
    ex = json.loads((A / "search_drivers_12293" / "excited_check.json").read_text())
    res["12299"] = dict(left=lv, right=rl, survey=ex)
    checks["12299: calibrated levels -- every massless-type and every excited-tachyon-labelled state at (0, 0)"] = (
        all(k.endswith("'0')") for k in lv) and set(rl["ctrl"]) == {"('massless-type', '0')", "('tachyon-type', '0')"}
        and ex["models"] == 20 and set(ex["table"]) == {"('excited-tachyon label', '0', '0')", "('massless-type', '0', '0')"})
    pg = json.loads((A / "search_drivers_12300" / "lift_pg.json").read_text())
    res["12300"] = pg
    checks["12300: 48/48 liftable under gauge + point group + Witten"] = pg["liftable"] == 48 and pg["fractional_fermions"] == 48
    tx = json.loads((A / "search_drivers_12301" / "texture.json").read_text())
    res["12301"] = {k: dict(control=v["control"]) for k, v in tx.items()}
    def lowest(r, kind):
        vals = [x for M in r[kind].values() for row in M for x in row if x is not None]
        return min(vals) if vals else None
    checks["12301: controls at degree 0; SM_808 down >= 7, SM_2579 no down to degree 12"] = (
        all(v == 0 for r in tx.values() for v in r["control"].values())
        and lowest(tx["SM_20260926_808_24__odd"], "down") == 7 and lowest(tx["SM_20260926_2579_27__odd"], "down") is None)
    lc = A / "search_drivers_12294" / "lr_census_all.json"
    if lc.exists():
        d = json.loads(lc.read_text())
        res["12302"] = d["table"]
        hits = sorted(k for k, v in d["results"].items() if k.endswith("__w6odd") and any(x.get("sm_values") for x in v))
        res["12302_hits"] = hits
    checks = {k: bool(v) for k, v in checks.items()}
    res["checks"] = checks
    res["all_checks_pass"] = all(checks.values())
    OUT.write_text(json.dumps(res, indent=2, default=str))
    print(json.dumps(checks, indent=1), res["all_checks_pass"])
    return res


if __name__ == "__main__":
    main()
