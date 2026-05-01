from __future__ import annotations

from scripts.w33_cct_qutrit_core_bridge_audit import (
    cct_qutrit_core_bridge_summary,
    q_factorial_equals_two_q_hits,
)


def test_cct_trit_packet_selects_q_equals_three_uniquely() -> None:
    summary = cct_qutrit_core_bridge_summary()

    assert q_factorial_equals_two_q_hits() == (3,)
    assert summary["cct_trit_packet"] == {
        "alphabet_size": 3,
        "states": ("off", "on", "undecided"),
        "q_factorial_equals_two_q_hits": (3,),
        "unique_positive_selector": 3,
    }


def test_two_qutrit_pauli_projectivization_is_the_40_symbol_shell() -> None:
    summary = cct_qutrit_core_bridge_summary()

    assert summary["two_qutrit_pauli_packet"] == {
        "qutrit_count": 2,
        "phase_space_dimension": 4,
        "affine_exponent_vectors": 81,
        "identity_vector": 1,
        "nonidentity_exponent_vectors": 80,
        "nonzero_scalar_orbit_size": 2,
        "projective_pauli_symbols": 40,
        "projectivization": "F_3^4 minus 0, modulo F_3^*",
    }


def test_w33_commutation_packet_is_gq33_two_qutrit_geometry() -> None:
    summary = cct_qutrit_core_bridge_summary()

    assert summary["w33_commutation_packet"] == {
        "geometry": "W(3,3) = GQ(3,3) two-qutrit Pauli commutation geometry",
        "point_count": 40,
        "line_count": 40,
        "points_per_line": 4,
        "lines_per_point": 4,
        "point_line_incidences": 160,
        "collinearity_srg": (40, 12, 2, 4),
        "commuting_neighbors_per_symbol": 12,
        "commutation_edges": 240,
        "edge_density": "4/13",
    }


def test_mub_spread_layer_sits_on_the_same_qutrit_core() -> None:
    summary = cct_qutrit_core_bridge_summary()

    assert summary["mub_spread_packet"] == {
        "complete_mub_frames": 36,
        "lines_per_complete_mub": 10,
        "spreads_per_line": 9,
        "spread_line_incidences": 360,
        "morita_rank": 16,
        "common_spine": "1 + 15",
        "line_side": (1, 15, 24),
        "spread_side": (1, 15, 20),
    }


def test_qutrit_core_bridge_theorem_flags_are_all_true() -> None:
    summary = cct_qutrit_core_bridge_summary()

    assert summary["theorem"] == {
        "cct_trit_selector_is_unique_q_equals_3": True,
        "two_qutrit_pauli_projectivization_is_w33_40_shell": True,
        "w33_commutation_geometry_is_gq33_srg": True,
        "mub_spread_layer_lives_on_same_two_qutrit_core": True,
        "qutrit_core_is_the_common_cct_w33_owner": True,
    }
