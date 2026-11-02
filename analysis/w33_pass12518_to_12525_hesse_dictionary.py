"""Passes 12518-12525 (Claude track): the q = 9 hyperoval floor, the heavy case, and the codeword <-> Hesse dictionary.

12518 -- star cube-and-conquer: no hyperoval of W(3,9) with <= 46 lines (511 classes INFEASIBLE, positive control at 48).
12519 -- heavy cases: minima 16 (q = 3) and 28 (q = 5); at q = 9, W = 46 all 42 cases INFEASIBLE, with a positive control.  With 12518: the q = 9 minimum is 48.
12520 -- Cui-Wang: both groups have order 648; an intertwiner exists only with the mirror convention.
12521 -- the B4 image = Stab(c) = centraliser of sigma_5; 108 + 108 = covered / uncovered; uncovered -> 9 SIC states, covered -> 12 MUB states; P_c syndromes, Weil, T'.
12522 -- the 40-line hyperovals of W(3,7) are one PGSp(4,7) orbit of 720,300 cubes, stabiliser 384.
12523 -- the 216 codewords = the synthematic totals of the 36 double-sixes = Kramers reversal + doily spread; the five-circuit bijection; five-fold Bell contexts; letters versus totals.
12524 -- the order-27 subgroup acts as a syndrome-controlled Weyl operator.
12525 -- GAP stabilisers D16 x S4 (q = 7), order 1920 (q = 9); CaDiCaL re-check at q = 3, 5; q = 9 uniqueness status.
12526 -- the other track's 216-point frame = 36 regular 5-simplices; five-spaces on SRG(36,15,6,6); 120 shared directions = (line, matching).
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
    for q, W in ((7, 38), (7, 40), (9, 46)):
        r = load(f"heavy_split_q{q}_W{W}.json")
        res["heavy_status"][f"q{q}_W{W}"] = "pending" if r is None else dict(cases=r["cases"], infeasible=r["infeasible"], unknown=r["unknown"], feasible=[f["weight"] for f in r["feasible"]])
    cl, clb, cs, h7 = load("classify_q7.json"), load("classify_q7b_11905.json"), load("cube_stabiliser_q7.json"), load("heavy_split_q7_W38.json")
    res.update(classify=cl, classify_b=clb, cube_orbit=cs)
    decided = {c["rep"]: c for c in cl["per_class"]}
    checks["12519: q = 7 heavy cases at W = 38 all INFEASIBLE"] = h7["infeasible"] == h7["cases"] == 34 and not h7["unknown"] and not h7["feasible"]
    checks["12522: 22 star classes empty, class 24 one cube, class 11905 finished by exclusion: one orbit of 42 cubes, then INFEASIBLE"] = (
        sum(c["status"] == "INFEASIBLE" for c in cl["per_class"]) == 22 and decided[24]["status"] == "OPTIMAL" and decided[24]["solutions"] == decided[24]["cubes"] == 1
        and decided[11905]["non_cubes"] == 0 and clb["final_status"] == "INFEASIBLE" and clb["orbits"] == [{"size": 42, "cube": True}])
    count = 343 * (decided[24]["orbit"] * 1 + decided[11905]["orbit"] * clb["total_sets"]) * 400 // 40
    checks["12522: the count 720,300 agrees with direct orbit enumeration, stabiliser 384"] = count == cs["orbit"] == 720300 and cs["stabiliser"] == 384
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
    fc, cb, st6, kd, cs2, ps, sy, bg = (load(n) for n in ("five_circuit_map.json", "common_bell_contexts.json", "synthematic_totals.json", "kramers_doily.json", "codeword_vs_spread.json", "pair_of_sic.json", "syndrome_theorem.json", "bell_generalisation.json"))
    res.update(five_circuit=fc, common_bell=cb, totals=st6, kramers=kd, spread=cs2, sic_pairs=ps, syndrome=sy, generalisation=bg)
    checks["12523: each stabiliser fixes one five-circuit; equivariant bijection of the 216 onto the 216; the circuit covers exactly the 20 uncovered points"] = (
        fc["invariant_circuits"] == 1 and fc["bijection"] and fc["union_of_circuit_points"] == 20 and fc["sentinel_pairwise_intersections"] == [2])
    checks["12523: grid minus pair = sentinel, S = all lines missing the 20 points, for all 216; 24 lines Bell, 16 lines product"] = (
        cb["grid_minus_pair_is_the_sentinel_all_216"] and cb["the_10_lines_are_all_lines_missing_the_20_points_all_216"] and cb["lines_by_intersection_with_a_sentinel"] == {"0": 24, "2": 16}
        and cb["schmidt_spectra_by_line_type"] == {"2": {"(1.0, 0.0, 0.0)": 144}, "0": {"(0.3333, 0.3333, 0.3333)": 216}})
    checks["12523: 36 double-sixes, 6 totals each (6 of 3003 five-subsets), every codeword's circuit is a total, bijection"] = (
        st6["double_sixes"] == 36 and st6["totals_total"] == 216 and st6["every_circuit_is_a_total"] and st6["bijection_codewords_totals"] and st6["codewords_per_double_six"] == [6]
        and st6["5_subsets_of_15_synthemes_that_are_totals"] == 6 and st6["two_totals_share_one_syntheme"] == [1])
    checks["12523: 36 fixed-point-free outer involutions each swap 15 splits forming a GQ(2,2) with 6 spreads; all 216 codewords arise once"] = (
        kd["outer_involutions_fixing_15_sentinels"] == 36 and kd["all_15_swap_the_factors"] == [15] and kd["doily_is_GQ22"] and kd["spreads_per_doily"] == {"6": 36} and kd["codewords_hit"] == 216 and kd["each_codeword_from_unique_theta"] == [1]
        and kd["fixed_point_counts"]["0"] == 36)
    gapa5 = (D / "gap_a5.out").read_text()
    checks["12523: a codeword fixes one spread and is disjoint from it; its A5 [5,5,10,20] and the cores' [10,30] are the two classes in A6"] = (
        cs2["spreads_fixed_by_Stab"] == 1 and cs2["intersection_with_fixed_spread"] == 0 and cs2["A5_line_orbits"] == [5, 5, 10, 20] and "[ 10, 30 ]" in gapa5 and "[ 5, 5, 10, 20 ]" in gapa5)
    checks["12523: uncovered T_c-classes biject with the 36 pairs of SIC points; the stabilising involution is the third point"] = ps["uncovered_pair_labels"] == 36 and ps["classes_per_pair"] == [1] and ps["stabiliser_involution_is_third_point"]
    checks["12523: at q = 3, 5, 7, 9 the uncovered points are the union of the missed factorisations"] = (
        [g["result"]["sentinels_missed"] for g in bg] == [5, 40, 87, 330] and all(g["result"]["closure_is_S"] and g["result"]["union_missed_pts"] + g["result"]["covered"] == {3: 40, 5: 156, 7: 400, 9: 820}[g["q"]] for g in bg))
    checks["12524: exactly 27 elements are scalar on the reducible syndrome; 9 orthogonal operators on s = 1; L^-1 on s = 2"] = (
        sy["elements_scalar_on_reducible_syndrome"] == sy["N"] == 27 and sy["distinct_block_ops_mod_phase"] == 9 and sy["orthogonal_operator_basis"] and sy["outside_N_scalar_on_reducible"] == 0
        and sum(v for k, v in sy["power_law_counts"].items() if "'b2~b1^-1', np.True_" in k) == 27)
    gs = (D / "gap_stab.out").read_text().replace("\n", " ")
    checks["12525: GAP: q = 7 stabiliser 384 = D16 x S4, orbit 720300; q = 9 stabiliser 1920, orbit 3586680"] = "D16 x S4" in gs and "orbit=720300" in gs and "stab=1920" in gs and "orbit=3586680" in gs and "[ 384, 18032 ]" in gs
    c3, c3b, c5, c5b = (load(f"recheck_cadical_q{q}_W{W}.json") for q, W in ((3, 8), (3, 10), (5, 18), (5, 20)))
    checks["12525: CaDiCaL reproduces the star verdicts at q = 3, 5"] = c3["unsat"] == 2 and not c3["sat"] and c3b["unsat"] == 1 and [s["weight"] for s in c3b["sat"]] == [10] and c5["unsat"] == 4 and c5b["unsat"] == 3 and [s["weight"] for s in c5b["sat"]] == [20]
    r7 = load("recheck_cadical_q7_W38.json"); res["second_solver"] = dict(q7_W38="pending" if r7 is None else dict(unsat=r7["unsat"], sat=r7["sat"], classes=r7["classes"]), q9="not attempted")
    cq = load("classify_q9.json"); res["classify_q9"] = "pending" if cq is None else dict(done=cq.get("done", False), infeasible=cq["infeasible"], feasible=[(f["rep"], f["normal_forms"], f["sets"]) for f in cq["feasible"]], unknown=cq["unknown"], classes=cq["classes"])
    sf = load("simplex_frame.json"); res["simplex_frame"] = sf
    checks["12526: Z_s is linear in the total's sentinels; each double-six's 6 rows sum to zero with inner product -8; rank 24"] = (
        sf["row_formula_all_216"] and sf["rows_sum_to_zero_each_double_six"] and sf["inner_products_within_double_six"] == {"-8": 540} and sf["ranks"] == [5] and sf["rank_all"] == 24)
    checks["12526: projectors sum to 7.5 E_2; the 36 five-spaces carry SRG(36,15,6,6)"] = (
        sf["sum_projectors_eigs"]["7.5"] == 24 and sf["SRG_on_36"] == [15] and sf["common_lambda_mu"] == [6] and sum(sf["principal_cos2_spectra_between_five_spaces"].values()) == 630)
    checks["12526: 120 shared directions, each in 3 spaces; +-3 entries = a line with a perfect matching, all 120 occur"] = (
        sf["shared_directions"] == 120 and sf["spaces_per_direction"] == [3] and sf["three_entries_are_a_line_with_a_matching"] and sf["distinct_line_matchings"] == 120)
    checks["12526: control -- reproduces the other track's cubic moment 108 on all 160 collinear triples"] = sf["control_cubic_moment_on_collinear_triples"] == {"108": 160}
    checks = {k: bool(v) for k, v in checks.items()}
    res["checks"] = checks
    res["all_checks_pass"] = all(checks.values())
    OUT.write_text(json.dumps(res, indent=2, default=str))
    print(json.dumps(checks, indent=1), res["all_checks_pass"], res["heavy_status"], res["cube_orbit"])
    return res


if __name__ == "__main__":
    main()
