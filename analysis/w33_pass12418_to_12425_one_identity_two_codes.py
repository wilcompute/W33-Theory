"""Passes 12418-12425: one SRG identity, two codes (Claude track).

12418 -- accepts the cross-track correction 923c4eb20: in the split case the Hodge criterion is the balanced 3 + 3 eigenspace split; tr kappa
  = 0 is equivalent only for p != 3 (kappa = i I over F_9 has trace 6i = 0).  Records the completed relaxed hypercharge search (59/59, no
  solution).
12419 -- for the W(3,q) collinearity graph, A^2 + 2A - (q^2 - 1) I = (q + 1) J.  Its interesting primes (those dividing r - s = 2q;
  Brouwer-van Eijl 1992, Brouwer-Van Maldeghem 'p-Ranks') are 2 and p, and the identity reduces to
    mod 2:  A^2 = 0          -> binary CSS code [[q^3+q^2+q+1, q^2 - 1, d]]  (rank_2 A = q(q^2+1)/2 + 1, the in-corpus rank law, Pass 322)
    mod p:  (A + I)^2 = J    -> every qupit graph-state cut-rank <= rank_p(A + I) = 1 + C(p+2, 3)
  because A + I mod p IS the point-hyperplane incidence of PG(3,p) under the symplectic polarity (Smith 1969; in-corpus 2026-10-22 note).
  Checked at q = 3, 5, 7: ranks 16/66/176 and 11/36/85; codes k = 8/24/48.
12420 -- the ceiling is attained (hill-climb on half-size regions: 11, 36, 85; random regular graphs of the same degree reach 20/78/200).
  It is NOT an area law: the ceiling fraction (1 + C(p+2,3)) / (p^3+p^2+p+1) -> 1/6 (0.275, 0.231, 0.213).
12421 -- distance: the symmetric difference of two intersecting lines (weight 2q) is a nontrivial logical (all 240 at q = 3 -- the
  cross-track minimum hexads; 40/40 sampled at q = 5, 7), so d <= 2q; d = 2q proved at q = 3 (923c4eb20), conjectured for q >= 5.
12425 -- synthesis: the cross-track binary code and this track's ternary ceiling are the two 'interesting-prime' reductions of one identity.
"""

import json
from math import comb
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "w33_pass12418_to_12425_one_identity_two_codes.json"
A = ROOT / "analysis"


def main():
    checks, res = {}, {}
    vl = json.loads((A / "search_drivers_12373" / "vet_loose.json").read_text())
    res["12418_relaxed"] = dict(candidates=len(vl), with_solution=sum(1 for v in vl.values() if v))
    checks["12418: relaxed hypercharge search complete -- 59 candidates, no solution"] = len(vl) == 59 and res["12418_relaxed"]["with_solution"] == 0
    tc = json.loads((A / "search_drivers_12419" / "two_codes.json").read_text())
    cf = json.loads((A / "search_drivers_12419" / "css_family.json").read_text())
    res["12419_12420"] = tc; res["12421"] = cf
    ok = True
    for q in ("3", "5", "7"):
        qq = int(q); t = tc[q]
        ok &= t["srg_identity"] and t["A2_zero_mod2"] and t["AplusI_sq_J_modp"]
        ok &= t["rank2_A"] == qq * (qq * qq + 1) // 2 + 1 and t["css_k"] == qq * qq - 1
        ok &= t["rankp_AplusI"] == 1 + comb(qq + 2, 3) == cf[q]["smith_rank"]
    checks["12419: both congruences hold at q = 3, 5, 7; rank_2 A = q(q^2+1)/2+1, k = q^2-1; rank_p(A+I) = 1 + C(p+2,3) (Smith)"] = ok
    checks["12420: the ceiling is attained (11, 36, 85) while random regular graphs reach n/2; ceiling fraction decreasing toward 1/6"] = (
        all(tc[q]["half_cut_rank_found"] == tc[q]["rankp_AplusI"] for q in tc) and all(tc[q]["control_half_cut_rank"] == tc[q]["n"] // 2 for q in tc)
        and tc["3"]["ceiling_fraction"] > tc["5"]["ceiling_fraction"] > tc["7"]["ceiling_fraction"] > 1 / 6)
    checks["12421: weight-2q intersecting-line symmetric differences are logicals (240/240 at q = 3; 40/40 at q = 5, 7)"] = (
        cf["3"]["weight_2q_logicals"] == 240 and cf["5"]["weight_2q_logicals"] == 40 and cf["7"]["weight_2q_logicals"] == 40)
    checks = {k: bool(v) for k, v in checks.items()}
    res["checks"] = checks
    res["all_checks_pass"] = all(checks.values())
    OUT.write_text(json.dumps(res, indent=2, default=str))
    print(json.dumps(checks, indent=1), res["all_checks_pass"])
    return res


if __name__ == "__main__":
    main()
