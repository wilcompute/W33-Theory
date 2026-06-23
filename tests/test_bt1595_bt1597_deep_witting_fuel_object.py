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


def test_bt1595_bijects_witting_reject_shell_to_oam_hesse_loop():
    run_tool(
        "bt1594_hesse_t_universality_witness_loop.py",
        "bt1594_hesse_t_universality_witness_loop.json",
    )
    result = run_tool(
        "bt1595_witting_matter_fuel_bijection.py",
        "bt1595_witting_matter_fuel_bijection.json",
    )

    assert result["verified"] is True
    assert result["counts"]["fuel_segments"] == 1080
    assert result["counts"]["ticks"] == 77760
    assert result["identity"]["per_gate_refinement"] == (
        "9*24 = 216 = 8 Witting source rays * 27 incompatible targets"
    )
    assert set(result["histograms"]["gate_segments"].values()) == {216}
    assert set(result["histograms"]["source_reject_pairs"].values()) == {27}
    assert result["checks"]["fuel_rows_biject_reject_pairs"] is True


def test_bt1596_runtime_economy_splits_control_and_fuel_rails():
    run_tool(
        "bt1595_witting_matter_fuel_bijection.py",
        "bt1595_witting_matter_fuel_bijection.json",
    )
    result = run_tool(
        "bt1596_contextual_runtime_economy_ledger.py",
        "bt1596_contextual_runtime_economy_ledger.json",
    )

    assert result["verified"] is True
    assert result["ordered_pair_counts"] == {
        "same": 40,
        "compatible_distinct": 480,
        "accepted": 520,
        "contextual_fuel": 1080,
        "total": 1600,
    }
    assert result["runtime_ledger"]["accepted_communication"]["ticks"] == 37440
    assert result["runtime_ledger"]["contextual_fuel"]["ticks"] == 77760
    assert result["runtime_ledger"]["complete_witting_pair_cycle"]["ticks"] == 115200
    assert result["ratios"]["accepted_to_fuel"] == "13/27"


def test_bt1597_universal_transaction_object_packages_the_architecture():
    run_tool(
        "bt1596_contextual_runtime_economy_ledger.py",
        "bt1596_contextual_runtime_economy_ledger.json",
    )
    result = run_tool(
        "bt1597_universal_transaction_object.py",
        "bt1597_universal_transaction_object.json",
    )

    assert result["verified"] is True
    assert result["ticks"] == {
        "accepted_control": 37440,
        "contextual_fuel": 77760,
        "complete_cycle": 115200,
    }
    assert result["universal_transaction_identity"]["fuel_refinement"] == (
        "1080 = 5 gates * 9 OAM sectors * 24 words = 40 rays * 27 incompatible targets"
    )
    assert result["checks"]["non_clifford_port_required"] is True
    assert result["checks"]["deterministic_kernel_not_universal_alone"] is True


def test_bt1595_bt1597_publication_anchors():
    run_tool(
        "bt1586_operator_oam_full_appendix_splicer.py",
        "bt1586_operator_oam_full_appendix_splicer.json",
        "--apply",
    )
    paper = (ROOT / "photonic_holonet.tex").read_text(encoding="utf-8")
    insert = (ROOT / "analysis" / "BT1595_BT1597_holonet_insert.tex").read_text(
        encoding="utf-8"
    )
    docs = (ROOT / "docs" / "index.html").read_text(encoding="utf-8")
    focused = (ROOT / "scripts" / "run_focused_bridge_tests.py").read_text(
        encoding="utf-8"
    )

    assert "BT1595_BT1597_holonet_insert.tex" in paper
    assert "40\\cdot27" in insert
    assert "Witting Fuel Transaction Object" in docs
    assert "test_bt1595_bt1597_deep_witting_fuel_object.py" in focused
