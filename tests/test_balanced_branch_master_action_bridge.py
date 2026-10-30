from exploration.w33_balanced_branch_master_action_bridge import (
    build_balanced_branch_master_action_summary,
)


def test_balanced_branch_master_action_summary() -> None:
    summary = build_balanced_branch_master_action_summary()

    validated = summary["validated_v29_input"]
    assert validated["status"] == "ok"
    assert validated["source_file"] == "archive/outputs/V29_output_q_stiffness_validate/summary.json"
    assert validated["diag_rel_std"] < 0.03
    assert validated["offdiag_rel_rms"] < 0.01
    assert validated["finite_difference_pairs"] == 5
    assert validated["finite_difference_rel_err_mean"] < 0.02

    selector = summary["shape_selector"]
    assert selector["total_norm_formula"] == "T = x + y = tr(C^* C)"
    assert selector["selector_formula"] == "chi = 4 |det C|^2 / T^2 = 4 x y / (x + y)^2"
    assert selector["selector_range"] == "0 <= chi <= 1"
    assert selector["rank_one_value"] == "0"
    assert selector["balanced_value"] == "1"
    assert selector["unbalanced_example_value"] == "3/4"
    assert selector["potential_in_T_and_chi"] == "V = -mu T + (u - vA chi / 4) T^2"

    stationary = summary["master_action_stationary_system"]
    assert stationary["potential"] == "V(x, y) = -mu (x + y) + u (x + y)^2 - vA x y"
    assert stationary["balanced_solution"] == "x = y = mu / (4u - vA)"
    assert stationary["exact_sample_t"] == "3/16"
    assert stationary["exact_sample_gradient"] == ["0", "0"]
    assert stationary["exact_sample_stationary_equations_vanish"] is True

    hessian = summary["master_action_hessian_split"]
    assert hessian["hessian_formula"] == "H = [[2u, 2u - vA], [2u - vA, 2u]]"
    assert hessian["radial_vector"] == "(1, 1)"
    assert hessian["shape_vector"] == "(1, -1)"
    assert hessian["radial_eigenvalue"] == "4u - vA"
    assert hessian["shape_eigenvalue"] == "vA"
    assert hessian["exact_sample_radial_eigenpair"] is True
    assert hessian["exact_sample_shape_eigenpair"] is True
    assert hessian["exact_sample_radial_value"] == "16"
    assert hessian["exact_sample_shape_value"] == "4"

    observational = summary["observational_balanced_sample"]
    assert observational["u"] == 1.0
    assert observational["vA"] == 1.0
    assert observational["locally_stable"] is True
    assert observational["hessian_eigenvalues"] == [1.0, 3.0]

    q_lock = summary["selected_point_q_lock"]
    assert q_lock["Q_curv"] == "52"
    assert q_lock["Q_top"] == "56"
    assert q_lock["c_EH"] == 320
    assert q_lock["a2"] == 2240
    assert q_lock["c6"] == 12480
    assert q_lock["weinberg_lock"] == "3/13"

    theorem = summary["master_action_theorem"]
    assert theorem["normalized_selector_distinguishes_rank1_from_balanced_rank2"] is True
    assert theorem["nonzero_stationary_point_is_forced_to_be_balanced"] is True
    assert theorem["shape_stability_is_exactly_vA"] is True
    assert theorem["radial_stability_is_exactly_4u_minus_vA"] is True
    assert theorem["local_nonzero_vacuum_is_stable_when_vA_positive_and_4u_minus_vA_positive"] is True
    assert theorem["validated_v29_input_supports_shape_blind_quadratic_observation"] is True
    assert theorem["global_refinement_tower_realization_and_orientation_remain_open"] is True
