"""Passes 12466-12473 (Claude track).

12466 -- d = 2q in LINE variables: kernel words are N y with sum y even, and by the k-line lemma (12460) a word of weight < 2q needs
  >= q + 2 lines in every representation.  CP-SAT with native XOR (s_p = XOR of y over the lines through p): q = 3 controls exact
  (weight 4 infeasible; weight 6 found as 2 lines); q = 5, weights 6-8 with >= 7 lines: UNKNOWN after 600 s -- the dual encoding is no
  stronger than the primal (12450), so CP-SAT is not the q = 7 lever in either variable set.
12467 -- even line sets (ker_2 N: every point on an even number of chosen lines), exact MILP minimum: 6, 10, 20 at q = 2, 3, 5, every
  optimum with coverage exactly {0, 2}.  q = 2 is the grid of 2(q+1) lines (control: W(2)'s lines are regular); for odd q the minimum
  exceeds 2(q+1) (10 > 8, 20 > 12), consistent with W(q), q odd, having no (q,1) grid sub-quadrangle.  The remaining case of d = 2q needs
  a line set within |S| < 2q odd points of an even set; how small even sets can be is the structural input.
12468-12470 -- the k_Y window.  Cited: 12131 (k_Y = 5/3 + 4n for every fraction-free hypercharge, Schellekens' self-duality argument)
  and 12154 (non-SUSY running needs k_Y ~ 1.29).  So a viable model needs 1 <= k_Y < 5/3 (1 = the e^c conformal-weight bound) and
  hence fractionally charged string states, which must then be lifted -- the SM_2541 mechanism (12451), at a smaller k_Y.
  Spectrum floors for SM_2541: the single-field Cauchy-Schwarz floor is exactly 1 in every model (uninformative); the ONE-GENERATION
  floor (least-norm t over every choice of Q, u^c, d^c, L, e^c representatives, both signs, anomaly-free) is 1.19 for c22 -- the
  geometry admits k_Y ~ 1.3 for one generation.  Three generations, exhaustively in the 1/6 menu: c22 has exactly 6 hypercharges, min
  11/3; with a necessary L1 cap (sum |t_j| <= 4 sqrt(K/2)) at K = 5/3 the capped enumeration finds only k_Y = 17/3 -- PROVED: no
  three-generation hypercharge of c22 with k_Y <= 5/3 in that menu.  The 1/18 menu (|Y| <= 2) hit the solver time limit: open.
"""

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "w33_pass12466_to_12473_dual_lines_even_sets_ky_floor.json"
A = ROOT / "analysis"


def j(p):
    return json.loads((A / p).read_text())


def main():
    checks, res = {}, {}
    d34, d36, d58 = (j(f"search_drivers_12466/dual_q{q}_{a}_{b}.json") for q, a, b in ((3, 4, 4), (3, 6, 6), (5, 6, 8)))
    res["12466"] = dict(q3_w4=d34, q3_w6=d36, q5_w6_8=d58)
    checks["12466: dual line model controls exact at q = 3 (weight 4 infeasible; weight 6 = 2 lines, in the kernel); q = 5 UNKNOWN (tool limit)"] = (
        d34["status"] == "INFEASIBLE" and d36["weight"] == 6 and d36["n_lines"] == 2 and d36["in_kernel"] and d58["status"] == "UNKNOWN")
    ev = {q: j(f"search_drivers_12466/even_line_sets_q{q}.json") for q in (2, 3, 5)}
    p7 = A / "search_drivers_12466/even_line_sets_q7.json"
    if p7.exists():
        ev[7] = json.loads(p7.read_text())
    res["12467"] = ev
    checks["12467: minimum even line sets 6, 10, 20 at q = 2, 3, 5 (exact, verified even, coverage {0,2}); odd q exceed 2(q+1)"] = (
        [ev[q]["min_even_line_set"] for q in (2, 3, 5)] == [6, 10, 20] and all(ev[q]["optimal"] and ev[q]["verified_even"]
        and ev[q]["coverage_profile"] == [0, 2] for q in (2, 3, 5)) and ev[2]["min_even_line_set"] == 2 * 3
        and all(ev[q]["min_even_line_set"] > 2 * (q + 1) for q in (3, 5)))
    kf = j("search_drivers_12468/ky_floor.json")
    res["12468_cs_floor"] = kf
    checks["12468: single-field Cauchy-Schwarz floor = 1 in all 52 SM_2541 models and the SM_2913 control (the universal e^c bound)"] = (
        sum(1 for k in kf if not k.startswith("control")) == 52 and all(abs(v["kY_floor_float"] - 1) < 1e-12 for v in kf.values()))
    fl = {p.stem: json.loads(p.read_text()) for p in (A / "search_drivers_12468/floors").glob("*.json")}
    res["12468_generation_floor"] = {k: v["kY_floor_generation"] for k, v in fl.items()}
    c22 = fl["Z6II_06_SM_20260917_2541_c22"]["kY_floor_generation"]
    checks["12468: c22 one-generation floor 1.19 < 1.29 (the geometry does not forbid the unification value for one generation)"] = 1.18 < c22 < 1.19
    res["12468_family_floor_range"] = [min(res["12468_generation_floor"].values()), max(res["12468_generation_floor"].values()), len(fl)]
    checks["12468: all 52 SM_2541 models share the one-generation floor 1.187 (siblings of one parent)"] = (
        len(fl) == 52 and max(res["12468_generation_floor"].values()) - min(res["12468_generation_floor"].values()) < 1e-9)
    if 7 in ev:
        checks["12467: q = 7 even line set -- MILP hit its time limit with an even set of 40 lines (upper bound only)"] = (
            not ev[7]["optimal"] and ev[7]["verified_even"] and ev[7]["min_even_line_set"] == 40)
    ys = j("search_drivers_12468/ysearch_Z6II_06_SM_20260917_2541_c22_noanom_loose.json")
    kc = j("search_drivers_12468/ysearch_Z6II_06_SM_20260917_2541_c22_noanom_loose_kcap5o3.json")
    kc4 = j("search_drivers_12468/ysearch_Z6II_06_SM_20260917_2541_c22_noanom_loose_kcap4.json")
    from fractions import Fraction as F
    res["12469"] = dict(all_kY=sorted({s["kY"] for s in ys["solutions"]}), capped_5o3=[s["kY"] for s in kc["solutions"]])
    checks["12469: c22 exhaustive in the 1/6 menu -- exactly 6 three-generation hypercharges, min k_Y = 11/3"] = (
        len(ys["solutions"]) == 6 and min(F(s["kY"]) for s in ys["solutions"]) == F(11, 3))
    checks["12469: L1-capped enumeration at K = 5/3 finds only k_Y = 17/3 > 5/3 -- no c22 hypercharge with k_Y <= 5/3 in the 1/6 menu (cap control at K = 4 keeps true solutions)"] = (
        [s["kY"] for s in kc["solutions"]] == ["17/3"] and len(kc4["solutions"]) >= 3)
    checks = {k: bool(v) for k, v in checks.items()}
    res["checks"] = checks
    res["all_checks_pass"] = all(checks.values())
    OUT.write_text(json.dumps(res, indent=2, default=str))
    print(json.dumps(checks, indent=1), res["all_checks_pass"])
    return res


if __name__ == "__main__":
    main()
