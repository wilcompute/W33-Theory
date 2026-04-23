from __future__ import annotations

from scripts.w33_flavor_frontier_audit import analyze, arithmetic_q3_uniqueness_packet, classify_flavor_frontier


def test_arithmetic_q3_uniqueness_packet_is_clean() -> None:
    packet = arithmetic_q3_uniqueness_packet()

    assert packet["prime_alpha_hits_up_to_199"] == (3,)
    assert packet["v4_cyclotomic_hits_up_to_199"] == (3,)
    assert packet["phi_of_k_equals_4_hits_up_to_199"] == (3,)


def test_flavor_frontier_audit_keeps_exact_and_promoted_layers_separate() -> None:
    records = {record["name"]: record for record in classify_flavor_frontier()}
    payload = analyze()
    theorem = payload["flavor_frontier_theorem"]

    assert records["exact_q3_arithmetic_uniqueness"]["support_level"] == "repo-exact arithmetic"
    assert records["section84_section86_internal_ckm_conflict"]["support_level"] == "paper-only internal inconsistency"
    assert records["existing_exact_ckm_bridges_are_stronger_than_raw_q_over_phi3"]["support_level"] == "repo-exact bridge dominates paper ansatz"
    assert records["section90_pmns_is_a_nonexact_alternative_ansatz"]["support_level"] == "paper-only phenomenology"
    assert records["section83_running_alpha_is_qualitative_not_precision_closed"]["support_level"] == "paper-only heuristic"

    assert theorem["the_mod_3_alpha_uniqueness_theorem_is_exact"] is True
    assert theorem["sections_84_and_86_do_not_define_the_same_wolfenstein_A"] is True
    assert theorem["the_exact_tangent_and_levi_ckm_routes_beat_raw_q_over_phi3_for_cabibbo"] is True
    assert theorem["section90_pmns_is_not_the_repo_exact_pmns_theorem"] is True
    assert theorem["section83_alpha_running_is_not_a_precision_match_to_current_pdg_data"] is True

    conflict = records["section84_section86_internal_ckm_conflict"]["evidence"]
    assert round(conflict["section84_A"], 6) == 0.877058
    assert round(conflict["section86_A"], 6) == 0.83666

    ckm = records["existing_exact_ckm_bridges_are_stronger_than_raw_q_over_phi3"]["evidence"]
    assert round(ckm["raw_lambda_relative_error"], 6) == round(abs(3 / 13 - 0.22501) / 0.22501, 6)
    assert ckm["exact_tangent_relative_error"] < ckm["raw_lambda_relative_error"]
    assert ckm["levi_lambda_relative_error"] < ckm["raw_lambda_relative_error"]

    pmns = records["section90_pmns_is_a_nonexact_alternative_ansatz"]["evidence"]
    assert pmns["exact_pmns_solar_relative_error"] < pmns["section90_solar_relative_error"]
    assert pmns["exact_pmns_reactor_relative_error"] < pmns["section90_reactor_relative_error"]
    assert pmns["section90_atmospheric_relative_error"] < pmns["exact_pmns_atmospheric_relative_error"]

    running = records["section83_running_alpha_is_qualitative_not_precision_closed"]["evidence"]
    assert round(running["pdg_alpha5_mz_inverse"], 3) == 127.930
    assert running["z_pole_absolute_gap"] > 7.0
