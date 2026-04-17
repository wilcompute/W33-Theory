from exploration.w33_modular_weight12_line_triad_bridge import build_summary


def test_weight12_line_triad_theorem() -> None:
    summary = build_summary()
    assert all(summary["weight12_line_triad_theorem"].values())


def test_weight12_line_triad_determinants() -> None:
    summary = build_summary()
    dictionary = summary["weight12_line_triad_dictionary"]

    assert dictionary["det_L_D"] == -12
    assert dictionary["det_I_D"] == -691
    assert dictionary["det_I_L"] == 455
    assert dictionary["det_I_L_factorization"]["product"] == 455


def test_weight12_line_triad_qseries_relations() -> None:
    summary = build_summary()
    qdict = summary["weight12_line_triad_qseries_dictionary"]

    assert qdict["12_Theta_Leech"] == qdict["7_E4_cubed_plus_5_E6_squared"]
    assert qdict["12_times_691_E12"] == qdict["691_times_12_Theta_Leech_plus_455_times_1728_Delta"]
