"""Passes 12527-12533 (Claude track): orthonormal frames, knots, Mermin squares, the Burkhardt quartic.

12527 -- the q = 5 minimal set is the weight-2 shell of an orthonormal frame; W(3,13) has an even set of 160 lines (verified in the separately built geometry).
12528 -- |V(e^{i pi/3})| of a plat closure = sqrt(3)^dim(L0 meet beta L0); the bracket is 3 <cap| U |cap>.
12529 -- q = 2: contextual iff |S| = 2 mod 4; q = 4: contextuality is not specific to even sets.
12530 -- the 216 totals are A5 root stars; F becomes const * sigma_4 under v_i -> e_0 - e_i, for all 216.
12531 -- no tested subset of the 36 simplices is tight or detects the lines.
12532 -- HiGHS independently confirms the hyperoval floors at q = 7, 9; a from-scratch search reproduces q = 3, 5.
12533 -- W(3,3) points = Fox tricolourings of 6 points = zero-charge Z_3 parafermion monomials; the TL6 generators act by the Fox rule.
"""

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
D = ROOT / "analysis" / "search_drivers_12466"
OUT = ROOT / "data" / "w33_pass12527_to_12533_frames_knots_burkhardt.json"


def load(name):
    p = D / name
    return json.loads(p.read_text()) if p.exists() else None


def main():
    checks, res = {}, {}
    v5, v13, ff = load("verify_frame_set_q5.json"), load("verify_frame_set_q13.json"), load("frame_family.json")
    res.update(frame_q5=v5, frame_q13=v13, frame_family=ff)
    checks["12527: q = 5: the weight-2 shell has 20 points, line intersections 0 and 2, and is even in the separately built W(3,5)"] = (
        v5["weight"] == 20 and v5["line_intersection_histogram"] == {"0": 96, "2": 60} and v5["all_points_even_in_W"] and v5["lines_in_W"] == 20
        and next(o for o in v5["orbit_table"] if o["chosen"])["hamming"] == 2)
    chosen13 = [o for o in v13["orbit_table"] if o["chosen"]]
    checks["12527: q = 13: one orbit of size 160 of a Hamming-weight-4 vector, even in the separately built W(3,13), coverage 0/2/4, below 168"] = (
        v13["weight"] == 160 < 168 and len(chosen13) == 1 and chosen13[0]["hamming"] == 4 and v13["all_points_even_in_W"] and v13["lines_in_W"] == 160
        and v13["coverage_in_W"] == {"0": 1340, "2": 960, "4": 80} and v13["isotropic_lines_have_p02_plus_p13_zero_and_map_to_the_quadric"]
        and 6 * 6 % 13 == (-3) % 13 and 1 + 1 + 1 + 36 == 39 and 39 % 13 == 0)
    fmin = {}
    for q in (3, 5, 7, 9, 11, 13, 17):
        r = load(f"frame_orbits_q{q}.json")
        if r: fmin[q] = min(s["weight"] for s in r["search"] if "weight" in s)
    res["frame_minimum"] = fmin
    checks["12527: frame minima 20, 20, 60, 80, 112, 160, 320 at q = 3, 5, 7, 9, 11, 13, 17"] = fmin == {3: 20, 5: 20, 7: 60, 9: 80, 11: 112, 13: 160, 17: 320}
    res["larger_q_frame_status"] = {q: ("pending" if load(f"frame_orbits_q{q}.json") is None else min(s["weight"] for s in load(f"frame_orbits_q{q}.json")["search"] if "weight" in s)) for q in (19, 23, 25, 29)}
    kn, ko = load("knots_w33.json"), load("knots_overlap.json")
    res.update(knots=kn, knots_overlap=ko)
    checks["12528: p0, p2, p4 lie on one line; plat closures: 220/220 agree with d = dim(L0 meet beta L0); three control lines disagree"] = (
        kn["p4_on_line_of_p0_p2"] and kn["all_three_commute"] and kn["plat_tests"] == kn["plat_agree"] == 220 and all(int(v) >= 80 for v in kn["control_other_lines_mismatches"].values()))
    checks["12528: standard closure agrees with reduced Burau at t = -1 for n = 3, 5, 90/90"] = all(kn["standard_closure_vs_burau"][n]["agree"] == 90 for n in ("3", "5"))
    checks["12528: known knots: trefoil 1, figure-eight 0, Hopf 0, unknot 0, two trefoils 2, T(3,5) 0"] = all(v["got"] == v["expected"] for v in kn["known"].values())
    checks["12528: bracket = 3 <cap|U|cap> as a complex identity on 160/160 words"] = int(ko["complex_identity_agree"]) == 160 == int(ko["abs_vs_line_agree"]) and ko["worst_error"] < 1e-9 and ko["cap_is_P4_eigenstate"]
    f = ko["long_word_dim_frequencies"]
    checks["12528: long words: dim frequencies within 0.01 of 27/40, 12/40, 1/40"] = abs(f["0"] - 27 / 40) < 0.01 and abs(f["1"] - 12 / 40) < 0.01 and abs(f["2"] - 1 / 40) < 0.01
    me = load("mermin_even.json"); res["mermin"] = me
    q2, q4 = me[0], me[1]
    checks["12529: q = 2: contextual iff |S| = 2 mod 4 on all 31 words; a single context is noncontextual; 10 minimal words"] = (
        q2["contextual_iff_weight_2_mod_4"] and q2["all_words"] == {"noncontextual|8": 15, "CONTEXTUAL|6": 10, "CONTEXTUAL|10": 6} and q2["single_context"] == {"noncontextual|1": 1} and q2["minimal_words"] == 10)
    checks["12529: q = 4: one line and two meeting lines noncontextual; irreducible contextual cores as small as 6 lines with 9 meetings"] = (
        not q4["one_line_contextual"] and not q4["two_meeting_lines_contextual"] and q4["smallest_core"] == 6 and any(c["irreducible_core"] == 6 and c["core_graph_edges"] == 9 for c in q4["irreducible_contextual_cores"]))
    bk = load("burkhardt_totals.json"); res["burkhardt"] = bk
    checks["12530: unique quartic invariant, singular at the 45 mirrors; control is not"] = (
        bk["quartic_invariants_of_all_45_reflections"] == 1 and bk["F_invariant_under_all_45"] and bk["max_grad_norm_at_45_nodes"] < 1e-10 and bk["control_grad_norm_random"] > 0.01 and bk["mirror_overlaps_0_if_disjoint_half_otherwise"])
    checks["12530: 40 Jacobi planes (rank 3, F vanishes), 40 Steiner hyperplanes (rank 4, 18 nodes, F = product of 4 planes)"] = (
        bk["point_gives_rank_3_span_of_9_nodes"] and bk["max_F_on_j_planes"] < 1e-10 and bk["line_gives_span_rank"] == {"4": 40} and bk["nodes_in_a_steiner_prime"] == [18] and bk["steiner_prime_F_is_product_of_its_4_planes_max_spread"] < 1e-9)
    checks["12530: all 216 totals are A5 stars: rank 5, Gram det 3/16, group order 720, 15 mirrors, 36 subsystems; controls differ"] = (
        bk["total_is_A5_star_gram"] and bk["total_node_rank"] == {"5": 216} and bk["total_gram_abs_det"] == {"0.1875": 216} and bk["total_reflection_group_order"] == {"720": 216} and bk["total_mirror_closure_size"] == {"15": 216} and bk["distinct_subsystems"] == 36
        and "0.1875" not in bk["control_other_5_sets_abs_det_top"])
    checks["12530: F = const * sigma_4 under v_i -> e_0 - e_i for all 216 totals"] = bk["F_equals_const_sigma4_max_spread_over_216"] < 1e-9
    ts, to = load("tomography_subset.json"), load("tomography_orbits.json"); res.update(tomography_subset=ts, tomography_orbits=to)
    checks["12531: negative within the tested subsets: no sample up to k = 12 and no proper orbit union is tight or detects the lines"] = (
        all(v["detects_in_600"] == 0 and v["tight_in_600"] == 0 for v in ts["by_k"].values()) and all(not u["tight"] and not u["detects"] for r in to.values() for u in r["unions"]))
    hs = [load(f"recheck_highs_q{q}_W{W}_0_{n}.json") for q, W, n in ((3, 8, 2), (5, 18, 4), (5, 20, 4))]
    checks["12532: HiGHS reproduces the star verdicts at q = 3, 5"] = hs[0]["infeasible"] == 2 and hs[1]["infeasible"] == 4 and hs[2]["infeasible"] == 3 and [x["weight"] for x in hs[2]["feasible"]] == [20] and not any(h["unknown"] for h in hs)
    dfs = (D / "dfs_controls.out").read_text()
    checks["12532: the from-scratch search reproduces q = 3, 5 with exact solution counts"] = "q3W8 DONE total_solutions 0" in dfs and "q3W10 DONE total_solutions 1" in dfs and "q5W18 DONE total_solutions 0" in dfs and "q5W20 DONE total_solutions 5" in dfs
    log7 = D / "dfs_q7_W38.log"
    res["second_solver"] = dict(dfs_q7_W38_cases_finished=(sum(1 for x in log7.read_text().splitlines() if x.startswith("case")) if log7.exists() else None), highs="see the 12532 checks", cadical_q7="stopped: no case finished")
    h7a, h7b, h9, hc9 = load("recheck_highs_q7_W38_0_1.json"), load("recheck_highs_q7_W38_1_24.json"), load("recheck_highs_q9_W46_0_511.json"), load("highs_control_q9.json")
    checks["12532: HiGHS: q = 7, W = 38 all 24 infeasible; q = 9, W = 46 all 511 infeasible; class 24380 has optimum 48"] = (
        h7a["infeasible"] + h7b["infeasible"] == 24 and not h7a["unknown"] + h7b["unknown"] and h9["infeasible"] == 511 and not h9["unknown"] and not h9["feasible"] and hc9["class_24380_min_weight"] == 48 and hc9["class_24380_status"] == 0)
    hh7 = load("heavy_highs_q7_W38.json"); res["heavy_highs"] = {f"q{q}_W{W}": (lambda r: "pending" if r is None else dict(cases=r["cases"], infeasible=r["infeasible"], unknown=r["unknown"], feasible=[f["weight"] for f in r["feasible"]]))(load(f"heavy_highs_q{q}_W{W}.json")) for q, W in ((7, 38), (7, 40), (9, 46), (9, 48))}
    res["heavy_status"] = res["heavy_highs"]
    checks["12532: HiGHS heavy cases: q = 7, W = 38 all 34 infeasible"] = hh7["infeasible"] == hh7["cases"] == 34 and not hh7["unknown"] and not hh7["feasible"]
    fx, pf, fp = load("fox_w33.json"), load("parafermion_w33.json"), load("fox_general_p.json"); res.update(fox=fx, parafermion=pf, fox_general_p=fp)
    checks["12533: Fox is a B6 rep on V, unique invariant form, non-degenerate, transvections; a similitude intertwines all 5 generators; caps map onto L0"] = (
        fx["fox_preserves_alternating_sum"] and fx["fox_is_a_braid_rep"] and fx["invariant_alternating_forms_dim"] == 1 and fx["form_nondegenerate"] and fx["sigma_is_a_transvection"] and fx["linear_similitude_exists"]
        and all(fx["intertwines_each_generator_same_sign"].values()) and fx["caps_map_to_L0"] and fx["cap_colourings_mod_const"] == 9)
    checks["12533: diagram colourings = 3^(1 + d) and Jones = sqrt3^d on 150/150; colourings vs Jones 60/60 at 2, 4, 8 strands"] = (
        fx["plat_fox_nullity_eq_1_plus_d__and_jones_eq_d"] == {"(True, True)": 150} and all(v["agree"] == v["tests"] == 60 for v in fx["general_strands_fox_vs_jones"].values()))
    checks["12533: explicit parafermions: constant commutation exponent, charge-sector Pauli group of 81 trace-orthonormal classes, closed form matches"] = (
        len(pf["g_i_g_j_constant_exponent_for_i_lt_j"]) == 1 and pf["closed_form_fox_invariant"] and pf["constants_in_radical"] and pf["zero_charge_monomials_commute_with_Q"] and pf["commutators_match_closed_form"]
        and pf["sector_dims"] == [9, 9, 9] and pf["constant_colouring_is_scalar_on_a_sector"] and pf["81_classes_trace_orthonormal"] and pf["each_is_unitary_on_sector"])
    checks["12533: the triangle: TL6 generators from bilinear eigenprojectors act by the (inverse) Fox rule, all 5 generators and all 3 projectors; TL holds"] = (
        all(v == ["inverse"] * 3 for v in pf["TL_generator_acts_on_monomials_by"].values()) and pf["neighbouring_bilinear_eigenprojectors_satisfy_TL"])
    checks["12533: p = 3, 5, 7, 11: form invariant, non-degenerate, caps isotropic, 120/120 colouring counts; control Lagrangian disagrees"] = all(
        v["form_invariant"] and v["nondegenerate"] and v["caps_isotropic"] and v["plat_agree"] == v["plat_tests"] == 120 and v["other_lagrangian_is_isotropic"] and v["control_mismatches"] > 0 for v in fp.values())
    hq946, hq948 = load("heavy_highs_q9_W46.json"), load("heavy_highs_q9_W48.json")
    checks["12532: HiGHS heavy cases: q = 9, W = 46 and W = 48 all 42 infeasible, none unknown: the minimum is 48 and every minimal set is a hyperoval"] = all(h["infeasible"] == h["cases"] == 42 and not h["unknown"] and not h["feasible"] for h in (hq946, hq948))
    kg, mc, tm, cp = load("kauffman_golden.json"), load("magic_colour.json"), load("tl_module_even_weil.json"), load("colour_patterns.json"); res.update(kauffman=kg, magic=mc, tl_module=tm, colour_patterns=cp)
    checks["12537: Q at the golden ratio matches 5-colourings 150/150, Q(-1) matches 3-colourings 150/150; trefoil controls"] = (
        kg["tests"] == {"golden": [150, 150], "at_minus1": [150, 150]} and abs(kg["trefoil_at_golden_vs_formula"][0] - kg["trefoil_at_golden_vs_formula"][1]) < 1e-9 and abs(kg["trefoil_at_minus1"] + 3) < 1e-9)
    checks["12537: the odd state has W = -1/3, sum-negativity 1/3, Weyl overlaps 1/4; stabiliser states have W >= 0; parity measurement reaches it with probability 1/2"] = (
        min(mc["odd_state_W"]) == -0.333333 and abs(mc["sum_negativity"] - 1 / 3) < 1e-9 and mc["weyl_orbit_overlaps"] == [0.25] and mc["min_W_on_stabiliser_states"] > -1e-9 and mc["prob_of_odd_outcome_from_stabiliser_states"] == [0.0, 0.5])
    checks["12537: the TL6 vacuum module has dimension 5 and exactly one displaced parity acts as +1 on it, commuting with all projectors, +1 eigenspace of dimension 5"] = (
        tm["module_dimension"] == 5 and tm["module_invariant_under_all_R"] and len(tm["displaced_parities_acting_as_plus_one_on_module"]) == 1 and all(tm["centre_commutes_with_all_Pi"]) and tm["centre_parity_plus_one_dimension"] == 5)
    checks["12537: exactly the 5 non-crossing bipartite matchings are lines; 2 codewords contain all 5; colour-size census of the 40 points"] = (
        cp["matchings"]["bipartite"] == 6 and cp["matchings"]["bipartite_are_lines"] == 5 and cp["matchings"]["bipartite_noncrossing"] == 5 and cp["codewords_by_number_of_matching_lines"]["5"] == 2 and sum(cp["points_by_colour_class_sizes"].values()) == 40)
    tr = load("codeword_triangle.json"); res["triangle"] = tr
    checks["12537: triangles of codewords: one orbit of 720, stabiliser 36, from 2160 pairs sharing 5 lines; caps stabiliser order 12"] = (
        tr["triples_summing_to_zero"] == 720 and tr["triangle_orbit_size"] == 720 and tr["triangle_stabiliser_order"] == 36 and tr["pairwise_intersection_counts"]["5"] == 2160 and tr["caps_stabiliser_order"] == 12)
    checks = {k: bool(v) for k, v in checks.items()}
    res["checks"] = checks
    res["all_checks_pass"] = all(checks.values())
    OUT.write_text(json.dumps(res, indent=2, default=str))
    print(json.dumps(checks, indent=1), res["all_checks_pass"], res["larger_q_frame_status"], res["second_solver"]["dfs_q7_W38_cases_finished"])
    return res


if __name__ == "__main__":
    main()
