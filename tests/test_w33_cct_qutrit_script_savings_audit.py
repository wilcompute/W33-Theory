from __future__ import annotations

from scripts.w33_cct_qutrit_script_savings_audit import (
    build_qutrit_script_savings_audit,
)


def _record_by_path(summary: dict[str, object], path: str) -> dict[str, object]:
    for record in summary["records"]:
        if record["path"] == path:
            return record
    raise AssertionError(f"missing qutrit/quasicrystal-script record for {path}")


def test_qutrit_script_savings_audit_finds_relevant_scripts() -> None:
    summary = build_qutrit_script_savings_audit()

    assert summary["inventory"]["audited_script_count"] >= 5
    assert summary["theorem"]["relevant_scripts_were_scanned"] is True
    assert summary["theorem"]["two_qutrit_pauli_script_is_detected"] is True
    assert (
        summary["theorem"][
            "scripts_have_actionable_quasicrystal_trit_savings_classification"
        ]
        is True
    )


def test_quasicrystal_trit_savings_bridge_is_complete_against_corrected_rule() -> None:
    summary = build_qutrit_script_savings_audit()
    record = _record_by_path(
        summary, "scripts/w33_cct_quasicrystal_trit_savings_audit.py"
    )

    assert record["alignment"] == "complete_cct_quasicrystal_trit_savings_spine"
    assert record["criteria"] == {
        "qutrit_core_language": True,
        "two_qutrit_w33_bridge": True,
        "quasicrystal_carrier": True,
        "empire_possibility_windows": True,
        "least_change_trit_savings_rule": True,
        "neighbor_clock_packet": True,
    }


def test_qutrit_core_bridge_is_owner_but_not_full_trit_savings_rule() -> None:
    summary = build_qutrit_script_savings_audit()
    record = _record_by_path(summary, "scripts/w33_cct_qutrit_core_bridge_audit.py")

    assert record["alignment"] == (
        "qutrit_w33_core_missing_quasicrystal_trit_savings_layer"
    )
    assert record["criteria"]["qutrit_core_language"] is True
    assert record["criteria"]["two_qutrit_w33_bridge"] is True
    assert record["criteria"]["quasicrystal_carrier"] is False
    assert record["criteria"]["least_change_trit_savings_rule"] is False


def test_two_qutrit_pauli_script_has_core_but_needs_quasicrystal_layer() -> None:
    summary = build_qutrit_script_savings_audit()
    record = _record_by_path(summary, "scripts/w33_two_qutrit_pauli.py")

    assert record["alignment"] == (
        "qutrit_w33_core_missing_quasicrystal_trit_savings_layer"
    )
    assert record["criteria"]["qutrit_core_language"] is True
    assert record["criteria"]["two_qutrit_w33_bridge"] is True
    assert record["criteria"]["quasicrystal_carrier"] is False


def test_priority_gaps_are_reported_as_paths() -> None:
    summary = build_qutrit_script_savings_audit()
    gaps = summary["priority_gaps"]

    assert isinstance(
        gaps["qutrit_w33_core_scripts_missing_quasicrystal_trit_savings_layer"],
        tuple,
    )
    assert isinstance(
        gaps["quasicrystal_savings_scripts_missing_w33_qutrit_bridge"], tuple
    )
    assert isinstance(gaps["partial_context_scripts_needing_manual_review"], tuple)
