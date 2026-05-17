from __future__ import annotations

import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from verify_dcmii_projective_screen_bulk_qec_bridge import (  # noqa: E402
    DATA_PATH,
    RESULT_PATH,
    build_bridge,
    write_bridge,
)


def test_screen_bulk_split_rescues_pg23_without_replacing_w33() -> None:
    payload = build_bridge()
    summary = payload["summary"]
    ids = payload["identities"]
    layers = payload["typed_layers"]

    assert summary["part"] == "DCMII"
    assert summary["decimal"] == 902
    assert summary["pg3_points"] == 40
    assert summary["screen_points"] == 13
    assert summary["affine_bulk_points"] == 27
    assert summary["w33_vertices"] == 40
    assert summary["w33_edges"] == 240
    assert layers["projective_screen"]["points"] == 13
    assert layers["w33_closed_screen"]["points"] == 13
    assert ids["projective_space_splits_as_screen_plus_bulk"] is True
    assert ids["closed_screen_matches_pg2_cardinality"] is True
    assert ids["pg2_complete_graph_not_w33_screen_induced_graph"] is True


def test_affine_bulk_lifts_to_qec_tail_and_photonic_carrier() -> None:
    payload = build_bridge()
    qec = payload["typed_layers"]["qec_runtime"]
    affine = payload["typed_layers"]["affine_bulk"]
    ids = payload["identities"]

    assert affine["points"] == 27
    assert affine["ternary_lift"] == 81
    assert affine["nilpotent_double"] == 162
    assert qec["base_code"] == {"n": 240, "k": 81, "d_z": 4}
    assert qec["directed_carrier"] == 480
    assert qec["q4_routing_length"] == 1296
    assert qec["steane_phi6_length"] == 82320
    assert ids["affine_bulk_ternary_lift_is_h1"] is True
    assert ids["point_stabilizer_is_q4_packet_length"] is True


def test_center_partition_and_projective_share_are_exact() -> None:
    payload = build_bridge()
    partition = payload["center_partition"]
    shares = payload["shares"]
    ids = payload["identities"]

    assert partition["classes"] == {"center": 1, "screen_rim": 12, "affine_bulk": 27}
    assert partition["quotient_matrix"] == [[0, 12, 0], [1, 2, 9], [0, 4, 8]]
    assert partition["eigenvalues"] == [12, 2, -4]
    assert shares["screen_share"] == {"numerator": 3, "denominator": 13}
    assert shares["complement_share"] == {"numerator": 10, "denominator": 13}
    assert ids["quotient_matrix_is_center_partition"] is True
    assert ids["dressed_projective_share_is_screen_share"] is True


def test_bridge_reads_prior_screen_and_qec_anchors() -> None:
    payload = build_bridge()

    assert all(payload["anchors"].values())
    assert payload["identities"]["anchors_present"] is True
    assert payload["summary"]["all_identities_hold"] is True


def test_write_and_reload() -> None:
    data_path, result_path = write_bridge()
    assert data_path == DATA_PATH
    assert result_path == RESULT_PATH

    data = json.loads(data_path.read_text(encoding="utf-8"))
    result = json.loads(result_path.read_text(encoding="utf-8"))
    assert data["summary"]["all_identities_hold"] is True
    assert result["decimal"] == 902
    assert result["status"].startswith("VERIFIED")
