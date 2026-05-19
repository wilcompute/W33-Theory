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
    completed_defect_spectral_L_function,
    completed_defect_spectral_log,
    completed_defect_spectral_profile,
    completed_defect_spectral_reciprocity,
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