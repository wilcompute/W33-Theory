"""Passes 12518-12525 (Claude track): the q = 9 hyperoval floor, the heavy case, and the codeword <-> Hesse dictionary.

12518 -- star cube-and-conquer: no hyperoval of W(3,9) with <= 46 lines (511 classes INFEASIBLE, positive control at 48).
12519 -- heavy cases: minima 16 (q = 3) and 28 (q = 5); at q = 9, W = 46 all 42 cases INFEASIBLE, with a positive control.  With 12518: the q = 9 minimum is 48.
12520 -- Cui-Wang: both groups have order 648; an intertwiner exists only with the mirror convention.
12521 -- the B4 image = Stab(c) = centraliser of sigma_5; 108 + 108 = covered / uncovered; uncovered -> 9 SIC states, covered -> 12 MUB states; P_c syndromes, Weil, T'.
12522 -- the q = 7 classification status.
"""

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
D = ROOT / "analysis" / "search_drivers_12466"
OUT = ROOT / "data" / "w33_pass12518_to_12525_hesse_dictionary.json"


def load(name):
    p = D / name
    return json.loads(p.read_text()) if p.exists() else None


def all_infeasible(r):
    return r is not None and not r["unknown"] and not r["feasible"] and r["infeasible"] == r["star_orbits"]


def main():
    checks, res = {}, {}
    star = {f"{q}_{W}": load(f"star_cubes_q{q}_W{W}.json") for q, W in ((3, 8), (3, 10), (5, 18), (5, 20), (7, 38), (9, 46))}
    ctl = load("star48_control.json")
    checks["12518: star classes 2, 4, 24, 511 at q = 3, 5, 7, 9"] = [star[k]["star_orbits"] for k in ("3_8", "5_18", "7_38", "9_46")] == [2, 4, 24, 511]
    checks["12518: controls -- no hyperoval below the known minima 10, 20, 40, and the minima are found at q = 3, 5"] = (
        all_infeasible(star["3_8"]) and all_infeasible(star["5_18"]) and all_infeasible(star["7_38"])
        and [f["weight"] for f in star["3_10"]["feasible"]] == [10] and [f["weight"] for f in star["5_20"]["feasible"]] == [20])
    checks["12518: W(3,9) has no hyperoval of <= 46 lines: all 511 classes INFEASIBLE, none unknown"] = all_infeasible(star["9_46"])
    checks["12518: positive control -- the known 48-set's own class is OPTIMAL at weight 48"] = ctl["status_W48"] == "OPTIMAL" and ctl["weight"] == 48
    h5, h3, h5m = load("heavy_split_q5_W26.json"), load("heavy_split_q3_W30_min.json"), load("heavy_split_q5_W40_min.json")
    checks["12519: q = 5 heavy cases at W = 26 all INFEASIBLE"] = h5["infeasible"] == h5["cases"] and not h5["unknown"] and not h5["feasible"]
    checks["12519: heavy minima 16 at q = 3 and 28 at q = 5"] = min(f["weight"] for f in h3["feasible"]) == 16 and min(f["weight"] for f in h5m["feasible"]) == 28
    h9, hc = load("heavy_split_q9_W46.json"), load("heavy_control.json")
    checks["12519: q = 9 heavy cases at W = 46 all INFEASIBLE, none unknown"] = h9["cases"] == h9["infeasible"] == 42 and not h9["unknown"] and not h9["feasible"]
    checks["12519: positive control -- an 88-line even set of coverage 4 lands in a listed case and satisfies its model"] = (
        hc["lands_in_listed_case"] and hc["max_coverage"] == 4 and hc["weight"] == 88 and hc["status_at_own_weight"] in ("OPTIMAL", "FEASIBLE"))
    res["q9_minimum"] = 48 if all_infeasible(star["9_46"]) and h9["infeasible"] == h9["cases"] and not h9["unknown"] and ctl["weight"] == 48 else None
    res["heavy_status"] = {}
    for q, W in ((7, 38), (9, 46)):
        r = load(f"heavy_split_q{q}_W{W}.json")
        res["heavy_status"][f"q{q}_W{W}"] = "pending" if r is None else dict(cases=r["cases"], infeasible=r["infeasible"], unknown=r["unknown"], feasible=[f["weight"] for f in r["feasible"]])
    cl = load("classify_q7.json")
    res["classify_status"] = "pending" if cl is None else cl["total"]
    cw = load("cuiwang_compare.json")
    iw = cw["intertwiners"]
    checks["12520: both groups have order 648, centre 3; intertwiner for the inverse generators, none for the generators themselves"] = (
        cw["CW_group_order"] == cw["native_group_order"] == 648 and cw["CW_center"] == cw["native_center"] == 3
        and iw["sigma_inverse|123"]["invertible"] and not iw["sigma|123"]["invertible"] and not iw["sigma|321"]["invertible"])
    b, d1, d2, d3, tp = (load(n) for n in ("braid_point_stabiliser.json", "hesse_dictionary.json", "hesse_dictionary2.json", "hesse_dictionary3.json", "tprime_block.json"))
    res.update(point_stabiliser=b, dictionary=d1, dictionary2=d2, dictionary3=d3, tprime=tp, star48_control=ctl)
    checks["12521: the B4 image fixes exactly one point c = perp(p0, p1, p2) and equals its whole stabiliser (648)"] = (
        len(b["points_fixed_by_G"]) == 1 and b["points_fixed_by_G"] == b["perp_of_p0_p1_p2"] and b["G_equals_stabiliser"] and b["stabiliser_of_c_in_PSp43"] == 648)
    checks["12521: the two B4 orbits are exactly 'c covered' and 'c uncovered', 108 each"] = (
        b["coverage_of_c"] == {"2": 108, "0": 108} and sorted((o["size"], tuple(o["coverages"])) for o in b["orbits_vs_coverage"]) == [(108, (0,)), (108, (2,))])
    st = {o["order"]: sorted(o["element_orders"].items()) for o in b["codeword_stabilisers_in_G"]}
    shapes = [sorted(o["element_orders"].items()) for o in b["codeword_stabilisers_in_G"]]
    checks["12521: stabilisers are S3 (covered) and Z6 (uncovered)"] = sorted(shapes) == sorted([[("1", 1), ("2", 3), ("3", 2)], [("1", 1), ("2", 1), ("3", 2), ("6", 2)]]) and list(st) == [6]
    checks["12521: T_c fixes no codeword; 9 involutions = 9 hyperbolic lines through c; 12 affine lines"] = (
        d1["Tc_fixes_no_codeword"] and d1["involutions"] == 9 and d1["distinct_hyperbolic_lines_through_c"] == 9 and d1["affine_lines"] == 12 and d1["each_line_has_3"])
    checks["12521: 216 = 9*12 + 12*9"] = d1["uncovered_fibres_over_9_involutions"] == [12] * 9 and d1["covered_fibres_over_12_lines"] == [9] * 12
    checks["12521: T_c-classes biject with 36 (involution, line) pairs and 36 (Hesse line, pair) labels"] = (
        d3["uncovered_flags"] == 36 and d3["uncovered_classes_per_flag"] == [1] and d3["covered_line_pair_labels"] == 36 and d3["covered_classes_per_label"] == [1])
    checks["12521: the involution eigenvectors are a SIC (all 36 overlaps 1/4) on both 3-blocks"] = d1["SIC_overlaps_per_3_block"] == [{"0.25": 36}, {"0.25": 36}]
    checks["12521: control -- the 12 dual vectors are 4 MUBs (overlaps 0 x 12, 1/3 x 54), not 1/4"] = d2["collinear_SIC_triples_rank2"] == 12 and d2["dual_state_overlaps"] == {"0.333333": 54, "0.0": 12}
    checks["12521: a covered codeword's pair never contains the pointwise-fixed direction"] = d2["direction_in_chosen_pair"] == {"False": 108}
    sp = d2["Pc_eigenspaces"]
    checks["12521: P_c commutes with B4; three invariant 3-dim syndrome spaces, commutants 1, 1, 2"] = (
        all(d2["Pc_commutes_with_generators"]) and all(s["dim"] == 3 and s["leak"] == 0 for s in sp) and sorted(s["commutant_dim"] for s in sp) == [1, 1, 2])
    checks["12521: codeword stabiliser has S5's order profile; derived orbits 108 (uncovered) + 36 + 36 + 36 (covered), as 2026-08-29"] = (
        d3["codeword_stabiliser_in_PSp43"] == {"1": 1, "2": 25, "3": 20, "4": 30, "5": 24, "6": 20}
        and d3["derived_orbits_(size,covered)"] == [[36, True], [36, True], [36, True], [108, False]])
    checks["12521: N (27) is scalar on the 2-block, traceless off centre on a 3-block"] = d3["N_order"] == 27 and d3["kernel_on_2_block_projective"] == 54 and d3["N_abs_trace_on_3_block"] == {"3.0": 3, "0.0": 24}
    wp = {k: v for k, v in d3["weil_abs_trace_profile"]}
    sp0 = {k: v for k, v in d3["syndrome0_abs_trace_profile"]}
    checks["12521: the reducible syndrome's absolute character = 27 x Weil of SL(2,3); control: a 3-block differs"] = (
        d3["weil_projective_order"] == 24 and wp.keys() == sp0.keys() and all(sp0[k] == 27 * wp[k] for k in wp) and d3["control_3_block_abs_trace_profile"] != d3["syndrome0_abs_trace_profile"])
    checks["12521: the 2-block is SL(2,3), the T' doublet with traces 2, -2, -1, 0, 1, factoring through B3"] = (
        tp["order"] == 24 and tp["centre"] == 2 and tp["element_orders"] == {"1": 1, "2": 1, "3": 8, "4": 6, "6": 8} and tp["sigma1_equals_sigma3_up_to_sign"])
    checks = {k: bool(v) for k, v in checks.items()}
    res["checks"] = checks
    res["all_checks_pass"] = all(checks.values())
    OUT.write_text(json.dumps(res, indent=2, default=str))
    print(json.dumps(checks, indent=1), res["all_checks_pass"], res["heavy_status"], res["classify_status"])
    return res


if __name__ == "__main__":
    main()
