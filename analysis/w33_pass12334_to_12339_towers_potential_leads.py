"""Passes 12334-12339: the brother's momentum towers from the parent, a truncated one-loop potential along R_6 (no minimum in the
window), and a new lead -- tachyon-free three-doublet non-SUSY parents (Claude track).

12334 -- towers.  The bicharacter (S = {e6}) predicts the brother from the parent sector by sector, and the prediction was checked on
  the full field multiset of all 15 lineage variants (physical classes boson/fermion; the engine's U(1) bases and CPT-pair labels differ
  between runs): 15/15 exact.  Rule:
    even Z6-power sectors (e6 in the centralizer): the brother keeps the parent states with V_h.lam even; those with V_h.lam odd move to
      half-integer e6 momentum (per variant 52 fermions + 16 tachyons, 8 in v12, v13);
    odd sectors (localised on torus 3): unchanged, except at fixed points with odd e6 label, where B(w, h) = 1/2 swaps bosons and fermions.
  (A first version applied the parity rule to all sectors and failed its control; the corrected rule was read off the sector table and
  then confirmed on all 15 variants.)  This supplies the e6-odd spectrum the engine never prints -- no engine patch needed.
12335 -- truncated one-loop potential along R_6 (alpha' = 1): species with e6 momentum = brother's even-sector states (integer tower:
  366 bosonic, 144 fermionic components) and the half tower (288 fermionic, 16 tachyonic components at level -1/6); V = -sum (-1)^F d I,
  I = int_F d^2tau/tau2^3 exp(-4 pi tau2 l) sum_{n,w} exp(-pi tau2 (n^2/R^2 + w^2 R^2)) cos(2 pi tau1 n w).  V(R) rises monotonically from
  -668 (R = 0.15) to -165.5 at the window edge R = sqrt(3/8) (finite there; divergent beyond, where the tachyon term grows), and falls as
  -1/R toward R -> 0 (integer-tower bosons dominate the winding sum): NO minimum in the window -- the radius runs to small R (the
  T-dual decompactification).  Controls: tau2 cutoff 40 vs 120 at R = 0.4 (-251.08 vs -251.15); edge threshold exactly R^2 = 3/8.
  Truncation: massive internal levels omitted.  (Casimir stabilisation background: Ponton-Poppitz, hep-ph/0105021, as cited by the
  other track's 2026-10-27 radion study -- a different, field-theory object.)
12336 -- projections of winding states (the R_5 channel): not computed -- absolute projection phases for winding states have no
  calibration in hand; the R_5 bound stays an upper bound on the danger.
12337 -- the standalone note against the corpus: scripts/check_rediscovery.py reports no collision; RESULTS_INDEX has no other entry
  on bicharacters, brother models or torsion.
12338 -- a necessary three-generation test without a hypercharge ansatz on the 99 tachyon-free parents (12324): 17 parents carry three
  net (3,2) doublets for some SU(3) x SU(2) choice -- lineages SM_2618 (4), SM_2503 (6), SM_574 (3), SM_2913 (3), SM_1105 (1, v12, the
  'tachyon-free non-free model' 12180 noted only as an interpolation endpoint); their Scherk-Schwarz brothers reach at most 2 (12180).
  LEAD, not a result: hypercharge, full SM structure and tachyon-freedom away from the orbifold point unchecked.
12339 -- synthesis: the Scherk-Schwarz left-right lineage has no radius minimum in its tachyon-free window (truncated one-loop); the
  route's next candidates are the tachyon-free three-doublet non-SUSY parents themselves.
"""

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "w33_pass12334_to_12339_towers_potential_leads.json"
A = ROOT / "analysis"


def main():
    checks, res = {}, {}
    s3 = json.loads((A / "search_drivers_12334" / "split3.json").read_text())
    res["12334"] = s3
    checks["12334: sector rule reproduces all 15 brothers exactly (0 mismatches)"] = len(s3) == 15 and all(
        v["rule_matches"] and v["mismatch"] == 0 for v in s3.values())
    p = json.loads((A / "search_drivers_12335" / "potential.json").read_text())
    c = json.loads((A / "search_drivers_12335" / "controls.json").read_text())
    Vs = [p["V"][k] for k in sorted(p["V"], key=float)]
    res["12335"] = dict(V=p["V"], controls=c, species=p["species"])
    checks["12335: V rises monotonically across the window (no minimum); cutoff stable; finite at the edge"] = (
        all(b > a for a, b in zip(Vs, Vs[1:])) and abs(c["R04_T40"] - c["R04_T120"]) < 0.2
        and c["R061_T400"] > c["R060_T400"] and c["R0612_T1500"] > c["R061_T400"])
    g = json.loads((A / "search_drivers_12338" / "gen3.json").read_text())
    res["12338"] = g
    checks["12338: 17 tachyon-free parents with three net (3,2) doublets; brothers at most 2"] = (
        len(g["hits"]) == 17 and all(h.endswith("__ctrl") for h in g["hits"]))
    checks = {k: bool(v) for k, v in checks.items()}
    res["checks"] = checks
    res["all_checks_pass"] = all(checks.values())
    OUT.write_text(json.dumps(res, indent=2, default=str))
    print(json.dumps(checks, indent=1), res["all_checks_pass"])
    return res


if __name__ == "__main__":
    main()
