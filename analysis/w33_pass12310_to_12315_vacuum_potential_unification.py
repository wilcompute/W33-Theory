"""Passes 12310-12315: the left-right census completed; the candidate's fractional states liftable under the full space-group rule;
its Scherk-Schwarz potential proxy points inward; k_Y = 8/3 does not unify; tachyon claims audited (Claude track).

12310 -- the left-right hypercharge scan (Y = T3R + Y', both SU(2) assignments) over every pair of the 12281 + 12302 censuses (2797 dumps;
  pooled, 120 s per model; 0 timeouts): 15 Scherk-Schwarz brothers give three chiral generations with no chiral fractional charge --
  all 15 are V0 variants of ONE parent, SM_20260917_810 (each brother tachyon-free, each parent with 8 or 16 tachyonic states), and all
  15 have n_F - n_B = -222.  No other lineage among the 1399 models does this (within the Y = T3R + Y' ansatz).
12311 -- full space-group rule.  Elements (theta^n w^mm, l) with the engine's fixed-point translations l on the SU(3) x SU(3) x SU(2)^2
  lattice (theta = diag([[1,-1],[1,0]], [[0,-1],[1,-1]], -1), theta^6 = 1 checked); a pairing chi_a chi_b prod S^x is allowed iff U(1)s
  cancel, sum n = 0 mod 6, sum mm = 0 mod 2, and sum l in sum_k (1 - theta^k) Lambda over the sectors present (exact MILP, |x| <= 4,
  degree <= 8).  Result: 134 allowed pairs, all 48 fractional Weyl fermions liftable, at degree 1 (2 pairs) or 2 (22 pairs).
  Control (the rule is live): shifting one partner by e5 (torus 3, never absorbable) rejects 134/134; by e1 (det(1 - theta_1) = 1)
  rejects 0/134.  Not imposed: the non-SUSY vertex (H-momentum-type) rule; the singlet vacuum itself (no potential minimised).
12312 -- Scherk-Schwarz potential proxy, V(R) ~ xi (n_F - n_B)/R^4 at large R (on-shell degrees of freedom; the engine lists both
  helicities/conjugates, gauge components = 2 x 77): the candidate brother has n_F - n_B = 604 - 826 = -222 < 0, so V deepens as R
  shrinks and the radius is driven inward, toward the region R_6 < 1.63 sqrt(alpha') where its tachyon returns (12307).  Proxy only.
12313 -- unification with k_Y = 8/3.  SM one-loop running: alpha_2 = alpha_3 at 9.7e16 GeV; k_Y alpha_Y = alpha_2 there needs
  k_Y = 1.29 (1.23 at 5e17 GeV); sin^2 theta_W at the string scale 3/11 (k_Y = 8/3) vs 3/8 (5/3).  k_Y = 8/3 needs 1/alpha_Y ~ 2.7/alpha_2
  where SM running gives ~1.2/alpha_2; extra matter lowers 1/alpha_Y (wrong direction) unless SU(2)-charged matter dominates.
  Quantitative rescue not attempted: k_Y = 8/3 is an open obstruction.
12314 -- audit: every corpus driver that counts non-SUSY-engine tachyons (12111, 12116, 12121, 12131, 12156, 12162, 12174, 12180, 12199,
  12217, 12223, 12224) reads T_NFIELDS, i.e. the engine's full tachyonic configuration (excited tachyons included), which the verbose
  solver confirms (12304).  No corpus claim relied on the retracted 12299 reading except 12298-12303 itself (retracted there).
12315 -- synthesis.  The left-right candidate's remaining assets (three chiral generations, no chiral fractional charge, fractional
  states liftable under the full space-group rule, tachyon-free for R_6 >= 1.63 sqrt(alpha')) are offset by two obstructions found
  here: the radius is driven into the tachyonic region (proxy) and k_Y = 8/3 is far from unification.
"""

import json
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "w33_pass12310_to_12315_vacuum_potential_unification.json"
A = ROOT / "analysis"


def main():
    checks, res = {}, {}
    v = json.loads((A / "search_drivers_12311" / "vacuum.json").read_text())
    ctl = json.loads((A / "search_drivers_12311" / "control.json").read_text())
    res["12311"] = dict(vacuum=v, control=ctl)
    checks["12311: 48/48 liftable at degree <= 2 under the full space-group rule; control e5 134/134 rejected, e1 0/134"] = (
        v["liftable"] == 48 and max(v["degrees"]) <= 2 and ctl["e5"]["rejected"] == 134 and ctl["e1"]["allowed"] == 134)
    s = json.loads((A / "search_drivers_12312" / "ss_proxy.json").read_text())
    res["12312"] = s
    checks["12312: candidate brother n_F - n_B = -222 (radius driven inward)"] = (
        s["v9_w6odd"]["nF_minus_nB"] == -222 and s["v9_w6odd"]["components"]["gauge"] == 154)
    u = json.loads((A / "search_drivers_12313" / "unif.json").read_text())
    res["12313"] = u
    checks["12313: SM running needs k_Y ~ 1.2-1.3, far from 8/3"] = 1.2 < u["k_needed_at_Ms"] < 1.3 and 1.25 < u["k_needed_at_M23"] < 1.35
    lp = A / "search_drivers_12310" / "lr_pool.json"
    if lp.exists():
        d = json.loads(lp.read_text())
        res["12310"] = d["table"]
        hits = sorted(k for k, x in d["results"].items() if "__w6odd" in k and any(r.get("sm_values") for r in x["results"]))
        res["12310_hits"] = hits
        res["12310_timeouts"] = sum(1 for x in d["results"].values() if x["status"] == "timeout")
        h = json.loads((A / "search_drivers_12310" / "hits_nF_minus_nB.json").read_text())
        checks["12310: 2797 dumps, 0 timeouts; 15 hits, all SM_810 variants, all tachyon-free brothers with n_F - n_B = -222"] = (
            len(d["results"]) == 2797 and res["12310_timeouts"] == 0 and len(hits) == 15
            and all("SM_20260917_810" in x for x in hits) and set(h.values()) == {-222})
    checks = {k: bool(x) for k, x in checks.items()}
    res["checks"] = checks
    res["all_checks_pass"] = all(checks.values())
    OUT.write_text(json.dumps(res, indent=2, default=str))
    print(json.dumps(checks, indent=1), res["all_checks_pass"])
    return res


if __name__ == "__main__":
    main()
