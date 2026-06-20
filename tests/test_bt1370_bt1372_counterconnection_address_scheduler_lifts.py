#!/usr/bin/env python3
"""Regression tests for BT1370-BT1372."""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def run_script(relpath: str) -> None:
    subprocess.run([sys.executable, str(ROOT / relpath)], cwd=ROOT, check=True)


def load_json(relpath: str) -> dict:
    return json.loads((ROOT / relpath).read_text(encoding="utf-8"))


def test_bt1370_s3_counterconnection() -> None:
    run_script("analysis/bt1370_s3_counterconnection_phase_holonomy_correction.py")
    data = load_json("data/bt1370_s3_counterconnection_phase_holonomy_correction.json")
    assert data["verified"] is True
    assert data["phase_only_boundary"]["odd_quadrangle_holonomies"] == 29160
    assert data["full_s3_counterconnection"]["corrected_residual_profile"] == {
        "012": 540
    }
    assert data["full_s3_counterconnection"]["nonidentity_corrections"] == 380
    assert data["full_s3_counterconnection"]["transposition_corrections"] == 300
    assert data["full_s3_counterconnection"]["c3_corrections"] == 80


def test_bt1371_q6_tomotope_address_table() -> None:
    run_script("analysis/bt1371_q6_tomotope_explicit_orbit_address_table.py")
    data = load_json("data/bt1371_q6_tomotope_explicit_orbit_address_table.json")
    assert data["verified"] is True
    assert len(data["address_table"]) == 192
    assert len({row["q6_edge_index"] for row in data["address_table"]}) == 192
    assert data["checks"]["equivariance_holds_for_all_group_elements"] is True
    assert (
        data["source"]["tomotope_group"]["order_profile"]
        == data["source"]["q6_group"]["order_profile"]
    )


def test_bt1372_three_epoch_scheduler_lift() -> None:
    run_script("analysis/bt1372_three_epoch_steinberg_basis_scheduler_lift.py")
    data = load_json("data/bt1372_three_epoch_steinberg_basis_scheduler_lift.json")
    assert data["verified"] is True
    assert data["one_epoch_boundary"]["division"] == "2160 = 81 * 26 + 54"
    assert data["three_epoch_lift"]["identity"] == "3 * 2160 = 6480 = 81 * 80"
    assert data["three_epoch_lift"]["basis_count_profile"] == {"80": 81}
    assert data["three_epoch_lift"]["generation_counts"] == {
        "0": 2160,
        "1": 2160,
        "2": 2160,
    }
    assert data["checks"]["epoch_advance_commutes_with_generation_cycle"] is True


def test_bt1370_bt1372_docs_index_card_present() -> None:
    text = (ROOT / "docs" / "index.html").read_text(encoding="utf-8")
    assert (
        "BT1370&ndash;BT1372: counterconnection, Q6 address table, and three-epoch scheduler lift"
        in text
    )
    assert "BT1370_BT1372_counterconnection_address_scheduler_lifts.md" in text
    assert "29160" in text
    assert "3&times;2160 = 6480 = 81&times;80" in text


if __name__ == "__main__":
    test_bt1370_s3_counterconnection()
    test_bt1371_q6_tomotope_address_table()
    test_bt1372_three_epoch_scheduler_lift()
    test_bt1370_bt1372_docs_index_card_present()
    print("BT1370-BT1372 focused tests passed")
