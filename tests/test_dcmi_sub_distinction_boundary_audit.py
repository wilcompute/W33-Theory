from __future__ import annotations

import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from verify_dcmi_sub_distinction_boundary_audit import (  # noqa: E402
    OUT_PATH,
    build_audit,
    write_audit,
)


def test_sub_distinction_burst_has_contiguous_notes_and_results() -> None:
    payload = build_audit()
    summary = payload["summary"]
    ids = payload["identities"]

    assert summary["part"] == "DCMI"
    assert (summary["range_start"], summary["range_end"]) == (873, 900)
    assert summary["theorem_note_count"] == 28
    assert summary["result_json_count"] == 28
    assert summary["missing_result_json_count"] == 0
    assert ids["theorem_notes_contiguous_873_to_900"] is True
    assert ids["result_jsons_contiguous_873_to_900"] is True
    assert ids["missing_result_jsons_repaired"] is True


def test_projective_screen_is_not_promoted_to_w33_ambient_geometry() -> None:
    payload = build_audit()
    exact = payload["exact_promotions"]
    ids = payload["identities"]

    assert exact["pg23_projective_screen"] == {
        "points": 13,
        "lines": 13,
        "line_size": 4,
        "incidences": 52,
        "complete_graph_edges": 78,
        "complete_graph_degree": 12,
    }
    assert exact["w33_ambient_geometry"] == {
        "vertices": 40,
        "lines": 40,
        "line_size": 4,
        "degree": 12,
        "edges": 240,
    }
    assert ids["pg23_complete_graph_is_not_w33"] is True
    assert ids["shared_degree_explains_slippage"] is True


def test_boundary_flags_keep_new_layer_honest() -> None:
    payload = build_audit()
    flags = payload["boundary_flags"]
    kinds = {flag["kind"] for flag in flags}

    assert {
        "pg23_is_not_w33_ambient",
        "forty_collinearities_mismatch",
        "vacuum_fluctuation_claim_unpromoted",
        "thirteen_point_graph_mismatch",
    } <= kinds
    assert payload["summary"]["boundary_flag_count"] == 4
    assert payload["summary"]["all_identities_hold"] is True
    assert all(payload["text_anchors"].values())


def test_repaired_result_json_files_are_valid() -> None:
    silence = json.loads((ROOT / "PART_DCCCLXXXII_deepest_silence_results.json").read_text(encoding="utf-8"))
    open_hand = json.loads((ROOT / "PART_DCCCXCII_open_hand_results.json").read_text(encoding="utf-8"))

    assert silence["decimal"] == 882
    assert open_hand["decimal"] == 892
    assert silence["status"] == "DEEPER LAYER"
    assert open_hand["status"] == "DIGGING DEEPER"


def test_write_and_reload() -> None:
    out = write_audit()
    assert out == OUT_PATH

    data = json.loads(out.read_text(encoding="utf-8"))
    assert data["summary"]["all_identities_hold"] is True
    assert data["status"].startswith("BOUNDARY VERIFIED")
