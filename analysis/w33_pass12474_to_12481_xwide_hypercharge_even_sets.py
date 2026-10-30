"""Passes 12474-12481 (Claude track).

12474 -- minimal even line sets with a line-pair symmetry break: every point of line 0 is covered evenly, so a second chosen line meets
  line 0, and the stabiliser of line 0 is transitive on the lines meeting it -- fix one.  Control q = 5 reproduces the exact minimum 20
  (in half the time); q = 7: see the certificate (optimum or time limit).
12475 -- SM_2541_c22 in the 1/18 charge menu (|Y| <= 2 for every non-quark field) with the necessary L1 cap sum|t_j| <= 4 sqrt(K/2) at
  K = 5/3: the complete capped enumeration (ends INFEASIBLE, not at a time limit) finds only k_Y = 17/3 and 461/81 -- PROVED: no
  three-generation hypercharge of c22 has k_Y <= 5/3 in the 1/18 menu either.  With 12469 (1/6 menu) the SM_2541 route to the window
  1 <= k_Y < 5/3 is closed for c22 in both menus; the one-generation floor 1.187 is therefore NOT attainable by a full spectrum.
"""

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "w33_pass12474_to_12481_xwide_hypercharge_even_sets.json"
A = ROOT / "analysis"


def main():
    checks, res = {}, {}
    e5 = json.loads((A / "search_drivers_12466/even_line_sets_q5_sym2.json").read_text())
    res["12474_q5_sym2"] = e5
    checks["12474: line-pair symmetry break reproduces the exact q = 5 minimum 20 (optimal, verified even, coverage {0,2})"] = (
        e5["optimal"] and e5["min_even_line_set"] == 20 and e5["verified_even"] and e5["coverage_profile"] == [0, 2])
    p7 = A / "search_drivers_12466/even_line_sets_q7_sym2.json"
    if p7.exists():
        e7 = json.loads(p7.read_text()); res["12474_q7_sym2"] = e7
        res["12474_q7_status"] = (f"exact minimum {e7['min_even_line_set']}" if e7["optimal"] else
                                  f"time limit; best even set {e7.get('min_even_line_set')} (upper bound)")
        checks["12474: q = 7 minimum even line set is exactly 40 (optimal with the symmetry break; refutes the 5(q-1) = 30 guess of 12467); "
               "odd q give 10, 20, 40 -- fits 5 * 2^((q-1)/2) [conjecture, three points]"] = (
            e7["optimal"] and e7["min_even_line_set"] == 40 and e7["verified_even"] and e7["coverage_profile"] == [0, 2])
    xw = json.loads((A / "search_drivers_12468/ysearch_Z6II_06_SM_20260917_2541_c22_noanom_xwide_kcap5o3.json").read_text())
    log = (A / "search_drivers_12468/xwide_long.log").read_text(encoding="utf-8", errors="ignore")
    res["12475"] = dict(kY=[s["kY"] for s in xw["solutions"]], ended="infeasible" if "is Infeasible" in log else "time limit")
    from fractions import Fraction as F
    checks["12475: 1/18 menu, cap K = 5/3, complete enumeration (ends infeasible) finds only k_Y in {17/3, 461/81}, all > 5/3"] = (
        res["12475"]["ended"] == "infeasible" and set(res["12475"]["kY"]) == {"17/3", "461/81"}
        and all(F(k) > F(5, 3) for k in res["12475"]["kY"]) and all(s["exact_values_ok"] for s in xw["solutions"]))
    checks = {k: bool(v) for k, v in checks.items()}
    res["checks"] = checks
    res["all_checks_pass"] = all(checks.values())
    OUT.write_text(json.dumps(res, indent=2, default=str))
    print(json.dumps(checks, indent=1), res["all_checks_pass"])
    return res


if __name__ == "__main__":
    main()
