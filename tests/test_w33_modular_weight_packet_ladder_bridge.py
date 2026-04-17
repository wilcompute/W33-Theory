from exploration.w33_modular_weight_packet_ladder_bridge import build_summary


def test_modular_weight_packet_ladder_theorem() -> None:
    summary = build_summary()
    assert all(summary["modular_weight_packet_ladder_theorem"].values())


def test_low_weight_packet_dictionary() -> None:
    summary = build_summary()
    dictionary = summary["modular_weight_packet_ladder_dictionary"]

    assert dictionary["chart_count"] == 4
    assert dictionary["centered_toroidal_shell"] == 6
    assert dictionary["bosonic_octet"] == 8
    assert dictionary["Phi_4_packet"] == 10
    assert dictionary["modular_period"] == 12
    assert dictionary["G2_dimension"] == 14


def test_common_input_modular_dimensions() -> None:
    summary = build_summary()
    common = summary["common_input_monomial_dictionary"]

    assert [common[w]["dim_M"] for w in [16, 20, 24, 36, 40]] == [2, 2, 3, 4, 4]
    assert common[16]["monomials"] == [(4, 0), (1, 2)]
    assert common[24]["monomials"] == [(6, 0), (3, 2), (0, 4)]
