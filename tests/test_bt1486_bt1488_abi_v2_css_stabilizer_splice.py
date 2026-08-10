import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def run_tool(script: str, data: str) -> dict:
    subprocess.run([sys.executable, str(ROOT / "tools" / script)], check=True, cwd=ROOT)
    return json.loads((ROOT / "data" / data).read_text(encoding="utf-8"))


def test_bt1484_e6_dag_claim_table_v2_rerunnable():
    result = run_tool(
        "bt1484_e6_dag_claim_table_v2.py",
        "bt1484_e6_dag_claim_table_v2.json",
    )
    assert result["verified"] is True
    assert len(result["rows"]) == 14
    assert result["checks"]["has_72_node"] is True
    assert result["checks"]["has_81_node"] is True
    assert result["checks"]["has_c3_v4_node"] is True


def test_bt1486_retwined_css_from_abi_v2():
    result = run_tool(
        "bt1486_retwined_css_from_abi_v2.py",
        "bt1486_retwined_css_from_abi_v2.json",
    )
    assert result["verified"] is True
    assert result["counts"]["rows"] == 72
    assert result["counts"]["active_rows"] == 24
    assert result["counts"]["guard_rows"] == 48
    assert result["counts"]["moved_guard_value_rows"] == 24
    assert result["css"] == {
        "k": 81,
        "rank_hx": 39,
        "rank_hz": 120,
        "retwined_rule": "BT1425 guard-tail permutation on both HX and HZ",
    }
    assert result["axis_profiles"]["channel_rows"] == {"P0": 24, "P1": 24, "P2": 24}
    assert result["axis_profiles"]["triangle_rows"] == {
        "T0": 18,
        "T1": 18,
        "T2": 18,
        "T3": 18,
    }
    assert result["checks"]["x_syndromes_equivariant"] is True
    assert result["checks"]["z_syndromes_equivariant"] is True


def test_bt1487_v4_triangle_stabilizer_classifier():
    result = run_tool(
        "bt1487_v4_triangle_stabilizer_classifier.py",
        "bt1487_v4_triangle_stabilizer_classifier.json",
    )
    assert result["verified"] is True
    assert result["groups"]["triangle_partition_stabilizer"]["order"] == 24
    assert result["groups"]["d4_square_subgroup"]["order"] == 8
    assert result["groups"]["d4_square_subgroup"]["order_profile"] == {
        "1": 1,
        "2": 5,
        "4": 2,
    }
    assert result["checks"]["fano_point_stabilizer_reads_7_times_s4"] is True
    assert result["checks"]["fano_flag_stabilizer_reads_21_times_d4"] is True
    assert result["checks"]["tau4_is_d4_translation"] is True


def test_bt1488_paper_splice_v2_manifest():
    result = run_tool(
        "bt1488_paper_splice_v2_manifest.py",
        "bt1488_paper_splice_v2_manifest.json",
    )
    assert result["verified"] is True
    assert [row["order"] for row in result["cascade"]] == list(range(1, 9))
    assert result["cascade"][1]["name"] == "claim_dependency_table_v2"
    assert result["cascade"][1]["insert"] == "analysis/BT1484_e6_dag_claim_table_v2.tex"
    assert result["cascade"][1]["replaces"] == "analysis/BT1472_dag_claim_table.tex"
    preferred = result["preferred_exact_finite_insert_packet"]
    assert "BT1474_css_join_proof_table" in preferred
    assert "BT1480_tensor_product_grid_reading" in preferred
    assert "BT1482_closure_abi_v2" in preferred
    assert "BT1486_retwined_css_from_abi_v2" in preferred
    assert "BT1487_v4_triangle_stabilizer_classifier" in preferred
    assert result["cascade"][-1]["name"] == "rendered_equation_fill"
    assert "blocked" in result["cascade"][-1]["status"]


def test_bt1486_bt1488_publication_anchors():
    analysis = (
        ROOT / "analysis" / "BT1486_BT1488_abi_v2_css_stabilizer_splice.md"
    ).read_text(encoding="utf-8")
    insert = (ROOT / "analysis" / "BT1486_BT1488_holonet_insert.tex").read_text(encoding="utf-8")
    manifest = (ROOT / "analysis" / "BT1488_paper_splice_v2_manifest.md").read_text(encoding="utf-8")
    focused = (ROOT / "scripts" / "run_focused_bridge_tests.py").read_text(encoding="utf-8")

    assert "Fano-native" in analysis
    assert "BT1486 reruns the CSS join" in insert
    assert "BT1484 is the preferred claim table" in manifest
    assert "test_bt1486_bt1488_abi_v2_css_stabilizer_splice.py" in focused
