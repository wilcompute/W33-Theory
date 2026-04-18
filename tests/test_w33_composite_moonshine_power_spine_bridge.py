from exploration.w33_composite_moonshine_power_spine_bridge import build_summary


def test_composite_moonshine_power_spine_theorem() -> None:
    summary = build_summary()
    assert all(summary["composite_moonshine_power_spine_theorem"].values())


def test_composite_moonshine_power_spine_square_maps() -> None:
    rows = build_summary()["composite_moonshine_power_spine_dictionary"]["rows"]
    by_name = {row["class_name"]: row for row in rows}

    assert by_name["4A"]["square_inferred"] == "2B"
    assert by_name["6A"]["square_inferred"] == "3A"
    assert by_name["8A"]["square_inferred"] == "4C"
    assert by_name["10A"]["square_inferred"] == "5A"


def test_composite_moonshine_power_spine_power_maps() -> None:
    rows = build_summary()["composite_moonshine_power_spine_dictionary"]["rows"]
    by_name = {row["class_name"]: row for row in rows}

    assert by_name["4A"]["power_map"] == {2: "2B", 4: "1A"}
    assert by_name["6A"]["power_map"] == {2: "3A", 3: "2A", 6: "1A"}
    assert by_name["8A"]["power_map"] == {2: "4C", 4: "2B", 8: "1A"}
    assert by_name["10A"]["power_map"] == {2: "5A", 5: "2A", 10: "1A"}
