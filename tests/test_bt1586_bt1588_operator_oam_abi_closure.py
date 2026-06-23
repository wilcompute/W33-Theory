import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def run_tool(script: str, data: str, *args: str) -> dict:
    subprocess.run(
        [sys.executable, str(ROOT / "tools" / script), *args], check=True, cwd=ROOT
    )
    return json.loads((ROOT / "data" / data).read_text(encoding="utf-8"))


def test_bt1586_full_appendix_splicer_is_applied_and_idempotent():
    result = run_tool(
        "bt1586_operator_oam_full_appendix_splicer.py",
        "bt1586_operator_oam_full_appendix_splicer.json",
        "--apply",
    )
    paper = (ROOT / "photonic_holonet.tex").read_text(encoding="utf-8")

    assert result["verified"] is True
    assert result["applied"] is True
    assert result["insert_count"] == 10
    assert result["checks"]["idempotent_second_pass"] is True
    assert "% BT1586 OPERATOR_OAM_FULL_APPENDIX BEGIN" in paper
    assert r"\input{analysis/BT1586_BT1588_holonet_insert.tex}" in paper
    assert r"\input{analysis/BT1589_BT1591_holonet_insert.tex}" in paper
    assert r"\input{analysis/BT1592_BT1594_holonet_insert.tex}" in paper
    assert r"\input{analysis/BT1595_BT1597_holonet_insert.tex}" in paper


def test_bt1587_oam_recenter_transaction_abi_counts():
    result = run_tool(
        "bt1587_oam_recenter_transaction_abi.py",
        "bt1587_oam_recenter_transaction_abi.json",
    )
    assert result["verified"] is True
    assert result["counts"]["affine_internal_actions"] == 216
    assert result["counts"]["centered_transaction_words"] == 24
    assert result["counts"]["translations"] == 9
    assert result["counts"]["one_operation_ticks"] == 15552
    assert result["counts"]["five_witness_ticks"] == 77760
    assert result["class_counts"] == {
        "centered_frame": 24,
        "mixed_shift_phase": 96,
        "oam_shift_only": 48,
        "phase_shift_only": 48,
    }
    assert result["checks"]["each_word_reused_nine_times"] is True


def test_bt1588_literature_claim_firewall_keeps_sources_as_guardrails():
    run_tool(
        "bt1587_oam_recenter_transaction_abi.py",
        "bt1587_oam_recenter_transaction_abi.json",
    )
    result = run_tool(
        "bt1588_oam_literature_claim_firewall.py",
        "bt1588_oam_literature_claim_firewall.json",
    )
    assert result["verified"] is True
    assert len(result["sources"]) == 4
    assert result["checks"]["claim_ledger_has_three_blocked"] is True
    assert "oam_multiplexing_natphot_2026" in {
        source["key"] for source in result["sources"]
    }
    assert all(source["blocked_use"] for source in result["sources"])


def test_bt1586_bt1588_publication_anchors():
    paper = (ROOT / "photonic_holonet.tex").read_text(encoding="utf-8")
    insert = (ROOT / "analysis" / "BT1586_BT1588_holonet_insert.tex").read_text(
        encoding="utf-8"
    )
    docs = (ROOT / "docs" / "index.html").read_text(encoding="utf-8")
    focused = (ROOT / "scripts" / "run_focused_bridge_tests.py").read_text(
        encoding="utf-8"
    )

    assert "216 = 9\\cdot24" in insert
    assert "BT1586 OPERATOR_OAM_FULL_APPENDIX BEGIN" in paper
    assert "Operator/OAM ABI Closure" in docs
    assert "test_bt1586_bt1588_operator_oam_abi_closure.py" in focused
