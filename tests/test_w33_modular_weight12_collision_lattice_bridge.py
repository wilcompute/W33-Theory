from exploration.w33_modular_weight12_collision_lattice_bridge import build_summary


def test_weight12_collision_lattice_theorem() -> None:
    summary = build_summary()
    assert all(summary["weight12_collision_lattice_theorem"].values())


def test_weight12_collision_lattice_dictionary() -> None:
    summary = build_summary()
    dictionary = summary["weight12_collision_lattice_dictionary"]

    assert dictionary["dim_M_12"] == 2
    assert dictionary["dim_S_12"] == 1
    assert dictionary["change_matrix_rows"] == [[441, 250], [1, -1]]
    assert dictionary["change_matrix_determinant"] == -691


def test_packetized_collision_coefficients() -> None:
    summary = build_summary()
    theorem = summary["weight12_collision_lattice_theorem"]

    assert theorem["the_441_coefficient_is_exactly_the_square_of_the_ag21_packet_q_times_phi6"]
    assert theorem["the_250_coefficient_is_exactly_lambda_times_mu_plus_1_cubed"]
    assert theorem["the_discriminant_scale_1728_is_exactly_12_cubed"]
    assert theorem["the_first_integral_e12_fourier_correction_65520_is_exactly_E8_roots_times_the_ternary_commutant"]
