from w33_mass_gap_operator_ladder_bridge import (
    build_mass_gap_operator_ladder_summary,
)


def test_operator_ladder_dictionary_is_exact() -> None:
    summary = build_mass_gap_operator_ladder_summary()
    ladder = summary["operator_ladder_dictionary"]
    gaps = ladder["gap_dictionary"]
    dirac = ladder["dirac_positive_scales"]
    color = ladder["color_side_dictionary"]

    assert ladder["adjacency_spectrum"] == {"-4": 15, "2": 24, "12": 1}
    assert ladder["laplacian_spectrum"] == {"0": 1, "10": 24, "16": 15}
    assert ladder["yang_mills_action_spectrum"] == {"0": 1, "100": 24, "256": 15}

    assert dirac["lowest_formula"] == "sqrt(Phi_4) = sqrt(10)"
    assert dirac["higher_formula"] == "sqrt(16) = 4"
    assert dirac["lowest_radicand"] == 10
    assert dirac["higher_integer_branch"] == 4

    assert gaps["laplacian_gap_formula"] == "gap(L) = Phi_4 = 10"
    assert gaps["dirac_gap_formula"] == "gap(|D|) = sqrt(Phi_4) = sqrt(10)"
    assert gaps["yang_mills_gap_formula"] == "gap(H_YM) = Phi_4^2 = 100"
    assert gaps["normalized_gap_formula"] == "gap(L/k) = Phi_4 / k = 5/6"
    assert gaps["laplacian_gap"] == 10
    assert gaps["yang_mills_gap"] == 100
    assert gaps["normalized_gap"]["exact"] == "5/6"

    assert color["q"] == 3
    assert color["phi4"] == 10
    assert color["color_adjoint_dim"] == 8
    assert color["lambda"] == 2
    assert color["phi4_equals_color_adjoint_plus_lambda"] is True


def test_operator_ladder_factorizations_all_hold() -> None:
    summary = build_mass_gap_operator_ladder_summary()
    assert all(summary["exact_factorizations"].values())
