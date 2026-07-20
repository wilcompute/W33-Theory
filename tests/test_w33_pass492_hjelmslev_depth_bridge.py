from analysis.w33_pass492_hjelmslev_depth_bridge import (
    build_payload,
    candidate_depth,
    p1_local_count,
)


def test_local_projective_line_counts():
    assert p1_local_count(3, 1) == 4
    assert p1_local_count(3, 2) == 12
    assert p1_local_count(5, 1) == 6
    assert p1_local_count(5, 2) == 30


def test_observed_depths_and_predictions():
    assert candidate_depth(3, 2) == 12
    assert candidate_depth(5, 2) == 30
    assert candidate_depth(3, 3) == 36
    assert candidate_depth(7, 2) == 56
    assert candidate_depth(5, 3) == 150
    assert candidate_depth(3, 4) == 108


def test_payload_passes_and_is_fail_closed():
    payload = build_payload()
    assert payload["status"] == "PASS"
    assert all(payload["checks"].values())
    assert all(row["status"] == "PREREGISTERED_UNMEASURED" for row in payload["preregistered_falsifiers"])
    assert "remains a conjecture" in payload["boundary"]
