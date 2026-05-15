from __future__ import annotations

import json
from pathlib import Path

from exploration.w33_tomotope_klitzing_partial_operation_commutation import (
    build_summary,
    commutation_table,
    partial_a_operation_counts_inferred,
    partial_b_operation_counts,
    write_summary,
)


def test_partial_b_operation_ladder_is_direct_klitzing_chain() -> None:
    assert partial_b_operation_counts() == (12, 24, 48, 96)


def test_partial_a_operation_ladder_is_sheet_lift() -> None:
    assert partial_a_operation_counts_inferred() == (24, 48, 96, 192)


def test_sheet_and_operation_commute_stagewise() -> None:
    table = commutation_table()
    assert len(table) == 3
    assert all(row["commutes"] for row in table)
    assert [row["S_of_O"] for row in table] == [48, 96, 192]
    assert [row["O_of_S"] for row in table] == [48, 96, 192]


def test_summary_exposes_inference_scope_and_checks() -> None:
    summary = build_summary()
    assert summary["status"] == "ok"
    assert summary["source_anchor"]["partial_a_operation_rows_present"] is False
    assert summary["source_anchor"]["directly_encoded_operation_rows"] == "mod_b"
    counts = summary["source_anchor"]["klitzing_command_evidence_counts"]
    samples = summary["source_anchor"]["klitzing_command_evidence_samples"]
    assert counts["rect_mod_b"] >= 1
    assert counts["trunc_mod_b"] >= 1
    assert counts["exp_mod_b"] >= 1
    assert counts["omni_mod_b"] >= 1
    assert "rect(mod_b(e(x3o3o *b4o)))" in samples["rect_mod_b"]
    assert "trunc(mod_b(e(x3o3o *b4o)))" in samples["trunc_mod_b"]
    assert "exp(mod_b(e(x3o3o *b4o)))" in samples["exp_mod_b"]
    assert "omni(mod_b(e(x3o3o *b4o)))" in samples["omni_mod_b"]
    assert counts["rect_mod_a"] == 0
    assert counts["trunc_mod_a"] == 0
    assert counts["exp_mod_a"] == 0
    assert counts["omni_mod_a"] == 0
    assert samples["rect_mod_a"] == ""
    assert samples["trunc_mod_a"] == ""
    assert samples["exp_mod_a"] == ""
    assert samples["omni_mod_a"] == ""
    assert summary["checks"]["seed_sheet_law_exact"] is True
    assert summary["checks"]["operation_ladder_b_is_doubling"] is True
    assert summary["checks"]["operation_ladder_a_is_sheet_lift"] is True
    assert summary["checks"]["sheet_operation_commute"] is True
    assert summary["checks"]["inferred_omnitruncated_a_hits_192"] is True
    assert summary["checks"]["direct_mod_b_commands_present_in_klitzing_dumps"] is True
    assert summary["checks"]["direct_mod_a_commands_absent_for_tomotope_symbol"] is True


def test_write_summary_emits_json(tmp_path: Path) -> None:
    out = write_summary(tmp_path / "w33_tomotope_klitzing_partial_operation_commutation_summary.json")
    data = json.loads(out.read_text(encoding="utf-8"))
    assert data["operation_ladders"]["partial_a_inferred"] == [24, 48, 96, 192]
