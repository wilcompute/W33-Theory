from exploration.w33_weight12_moonshine_gap_bridge import build_summary


def test_weight12_moonshine_gap_theorem() -> None:
    summary = build_summary()
    assert all(summary["weight12_moonshine_gap_theorem"].values())


def test_weight12_moonshine_gap_first_split() -> None:
    summary = build_summary()
    first = summary["weight12_moonshine_gap_dictionary"]["first_moonshine_split"]

    assert first["j_tilde_q2"] == 196884
    assert first["leech_shell_196560"] == 196560
    assert first["oscillator_gap_324"] == 324
    assert first["sum"] == 196884
    assert first["gap_factorizations"]["four_times_81"] == 324
    assert first["gap_factorizations"]["eighteen_squared"] == 324


def test_weight12_moonshine_gap_second_split() -> None:
    summary = build_summary()
    second = summary["weight12_moonshine_gap_dictionary"]["second_moonshine_split"]

    assert second["leech_q3_shell"] == 16773120
    assert second["cross_term_24_times_196560"] == 4717440
    assert second["pure_oscillator_residue_3200"] == 3200
    assert second["sum"] == 21493760
    assert second["j_tilde_q3"] == 21493760
