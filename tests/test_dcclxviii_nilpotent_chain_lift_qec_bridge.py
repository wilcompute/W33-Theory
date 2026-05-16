"""Part DCCLXVIII -- nilpotent chain-lift / QEC bridge tests."""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from verify_dcclxviii_nilpotent_chain_lift_qec_bridge import (  # noqa: E402
    FUSION_EXPECTED,
    H1_EXPECTED,
    KLM,
    OUT_PATH,
    boundary_commutation_data,
    boundary_matrices,
    build_bridge,
    chain_homology_data,
    lifted_chain_data,
    nilpotent_chain_data,
    write_bridge,
)


def test_base_oriented_chain_complex_counts_and_ranks() -> None:
    data = chain_homology_data()

    assert data["chain_dimensions"] == {"C0": 40, "C1": 240, "C2": 160}
    assert data["boundary_ranks"] == {"rank_d1": 39, "rank_d2": 120}
    assert data["homology_dimensions"] == {"H0": 1, "H1": 81, "H2": 40}
    assert data["euler_characteristic"] == -40
    assert data["d1_d2_is_zero"] is True


def test_boundary_matrix_shapes_are_w33_chain_shapes() -> None:
    matrices = boundary_matrices()

    assert matrices["d1"].shape == (40, 240)
    assert matrices["d2"].shape == (240, 160)
    assert matrices["composition"].shape == (40, 160)


def test_dual_number_lift_doubles_chains_and_homology() -> None:
    data = lifted_chain_data()

    assert data["lifted_chain_dimensions"] == {"C0": 80, "C1": 480, "C2": 320}
    assert data["lifted_boundary_ranks"] == {"rank_d1": 78, "rank_d2": 240}
    assert data["lifted_homology_dimensions"] == {"H0": 2, "H1": 162, "H2": 80}
    assert data["lifted_euler_characteristic"] == -80


def test_lifted_edge_module_is_fusion_ledger_and_klm_cover() -> None:
    data = lifted_chain_data()["fusion_read"]

    assert data["C1_lifted_dimension"] == FUSION_EXPECTED == 480
    assert data["KLM_rail_cover"] == KLM == 960


def test_nilpotent_commutes_with_lifted_boundaries() -> None:
    data = boundary_commutation_data()

    assert data["d1_lift_shape"] == [80, 480]
    assert data["d2_lift_shape"] == [480, 320]
    assert data["rank_d1_lift"] == 78
    assert data["rank_d2_lift"] == 240
    assert data["d1_commutes_with_nilpotent"] is True
    assert data["d2_commutes_with_nilpotent"] is True
    assert data["lifted_composition_zero"] is True


def test_h1_nilpotent_realizes_0_81_162_81_0() -> None:
    data = nilpotent_chain_data()
    h1 = data["homology_nilpotents"]["H1"]

    assert data["local_increment"] == [[0, 1], [0, 0]]
    assert h1["dimension"] == 162
    assert h1["rank"] == H1_EXPECTED == 81
    assert h1["kernel_dimension"] == 81
    assert h1["image_dimension"] == 81
    assert h1["square_zero"] is True
    assert data["exact_sequence_on_h1"] == "0 -> 81 -> 162 -> 81 -> 0"


def test_chain_nilpotents_have_image_equals_kernel_in_each_degree() -> None:
    data = nilpotent_chain_data()["chain_nilpotents"]

    assert data["C0"]["rank"] == 40
    assert data["C1"]["rank"] == 240
    assert data["C2"]["rank"] == 160
    assert all(entry["kernel_dimension"] == entry["image_dimension"] for entry in data.values())
    assert all(entry["square_zero"] is True for entry in data.values())


def test_summary_and_identities_hold() -> None:
    payload = build_bridge()
    summary = payload["summary"]

    assert summary["vertex_count"] == 40
    assert summary["edge_count"] == 240
    assert summary["triangle_count"] == 160
    assert summary["h1_dimension"] == 81
    assert summary["lifted_edge_dimension"] == 480
    assert summary["lifted_h1_dimension"] == 162
    assert summary["induced_nilpotent_rank_h1"] == 81
    assert summary["all_identities_hold"] is True
    assert all(payload["identities"].values())


def test_honesty_boundary_and_snake_read_are_present() -> None:
    payload = build_bridge()

    assert "chain-complex and nilpotent-extension theorem" in payload["honesty_boundary"]
    assert "not an analogy" in payload["snake_eats_tail_read"]
    assert "C1=480" not in payload["theorem"]
    assert "doubles the edge-chain module to 480" in payload["theorem"]


def test_index_exposes_dcclxviii_chain_lift() -> None:
    text = (ROOT / "docs" / "index.html").read_text(encoding="utf-8")

    assert "Nilpotent\n              Chain-Lift / QEC Bridge" in text
    assert "<code>C1&otimes;F3[&epsilon;]/&epsilon;<sup>2</sup>=480</code>" in text
    assert "<code>H1=162</code>" in text


def test_write_and_reload() -> None:
    out = write_bridge()
    assert out == OUT_PATH
    data = json.loads(out.read_text(encoding="utf-8"))

    assert data["summary"]["all_identities_hold"] is True
    assert data["dual_number_lift"]["fusion_read"]["C1_lifted_dimension"] == 480
