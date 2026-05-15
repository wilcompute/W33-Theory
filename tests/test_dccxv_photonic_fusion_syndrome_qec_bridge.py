from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from verify_dccxv_photonic_fusion_syndrome_qec_bridge import build_bridge


def test_dccxv_summary_closes_fusion_and_klm_budgets() -> None:
    payload = build_bridge()
    summary = payload["summary"]

    assert summary["local_attempt_alphabet"] == 12
    assert summary["accepted_bond_slots"] == 240
    assert summary["heralded_syndrome_slots"] == 240
    assert summary["fusion_attempts"] == 480
    assert summary["klm_primitives"] == 960
    assert summary["all_identities_hold"] is True


def test_dccxv_fusion_attempt_ledger_is_accepted_plus_heralded_return() -> None:
    payload = build_bridge()
    ledger = payload["fusion_attempt_ledger"]

    assert ledger["rows"]["accepted_w33_bonds"] == {
        "theta": 105,
        "transport": 135,
        "total": 240,
    }
    assert ledger["rows"]["heralded_return_syndrome"] == {
        "theta": 105,
        "transport": 135,
        "total": 240,
    }
    assert ledger["column_totals"] == {"theta": 210, "transport": 270, "total": 480}


def test_dccxv_klm_primitive_ledger_is_doubled_fusion_ledger() -> None:
    payload = build_bridge()
    fusion = payload["fusion_attempt_ledger"]["rows"]
    klm = payload["klm_primitive_ledger"]

    assert klm["rows"]["accepted_w33_bonds"]["total"] == 2 * fusion["accepted_w33_bonds"]["total"]
    assert (
        klm["rows"]["heralded_return_syndrome"]["total"]
        == 2 * fusion["heralded_return_syndrome"]["total"]
    )
    assert klm["column_totals"] == {"theta": 420, "transport": 540, "total": 960}


def test_dccxv_local_to_global_lift_matches_qec_ouroboros() -> None:
    payload = build_bridge()
    lift = payload["local_to_global"]

    assert lift["vertices"] == 40
    assert lift["local_signed_clifford_slots"] == 6
    assert lift["local_a2_weyl_return_slots"] == 6
    assert lift["accepted_bond_slots"] == 40 * 6 == 240
    assert lift["heralded_syndrome_slots"] == 40 * 6 == 240
    assert lift["fusion_attempt_slots"] == 40 * 12 == 480
    assert lift["klm_primitive_slots"] == 40 * 24 == 960


def test_dccxv_qec_absorption_preserves_h1() -> None:
    payload = build_bridge()
    qec = payload["qec_absorption"]

    assert qec["edge_qubit_carrier"] == 240
    assert qec["vertex_check_rank"] + qec["triangle_check_rank"] == 159
    assert qec["vertex_check_rank"] + qec["triangle_check_rank"] + qec["logical_h1"] == 240
    assert qec["logical_h1"] == 81
    assert "H1=81" in qec["protected_read"]


def test_dccxv_theorem_boundary_blocks_overclaim() -> None:
    payload = build_bridge()

    assert "photonic fusion nondeterminism is native" in payload["theorem"]
    assert "does not prove a physical loss threshold" in payload["honesty_boundary"]
    assert all(payload["identities"].values())


def test_dccxv_index_exposes_fusion_syndrome_bridge() -> None:
    text = (ROOT / "docs" / "index.html").read_text(encoding="utf-8")

    assert "Photonic Fusion-Syndrome\n              QEC Bridge" in text
    assert "<code>240</code> accepted W33 bond slots plus" in text
    assert "<code>420+540=960</code> lift" in text
