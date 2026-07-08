from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import w33_pass80_native_k12_edge_vm as pass80


def test_pass80_native_k12_edge_vm_payload() -> None:
    payload = pass80.build_payload()
    assert payload["status"] == "PASS"
    assert all(payload["checks"].values())

    native = payload["track1_native_k12_code"]
    assert native["parameters"] == {
        "n": 66,
        "rank_x": 11,
        "rank_z": 47,
        "rank_sum": 58,
        "k_logical": 8,
        "distance": 3,
    }
    assert native["verified"] is True
    assert native["checks"]["all_edges_covered_by_triangle_checks"] is True

    edge = payload["track2_edge_zeta_factor_table"]
    assert edge["hashimoto_degree"] == 480
    assert edge["directed_edge_dimension"] == 480
    assert [row["degree"] for row in edge["factor_table"]] == [400, 2, 48, 30]

    spence = payload["track3_spence_residual_separator"]
    assert spence["prior_residual_pair"] == [20, 24]
    assert spence["separates_pair"] is True
    assert spence["total_6_subsets_per_graph"] == 3838380
    assert spence["difference_count"] == 20

    vm = payload["track4_terwilliger_vm_isa"]
    assert vm["micro_op_count"] == 16
    assert vm["channel_counts"] == {"Q": 3, "M2(Q)": 4, "M3(Q)": 9}
    assert all(vm["checks"].values())

    decoder = payload["track5_syndrome_decoder"]
    assert decoder["single_error_syndrome_count"] == 528
    assert decoder["all_single_errors_corrected"] is True


def test_pass80_json_result_when_present() -> None:
    path = Path("w33_pass80_native_k12_edge_vm.json")
    if not path.exists():
        return
    payload = json.loads(path.read_text(encoding="utf-8"))
    assert payload["status"] == "PASS"
    assert payload["track3_spence_residual_separator"]["separates_pair"] is True


if __name__ == "__main__":
    test_pass80_native_k12_edge_vm_payload()
    test_pass80_json_result_when_present()
