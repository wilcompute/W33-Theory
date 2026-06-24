import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def run_analysis(script: str, data_file: str) -> dict:
    subprocess.run(
        [sys.executable, str(ROOT / "analysis" / script)], check=True, cwd=ROOT
    )
    return json.loads((ROOT / "data" / data_file).read_text(encoding="utf-8"))


def test_bt1694_selects_asymmetric_dark_relic_branch():
    result = run_analysis(
        "bt1694_dark_asymmetric_relic_ratio.py",
        "bt1694_dark_asymmetric_relic_ratio.json",
    )

    assert result["verified"] is True
    assert result["symmetric_relic_check"]["mass_TeV"] > 30
    assert result["symmetric_relic_check"]["ratio_to_reference_dark_hadron"] > 1000
    assert result["abundance_ratio"]["Omega_DM"] == "4/15"
    assert result["abundance_ratio"]["Omega_b"] == "2/41"
    assert result["abundance_ratio"]["Omega_DM_over_Omega_b"] == "82/15"
    assert result["checks"]["ratio_lies_in_cosmic_coincidence_window"] is True


def test_bt1695_keeps_dark_braiding_as_finite_backbone():
    result = run_analysis(
        "bt1695_dark_anyon_braiding_gate_boundary.py",
        "bt1695_dark_anyon_braiding_gate_boundary.json",
    )

    assert result["verified"] is True
    assert result["group_order"] == 24
    assert len(result["conjugacy_classes"]) == 7
    assert result["D_2T_anyon_count"] == 42
    assert result["flux_order_lcm"] == 12
    assert result["derived_series_orders"] == [24, 8, 2, 1]
    assert result["checks"]["braiding_alone_universality_not_promoted"] is True


def test_bt1696_classifies_dscft_time_arrow_modes():
    result = run_analysis(
        "bt1696_dscft_time_arrow_modes.py",
        "bt1696_dscft_time_arrow_modes.json",
    )

    assert result["verified"] is True
    assert result["dimension"]["d"] == 4
    assert result["dimension"]["threshold"] == 2.25
    modes = {row["name"]: row for row in result["w33_laplacian_modes"]}
    assert modes["vacuum"]["series"] == "complementary"
    assert modes["matter_boundary"]["series"] == "principal"
    assert modes["bulk_isometry"]["series"] == "principal"
    assert modes["matter_boundary"]["complex_weights"] is True
    assert modes["bulk_isometry"]["complex_weights"] is True
    assert result["heawood_clock"]["von_neumann_entropy"] > 0


def test_bt1694_bt1696_publication_anchors():
    note = (ROOT / "analysis" / "BT1694_BT1696_dark_braiding_dscft_relic.md").read_text(
        encoding="utf-8"
    )
    docs = (ROOT / "docs" / "index.html").read_text(encoding="utf-8")
    focused = (ROOT / "scripts" / "run_focused_bridge_tests.py").read_text(
        encoding="utf-8"
    )

    assert "BT1694-BT1696" in note
    assert "82/15" in note
    assert "Dark Relic/Braiding/dS-CFT Boundary" in docs
    assert "test_bt1694_bt1696_dark_braiding_dscft_relic.py" in focused
