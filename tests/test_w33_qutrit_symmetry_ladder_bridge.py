from __future__ import annotations

from pathlib import Path

import pytest
from w33_qutrit_symmetry_ladder_bridge import build_qutrit_symmetry_ladder_summary

SAGE_TRANSPORT = (
    Path(__file__).resolve().parents[1]
    / "artifacts"
    / "sage_h27_to_schlafli_effective_triads_conjugacy.json"
)

pytestmark = pytest.mark.skipif(
    not SAGE_TRANSPORT.exists(),
    reason="optional Sage H27-to-Schlafli transport artifact is absent",
)


def test_qutrit_symmetry_ladder_dictionary_is_exact() -> None:
    summary = build_qutrit_symmetry_ladder_summary()
    ladder = summary["symmetry_ladder_dictionary"]

    projective = ladder["projective_layer"]
    full = ladder["full_graph_layer"]
    local = ladder["local_h27_layer"]
    neighbor = ladder["neighbor_bus_layer"]

    assert projective["group_label"] == "PSp(4,3)"
    assert projective["order"] == 25920
    assert projective["point_orbit_size"] == 40
    assert projective["point_stabilizer_order"] == 648
    assert projective["edge_orbit_size"] == 240
    assert projective["edge_stabilizer_order"] == 108
    assert tuple(projective["generator_names"]) == ("S1", "T1", "S2", "T2", "SWAP")

    assert full["group_label"] == "Aut(W33)"
    assert full["order"] == 51840
    assert full["point_stabilizer_order"] == 1296
    assert full["edge_stabilizer_order"] == 216

    assert local["affine_group_order"] == 1296
    assert local["projective_subgroup_order"] == 648
    assert local["full_point_stabilizer_matches_local_affine"] is True
    assert local["projective_point_stabilizer_matches_local_projective"] is True

    assert neighbor["neighbor_count"] == 12
    assert neighbor["induced_group_order"] == 432
    assert neighbor["kernel_from_full_stabilizer_order"] == 3
    assert neighbor["triangle_action_order"] == 24
    assert neighbor["triangle_action_is_s4"] is True
    assert neighbor["triangle_kernel_order"] == 18
    assert neighbor["translation_subgroup_order"] == 9
    assert neighbor["translation_subgroup_is_normal_abelian"] is True
    assert neighbor["involution_count"] == 45
    assert neighbor["reflection_count"] == 36
    assert neighbor["rotation_count"] == 9
    assert neighbor["reflection_centralizer_matches_d12"] is True

    assert (
        ladder["exact_factorizations"]["projective_order_factorization"]
        == "25920 = 40 * 648 = 240 * 108"
    )
    assert (
        ladder["exact_factorizations"]["full_order_factorization"]
        == "51840 = 2 * 25920 = 40 * 1296 = 240 * 216"
    )
    assert (
        ladder["exact_factorizations"]["neighbor_action_factorization"]
        == "432 = 9 * 48"
    )
    assert (
        ladder["exact_factorizations"]["point_stabilizer_factorization"]
        == "1296 = 2 * 648"
    )


def test_qutrit_symmetry_ladder_theorem_all_hold() -> None:
    summary = build_qutrit_symmetry_ladder_summary()
    assert all(summary["symmetry_ladder_theorem"].values())
    assert "25920 versus 51840 ambiguity" in summary["boundary_note"]
