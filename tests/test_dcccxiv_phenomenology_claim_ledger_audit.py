from __future__ import annotations

import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from verify_dcccxiv_phenomenology_claim_ledger_audit import (  # noqa: E402
    OUT_PATH,
    build_audit,
    write_audit,
)


def test_ledger_is_contiguous_phenomenology_burst() -> None:
    payload = build_audit()
    summary = payload["summary"]

    assert summary["range_start"] == 784
    assert summary["range_end"] == 813
    assert summary["expected_result_count"] == 30
    assert summary["result_file_count"] == 30
    assert summary["markdown_file_count"] == 30
    assert payload["identities"]["result_ledger_is_contiguous_784_to_813"] is True
    assert payload["identities"]["all_result_decimals_are_unique"] is True


def test_status_classes_show_not_uniformly_proven() -> None:
    payload = build_audit()
    summary = payload["summary"]

    assert summary["claimed_proven_count"] > 0
    assert summary["prediction_count"] > 0
    assert summary["partial_count"] > 0
    assert summary["tension_count"] > 0
    assert summary["mixed_count"] > 0
    assert payload["identities"]["ledger_contains_mixed_or_non_proven_claims"] is True


def test_top_mass_sigma_status_mismatch_is_flagged() -> None:
    payload = build_audit()
    flags = payload["audit_flags"]

    top_flags = [
        flag
        for flag in flags
        if flag["kind"] == "sigma_status_mismatch" and flag.get("part") == "DCCCII"
    ]
    assert top_flags
    assert top_flags[0]["claimed_limit_sigma"] == 1.0
    assert top_flags[0]["max_sigma_in_payload"] >= 3.3
    assert payload["identities"]["top_mass_sigma_mismatch_is_detected"] is True


def test_master_verification_staleness_is_flagged() -> None:
    payload = build_audit()
    flags = payload["audit_flags"]

    stale = [flag for flag in flags if flag["kind"] == "stale_master_verification"]
    assert stale
    assert stale[0]["part"] == "DCCXCVIII"
    assert stale[0]["through_decimal"] == 797
    assert stale[0]["current_max_decimal"] == 813
    assert stale[0]["stale_by"] == 16
    assert payload["summary"]["master_verification_stale_by"] == 16


def test_theorem_boundary_and_public_index_exposure() -> None:
    payload = build_audit()
    index = (ROOT / "docs" / "index.html").read_text(encoding="utf-8")

    assert "Phenomenology Claim-Ledger Audit" in payload["theorem"]
    assert "does not validate the underlying phenomenological derivations" in payload["honesty_boundary"]
    assert "Phenomenology Claim-Ledger Audit" in index
    assert "<code>DCCLXXXIV-DCCCXIII</code>" in index
    assert "<code>DCCCII</code>" in index
    assert "<code>DCCXCVIII</code>" in index


def test_write_and_reload() -> None:
    out = write_audit()
    assert out == OUT_PATH

    data = json.loads(out.read_text(encoding="utf-8"))
    assert data["summary"]["all_identities_hold"] is True
    assert data["summary"]["audit_flag_count"] >= 2
