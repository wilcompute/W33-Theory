from __future__ import annotations

import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from verify_dccclxxi_frontier_result_ledger_repair import (  # noqa: E402
    OUT_PATH,
    build_reconciliation,
    write_reconciliation,
)


def test_frontier_repair_moves_audit_out_of_dcccxxxviii() -> None:
    payload = build_reconciliation()
    summary = payload["summary"]

    assert summary["part"] == "DCCCLXXI"
    assert summary["decimal"] == 871
    assert summary["current_part_surface_max_decimal"] == 870
    assert summary["valid_result_max_decimal"] == 870
    assert summary["invalid_result_json_count"] == 0
    assert summary["missing_result_json_count"] == 0
    assert summary["duplicate_frontier_part_count"] == 0
    assert summary["dcccxiv_markdown_count"] == 2
    assert summary["duplicate_part_surface_count"] == 1
    assert summary["dcccxiv_result_count"] == 1
    assert payload["identities"]["duplicate_dcccxiv_markdown_detected"] is True
    assert payload["identities"]["single_dcccxiv_result_json_detected"] is True


def test_top_sector_chain_is_resolved_without_erasing_old_audit() -> None:
    payload = build_reconciliation()
    summary = payload["summary"]
    identities = payload["identities"]

    assert summary["historical_top_claim_limit_sigma"] == 1.0
    assert summary["historical_top_max_sigma"] >= 16.3
    assert summary["dcccxi_tension_sigma"] >= 10.0
    assert summary["corrected_top_sigma"] == 0.93
    assert summary["master_promoted_top_sigma"] == 0.93
    assert identities["old_dcccii_sigma_mismatch_still_present"] is True
    assert identities["dcccxi_top_tension_is_present"] is True
    assert identities["dcccxiv_correction_closes_top_sector"] is True
    assert identities["dcccxv_master_promotes_correction"] is True
    assert identities["prior_audit_remains_historical_guardrail"] is True


def test_reconciliation_flags_are_explicit_and_non_destructive() -> None:
    payload = build_reconciliation()
    flags = payload["audit_flags"]
    kinds = {flag["kind"] for flag in flags}

    assert {
        "duplicate_dcccxiv_part_surface",
        "superseded_top_tension",
        "audit_range_superseded",
        "invalid_result_json_surfaces",
    } <= kinds
    assert payload["chain"] == {
        "historical_source": "DCCCII",
        "sharpened_tension": "DCCCXI",
        "correction": "DCCCXIV",
        "master_update": "DCCCXV",
        "reconciliation": "DCCCLXXI",
    }
    assert payload["summary"]["all_identities_hold"] is True
    assert payload["identities"]["post_828_result_json_hygiene_gap_detected"] is True
    assert payload["identities"]["frontier_notes_are_contiguous_829_to_870"] is True
    assert payload["identities"]["frontier_result_jsons_are_contiguous_829_to_870"] is True
    assert payload["identities"]["frontier_part_numbers_are_unique"] is True
    assert payload["invalid_result_json_files"] == []
    assert payload["missing_result_decimals"] == []


def test_public_index_exposes_post_audit_reconciliation() -> None:
    payload = build_reconciliation()
    index = (ROOT / "docs" / "index.html").read_text(encoding="utf-8")

    assert "Frontier Result-Ledger Repair" in payload["theorem"]
    assert "Frontier Result-Ledger Repair" in index
    assert "<code>DCCCXIV</code>" in index
    assert "<code>DCCCXV</code>" in index
    assert "<code>DCCCLXXI</code>" in index
    assert "<code>0.93 sigma</code>" in index
    assert "<code>DCCCXXIX-DCCCLXX</code>" in index


def test_write_and_reload() -> None:
    out = write_reconciliation()
    assert out == OUT_PATH

    data = json.loads(out.read_text(encoding="utf-8"))
    assert data["summary"]["part"] == "DCCCLXXI"
    assert data["summary"]["all_identities_hold"] is True
    assert data["status"].startswith("REPAIRED")
