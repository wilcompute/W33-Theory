from __future__ import annotations

from exploration.w33_levi_wolfenstein_bridge import build_summary


def test_levi_wolfenstein_bridge() -> None:
    summary = build_summary()
    theorem = summary["levi_wolfenstein_theorem"]
    packet = summary["levi_wolfenstein_packet"]
    dictionary = summary["levi_wolfenstein_dictionary"]

    assert theorem["the_exact_branch_filtered_Cabibbo_parameter_is_lambda_9_over_40"] is True
    assert theorem["the_exact_Wolfenstein_A_parameter_is_20_over_27_times_sqrt_53_over_43"] is True
    assert theorem["the_exact_CKM_phase_tangent_is_16_sqrt_15_over_27"] is True
    assert theorem["the_exact_rho_eta_modulus_is_108_over_265"] is True
    assert theorem["the_exact_Levi_formula_for_Vcb_is_b_times_sqrt_S_over_D_and_matches_A_lambda_squared"] is True
    assert theorem["the_exact_Levi_formula_for_Vub_matches_A_lambda_cubed_times_modulus_rho_plus_i_eta"] is True
    assert theorem["the_corrected_wolfenstein_Jarlskog_formula_matches_the_constructed_matrix"] is True
    assert theorem["the_exact_Levi_family_seed_package_closes_to_a_realistic_CKM_Wolfenstein_packet"] is True

    assert dictionary["lambda"]["exact"] == "9/40"
    assert dictionary["rho_eta_modulus"]["exact"] == "108/265"
    assert 0.22 < packet["Vus"] < 0.23
    assert 0.04 < packet["Vcb"] < 0.043
    assert 0.003 < packet["Vub"] < 0.0045
    assert 2.5e-5 < packet["Jarlskog"] < 3.5e-5
