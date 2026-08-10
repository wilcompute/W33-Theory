import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def run_tool(script: str, data: str) -> dict:
    subprocess.run([sys.executable, str(ROOT / "tools" / script)], check=True, cwd=ROOT)
    return json.loads((ROOT / "data" / data).read_text(encoding="utf-8"))


def test_bt1489_s4_d4_v4_row_action_lift():
    result = run_tool(
        "bt1489_s4_d4_v4_row_action_lift.py",
        "bt1489_s4_d4_v4_row_action_lift.json",
    )
    assert result["verified"] is True
    assert result["counts"]["rows"] == 72
    assert result["counts"]["s4_branch_actions"] == 24
    assert result["counts"]["d4_branch_actions"] == 8
    assert result["counts"]["v4_translation_actions"] == 4
    assert result["row_action_profiles"]["s4_order_profile"] == {
        "1": 1,
        "2": 9,
        "3": 8,
        "4": 6,
    }
    assert result["checks"]["row_action_is_homomorphism"] is True
    assert result["checks"]["column_formula_preserved"] is True
    assert result["checks"]["shear_identity_fixes_all_72_rows_at_branch_layer"] is True


def test_bt1490_fano_e6_commuting_square():
    result = run_tool(
        "bt1490_fano_e6_commuting_square.py",
        "bt1490_fano_e6_commuting_square.json",
    )
    assert result["verified"] is True
    assert result["counts"] == {
        "commuting_product": 504,
        "e6_abi_rows": 72,
        "e6_h1_closure": 81,
        "fano_flag_bus": 168,
        "fano_point_bus": 168,
        "shared_fiber": 24,
    }
    assert result["checks"]["shared_fiber_matches_v4_times_row_values"] is True
    assert result["checks"]["shared_fiber_refactors_as_three_d4_flags"] is True
    assert result["checks"]["fano_168_is_twenty_one_flags_times_d4"] is True
    assert result["checks"]["point_fiber_to_flag_d4_is_bijective"] is True
    assert result["checks"]["commuting_square_paths_agree"] is True


def test_bt1491_paper_splice_v2_idempotent():
    first = run_tool(
        "bt1491_paper_splice_v2_idempotent.py",
        "bt1491_paper_splice_v2_idempotent.json",
    )
    second = run_tool(
        "bt1491_paper_splice_v2_idempotent.py",
        "bt1491_paper_splice_v2_idempotent.json",
    )
    assert first["verified"] is True
    assert second["verified"] is True
    assert second["splice"]["action"] == "unchanged"
    assert second["splice"]["after_marker_count"] == 1
    assert all(count == 1 for count in second["splice"]["input_counts"].values())
    main_tex = (ROOT / "photonic_holonet.tex").read_text(encoding="utf-8")
    assert "% BT1491 exact finite insert stack start" in main_tex
    assert main_tex.count(r"\input{analysis/BT1489_BT1491_holonet_insert}") == 1


def test_bt1489_bt1491_publication_anchors():
    analysis = (ROOT / "analysis" / "BT1489_BT1491_row_square_splice.md").read_text(
        encoding="utf-8"
    )
    insert = (ROOT / "analysis" / "BT1489_BT1491_holonet_insert.tex").read_text(
        encoding="utf-8"
    )
    focused = (ROOT / "scripts" / "run_focused_bridge_tests.py").read_text(
        encoding="utf-8"
    )
    docs = (ROOT / "docs" / "index.html").read_text(encoding="utf-8")

    assert "shared 24-state fiber" in analysis
    assert "BT1490 is the new finite-geometry lock" in insert
    assert "test_bt1489_bt1491_row_square_splicer.py" in focused
    assert "Fano/E6 ABI Fiber" in docs
    assert "168 = 7&middot;24 = 21&middot;8" in docs
