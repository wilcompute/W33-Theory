from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import w33_pass79_full_closure as pass79


def test_pass79_full_closure_payload() -> None:
    payload = pass79.build_payload()
    assert payload["status"] == "PASS"
    assert all(payload["checks"].values())

    code = payload["track1_code_witness"]
    assert code["parameters"] == {
        "n": 66,
        "rank_stabilizer": 58,
        "k_logical": 8,
        "distance": 3,
    }
    assert code["canonical_geometric_code_claimed"] is False
    assert code["weight_1_2_errors_checked"] == 137808
    assert code["nonstabilizer_logical_weight_1_2_count"] == 0
    assert code["distance_verified"] is True

    edge = payload["track2_gap_edge_space"]
    assert edge["point_action"]["suborbit_sizes"] == [1, 12, 27]
    assert edge["directed_edge_action"]["degree"] == 480
    assert edge["directed_edge_action"]["rank"] == 24
    assert edge["directed_edge_action"]["dimension_sum"] == 480
    assert edge["undirected_edge_action"]["degree"] == 240
    assert edge["undirected_edge_action"]["rank"] == 10
    assert edge["undirected_edge_action"]["dimension_sum"] == 240

    terw = payload["track3_gap_terwilliger_wedderburn"]
    assert terw["dimension"] == 16
    assert terw["center_dimension"] == 5
    assert terw["radical_dimension"] == 0
    assert terw["component_dimensions"] == [1, 1, 1, 4, 9]
    assert terw["wedderburn_block_sizes"] == [1, 1, 1, 2, 3]

    spence = payload["track4_spence_hearing_table"]
    assert spence["graph_count"] == 28
    assert spence["all_srg_40_12_2_4"] is True
    assert spence["summary"]["W33_spence_index_candidate"] == 28
    assert spence["summary"]["Q43_spence_index_candidate"] == 27
    assert spence["summary"]["local_plus_alpha_classes"] == 27

    local_plus_alpha = next(
        row
        for row in spence["hearing_table"]
        if row["invariant"] == "local_histogram_plus_alpha"
    )
    assert local_plus_alpha["residual_non_singletons"] == [[20, 24]]


def test_pass79_json_result_matches_verifier_when_present() -> None:
    path = Path("w33_pass79_full_closure.json")
    if not path.exists():
        return
    payload = json.loads(path.read_text(encoding="utf-8"))
    assert payload["status"] == "PASS"
    assert payload["track3_gap_terwilliger_wedderburn"]["block_reading"] == (
        "Q + Q + Q + M_2(Q) + M_3(Q)"
    )


if __name__ == "__main__":
    test_pass79_full_closure_payload()
    test_pass79_json_result_matches_verifier_when_present()
