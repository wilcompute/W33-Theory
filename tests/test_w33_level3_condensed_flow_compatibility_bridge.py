from exploration.w33_level3_condensed_flow_compatibility_bridge import build_summary


def test_flow_compatibility_theorem() -> None:
    summary = build_summary()
    assert all(summary["flow_compatibility_theorem"].values())


def test_condensed_e4_starts_classically() -> None:
    summary = build_summary()
    e4 = summary["level3_condensed_dictionary"]["E4_condensed"]
    assert e4[:6] == [1, 240, 2160, 6720, 17520, 30240]


def test_condensed_e6_starts_classically() -> None:
    summary = build_summary()
    e6 = summary["level3_condensed_dictionary"]["E6_condensed"]
    assert e6[:6] == [1, -504, -16632, -122976, -532728, -1575504]
