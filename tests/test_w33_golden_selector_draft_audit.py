from scripts.w33_golden_selector_draft_audit import build_draft_selector_obstruction_summary


def test_draft_certificate_fails_on_its_flatness_assertion() -> None:
    summary = build_draft_selector_obstruction_summary()
    failure = summary["draft_certificate_failure"]

    assert failure == {
        "exception_type": "AssertionError",
        "message": "Flatness FAILED: 864 violations in 12960 quads",
        "expected_message": "Flatness FAILED: 864 violations in 12960 quads",
    }


def test_draft_transport_data_is_constructed_before_failure() -> None:
    summary = build_draft_selector_obstruction_summary()

    assert summary["transport_data"] == {
        "line_count": 40,
        "transport_edge_count": 480,
    }


def test_draft_selector_failure_sits_on_the_nonlocal_carrier() -> None:
    summary = build_draft_selector_obstruction_summary()

    assert summary["quadrangle_audit"] == {
        "total_quadrangles_checked": 12960,
        "flatness_violations": 864,
        "local_quadrangles_checked": 0,
        "local_flatness_violations": 0,
        "nonlocal_quadrangles_checked": 12960,
        "nonlocal_flatness_violations": 864,
    }


def test_draft_selector_theorem_records_the_live_frontier_correctly() -> None:
    summary = build_draft_selector_obstruction_summary()

    assert summary["theorem"] == {
        "draft_selector_certificate_currently_fails": True,
        "draft_failure_is_the_flatness_assertion": True,
        "draft_selector_is_not_a_flat_c2_connection": True,
        "draft_flatness_failure_lives_on_the_nonlocal_quadrangle_carrier": True,
        "draft_local_sign_rule_does_not_close_the_live_supplement_m_frontier": True,
    }
    assert "864 of the 12960 nonlocal quadrangles" in summary["interpretation"]