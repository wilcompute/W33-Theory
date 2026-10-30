from exploration.w33_balanced_branch_vacuum_bridge import (
    build_balanced_branch_vacuum_summary,
)


def test_balanced_branch_vacuum_summary() -> None:
    summary = build_balanced_branch_vacuum_summary()

    observation = summary["local_v29_stiffness_observation"]
    assert observation["status"] == "ok"
    assert observation["source_file"] == "archive/outputs/V29_output_q_stiffness/summary.json"
    assert observation["diag_cv"] < 0.03
    assert observation["offdiag_rms_ratio"] < 0.01
    assert observation["eig_std_ratio"] < 0.09

    packet = summary["bridge_packet_input"]
    assert packet["rank_one_branch_kills_packet"] is True
    assert packet["rank_two_branch_scales_quartically"] is True
    assert packet["local_a4_only_prefactor"] == "27/(16 pi^2)"

    identity = summary["balanced_rank2_identity"]
    assert identity["radius_formula"] == "r^2 = tr(C^* C) = x + y"
    assert identity["determinant_formula"] == "|det C|^2 = x y"
    assert identity["shape_identity"] == "4 |det C|^2 = r^4 - (x - y)^2"
    assert identity["determinant_bound"] == "|det C|^2 <= r^4 / 4"
    assert identity["equality_condition"] == "iff x = y"
    assert identity["balanced_example_saturates_bound"] is True
    assert identity["unbalanced_example_is_strict"] is True
    assert identity["shape_identity_checks_pass"] is True

    action = summary["reduced_master_action"]
    assert action["potential"] == "V(C) = -mu tr(C^* C) + u tr(C^* C)^2 - v A |det C|^2"
    assert action["shape_decomposition"] == (
        "V = -mu r^2 + (u - A v / 4) r^4 + (A v / 4) (x - y)^2"
    )
    assert action["balanced_stationary_radius"] == "r_*^2 = 2 mu / (4 u - A v)"
    assert action["balanced_vacuum_value"] == "V_* = -mu^2 / (4 u - A v)"
    assert action["sample_radius_sq"] == "1/2"
    assert action["sample_vacuum_value"] == "-3/4"
    assert action["sample_decomposition_matches_direct_potential"] is True

    q_lock = summary["selected_point_q_lock"]
    assert q_lock["Q_curv"] == "52"
    assert q_lock["Q_top"] == "56"
    assert q_lock["c_EH"] == 320
    assert q_lock["a2"] == 2240
    assert q_lock["c6"] == 12480
    assert q_lock["weinberg_lock"] == "3/13"

    theorem = summary["balanced_branch_theorem"]
    assert theorem["quartic_bridge_packet_is_the_first_exact_shape_selector"] is True
    assert theorem["balanced_rank2_branch_uniquely_maximizes_det_packet_at_fixed_radius"] is True
    assert theorem["shape_imbalance_penalty_is_exactly_quadratic_in_x_minus_y"] is True
    assert theorem["nonzero_balanced_stationary_radius_exists_when_mu_positive_and_4u_gt_Av"] is True
    assert theorem["q3_package_fixes_total_curvature_quantum_but_not_yet_global_realization"] is True
    assert theorem["actual_refinement_tower_orientation_and_counting_remain_open"] is True
