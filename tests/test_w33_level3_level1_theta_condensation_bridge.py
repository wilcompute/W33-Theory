from exploration.w33_level3_level1_theta_condensation_bridge import build_summary


def test_condensation_theorem() -> None:
    summary = build_summary()
    assert all(summary["condensation_theorem"].values())


def test_e4_and_e6_condensation_formulas() -> None:
    summary = build_summary()
    dictionary = summary["level1_condensation_dictionary"]

    assert dictionary["E4_formula"] == "E4 = 4*theta_{A2 E6} - 3*theta_{A2^4}"
    assert dictionary["E6_formula"] == "E6 = 9*theta_{A2^6} - 6*theta_{A2^3 E6} - 2*theta_{E6^2}"


def test_weight12_triad_condenses() -> None:
    summary = build_summary()
    w12 = summary["weight12_condensation_dictionary"]

    assert w12["D_condensed"][:4] == [0, 1728, -41472, 435456]
    assert w12["L_condensed"][:4] == [12, 0, 2358720, 201277440]
    assert w12["I_condensed"][:4] == [691, 65520, 134250480, 11606736960]
