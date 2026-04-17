from exploration.w33_level3_source_flow_bridge import build_summary


def test_level3_source_flow_theorem() -> None:
    summary = build_summary()
    assert all(summary["level3_source_flow_theorem"].values())


def test_level3_source_coefficients() -> None:
    summary = build_summary()
    coeffs = summary["level3_source_dictionary"]["E2_level3_coefficients"]

    assert coeffs[:10] == [1, 12, 36, 12, 84, 72, 36, 96, 180, 12]


def test_delta3_mixed_source_flow() -> None:
    summary = build_summary()
    theorem = summary["level3_source_flow_theorem"]

    assert theorem[
        "the_first_level3_cusp_obeys_the_exact_mixed_source_flow_2qdDelta3_equals_E2_plus_E2level3_times_Delta3"
    ] is True
