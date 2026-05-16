from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from verify_dcclv_frobenius_octahedral_edge_phase_lift import (  # noqa: E402
    build_bridge,
    write_bridge,
)


def test_summary_values() -> None:
    payload = build_bridge()
    s = payload["summary"]

    assert s["q"] == 3
    assert s["frobenius_carrier"] == 240
    assert s["w33_vertices"] == 40
    assert s["octahedral_phase_pairs"] == 6
    assert s["edge_phase_slots"] == 240
    assert s["directed_phase_slots"] == 480
    assert s["full_chain_closure_dimension"] == 480
    assert s["all_identities_hold"] is True


def test_octahedral_phase_pairs_are_antipodal_edge_orbits() -> None:
    payload = build_bridge()
    phase_data = payload["octahedral_phase_data"]

    assert phase_data["phase_pair_count"] == 6
    assert phase_data["directed_phase_count"] == 12
    assert len(phase_data["antipodal_edge_pair_orbits"]) == 6
    assert all(len(orbit) == 2 for orbit in phase_data["antipodal_edge_pair_orbits"])


def test_carrier_counts_link_frobenius_edges_and_directed_lift() -> None:
    payload = build_bridge()
    counts = payload["carrier_counts"]

    assert counts["frobenius_nonbase_elements"] == 240
    assert counts["gq_edges"] == {"numerator": 240, "denominator": 1}
    assert counts["w33_edges"] == 240
    assert counts["w33_directed_edges"] == 480
    assert counts["w33_full_clique_chain_nonempty_simplices"] == 480


def test_qec_read_closes_the_240_edge_carrier() -> None:
    payload = build_bridge()
    qec = payload["qec_read"]

    assert qec["physical_edge_slots"] == 240
    assert qec["rank_X_vertex_checks"] == 39
    assert qec["rank_Z_triangle_checks"] == 120
    assert qec["logical_H1"] == 81
    assert qec["stabilizer_rank"] == 159
    assert qec["closure"] == 240
    assert qec["rate"] == {"numerator": 27, "denominator": 80}


def test_slot_samples_have_expected_local_ranges() -> None:
    payload = build_bridge()
    samples = payload["slot_samples"]

    assert samples["edge_phase_slots_first_12"][:6] == [
        {"w33_vertex": 0, "phase_pair": phase} for phase in range(6)
    ]
    assert samples["directed_phase_slots_first_12"] == [
        {"w33_vertex": 0, "directed_phase": phase} for phase in range(12)
    ]


def test_all_identities_hold_and_boundary_is_explicit() -> None:
    payload = build_bridge()

    assert all(payload["identities"].values())
    assert "not construct a canonical" in payload["bridge_claim"]["conditional_layer"]


def test_write_and_reload(tmp_path: Path) -> None:
    out = write_bridge(tmp_path / "dcclv.json")

    assert out.exists()
    assert out.read_text(encoding="utf-8").startswith("{")
