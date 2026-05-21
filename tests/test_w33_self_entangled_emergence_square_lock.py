from __future__ import annotations

from analysis.w33_self_entangled_emergence_square_lock import (
    self_entangled_emergence_square_lock_packet,
)


def test_mclxxxvii_seed_and_emergent_packets() -> None:
    packet = self_entangled_emergence_square_lock_packet()

    assert packet["seed_packet"] == {
        "directed_changes": 6,
        "now_rays": 4,
        "plaquette_seed": 24,
        "identity": "24 = 6*4",
    }
    assert packet["emergent_router_packet"] == {
        "plaquettes": 24,
        "q4_edges": 32,
        "monodromy": 18432,
        "identity": "18432 = 24*32*24 = (6*4)^2*32",
    }


def test_mclxxxvii_all_checks_pass() -> None:
    packet = self_entangled_emergence_square_lock_packet()

    assert packet["checks"] == {
        "temporal_seed_is_6_times_4": True,
        "plaquette_equals_temporal_seed": True,
        "router_edges_are_32": True,
        "monodromy_is_18432": True,
        "emergence_square_lock": True,
        "expanded_square_lock": True,
        "router_centered_ratio": True,
        "plaquette_centered_ratio": True,
        "symmetric_plaquette_factors": True,
    }
    assert packet["n_verified"] == 9
