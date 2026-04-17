from exploration.w33_modular_generator_packet_bridge import build_summary


def test_modular_generator_packet_bridge_theorem() -> None:
    summary = build_summary()
    assert all(summary["modular_generator_packet_theorem"].values())


def test_modular_generator_packet_dictionary() -> None:
    summary = build_summary()
    dictionary = summary["modular_generator_packet_dictionary"]

    assert dictionary["E4_weight"] == 4
    assert dictionary["E6_weight"] == 6
    assert dictionary["Phi_4_packet"] == 10
    assert dictionary["modular_period"] == 12
    assert dictionary["corrected_24_packet"] == 24


def test_monomial_collision_dictionary() -> None:
    summary = build_summary()
    monomials = summary["monomial_dictionary"]

    assert monomials["weight_10_monomials"] == [(1, 1)]
    assert monomials["weight_12_monomials"] == [(3, 0), (0, 2)]
    assert monomials["dim_M_10"] == 1
    assert monomials["dim_M_12"] == 2
