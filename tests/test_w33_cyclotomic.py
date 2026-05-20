import cmath
import math

from w33.cyclotomic import (
    cyclotomic_prime_support,
    cyclotomic_prime_support_scan,
    cyclotomic_known_perfect_power_solutions,
    cyclotomic_ljunggren_reduction,
    cyclotomic_perfect_power_theorem,
    branch_classes_for_split_prime,
    completed_cumulant_constant,
    completed_defect_adelic_centered_reciprocity,
    completed_defect_adelic_log_artanh,
    completed_defect_adelic_product,
    completed_global_centered_reciprocity,
    completed_higher_cumulant_profile,
    completed_local_centered_reciprocity,
    completed_defect_dirichlet_local_factor,
    completed_defect_dirichlet_log_artanh,
    completed_defect_dirichlet_log_artanh_profile,
    completed_defect_dirichlet_log_artanh_series,
    completed_defect_dirichlet_reciprocity_profile,
    completed_defect_dirichlet_log_derivative,
    completed_defect_dirichlet_product,
    completed_defect_dirichlet_profile,
    completed_defect_local_centered_reciprocity_from_z,
    completed_defect_local_centered_reciprocity_in_s,
    completed_defect_local_factor_from_z,
    completed_defect_local_log_artanh_form,
    completed_defect_local_log_artanh_series,
    completed_defect_counterterm_local,
    completed_local_log_derivative_at_one,
    completed_local_log_nth_derivative_at_one,
    completed_log_nth_derivative_at_one,
    completed_defect_spectral_coordinate,
    completed_defect_spectral_local_factor,
    completed_defect_spectral_local_log,
    completed_defect_spectral_local_log_odd_coefficient,
    completed_defect_spectral_local_log_series,
    completed_defect_spectral_local_radius,
    completed_defect_spectral_local_linear_kernel,
    completed_defect_spectral_local_log_lambda_derivative,
    completed_defect_spectral_local_log_odd_coefficient_bound,
    completed_defect_spectral_L_function,
    completed_defect_spectral_log_odd_coefficient,
    completed_defect_spectral_log,
    completed_defect_spectral_log_compact_tail_bound,
    completed_defect_spectral_log_lambda_derivative,
    completed_defect_spectral_log_odd_tail_bound,
    completed_defect_spectral_log_series,
    completed_defect_spectral_global_limit_profile,
    completed_defect_spectral_hessian_tail_bound,
    completed_defect_spectral_profile,
    completed_defect_spectral_phase_geometry_profile,
    completed_defect_spectral_legendre_dual,
    completed_defect_spectral_equation_of_state_inverse,
    completed_defect_spectral_equation_of_state_profile,
    completed_defect_spectral_infinite_equation_of_state_interval,
    completed_defect_spectral_infinite_dual_branch_profile,
    completed_defect_spectral_dual_stiffness,
    completed_defect_spectral_infinite_dual_stiffness_interval,
    completed_defect_spectral_infinite_dual_stiffness_profile,
    completed_defect_spectral_real_packet,
    completed_defect_spectral_uniform_wall_packet,
    completed_defect_spectral_uniform_wall_profile,
    completed_defect_spectral_wall_effective_packet,
    completed_defect_spectral_wall_effective_profile,
    completed_defect_spectral_infinite_wall_packet,
    completed_defect_spectral_infinite_wall_profile,
    completed_defect_spectral_infinite_compact_real_packet,
    completed_defect_spectral_infinite_boundary_corridor_packet,
    completed_defect_spectral_infinite_boundary_corridor_profile,
    completed_defect_spectral_infinite_boundary_average_packet,
    completed_defect_spectral_infinite_boundary_average_profile,
    completed_defect_spectral_third_derivative_real_global,
    completed_defect_spectral_boundary_mean_witness_packet,
    completed_defect_spectral_boundary_mean_witness_profile,
    completed_defect_spectral_boundary_barycentric_witness_packet,
    completed_defect_spectral_boundary_barycentric_witness_profile,
    completed_defect_spectral_boundary_barycentric_stability_packet,
    completed_defect_spectral_boundary_barycentric_wallward_flow_packet,
    completed_defect_spectral_boundary_barycentric_dispersion_turning_packet,
    completed_defect_spectral_boundary_barycentric_recurrence_resonance_packet,
    completed_defect_spectral_boundary_barycentric_recurrence_phase_packet,
    completed_defect_spectral_boundary_barycentric_gap_handoff_packet,
    completed_defect_spectral_boundary_barycentric_gap_handoff_cutoff_profile,
    completed_defect_spectral_boundary_barycentric_gap_handoff_convergence_signature,
    completed_defect_spectral_dual_softening_density,
    completed_defect_spectral_boundary_transfer_packet,
    completed_defect_spectral_relative_error_bound,
    completed_defect_spectral_reciprocity,
    completed_defect_spectral_real_local_coordinates,
    completed_defect_spectral_local_hessian_real,
    completed_defect_spectral_local_order_parameter_real,
    completed_defect_spectral_infinite_cutoff_profile,
    completed_defect_spectral_order_parameter_tail_bound,
    completed_defect_spectral_order_parameter_real_global,
    completed_defect_spectral_hessian_real_global,
    completed_defect_spectral_series_profile,
    completed_defect_spectral_min_radius,
    completed_defect_spectral_uniform_radius_lower_bound,
    completed_defect_spectral_action,
    completed_defect_spectral_order_parameter,
    completed_defect_spectral_hessian,
    completed_defect_spectral_free_energy_profile,
    completed_defect_spectral_deformation_cumulant_profile,
    completed_reciprocity_profile,
    completed_tangent_profile,
    cyclotomic_perfect_power_scan,
    defect_density_partial_product,
    defect_spectral_involution,
    defect_dirichlet_local_factor,
    defect_dirichlet_product,
    defect_residue_classifier,
    defect_match_for_q,
    eisenstein_local_global_valuation_packet,
    eisenstein_ideal_witness,
    exact_branch_congruence_valuation,
    eisenstein_split_ideal_data,
    eisenstein_norm,
    empirical_defect_density,
    finite_adelic_expected_valuation,
    finite_adelic_valuation_euler_factor,
    finite_adelic_valuation_pgf,
    finite_adelic_variance_valuation,
    finite_cutoff_avoidance_density,
    finite_cutoff_branch_classes,
    finite_cutoff_defect_density,
    local_expected_valuation,
    local_valuation_euler_factor,
    local_valuation_pgf,
    local_divisibility_density,
    local_exact_valuation_density,
    local_variance_valuation,
    nontrivial_cube_roots_mod_prime_square,
    phi3_as_eisenstein_norm,
    phi3_roots_mod_prime_power,
    phi3_roots_mod_prime_square,
    phi6_as_eisenstein_norm,
    phi6_roots_mod_prime_power,
    phi6_roots_mod_prime_square,
    primitive_root_mod_prime_square,
    split_prime_packet_mean,
    split_prime_completed_local_factor,
    split_prime_completed_pgf,
    split_prime_completed_pgf_profile,
    split_prime_mertens_normalized,
    split_prime_mertens_product,
    split_prime_packet_pgf,
    split_prime_packet_pgf_profile,
    split_prime_packet_profile,
    valuation_tree,
)


def test_first_split_prime_residue_classes():
    assert phi3_roots_mod_prime_square(7) == [18, 30]
    assert phi6_roots_mod_prime_square(7) == [19, 31]
    assert phi3_roots_mod_prime_square(13) == [22, 146]
    assert phi6_roots_mod_prime_square(13) == [23, 147]
    assert phi3_roots_mod_prime_square(19) == [68, 292]
    assert phi6_roots_mod_prime_square(19) == [69, 293]


def test_order_three_units_match_phi3_roots():
    for p in [7, 13, 19, 31]:
        mod = p * p
        roots = nontrivial_cube_roots_mod_prime_square(p)
        assert roots == phi3_roots_mod_prime_square(p)
        assert roots == sorted({primitive_root_mod_prime_square(p) ** (p * (p - 1) // 3) % mod, primitive_root_mod_prime_square(p) ** (2 * p * (p - 1) // 3) % mod})
        for r in roots:
            assert pow(r, 3, mod) == 1
            assert r % mod != 1
            assert (r * r + r + 1) % mod == 0


def test_eisenstein_norm_factorization():
    assert eisenstein_norm(3, -1) == 13
    assert eisenstein_norm(3, 1) == 7
    for q in [3, 4, 7, 18, 19]:
        assert phi3_as_eisenstein_norm(q) == q * q + q + 1
        assert phi6_as_eisenstein_norm(q) == q * q - q + 1


def test_prime_power_root_lifts_and_negation_symmetry():
    assert phi3_roots_mod_prime_power(7, 1) == [2, 4]
    assert phi3_roots_mod_prime_power(7, 2) == [18, 30]
    assert phi6_roots_mod_prime_power(7, 1) == [3, 5]
    assert phi6_roots_mod_prime_power(7, 2) == [19, 31]
    for power in [1, 2, 3, 4]:
        mod = 7**power
        assert phi6_roots_mod_prime_power(7, power) == sorted({(-r) % mod for r in phi3_roots_mod_prime_power(7, power)})


def test_local_density_law_and_tree_payload():
    tree = valuation_tree(7, max_power=4)
    assert tree["phi3_roots"]["2"] == [18, 30]
    assert tree["phi6_roots"]["2"] == [19, 31]
    assert local_divisibility_density(7, 2) == 2 / 49
    assert local_exact_valuation_density(7, 2) == (2 / 49) - (2 / 343)


def test_local_pgf_euler_factor_and_moments():
    assert local_valuation_pgf(7, 0.0) == 5 / 7
    assert local_valuation_pgf(7, 1.0) == 1.0
    assert local_valuation_euler_factor(7, 1.0) == local_valuation_pgf(7, 1 / 7)
    assert local_expected_valuation(7) == 1 / 3
    assert local_expected_valuation(13) == 1 / 6
    assert local_expected_valuation(19) == 1 / 9
    assert local_variance_valuation(7) == local_expected_valuation(7)
    assert local_variance_valuation(13) == local_expected_valuation(13)


def test_finite_cutoff_crt_branch_factorization():
    assert branch_classes_for_split_prime(7, family="Phi3", power=2) == [18, 30]
    packet = finite_cutoff_branch_classes([7, 13], family="Phi3", power=2)
    assert packet["class_count"] == 4
    assert packet["expected_class_count"] == 4
    assert packet["modulus"] == 49 * 169
    assert packet["classes"] == [2174, 3019, 5261, 6106]
    assert math.isclose(packet["density"], 4 / (49 * 169), rel_tol=0.0, abs_tol=1e-18)
    assert math.isclose(finite_cutoff_defect_density([7, 13], power=2), 4 / (49 * 169), rel_tol=0.0, abs_tol=1e-18)
    assert math.isclose(finite_cutoff_avoidance_density([7, 13], power=2), (1 - 2 / 49) * (1 - 2 / 169), rel_tol=0.0, abs_tol=1e-18)


def test_finite_adelic_pgf_and_moments():
    assert finite_adelic_valuation_pgf([7, 13], 1.0) == 1.0
    assert math.isclose(
        finite_adelic_valuation_pgf([7, 13], 0.0),
        local_valuation_pgf(7, 0.0) * local_valuation_pgf(13, 0.0),
        rel_tol=0.0,
        abs_tol=1e-18,
    )


def test_cyclotomic_split_prime_support_law():
    phi3 = cyclotomic_prime_support(4, "Phi3")
    phi6 = cyclotomic_prime_support(5, "Phi6")
    assert phi3["exact_support"]
    assert phi6["exact_support"]
    assert phi3["support_primes"] == [3, 7]
    assert phi6["support_primes"] == [3, 7]
    scan = cyclotomic_prime_support_scan(limit_q=1000)
    assert scan["phi3_exact_support"]
    assert scan["phi6_exact_support"]
    assert scan["phi3_bad_examples"] == []
    assert scan["phi6_bad_examples"] == []
    assert 7 in scan["phi3_support_primes"] and 13 in scan["phi3_support_primes"]
    assert 7 in scan["phi6_support_primes"] and 13 in scan["phi6_support_primes"]


def test_split_prime_packet_growth_profile():
    assert split_prime_packet_mean(19).numerator == 11
    assert split_prime_packet_mean(19).denominator == 18
    assert split_prime_packet_mean(31).numerator == 61
    assert split_prime_packet_mean(31).denominator == 90
    profile = split_prime_packet_profile([19, 31, 1000])
    assert profile[0]["mean_fraction"] == "11/18"
    assert profile[1]["mean_fraction"] == "61/90"
    assert profile[2]["mean"] > profile[1]["mean"] > profile[0]["mean"]


def test_split_prime_packet_pgf_decay_profile():
    assert math.isclose(split_prime_packet_pgf(19, 0.0), finite_adelic_valuation_pgf([7, 13, 19], 0.0), rel_tol=0.0, abs_tol=1e-18)
    assert split_prime_packet_pgf(31, 1.0) == 1.0
    profile = split_prime_packet_pgf_profile([1000, 10000], [0.0, 0.5])
    assert profile["0.0"][1]["pgf"] < profile["0.0"][0]["pgf"]
    assert profile["0.5"][1]["pgf"] < profile["0.5"][0]["pgf"]
    assert profile["0.0"][0]["normalized_pgf"] > 0.0
    assert profile["0.5"][0]["normalized_pgf"] > 0.0


def test_completed_split_prime_euler_product_factorization():
    t = 0.5
    expected = 1.0
    for p in [7, 13, 19]:
        expected *= split_prime_completed_local_factor(p, t)
    assert math.isclose(split_prime_completed_pgf(19, t), expected, rel_tol=0.0, abs_tol=1e-18)
    mertens = split_prime_mertens_product(19)
    pgf = split_prime_packet_pgf(19, t)
    assert math.isclose(split_prime_completed_pgf(19, t), pgf * (mertens ** (-2 * (1 - t))), rel_tol=0.0, abs_tol=1e-15)
    assert split_prime_mertens_normalized(10000) > 0.0
    packet_profile = split_prime_packet_pgf_profile([1000, 10000], [0.0, 0.5])
    completed_profile = split_prime_completed_pgf_profile([1000, 10000], [0.0, 0.5])
    for key in ["0.0", "0.5"]:
        for packet_row, completed_row in zip(packet_profile[key], completed_profile[key], strict=True):
            assert math.isclose(packet_row["normalized_pgf"], completed_row["shadow_recovered"], rel_tol=0.0, abs_tol=1e-12)
    assert finite_adelic_expected_valuation([7, 13, 19]).numerator == 11
    assert finite_adelic_expected_valuation([7, 13, 19]).denominator == 18
    assert finite_adelic_variance_valuation([7, 13, 19]) == finite_adelic_expected_valuation([7, 13, 19])
    assert math.isclose(
        finite_adelic_valuation_euler_factor([7, 13], 1.0),
        local_valuation_euler_factor(7, 1.0) * local_valuation_euler_factor(13, 1.0),
        rel_tol=0.0,
        abs_tol=1e-18,
    )


def test_completed_tangent_constant_profile():
    local = completed_local_log_derivative_at_one(7)
    assert math.isclose(local, 2 / 6 + 2 * math.log(6 / 7), rel_tol=0.0, abs_tol=1e-15)
    profile = completed_tangent_profile([19, 31])
    assert math.isclose(profile[0]["completed_tangent_constant"], profile[0]["recombined"], rel_tol=0.0, abs_tol=1e-15)
    assert math.isclose(profile[1]["completed_tangent_constant"], profile[1]["recombined"], rel_tol=0.0, abs_tol=1e-15)
    assert profile[1]["completed_tangent_constant"] > profile[0]["completed_tangent_constant"] > 0.0
    assert math.isclose(completed_cumulant_constant(19), profile[0]["completed_tangent_constant"], rel_tol=0.0, abs_tol=1e-18)


def test_completed_reciprocity_and_hessian_tower():
    for p in [7, 13, 19]:
        assert math.isclose(completed_local_centered_reciprocity(p, 0.2), 1.0, rel_tol=0.0, abs_tol=1e-15)
        assert math.isclose(completed_local_log_nth_derivative_at_one(p, 2), 0.0, rel_tol=0.0, abs_tol=1e-18)
        assert math.isclose(completed_local_log_nth_derivative_at_one(p, 4), 0.0, rel_tol=0.0, abs_tol=1e-18)
    assert math.isclose(completed_local_log_nth_derivative_at_one(7, 3), 4 / (6**3), rel_tol=0.0, abs_tol=1e-18)
    assert math.isclose(completed_local_log_nth_derivative_at_one(7, 5), 48 / (6**5), rel_tol=0.0, abs_tol=1e-18)
    assert math.isclose(completed_global_centered_reciprocity(1000, 0.25), 1.0, rel_tol=0.0, abs_tol=1e-12)
    assert math.isclose(completed_log_nth_derivative_at_one(31, 2), 0.0, rel_tol=0.0, abs_tol=1e-18)
    assert math.isclose(
        completed_log_nth_derivative_at_one(19, 3),
        4 * ((1 / 6**3) + (1 / 12**3) + (1 / 18**3)),
        rel_tol=0.0,
        abs_tol=1e-18,
    )
    profile = completed_higher_cumulant_profile([19, 31], [1, 2, 3, 5])
    assert math.isclose(profile["2"][0]["log_derivative_at_one"], 0.0, rel_tol=0.0, abs_tol=1e-18)
    assert profile["3"][1]["log_derivative_at_one"] > profile["3"][0]["log_derivative_at_one"] > 0.0
    reciprocity = completed_reciprocity_profile([31, 1000], [0.2, 0.25])
    assert reciprocity["0.2"][0]["abs_error_from_one"] < 1e-12
    assert reciprocity["0.25"][1]["abs_error_from_one"] < 1e-12


def test_completed_dirichlet_package():
    assert math.isclose(defect_dirichlet_local_factor(7, 1.0).real, local_valuation_euler_factor(7, 1.0), rel_tol=0.0, abs_tol=1e-18)
    assert math.isclose(defect_dirichlet_product(13, 1.0).real, finite_adelic_valuation_euler_factor([7, 13], 1.0), rel_tol=0.0, abs_tol=1e-15)
    completed = completed_defect_dirichlet_product(31, 1.0)
    assert completed.imag == 0.0
    assert completed.real > 0.0
    profile = completed_defect_dirichlet_profile([31, 1000], [0.5, 1.0])
    assert profile["1.0"][1]["completed_real"] > 0.0
    assert profile["0.5"][1]["completed_real"] > 0.0
    assert completed_defect_dirichlet_log_derivative(31, 1.0).imag == 0.0
    assert completed_defect_dirichlet_local_factor(7, 1.0).real > defect_dirichlet_local_factor(7, 1.0).real


def test_completed_dirichlet_reciprocity_and_artanh_package():
    s = 0.5
    z7 = 7 ** (-s)
    z13 = 13 ** (-s)
    assert abs(completed_defect_local_factor_from_z(7, z7) - completed_defect_dirichlet_local_factor(7, s)) < 1e-15
    assert abs(completed_defect_local_centered_reciprocity_from_z(7, z7) - 1.0) < 1e-15
    assert abs(completed_defect_local_centered_reciprocity_in_s(7, s) - 1.0) < 1e-15
    s_star = defect_spectral_involution(7, s)
    assert abs(completed_defect_dirichlet_local_factor(7, s) * completed_defect_dirichlet_local_factor(7, s_star) - 1.0) < 1e-15
    adelic = {7: z7, 13: z13}
    assert abs(completed_defect_adelic_centered_reciprocity(adelic) - 1.0) < 1e-15
    exact_local_log = completed_defect_local_log_artanh_form(7, z7)
    exact_local_factor = completed_defect_local_factor_from_z(7, z7)
    assert abs(cmath.exp(exact_local_log) - exact_local_factor) < 1e-12
    assert abs(completed_defect_local_log_artanh_series(7, z7, max_terms=8) - exact_local_log) < 1e-10
    exact_global_log = completed_defect_dirichlet_log_artanh(31, s)
    series_global_log = completed_defect_dirichlet_log_artanh_series(31, s, max_terms=8)
    assert abs(cmath.exp(exact_global_log) - completed_defect_dirichlet_product(31, s)) < 1e-10
    assert abs(series_global_log - exact_global_log) < 1e-8
    assert abs(cmath.exp(completed_defect_adelic_log_artanh(adelic)) - completed_defect_adelic_product(adelic)) < 1e-12
    profile = completed_defect_dirichlet_log_artanh_profile([31, 1000], [0.5, 1.0], max_terms=8)
    assert profile["0.5"][1]["abs_series_error"] < 1e-7
    reciprocity_profile = completed_defect_dirichlet_reciprocity_profile([31, 1000], [0.5, 1.0])
    assert reciprocity_profile["0.5"][1]["max_abs_local_error_from_one"] < 1e-12


def test_completed_defect_spectral_l_family_package():
    s = 0.5
    x7 = completed_defect_spectral_coordinate(7, s)
    assert abs(x7 - ((7 ** (-s) - 1) / 6)) < 1e-15
    assert abs(completed_defect_spectral_local_factor(7, s, deformation=0.0) - 1.0) < 1e-15
    assert abs(completed_defect_spectral_L_function(31, s, deformation=0.0) - 1.0) < 1e-15
    assert abs(completed_defect_spectral_local_factor(7, s, deformation=1.0) - completed_defect_dirichlet_local_factor(7, s)) < 1e-15
    assert abs(completed_defect_spectral_L_function(31, s, deformation=1.0) - completed_defect_dirichlet_product(31, s)) < 1e-15
    assert abs(completed_defect_counterterm_local(7, s, deformation=1.0) * defect_dirichlet_local_factor(7, s) - completed_defect_dirichlet_local_factor(7, s)) < 1e-15
    local_log = completed_defect_spectral_local_log(7, s, deformation=0.5)
    local_val = completed_defect_spectral_local_factor(7, s, deformation=0.5)
    assert abs(cmath.exp(local_log) - local_val) < 1e-12
    global_log = completed_defect_spectral_log(31, s, deformation=0.5)
    global_val = completed_defect_spectral_L_function(31, s, deformation=0.5)
    assert abs(cmath.exp(global_log) - global_val) < 1e-10
    assert abs(completed_defect_spectral_reciprocity(31, s, deformation=0.5) - 1.0) < 1e-12
    profile = completed_defect_spectral_profile([31, 1000], [0.5, 1.0], [0.25, 0.5, 1.0])
    assert profile["0.5"]["0.5"][1]["abs_reciprocity_error"] < 1e-10
    assert profile["0.5"]["1.0"][0]["value_real"] > 0.0


def test_completed_defect_spectral_odd_taylor_tower_and_radius():
    s = 1.0
    x7 = completed_defect_spectral_coordinate(7, s)
    assert abs(x7 + (1 / 7)) < 1e-15
    assert abs(completed_defect_spectral_local_radius(7, s) - 7.0) < 1e-15
    assert abs(completed_defect_spectral_min_radius(31, s) - 7.0) < 1e-15
    assert completed_defect_spectral_uniform_radius_lower_bound() == 6.0

    coeff1_local = completed_defect_spectral_local_log_odd_coefficient(7, s, 1)
    coeff3_local = completed_defect_spectral_local_log_odd_coefficient(7, s, 3)
    coeff2_local = completed_defect_spectral_local_log_odd_coefficient(7, s, 2)
    assert abs(coeff2_local) < 1e-18
    assert abs(coeff1_local - (2 * x7 + 2 * ((7 ** (-s)) - 1) * math.log(6 / 7))) < 1e-15
    assert abs(coeff3_local - (2 * (x7**3) / 3)) < 1e-18

    coeff2_global = completed_defect_spectral_log_odd_coefficient(31, s, 2)
    assert abs(coeff2_global) < 1e-18

    exact_local_log = completed_defect_spectral_local_log(7, s, deformation=1.0)
    series_local_log = completed_defect_spectral_local_log_series(7, s, deformation=1.0, max_order=9)
    assert abs(series_local_log - exact_local_log) < 1e-10

    exact_global_log = completed_defect_spectral_log(1000, s, deformation=1.0)
    series_global_log = completed_defect_spectral_log_series(1000, s, deformation=1.0, max_order=9)
    assert abs(series_global_log - exact_global_log) < 1e-7

    profile = completed_defect_spectral_series_profile([31, 1000], [1.0], [0.5], [1, 3, 5, 7, 9])
    row = profile["1.0"]["0.5"][1]
    assert row["uniform_radius_lower_bound"] == 6.0
    assert row["min_local_radius"] >= 6.0
    assert row["approximants"]["9"]["abs_series_error"] < row["approximants"]["5"]["abs_series_error"]
    assert row["approximants"]["5"]["abs_series_error"] < row["approximants"]["3"]["abs_series_error"]


def test_completed_defect_spectral_infinite_cutoff_and_tail_bounds():
    s = 1.0
    kernel7 = completed_defect_spectral_local_linear_kernel(7, s)
    coeff1_7 = completed_defect_spectral_local_log_odd_coefficient(7, s, 1)
    assert abs(coeff1_7 - 2 * kernel7) < 1e-15
    assert completed_defect_spectral_local_log_odd_coefficient_bound(7, s, 2) == 0.0
    assert completed_defect_spectral_log_odd_tail_bound(1000, 1) > 0.0
    assert completed_defect_spectral_log_odd_tail_bound(1000, 3) < completed_defect_spectral_log_odd_tail_bound(100, 3)
    profile = completed_defect_spectral_infinite_cutoff_profile([1000, 10000, 100000], [1.0], [1, 3, 5])
    row1 = profile["1.0"]["1"]
    row3 = profile["1.0"]["3"]
    assert row1[-1]["tail_bound"] < row1[0]["tail_bound"]
    assert row3[-1]["tail_bound"] < row3[0]["tail_bound"]
    assert row1[-1]["abs_jump_from_previous"] is not None


def test_completed_defect_spectral_deformation_derivatives_and_free_energy():
    s = 1.0
    coeff1_local = completed_defect_spectral_local_log_odd_coefficient(7, s, 1)
    coeff3_local = completed_defect_spectral_local_log_odd_coefficient(7, s, 3)
    deriv1_zero = completed_defect_spectral_local_log_lambda_derivative(7, s, 1, deformation=0.0)
    deriv2_zero = completed_defect_spectral_local_log_lambda_derivative(7, s, 2, deformation=0.0)
    deriv3_zero = completed_defect_spectral_local_log_lambda_derivative(7, s, 3, deformation=0.0)
    assert abs(deriv1_zero - coeff1_local) < 1e-15
    assert abs(deriv2_zero) < 1e-18
    assert abs(deriv3_zero - (math.factorial(3) * coeff3_local)) < 1e-15

    global_deriv2_zero = completed_defect_spectral_log_lambda_derivative(31, s, 2, deformation=0.0)
    assert abs(global_deriv2_zero) < 1e-18

    h = 1e-6
    exact_local_deriv1_one = completed_defect_spectral_local_log_lambda_derivative(7, s, 1, deformation=1.0)
    fd_local_deriv1_one = (
        completed_defect_spectral_local_log(7, s, deformation=1.0 + h)
        - completed_defect_spectral_local_log(7, s, deformation=1.0 - h)
    ) / (2 * h)
    assert abs(exact_local_deriv1_one - fd_local_deriv1_one) < 1e-8

    action0 = completed_defect_spectral_action(31, s, deformation=0.0)
    hessian0 = completed_defect_spectral_hessian(31, s, deformation=0.0)
    order1 = completed_defect_spectral_order_parameter(31, s, deformation=1.0)
    assert abs(action0) < 1e-18
    assert abs(hessian0) < 1e-18
    assert order1.real != 0.0

    cumulants = completed_defect_spectral_deformation_cumulant_profile([31, 1000], [1.0], [0.0, 1.0], [1, 2, 3])
    assert abs(cumulants["1.0"]["0.0"][0]["order_2_real"]) < 1e-18
    free_energy = completed_defect_spectral_free_energy_profile([31, 1000], [1.0], [0.0, 1.0])
    assert abs(free_energy["1.0"]["0.0"][0]["action_real"]) < 1e-18
    assert abs(free_energy["1.0"]["0.0"][0]["hessian_real"]) < 1e-18


def test_completed_defect_spectral_standalone_global_limit_package():
    s = 1.0
    tail_1000 = completed_defect_spectral_log_compact_tail_bound(1000, 1.0)
    tail_100000 = completed_defect_spectral_log_compact_tail_bound(100000, 1.0)
    assert tail_100000 < tail_1000
    assert completed_defect_spectral_relative_error_bound(100000, 1.0) < completed_defect_spectral_relative_error_bound(1000, 1.0)

    profile = completed_defect_spectral_global_limit_profile([1000, 10000, 100000], [1.0], [1.0, 2.0])
    row_phys = profile["1.0"]["1.0"]
    row_deformed = profile["1.0"]["2.0"]
    assert row_phys[-1]["log_tail_bound"] < row_phys[0]["log_tail_bound"]
    assert row_phys[-1]["relative_value_error_bound"] < row_phys[0]["relative_value_error_bound"]
    assert row_phys[-1]["abs_jump_from_previous_log"] is not None
    assert row_phys[-1]["uniform_radius_lower_bound"] == 6.0
    assert row_deformed[-1]["relative_value_error_bound"] > row_phys[-1]["relative_value_error_bound"]
    assert row_phys[-1]["abs_reciprocity_error"] < 1e-12

    finite_value = completed_defect_spectral_L_function(100000, s, deformation=1.0)
    finite_log = completed_defect_spectral_log(100000, s, deformation=1.0)
    assert abs(cmath.exp(finite_log) - finite_value) < 1e-10


def test_completed_defect_spectral_phase_geometry_package():
    s = 1.0
    coords = completed_defect_spectral_real_local_coordinates(7, s)
    assert coords["a"] == 1 / 7
    assert coords["kernel"] > 0.0

    local_order_0 = completed_defect_spectral_local_order_parameter_real(7, s, deformation=0.0)
    local_order_1 = completed_defect_spectral_local_order_parameter_real(7, s, deformation=1.0)
    local_hessian_0 = completed_defect_spectral_local_hessian_real(7, s, deformation=0.0)
    local_hessian_1 = completed_defect_spectral_local_hessian_real(7, s, deformation=1.0)
    assert local_order_1 > local_order_0 > 0.0
    assert abs(local_hessian_0) < 1e-18
    assert local_hessian_1 > 0.0

    assert completed_defect_spectral_order_parameter_tail_bound(100000, 1.0) < completed_defect_spectral_order_parameter_tail_bound(1000, 1.0)
    assert completed_defect_spectral_hessian_tail_bound(100000, 1.0) < completed_defect_spectral_hessian_tail_bound(1000, 1.0)

    profile = completed_defect_spectral_phase_geometry_profile([1000, 10000, 100000], [1.0], [0.0, 1.0, 2.0])
    zero_rows = profile["1.0"]["0.0"]
    one_rows = profile["1.0"]["1.0"]
    two_rows = profile["1.0"]["2.0"]

    assert abs(zero_rows[-1]["hessian_real"]) < 1e-18
    assert zero_rows[-1]["order_positive"]
    assert one_rows[-1]["order_positive"] and one_rows[-1]["hessian_positive"]
    assert two_rows[-1]["order_positive"] and two_rows[-1]["hessian_positive"]
    assert one_rows[-1]["order_tail_bound"] < one_rows[0]["order_tail_bound"]
    assert one_rows[-1]["hessian_tail_bound"] < one_rows[0]["hessian_tail_bound"]
    assert one_rows[-1]["order_jump_from_previous"] is not None and one_rows[-1]["order_jump_from_previous"] > 0.0
    assert one_rows[-1]["hessian_jump_from_previous"] is not None and one_rows[-1]["hessian_jump_from_previous"] > 0.0


def test_completed_defect_spectral_equation_of_state_and_legendre_duality():
    s = 1.0
    prime_limit = 100000
    m0 = completed_defect_spectral_order_parameter_real_global(prime_limit, s, 0.0)
    m1 = completed_defect_spectral_order_parameter_real_global(prime_limit, s, 1.0)
    m2 = completed_defect_spectral_order_parameter_real_global(prime_limit, s, 2.0)
    assert m2 > m1 > m0 > 0.0
    assert completed_defect_spectral_hessian_real_global(prime_limit, s, 1.0) > 0.0

    recovered_1 = completed_defect_spectral_equation_of_state_inverse(prime_limit, s, m1)
    recovered_2 = completed_defect_spectral_equation_of_state_inverse(prime_limit, s, m2)
    assert abs(recovered_1 - 1.0) < 1e-10
    assert abs(recovered_2 - 2.0) < 1e-10

    dual_1 = completed_defect_spectral_legendre_dual(prime_limit, s, m1)
    dual_2 = completed_defect_spectral_legendre_dual(prime_limit, s, m2)
    assert abs(dual_1["deformation"] - 1.0) < 1e-10
    assert abs(dual_2["deformation"] - 2.0) < 1e-10
    assert dual_2["dual"] > dual_1["dual"]
    assert dual_1["hessian"] > 0.0 and dual_2["hessian"] > 0.0

    profile = completed_defect_spectral_equation_of_state_profile([1000, 10000, 100000], [1.0], [1.0, 2.0])
    one_rows = profile["1.0"]["1.0"]
    two_rows = profile["1.0"]["2.0"]
    assert one_rows[-1]["abs_inverse_error"] < 1e-10
    assert two_rows[-1]["abs_inverse_error"] < 1e-10
    assert two_rows[-1]["target_order_parameter"] > one_rows[-1]["target_order_parameter"]


def test_completed_defect_spectral_infinite_dual_branch_limit_package():
    s = 1.0
    target_order = completed_defect_spectral_order_parameter_real_global(1000, s, 1.0)
    interval_1k = completed_defect_spectral_infinite_equation_of_state_interval(1000, s, target_order)
    interval_10k = completed_defect_spectral_infinite_equation_of_state_interval(10000, s, target_order)
    interval_100k = completed_defect_spectral_infinite_equation_of_state_interval(100000, s, target_order)
    assert abs(interval_1k["upper_lambda"] - 1.0) < 1e-10
    assert interval_100k["interval_width"] < interval_10k["interval_width"] < interval_1k["interval_width"]

    recovered_10k = completed_defect_spectral_equation_of_state_inverse(10000, s, target_order)
    recovered_100k = completed_defect_spectral_equation_of_state_inverse(100000, s, target_order)
    assert 0.0 <= interval_10k["lower_lambda"] <= recovered_10k <= interval_10k["upper_lambda"] <= 1.0
    assert 0.0 <= interval_100k["lower_lambda"] <= recovered_100k <= interval_100k["upper_lambda"] <= recovered_10k

    profile = completed_defect_spectral_infinite_dual_branch_profile(1000, [1000, 10000, 100000], [1.0], [1.0, 2.0])
    one_rows = profile["1.0"]["1.0"]["rows"]
    two_rows = profile["1.0"]["2.0"]["rows"]
    assert abs(one_rows[0]["recovered_lambda"] - 1.0) < 1e-10
    assert abs(two_rows[0]["recovered_lambda"] - 2.0) < 1e-10
    assert one_rows[2]["recovered_lambda"] < one_rows[1]["recovered_lambda"] < one_rows[0]["recovered_lambda"]
    assert two_rows[2]["recovered_lambda"] < two_rows[1]["recovered_lambda"] < two_rows[0]["recovered_lambda"]
    assert one_rows[2]["interval_width"] < one_rows[1]["interval_width"] < one_rows[0]["interval_width"]


def test_completed_defect_spectral_dual_stiffness_package():
    s = 1.0
    prime_limit = 100000
    target_order = completed_defect_spectral_order_parameter_real_global(prime_limit, s, 1.0)

    packet = completed_defect_spectral_dual_stiffness(prime_limit, s, target_order, deformation_max=1.1)
    assert abs(packet["deformation"] - 1.0) < 1e-10
    assert packet["hessian"] > 0.0
    assert packet["stiffness"] > 0.0
    assert math.isclose(packet["stiffness"] * packet["hessian"], 1.0, rel_tol=0.0, abs_tol=1e-12)

    h = 1e-6
    dual_plus = completed_defect_spectral_legendre_dual(prime_limit, s, target_order + h, deformation_max=1.1)
    dual_minus = completed_defect_spectral_legendre_dual(prime_limit, s, target_order - h, deformation_max=1.1)
    fd_dual_prime = (dual_plus["dual"] - dual_minus["dual"]) / (2 * h)
    fd_inverse_slope = (dual_plus["deformation"] - dual_minus["deformation"]) / (2 * h)
    assert abs(fd_dual_prime - packet["deformation"]) < 1e-6
    assert abs(fd_inverse_slope - packet["stiffness"]) < 1e-4

    interval_1k = completed_defect_spectral_infinite_dual_stiffness_interval(1000, s, target_order, deformation_max=1.0)
    interval_10k = completed_defect_spectral_infinite_dual_stiffness_interval(10000, s, target_order, deformation_max=1.0)
    interval_100k = completed_defect_spectral_infinite_dual_stiffness_interval(100000, s, target_order, deformation_max=1.0)
    assert 0.0 < interval_1k["lower_stiffness"] <= interval_1k["upper_stiffness"]
    assert interval_100k["stiffness_interval_width"] < interval_10k["stiffness_interval_width"] < interval_1k["stiffness_interval_width"]
    assert interval_100k["lower_stiffness"] <= packet["stiffness"] <= interval_100k["upper_stiffness"]

    profile = completed_defect_spectral_infinite_dual_stiffness_profile(1000, [1000, 10000, 100000], [1.0], [1.0, 2.0])
    one_rows = profile["1.0"]["1.0"]["rows"]
    two_rows = profile["1.0"]["2.0"]["rows"]
    assert one_rows[2]["stiffness_interval_width"] < one_rows[1]["stiffness_interval_width"] < one_rows[0]["stiffness_interval_width"]
    assert two_rows[2]["stiffness_interval_width"] < two_rows[1]["stiffness_interval_width"] < two_rows[0]["stiffness_interval_width"]
    assert one_rows[2]["interval_lower_stiffness"] <= one_rows[2]["recovered_stiffness"] <= one_rows[2]["interval_upper_stiffness"]
    assert two_rows[2]["interval_lower_stiffness"] <= two_rows[2]["recovered_stiffness"] <= two_rows[2]["interval_upper_stiffness"]


def test_completed_defect_spectral_uniform_wall_limit_package():
    s = 1.0
    prime_limit = 100000
    near = completed_defect_spectral_real_packet(prime_limit, s, deformation=5.99)
    wall = completed_defect_spectral_uniform_wall_packet(prime_limit, s)
    assert wall["uniform_wall"] == 6.0
    assert wall["deformation"] == 6.0
    assert wall["hessian"] > near["hessian"] > 0.0
    assert wall["order_parameter"] > near["order_parameter"] > 0.0
    assert wall["stiffness"] < near["stiffness"]
    assert abs(wall["hessian"] - near["hessian"]) < 0.02

    profile = completed_defect_spectral_uniform_wall_profile([1000, 10000, 100000], [1.0], [5.0, 5.5, 5.9, 5.99, 6.0])
    wall_rows = [profile["1.0"][key][-1] for key in ["5.0", "5.5", "5.9", "5.99", "6.0"]]
    assert wall_rows[-1]["uniform_wall"] == 6.0
    assert wall_rows[-1]["wall_gap"] == 0.0
    assert wall_rows[-1]["hessian"] > wall_rows[-2]["hessian"] > wall_rows[0]["hessian"]
    assert wall_rows[-1]["stiffness"] < wall_rows[-2]["stiffness"] < wall_rows[0]["stiffness"]


def test_completed_defect_spectral_wall_effective_theory_package():
    packet = completed_defect_spectral_wall_effective_packet(100000, 1.0)
    assert packet["third_derivative"] > 0.0
    assert packet["epsilon_order_slope"] == packet["hessian"]
    assert packet["epsilon_hessian_slope"] == packet["third_derivative"]
    assert packet["epsilon_stiffness_slope"] > 0.0

    profile = completed_defect_spectral_wall_effective_profile([100000], [1.0], [1e-1, 1e-2, 1e-3])
    rows_1e1 = profile["1.0"]["0.1"][0]
    rows_1e2 = profile["1.0"]["0.01"][0]
    rows_1e3 = profile["1.0"]["0.001"][0]
    assert rows_1e3["order_error"] < rows_1e2["order_error"] < rows_1e1["order_error"]
    assert rows_1e3["hessian_error"] < rows_1e2["hessian_error"] < rows_1e1["hessian_error"]
    assert rows_1e3["stiffness_error"] < rows_1e2["stiffness_error"] < rows_1e1["stiffness_error"]


def test_completed_defect_spectral_boundary_transfer_law_package():
    packet = completed_defect_spectral_boundary_transfer_packet(10000, 1.0, subintervals=160)
    assert packet["wall_order_parameter"] > packet["interior_order_parameter"] > 0.0
    assert packet["wall_hessian"] > packet["interior_hessian"] > 0.0
    assert packet["interior_stiffness"] > packet["wall_stiffness"] > 0.0
    assert completed_defect_spectral_dual_softening_density(10000, 1.0, 4.0) > 0.0
    assert completed_defect_spectral_dual_softening_density(10000, 1.0, 6.0) > 0.0
    assert packet["action_transfer_error"] < 1e-4
    assert packet["order_transfer_error"] < 1e-4
    assert packet["stiffness_transfer_error"] < 1e-4


def test_completed_defect_spectral_infinite_wall_packet_package():
    wall_1k = completed_defect_spectral_infinite_wall_packet(1000, 1.0)
    wall_10k = completed_defect_spectral_infinite_wall_packet(10000, 1.0)
    wall_100k = completed_defect_spectral_infinite_wall_packet(100000, 1.0)

    assert wall_1k["action_tail_bound"] > wall_10k["action_tail_bound"] > wall_100k["action_tail_bound"] > 0.0
    assert wall_1k["order_tail_bound"] > wall_10k["order_tail_bound"] > wall_100k["order_tail_bound"] > 0.0
    assert wall_1k["hessian_tail_bound"] > wall_10k["hessian_tail_bound"] > wall_100k["hessian_tail_bound"] > 0.0
    assert wall_1k["relative_value_error_bound"] > wall_10k["relative_value_error_bound"] > wall_100k["relative_value_error_bound"] > 0.0

    assert wall_100k["lower_infinite_action"] <= wall_100k["action"] <= wall_100k["upper_infinite_action"]
    assert wall_100k["lower_infinite_order_parameter"] <= wall_100k["order_parameter"] <= wall_100k["upper_infinite_order_parameter"]
    assert wall_100k["lower_infinite_hessian"] <= wall_100k["hessian"] <= wall_100k["upper_infinite_hessian"]
    assert wall_100k["lower_infinite_stiffness"] <= wall_100k["stiffness"] <= wall_100k["upper_infinite_stiffness"]
    assert wall_100k["lower_infinite_dual"] <= wall_100k["dual"] <= wall_100k["upper_infinite_dual"]

    assert wall_100k["action"] > wall_10k["action"] > wall_1k["action"] > 0.0
    assert wall_100k["order_parameter"] > wall_10k["order_parameter"] > wall_1k["order_parameter"] > 0.0
    assert wall_100k["hessian"] > wall_10k["hessian"] > wall_1k["hessian"] > 0.0
    assert wall_100k["stiffness"] < wall_10k["stiffness"] < wall_1k["stiffness"]
    assert wall_100k["stiffness_interval_width"] < wall_10k["stiffness_interval_width"] < wall_1k["stiffness_interval_width"]

    profile = completed_defect_spectral_infinite_wall_profile([1000, 10000, 100000], [1.0, 2.0])
    rows_1 = profile["1.0"]
    rows_2 = profile["2.0"]
    assert rows_1[-1]["action_jump_from_previous"] is not None and rows_1[-1]["action_jump_from_previous"] > 0.0
    assert rows_1[-1]["order_jump_from_previous"] is not None and rows_1[-1]["order_jump_from_previous"] > 0.0
    assert rows_1[-1]["hessian_jump_from_previous"] is not None and rows_1[-1]["hessian_jump_from_previous"] > 0.0
    assert rows_1[-1]["stiffness_drop_from_previous"] is not None and rows_1[-1]["stiffness_drop_from_previous"] > 0.0
    assert rows_2[-1]["stiffness_interval_width_drop_from_previous"] is not None and rows_2[-1]["stiffness_interval_width_drop_from_previous"] > 0.0


def test_completed_defect_spectral_infinite_boundary_corridor_package():
    interior_1k = completed_defect_spectral_infinite_compact_real_packet(1000, 1.0, 4.0)
    interior_10k = completed_defect_spectral_infinite_compact_real_packet(10000, 1.0, 4.0)
    interior_100k = completed_defect_spectral_infinite_compact_real_packet(100000, 1.0, 4.0)

    assert interior_1k["action_tail_bound"] > interior_10k["action_tail_bound"] > interior_100k["action_tail_bound"] > 0.0
    assert interior_1k["order_tail_bound"] > interior_10k["order_tail_bound"] > interior_100k["order_tail_bound"] > 0.0
    assert interior_1k["hessian_tail_bound"] > interior_10k["hessian_tail_bound"] > interior_100k["hessian_tail_bound"] > 0.0
    assert interior_100k["lower_infinite_stiffness"] <= interior_100k["stiffness"] <= interior_100k["upper_infinite_stiffness"]
    assert interior_100k["lower_infinite_dual"] <= interior_100k["dual"] <= interior_100k["upper_infinite_dual"]

    corridor_1k = completed_defect_spectral_infinite_boundary_corridor_packet(1000, 1.0, subintervals=80)
    corridor_10k = completed_defect_spectral_infinite_boundary_corridor_packet(10000, 1.0, subintervals=80)
    corridor_100k = completed_defect_spectral_infinite_boundary_corridor_packet(100000, 1.0, subintervals=80)

    assert corridor_100k["finite_delta_action_in_corridor"]
    assert corridor_100k["finite_delta_order_parameter_in_corridor"]
    assert corridor_100k["finite_delta_hessian_in_corridor"]
    assert corridor_100k["finite_stiffness_loss_in_corridor"]
    assert corridor_100k["finite_dual_delta_in_corridor"]
    assert corridor_100k["infinite_delta_action_lower_bound"] > 0.0
    assert corridor_100k["infinite_delta_order_parameter_lower_bound"] > 0.0
    assert corridor_100k["infinite_delta_hessian_lower_bound"] > 0.0
    assert corridor_100k["infinite_stiffness_loss_lower_bound"] > 0.0

    assert (
        corridor_1k["infinite_delta_action_interval_width"]
        > corridor_10k["infinite_delta_action_interval_width"]
        > corridor_100k["infinite_delta_action_interval_width"]
        > 0.0
    )
    assert (
        corridor_1k["infinite_delta_order_parameter_interval_width"]
        > corridor_10k["infinite_delta_order_parameter_interval_width"]
        > corridor_100k["infinite_delta_order_parameter_interval_width"]
        > 0.0
    )
    assert (
        corridor_1k["infinite_delta_hessian_interval_width"]
        > corridor_10k["infinite_delta_hessian_interval_width"]
        > corridor_100k["infinite_delta_hessian_interval_width"]
        > 0.0
    )
    assert (
        corridor_1k["infinite_stiffness_loss_interval_width"]
        > corridor_10k["infinite_stiffness_loss_interval_width"]
        > corridor_100k["infinite_stiffness_loss_interval_width"]
        > 0.0
    )
    assert (
        corridor_1k["infinite_dual_delta_interval_width"]
        > corridor_10k["infinite_dual_delta_interval_width"]
        > corridor_100k["infinite_dual_delta_interval_width"]
        > 0.0
    )

    profile = completed_defect_spectral_infinite_boundary_corridor_profile([1000, 10000, 100000], [1.0], subintervals=60)
    rows = profile["1.0"]
    assert rows[-1]["action_corridor_width_drop_from_previous"] is not None and rows[-1]["action_corridor_width_drop_from_previous"] > 0.0
    assert rows[-1]["stiffness_corridor_width_drop_from_previous"] is not None and rows[-1]["stiffness_corridor_width_drop_from_previous"] > 0.0


def test_completed_defect_spectral_infinite_boundary_average_density_package():
    packet = completed_defect_spectral_infinite_boundary_average_packet(100000, 1.0, subintervals=80)
    corridor = completed_defect_spectral_infinite_boundary_corridor_packet(100000, 1.0, subintervals=80)
    width = packet["corridor_width"]

    assert width == 2.0
    assert packet["finite_average_order_parameter_in_corridor"]
    assert packet["finite_average_hessian_in_corridor"]
    assert packet["finite_average_third_derivative_in_corridor"]
    assert packet["finite_average_dual_softening_in_corridor"]
    assert packet["finite_average_dual_delta_density_in_corridor"]

    assert packet["finite_average_order_parameter"] == corridor["finite_delta_action"] / width
    assert packet["finite_average_hessian"] == corridor["finite_delta_order_parameter"] / width
    assert packet["finite_average_third_derivative"] == corridor["finite_delta_hessian"] / width
    assert packet["finite_average_dual_softening"] == corridor["finite_stiffness_loss"] / width
    assert packet["finite_average_dual_delta_density"] == corridor["finite_dual_delta"] / width
    assert packet["infinite_average_order_parameter_interval_width"] == corridor["infinite_delta_action_interval_width"] / width
    assert packet["infinite_average_hessian_interval_width"] == corridor["infinite_delta_order_parameter_interval_width"] / width
    assert packet["infinite_average_third_derivative_interval_width"] == corridor["infinite_delta_hessian_interval_width"] / width
    assert packet["infinite_average_dual_softening_interval_width"] == corridor["infinite_stiffness_loss_interval_width"] / width
    assert packet["infinite_average_dual_delta_density_interval_width"] == corridor["infinite_dual_delta_interval_width"] / width

    profile = completed_defect_spectral_infinite_boundary_average_profile([1000, 10000, 100000], [1.0], subintervals=60)
    rows = profile["1.0"]
    assert rows[-1]["average_order_width_drop_from_previous"] is not None and rows[-1]["average_order_width_drop_from_previous"] > 0.0
    assert rows[-1]["average_hessian_width_drop_from_previous"] is not None and rows[-1]["average_hessian_width_drop_from_previous"] > 0.0
    assert rows[-1]["average_third_derivative_width_drop_from_previous"] is not None and rows[-1]["average_third_derivative_width_drop_from_previous"] > 0.0
    assert rows[-1]["average_dual_softening_width_drop_from_previous"] is not None and rows[-1]["average_dual_softening_width_drop_from_previous"] > 0.0
    assert rows[-1]["average_dual_delta_width_drop_from_previous"] is not None and rows[-1]["average_dual_delta_width_drop_from_previous"] > 0.0


def test_completed_defect_spectral_boundary_mean_witness_ladder_package():
    packet = completed_defect_spectral_boundary_mean_witness_packet(100000, 1.0, subintervals=80)

    assert completed_defect_spectral_third_derivative_real_global(100000, 1.0, 4.0) > 0.0
    assert packet["mean_deformation_ladder_ordered"]
    assert packet["primal_mean_deformation_ladder_ordered"]
    assert packet["order_mean_abs_residual"] < 1e-10
    assert packet["hessian_mean_abs_residual"] < 1e-10
    assert packet["third_derivative_mean_abs_residual"] < 1e-10
    assert packet["dual_softening_mean_abs_residual"] < 1e-10

    assert abs(packet["order_mean_value"] - packet["finite_average_order_parameter"]) < 1e-10
    assert abs(packet["hessian_mean_value"] - packet["finite_average_hessian"]) < 1e-10
    assert abs(packet["third_derivative_mean_value"] - packet["finite_average_third_derivative"]) < 1e-10
    assert abs(packet["dual_softening_mean_value"] - packet["finite_average_dual_softening"]) < 1e-10

    assert 4.0 < packet["dual_softening_mean_deformation"] < packet["order_mean_deformation"]
    assert packet["order_mean_deformation"] < packet["hessian_mean_deformation"] < packet["third_derivative_mean_deformation"] < 6.0

    profile = completed_defect_spectral_boundary_mean_witness_profile([1000, 10000, 100000], [1.0], subintervals=60)
    rows = profile["1.0"]
    assert rows[-1]["mean_deformation_ladder_ordered"]
    assert rows[-1]["order_mean_deformation_jump_from_previous"] < rows[1]["order_mean_deformation_jump_from_previous"]
    assert rows[-1]["hessian_mean_deformation_jump_from_previous"] < rows[1]["hessian_mean_deformation_jump_from_previous"]
    assert rows[-1]["third_derivative_mean_deformation_jump_from_previous"] <= rows[1]["third_derivative_mean_deformation_jump_from_previous"]
    assert rows[-1]["dual_softening_mean_deformation_jump_from_previous"] < rows[1]["dual_softening_mean_deformation_jump_from_previous"]


def test_completed_defect_spectral_boundary_barycentric_witness_package():
    packet = completed_defect_spectral_boundary_barycentric_witness_packet(100000, 1.0, subintervals=80)
    width = packet["corridor_width"]

    assert width == 2.0
    assert packet["barycentric_ladder_ordered"]
    assert packet["primal_barycentric_ladder_ordered"]
    assert abs(packet["barycentric_gap_sum"] - 1.0) < 1e-15
    assert packet["dual_softening_barycentric_coordinate"] == (packet["dual_softening_mean_deformation"] - 4.0) / width
    assert packet["order_barycentric_coordinate"] == (packet["order_mean_deformation"] - 4.0) / width
    assert packet["hessian_barycentric_coordinate"] == (packet["hessian_mean_deformation"] - 4.0) / width
    assert packet["third_derivative_barycentric_coordinate"] == (packet["third_derivative_mean_deformation"] - 4.0) / width
    assert packet["interior_to_softening_barycentric_gap"] > 0.0
    assert packet["softening_to_order_barycentric_gap"] > 0.0
    assert packet["order_to_hessian_barycentric_gap"] > 0.0
    assert packet["hessian_to_third_derivative_barycentric_gap"] > 0.0
    assert packet["third_derivative_to_wall_barycentric_gap"] > 0.0

    profile = completed_defect_spectral_boundary_barycentric_witness_profile([1000, 10000, 100000], [1.0], subintervals=60)
    rows = profile["1.0"]
    assert rows[-1]["barycentric_ladder_ordered"]
    assert rows[-1]["order_barycentric_jump_from_previous"] < rows[1]["order_barycentric_jump_from_previous"]
    assert rows[-1]["hessian_barycentric_jump_from_previous"] < rows[1]["hessian_barycentric_jump_from_previous"]
    assert rows[-1]["third_derivative_barycentric_jump_from_previous"] <= rows[1]["third_derivative_barycentric_jump_from_previous"]
    assert rows[-1]["dual_softening_barycentric_jump_from_previous"] < rows[1]["dual_softening_barycentric_jump_from_previous"]


def test_completed_defect_spectral_boundary_barycentric_stability_signature():
    packet = completed_defect_spectral_boundary_barycentric_stability_packet([1000, 10000, 100000], [1.0, 2.0], subintervals=40)

    assert packet["minimum_finite_contraction_ratio"] > 100.0
    assert packet["per_s"]["1.0"]["all_coordinate_contractions_ge_100"]
    assert packet["per_s"]["2.0"]["all_coordinate_contractions_ge_100"]
    assert packet["per_s"]["1.0"]["coordinate_jump_ratios"]["third_derivative"]["second_jump_zero"]
    assert packet["per_s"]["2.0"]["coordinate_jump_ratios"]["third_derivative"]["contraction_ratio"] is None
    assert packet["per_s"]["1.0"]["barycentric_ladder_ordered"]
    assert packet["per_s"]["2.0"]["barycentric_ladder_ordered"]
    assert abs(packet["per_s"]["1.0"]["final_gap_sum"] - 1.0) < 1e-15
    assert abs(packet["per_s"]["2.0"]["final_gap_sum"] - 1.0) < 1e-15

    shift = packet["cross_s_shift"]
    assert shift["all_witnesses_shift_toward_wall"]
    assert shift["coordinate_offsets_strictly_increase"]
    assert shift["wall_gap_shrinks"]
    assert abs(shift["gap_offset_sum"]) < 1e-15
    assert shift["coordinate_offsets"]["dual_softening"] > 0.0
    assert shift["coordinate_offsets"]["dual_softening"] < shift["coordinate_offsets"]["order"]
    assert shift["coordinate_offsets"]["order"] < shift["coordinate_offsets"]["hessian"]
    assert shift["coordinate_offsets"]["hessian"] < shift["coordinate_offsets"]["third_derivative"]


def test_completed_defect_spectral_boundary_barycentric_wallward_flow_packet():
    s_values = [0.5, 1.0, 1.5, 2.0, 2.5, 3.0]
    packet = completed_defect_spectral_boundary_barycentric_wallward_flow_packet(100000, s_values, subintervals=40)

    assert packet["all_coordinate_jumps_positive"]
    assert packet["all_wall_gap_jumps_negative"]
    assert packet["all_barycentric_ladders_ordered"]
    assert packet["wall_gap_strictly_decreases"]
    assert packet["dual_softening_crosses_half"]
    assert packet["dual_softening_midpoint_crossing_index"] == len(s_values) - 1
    assert packet["dual_softening_midpoint_crossing_interval"] == {"left_s": 2.5, "right_s": 3.0}
    assert packet["initial_wall_gap"] > packet["final_wall_gap"] > 0.0
    assert packet["wall_gap_drop"] > 0.0

    rows = packet["rows"]
    assert len(rows) == len(s_values)
    for row in rows:
        assert row["barycentric_ladder_ordered"]
        assert 0.0 < row["dual_softening_barycentric_coordinate"] < row["order_barycentric_coordinate"]
        assert row["order_barycentric_coordinate"] < row["hessian_barycentric_coordinate"]
        assert row["hessian_barycentric_coordinate"] < row["third_derivative_barycentric_coordinate"] < 1.0

    offsets = packet["coordinate_offsets"]
    assert offsets["dual_softening"] > 0.0
    assert offsets["order"] > offsets["dual_softening"]
    assert offsets["hessian"] > offsets["order"]
    assert offsets["third_derivative"] > offsets["hessian"]


def test_completed_defect_spectral_boundary_barycentric_dispersion_turning_packet():
    s_values = [0.5, 1.0, 1.5, 2.0, 2.5, 3.0]
    packet = completed_defect_spectral_boundary_barycentric_dispersion_turning_packet(100000, s_values, subintervals=40)

    assert packet["all_coordinate_jumps_positive"]
    assert packet["all_wall_gap_jumps_negative"]
    assert packet["wall_gap_strictly_decreases"]
    assert packet["dominant_gap_all_interior_to_softening"]

    assert packet["entropy_peak_s"] == 2.0
    assert packet["concentration_trough_s"] == 2.0
    assert packet["entropy_rises_then_falls"]
    assert packet["concentration_falls_then_rises"]

    assert packet["entropy_sign_pattern"] == [1, 1, 1, -1, -1]
    assert packet["concentration_sign_pattern"] == [-1, -1, -1, 1, 1]

    rows = packet["rows"]
    assert rows[0]["gap_entropy"] < rows[1]["gap_entropy"] < rows[2]["gap_entropy"] < rows[3]["gap_entropy"]
    assert rows[3]["gap_entropy"] > rows[4]["gap_entropy"] > rows[5]["gap_entropy"]
    assert rows[0]["gap_concentration"] > rows[1]["gap_concentration"] > rows[2]["gap_concentration"] > rows[3]["gap_concentration"]
    assert rows[3]["gap_concentration"] < rows[4]["gap_concentration"] < rows[5]["gap_concentration"]


def test_completed_defect_spectral_boundary_barycentric_recurrence_resonance_packet():
    s_values = [0.5, 1.0, 1.5, 2.0, 2.5, 3.0]
    packet = completed_defect_spectral_boundary_barycentric_recurrence_resonance_packet(100000, s_values, subintervals=40)

    assert packet["shared_resonance_detected"]
    assert packet["shared_resonance_s"] == 2.0
    assert packet["entropy_peak_s"] == 2.0
    assert packet["concentration_trough_s"] == 2.0
    assert packet["dominant_gap_all_interior_to_softening"]
    assert packet["wall_gap_strictly_decreases"]
    assert packet["all_coordinate_jumps_positive"]
    assert packet["all_wall_gap_jumps_negative"]
    assert packet["entropy_sign_pattern"] == [1, 1, 1, -1, -1]
    assert packet["concentration_sign_pattern"] == [-1, -1, -1, 1, 1]

    entropy_harmonics = packet["entropy_harmonics"]
    concentration_harmonics = packet["concentration_harmonics"]
    assert entropy_harmonics["dc_dominates_nonzero_harmonics"]
    assert concentration_harmonics["dc_dominates_nonzero_harmonics"]
    assert entropy_harmonics["dominant_nonzero_harmonic_index"] == 1
    assert concentration_harmonics["dominant_nonzero_harmonic_index"] == 1
    assert entropy_harmonics["conjugate_symmetric"]
    assert concentration_harmonics["conjugate_symmetric"]
    assert entropy_harmonics["normalized_dft_abs"][1] < 0.05
    assert concentration_harmonics["normalized_dft_abs"][1] < 0.05
    assert abs(entropy_harmonics["dft_abs"][1] - entropy_harmonics["dft_abs"][5]) < 1e-12
    assert abs(concentration_harmonics["dft_abs"][1] - concentration_harmonics["dft_abs"][5]) < 1e-12

    entropy_recurrence = packet["entropy_recurrence"]
    concentration_recurrence = packet["concentration_recurrence"]
    assert abs(entropy_recurrence["coefficients"][0] + 0.7930288200175148) < 1e-12
    assert abs(entropy_recurrence["coefficients"][1] - 1.757925053075776) < 1e-12
    assert abs(concentration_recurrence["coefficients"][0] + 0.7838244705015696) < 1e-12
    assert abs(concentration_recurrence["coefficients"][1] - 1.8194198703813358) < 1e-12
    assert entropy_recurrence["max_abs_residual"] < 0.02
    assert concentration_recurrence["max_abs_residual"] < 0.009


def test_completed_defect_spectral_boundary_barycentric_recurrence_phase_packet():
    s_values = [0.5, 1.0, 1.5, 2.0, 2.5, 3.0]
    packet = completed_defect_spectral_boundary_barycentric_recurrence_phase_packet(100000, s_values, subintervals=40)

    assert packet["phase_split_detected"]
    assert packet["entropy_damped_oscillatory"]
    assert packet["concentration_real_expanding_mode_detected"]
    assert packet["shared_resonance_s"] == 2.0

    entropy = packet["entropy_phase"]
    concentration = packet["concentration_phase"]
    assert entropy["phase_type"] == "complex_conjugate"
    assert concentration["phase_type"] == "real_split"
    assert entropy["discriminant"] < 0.0
    assert concentration["discriminant"] > 0.0
    assert entropy["all_roots_inside_unit_disk"]
    assert not concentration["all_roots_inside_unit_disk"]
    assert concentration["has_unit_exceeding_root"]
    assert entropy["sum_matches_a1"] and entropy["product_matches_minus_a2"]
    assert concentration["sum_matches_a1"] and concentration["product_matches_minus_a2"]
    assert abs(entropy["spectral_radius"] - 0.8905216561193539) < 1e-12
    assert abs(concentration["spectral_radius"] - 1.11886943338041) < 1e-12
    assert abs(entropy["roots"][0]["imag"] + entropy["roots"][1]["imag"]) < 1e-15
    assert concentration["roots"][0]["imag"] == 0.0 and concentration["roots"][1]["imag"] == 0.0


def test_completed_defect_spectral_boundary_barycentric_gap_handoff_packet():
    s_values = [0.5, 1.0, 1.5, 2.0, 2.5, 3.0]
    packet = completed_defect_spectral_boundary_barycentric_gap_handoff_packet(100000, s_values, subintervals=40)

    assert packet["handoff_cascade_detected"]
    assert packet["primary_gap_all_interior_to_softening"]
    assert packet["shared_resonance_s"] == 2.0
    assert packet["secondary_handoff_sample_locks_to_resonance"]
    assert packet["secondary_handoff_crossing_precedes_resonance"]
    assert packet["wall_gap_rank_monotone_nonworsening_toward_lower_priority"]
    assert packet["softening_to_order_rank_improves"]
    assert packet["wall_drop_balances_interior_gains"]
    assert packet["dominant_wall_mass_recipient"] == "softening_to_order"
    assert packet["softening_to_order_receives_majority_wall_transfer"]

    assert packet["secondary_gap_sequence"] == [
        "third_derivative_to_wall",
        "third_derivative_to_wall",
        "third_derivative_to_wall",
        "softening_to_order",
        "softening_to_order",
        "softening_to_order",
    ]
    assert packet["wall_gap_rank_sequence"] == [2, 2, 2, 3, 4, 4]
    assert packet["softening_to_order_gap_rank_sequence"] == [3, 3, 3, 2, 2, 2]
    assert packet["order_to_hessian_gap_rank_sequence"] == [5, 4, 4, 4, 3, 3]

    secondary = packet["secondary_handoff"]
    assert secondary == {
        "left_gap": "softening_to_order",
        "right_gap": "third_derivative_to_wall",
        "left_s": 1.5,
        "right_s": 2.0,
        "left_difference": secondary["left_difference"],
        "right_difference": secondary["right_difference"],
        "linear_crossing_s": secondary["linear_crossing_s"],
        "first_sample_after_crossing_s": 2.0,
    }
    assert abs(secondary["linear_crossing_s"] - 1.7384967374464677) < 1e-12
    assert secondary["left_difference"] < 0.0 < secondary["right_difference"]

    tertiary = packet["order_hessian_wall_handoff"]
    assert tertiary["left_s"] == 2.0 and tertiary["right_s"] == 2.5
    assert abs(tertiary["linear_crossing_s"] - 2.279430142026481) < 1e-12
    assert tertiary["left_difference"] < 0.0 < tertiary["right_difference"]

    shares = packet["wall_mass_transfer_shares"]
    assert abs(packet["wall_gap_drop"] - 0.38305552720929903) < 1e-15
    assert abs(sum(shares.values()) - 1.0) < 1e-15
    assert abs(shares["softening_to_order"] - 0.5666305790962431) < 1e-12
    assert shares["softening_to_order"] > shares["order_to_hessian"] > shares["interior_to_softening"]
    assert shares["interior_to_softening"] > shares["hessian_to_third_derivative"]


def test_completed_defect_spectral_boundary_barycentric_gap_handoff_cutoff_profile():
    s_values = [0.5, 1.0, 1.5, 2.0, 2.5, 3.0]
    packet = completed_defect_spectral_boundary_barycentric_gap_handoff_cutoff_profile(
        [1000, 10000, 100000],
        s_values,
        subintervals=40,
    )

    assert packet["shared_resonance_all_equal"]
    assert packet["cascade_all_detected"]
    assert packet["secondary_sequences_all_equal"]
    assert packet["rank_sequences_all_equal"]
    assert packet["softening_rank_sequences_all_equal"]
    assert packet["order_rank_sequences_all_equal"]
    assert packet["dominant_recipient_all_equal"]
    assert packet["majority_transfer_all"]
    assert packet["wall_gap_drop_profile_converges"]
    assert packet["secondary_crossing_profile_converges"]
    assert packet["majority_transfer_profile_converges"]

    assert packet["wall_gap_drop_max_deviation"] < 1e-9
    assert packet["secondary_crossing_max_deviation"] < 1e-5
    assert packet["wall_gap_drop_reference"] > 0.0
    assert packet["secondary_crossing_reference"] is not None

    per_cutoff = packet["per_cutoff"]
    assert [row["prime_limit"] for row in per_cutoff] == [1000, 10000, 100000]
    assert all(row["shared_resonance_s"] == 2.0 for row in per_cutoff)
    assert all(row["handoff_cascade_detected"] for row in per_cutoff)
    assert all(
        row["secondary_gap_sequence"] == [
            "third_derivative_to_wall",
            "third_derivative_to_wall",
            "third_derivative_to_wall",
            "softening_to_order",
            "softening_to_order",
            "softening_to_order",
        ]
        for row in per_cutoff
    )
    assert all(row["wall_gap_rank_sequence"] == [2, 2, 2, 3, 4, 4] for row in per_cutoff)
    assert all(row["dominant_wall_mass_recipient"] == "softening_to_order" for row in per_cutoff)
    assert all(abs(sum(row["wall_mass_transfer_shares"].values()) - 1.0) < 1e-15 for row in per_cutoff)


def test_completed_defect_spectral_boundary_barycentric_gap_handoff_convergence_signature():
    s_values = [0.5, 1.0, 1.5, 2.0, 2.5, 3.0]
    packet = completed_defect_spectral_boundary_barycentric_gap_handoff_convergence_signature(
        [1000, 10000, 100000],
        s_values,
        subintervals=40,
    )

    assert packet["convergence_signature_detected"]
    signature = packet["directional_signature"]
    assert signature["wall_gap_drop_nondecreasing"]
    assert signature["secondary_crossing_nondecreasing"]
    assert signature["order_hessian_crossing_nonincreasing"]
    assert signature["softening_share_nonincreasing"]
    assert signature["interior_share_nondecreasing"]
    assert signature["order_hessian_share_nondecreasing"]
    assert signature["hessian_third_share_nonincreasing"]
    assert signature["secondary_reference_offset_nonincreasing"]
    assert signature["wall_reference_offset_nonincreasing"]

    assert packet["wall_gap_drop_sequence"][0] < packet["wall_gap_drop_sequence"][1] <= packet["wall_gap_drop_sequence"][2]
    assert packet["secondary_crossing_sequence"][0] < packet["secondary_crossing_sequence"][1] < packet["secondary_crossing_sequence"][2]
    assert packet["order_hessian_crossing_sequence"][0] > packet["order_hessian_crossing_sequence"][1] > packet["order_hessian_crossing_sequence"][2]
    assert packet["softening_share_sequence"][0] > packet["softening_share_sequence"][1] > packet["softening_share_sequence"][2]
    assert packet["interior_share_sequence"][0] < packet["interior_share_sequence"][1] < packet["interior_share_sequence"][2]


def test_eisenstein_exact_local_global_valuation_criterion():
    row_phi3 = exact_branch_congruence_valuation(18, 7, "Phi3")
    row_phi6 = exact_branch_congruence_valuation(19, 7, "Phi6")
    row_phi3_simple = exact_branch_congruence_valuation(4, 7, "Phi3")
    row_phi6_simple = exact_branch_congruence_valuation(5, 7, "Phi6")
    assert row_phi3["branch_valuation"] == 3
    assert row_phi3["phi_exponent"] == 3
    assert row_phi3["exact_criterion_holds"]
    assert row_phi3["exact_residue_mod_pn"] == 18
    assert not row_phi3["extends_to_next_power"]
    assert row_phi6["branch_valuation"] == 3
    assert row_phi6["phi_exponent"] == 3
    assert row_phi6["exact_criterion_holds"]
    assert row_phi6["exact_residue_mod_pn"] == 19
    assert row_phi3_simple["branch_valuation"] == 1 and row_phi3_simple["exact_criterion_holds"]
    assert row_phi6_simple["branch_valuation"] == 1 and row_phi6_simple["exact_criterion_holds"]
    packet3 = eisenstein_local_global_valuation_packet(18, "Phi3")
    packet6 = eisenstein_local_global_valuation_packet(19, "Phi6")
    assert packet3["all_exact"] and packet6["all_exact"]
    assert packet3["split_prime_rows"][0]["statement"].startswith("v_pi")


def test_eisenstein_prime_ideal_packet():
    packet = eisenstein_split_ideal_data(7, power=2)
    assert [row["phi3_residue"] for row in packet["packet"]] == [18, 30]
    assert sorted(row["phi6_residue"] for row in packet["packet"]) == [19, 31]
    witness3 = eisenstein_ideal_witness(18, "Phi3")
    witness6 = eisenstein_ideal_witness(19, "Phi6")
    assert witness3["ideal_witnesses"][0]["statement"].endswith("divides (q-ω) in Z[ω]")
    assert witness6["ideal_witnesses"][0]["statement"].endswith("divides (q+ω) in Z[ω]")


def test_cyclotomic_perfect_power_theorem_package():
    red3 = cyclotomic_ljunggren_reduction(18, "Phi3")
    red6 = cyclotomic_ljunggren_reduction(19, "Phi6")
    assert red3["x"] == 37 and red3["equation_check"]
    assert red6["x"] == 37 and red6["equation_check"]
    theorem = cyclotomic_perfect_power_theorem()
    assert theorem["solutions"] == cyclotomic_known_perfect_power_solutions()
    assert theorem["solutions"] == [
        {"family": "Phi3", "q": 18, "value": 343, "base": 7, "exponent": 3, "x": 37},
        {"family": "Phi6", "q": 19, "value": 343, "base": 7, "exponent": 3, "x": 37},
    ]


def test_first_cube_defect_and_classifier_match():
    phi3 = defect_match_for_q(18, "Phi3")
    phi6 = defect_match_for_q(19, "Phi6")
    assert phi3["matched"] and phi3["prime"] == 7 and phi3["q_mod_p2"] == 18
    assert phi6["matched"] and phi6["prime"] == 7 and phi6["q_mod_p2"] == 19


def test_exact_residue_classifier_on_moderate_window():
    payload = defect_residue_classifier(limit_q=300, prime_limit=200)
    assert payload["phi3_exact_classifier"]
    assert payload["phi6_exact_classifier"]
    assert payload["exact_classifier"]
    assert "nontrivial cube root of unity" in payload["cube_root_restatement"]


def test_perfect_power_scan_on_moderate_window():
    payload = cyclotomic_perfect_power_scan(limit_q=5000)
    assert payload["phi3_hits"] == [{"q": 18, "value": 343, "base": 7, "exponent": 3}]
    assert payload["phi6_hits"] == [{"q": 19, "value": 343, "base": 7, "exponent": 3}]


def test_defect_density_estimate_matches_empirical_scan():
    estimate = defect_density_partial_product(prime_limit=50000)
    empirical = empirical_defect_density(limit_q=5000)
    assert abs(empirical["phi3_density"] - estimate["defect_density_estimate"]) < 0.01
    assert abs(empirical["phi6_density"] - estimate["defect_density_estimate"]) < 0.01
