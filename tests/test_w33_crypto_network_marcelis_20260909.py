"""Regression gates for the 2026-09-09 crypto/network/Marcelis execution pass."""

from __future__ import annotations

import importlib.util
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def load(relpath: str, name: str):
    spec = importlib.util.spec_from_file_location(name, ROOT / relpath)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_contextual_decryption_global_section_boundary():
    m = load("analysis/w33_contextual_decryption_obstruction.py", "w33_contextual_decryption")
    row = m.verify()
    assert row["status"] == "PASS"
    assert row["control_W2"]["global_keys"] == 6
    assert row["W33"]["global_keys"] == 0
    assert row["contextuality_quantities"]["abramsky_barbosa_contextual_fraction"] == 1
    assert row["contextuality_quantities"]["ks_satisfiability_defect"] == "1/10"
    assert row["linearized_cohomology_probe"]["F2"]["solvable"] is True
    assert row["linearized_cohomology_probe"]["F3"]["solvable"] is True


def test_support_min_entropy_q3():
    m = load("analysis/w33_support_min_entropy.py", "w33_support_min_entropy")
    row = m.exact_row(3)
    assert row["optimal_classical_guessing_probability"] == "16/81"
    assert math.isclose(row["conditional_min_entropy_bits"], math.log2(81 / 16), rel_tol=0, abs_tol=1e-12)
    assert math.isclose(row["conditional_shannon_entropy_bits"], 8 / 3, rel_tol=0, abs_tol=1e-12)
    assert m.exact_row(2)["conditional_min_entropy_bits"] == 0


def test_witting_card_inverse_analyzer_compiler():
    m = load("analysis/w33_witting_card_single_photon_protocol.py", "w33_witting_card")
    rays = m.rays40()
    bases, _ = m.tetrads(rays)
    assert len(rays) == 40
    assert len(bases) == 40
    memberships = [0] * 40
    families = {}
    for T in bases:
        U = m.analyzer(rays, T)
        profile = [m.support_weight(rays[r]) for r in T]
        f = m.family(profile)
        families[f] = families.get(f, 0) + 1
        for slot, ray in enumerate(T):
            memberships[ray] += 1
            prepared = U.conj().T[:, slot]
            assert abs(abs(prepared.conj() @ rays[ray]) - 1) < 1e-10
    assert set(memberships) == {4}
    assert families == {
        "COMPUTATIONAL_DIRECT_RAILS": 1,
        "ONE_DIRECT_RAIL_PLUS_COMPLEMENT_TRITTER": 12,
        "FOUR_THREE_RAIL_WITTING_ROWS": 27,
    }


def test_marcelis_multichart_firewalls():
    m = load("analysis/w33_marcelis_multichart_atlas.py", "w33_marcelis_atlas")
    _, lines = m.w33()
    charts, web, trans = m.chart_web(lines)
    assert len(charts) == 540
    assert trans == {4: 540}
    assert {len(x) for x in web} == {6}
    assert m.edge_count(web) == 1620
    assert m.triangle_count(web) == 0
    d2 = m.distance_two_graph(web)
    assert {len(x) for x in d2} == {30}
    assert len(m.max_clique_exact(d2)) == 6
    assert m.find_trace_projective_counterexample() is not None


def test_heawood_chart_fibre_quotient():
    m = load("analysis/w33_heawood_chart_fibre_quotient.py", "w33_heawood_fibre")
    row = m.build_result()
    assert row["status"] == "PASS"
    assert row["counts"] == {
        "charts": 540,
        "chart_web_edges": 1620,
        "directed_chart_web_incidences": 3240,
        "heawood_fibre_vertices_per_chart": 14,
        "fano_translation_points_per_chart": 7,
        "fano_lines_per_chart": 7,
        "execution_lines_through_antipode": 3,
        "buffer_lines_not_through_antipode": 4,
        "execution_slots_over_all_charts": 1620,
        "web_neighbour_sheets_per_execution_slot": 2,
    }
    assert row["standard_local_fano"]["canonical_antipode_point"] == 7
    assert row["standard_local_fano"]["execution_lines"] == [
        [1, 6, 7], [2, 5, 7], [3, 4, 7]
    ]
    assert len(row["standard_local_fano"]["buffer_lines"]) == 4
    assert all(row["checks"].values())


def test_marcelis_gf4_trace_gauge():
    m = load("analysis/w33_marcelis_gf4_trace_gauge.py", "w33_marcelis_trace")
    row = m.build_result()
    assert row["status"] == "PASS"
    assert row["schema"] == "w33.marcelis-gf4-trace-gauge.v2"
    assert row["marcelis_source_gauge"]["trace_table"] == {
        "0": 0, "1": 0, "omega": 1, "omega^2": 1
    }
    assert row["projective_completion"]["domain_points"] == 85
    assert row["projective_completion"]["image_points"] == 15
    assert row["projective_completion"]["fibre_size_histogram"] == {
        "1": 1, "2": 2, "4": 4, "8": 8
    }
    assert row["checks"]["marcelis_plane_examples_reproduced"] is True
    assert row["checks"]["complement_algebra_matches_source_decimal_list"] is True
    assert row["checks"]["source_complement_binary_has_exact_two_entry_transposition"] is True
    assert row["marcelis_source_gauge"]["source_binary_mismatch_positions_zero_based"] == [3, 4]
    assert row["marcelis_source_gauge"]["complement_algebraic_bits"][3:5] == ["0111", "1001"]
    assert row["marcelis_source_gauge"]["complement_source_printed_bits"][3:5] == ["1001", "0111"]
    assert row["checks"]["raw_coordinate_trace_fails_projective_invariance"] is True
    assert row["checks"]["omega_gauge_is_representative_invariant"] is True
    assert all(row["checks"].values())


def test_heawood_execution_cycles_are_the_270_four_intersection_spread_pairs():
    m = load("analysis/w33_heawood_spread_pair_270_bridge.py", "w33_heawood_270")
    row = m.build_result()
    assert row["status"] == "PASS"
    assert row["counts"]["slot_cycles"] == 270
    assert row["counts"]["slot_cycle_length"] == 6
    assert row["counts"]["spreads"] == 36
    assert row["counts"]["spread_pairs_total"] == 630
    assert row["counts"]["spread_pairs_intersection_1"] == 360
    assert row["counts"]["spread_pairs_intersection_4"] == 270
    assert row["checks"]["slot_graph_is_270_disjoint_C6"] is True
    assert row["checks"]["C6_axis_unions_biject_to_four_intersection_spread_symdiffs"] is True
    assert row["checks"]["cycle_order_alternates_between_the_two_spread_sides"] is True
    assert all(row["checks"].values())


def test_marcelis_pg34_line_trace_census():
    m = load("analysis/w33_marcelis_pg34_line_trace_census.py", "w33_marcelis_line_trace")
    row = m.build_result()
    assert row["status"] == "PASS"
    assert row["counts"]["PG34_points"] == 85
    assert row["counts"]["PG34_lines"] == 357
    assert row["counts"]["PG32_lines_hit"] == 35
    assert row["counts"]["GF4_lines_to_binary_lines"] == 125
    assert row["counts"]["GF4_lines_to_five_point_plane_subsets"] == 232
    assert row["counts"]["distinct_five_point_plane_subsets"] == 30
    assert row["counts"]["binary_planes_hit"] == 15
    assert row["binary_line_lift_staircase"]["lift_multiplicity_histogram"] == {
        "1": 1, "2": 6, "4": 28
    }
    assert row["punctured_plane_census"]["subset_lift_multiplicity_histogram"] == {
        "4": 2, "8": 28
    }
    assert row["punctured_plane_census"]["container_plane_total_lift_histogram"] == {
        "8": 1, "16": 14
    }
    assert all(row["checks"].values())
