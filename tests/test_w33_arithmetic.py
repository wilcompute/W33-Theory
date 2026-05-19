from w33.arithmetic import (
    ARITHMETIC_OPERATORS,
    apply_operator_chain,
    arithmetic_closure_headlines,
    arithmetic_derivative,
    build_arithmetic_closure_table,
    cototient,
    divisor_count,
    divisor_sum,
    jordan_totient,
    operator_lift_headlines,
    radical,
    euler_totient,
    get_divisor_count_edges_pell_multiplier,
    get_divisor_count_valency_factorial,
    get_divisor_count_vertices_tomotope_cells,
    get_sigma_edge_j_shift,
    get_sigma_leech_exponent_efolds,
    get_sigma_logical_sector_ihara_square,
    get_sigma_q_pow_q_vertex_count,
    get_sigma_valency_klein_bitangents,
    get_totient_edges_binary_shell,
    get_totient_gauge_positive_multiplicity,
    get_totient_phi3_valency,
    get_totient_phi6_factorial,
    total_prime_factor_count,
    validate_arithmetic_closure_headlines,
    validate_operator_lift_headlines,
)


def test_basic_arithmetic_functions():
    assert euler_totient(13) == 12
    assert divisor_count(240) == 20
    assert divisor_sum(24) == 60


def test_headline_sigma_identities():
    assert get_sigma_edge_j_shift() == 744
    assert get_sigma_valency_klein_bitangents() == 28
    assert get_sigma_leech_exponent_efolds() == 60
    assert get_sigma_q_pow_q_vertex_count() == 40
    assert get_sigma_logical_sector_ihara_square() == 121


def test_headline_d_and_phi_identities():
    assert get_divisor_count_edges_pell_multiplier() == 20
    assert get_divisor_count_vertices_tomotope_cells() == 8
    assert get_divisor_count_valency_factorial() == 6
    assert get_totient_edges_binary_shell() == 64
    assert get_totient_gauge_positive_multiplicity() == 24
    assert get_totient_phi3_valency() == 12
    assert get_totient_phi6_factorial() == 6


def test_arithmetic_closure_payload():
    table = {row["primitive"]: row for row in build_arithmetic_closure_table()}
    assert table["edges_E"]["sigma_n"] == 744
    assert table["v"]["d_n"] == 8
    assert table["Phi_3"]["phi_n"] == 12
    assert validate_arithmetic_closure_headlines()
    assert all(item["match"] for item in arithmetic_closure_headlines())


def test_extended_operator_lifts():
    assert jordan_totient(2, 2) == 3
    assert jordan_totient(3, 2) == 8
    assert jordan_totient(4, 2) == 12
    assert jordan_totient(4, 4) == 240
    assert radical(40) == 10
    assert cototient(40) == 24
    assert total_prime_factor_count(40) == 4
    assert total_prime_factor_count(240) == 6
    assert arithmetic_derivative(8) == 12
    assert arithmetic_derivative(10) == 7
    assert arithmetic_derivative(27) == 27
    assert validate_operator_lift_headlines()
    assert all(item["match"] for item in operator_lift_headlines())


def test_operator_registry_and_chain_application():
    assert set(ARITHMETIC_OPERATORS) == {"phi", "d", "sigma_1", "rad", "Omega", "cot", "J2", "J4", "D"}
    assert apply_operator_chain(13, ("rad", "phi")) == 12
    assert apply_operator_chain(7, ("phi", "d")) == 4
    assert apply_operator_chain(12, ("cot", "sigma_1", "Omega")) == 2