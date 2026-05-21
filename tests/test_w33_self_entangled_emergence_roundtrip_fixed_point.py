from __future__ import annotations

from analysis.w33_self_entangled_emergence_roundtrip_fixed_point import (
    self_entangled_emergence_roundtrip_fixed_point_packet,
)


def test_mclxxxix_packets() -> None:
    packet = self_entangled_emergence_roundtrip_fixed_point_packet()

    assert packet["forward_packet"] == {
        "directed_changes": 6,
        "now_rays": 4,
        "seed": 24,
        "q4_edges": 32,
        "monodromy": 18432,
        "identity": "18432 = (6*4)^2*32",
    }
    assert packet["inverse_packet"] == {
        "recovered_seed": 24,
        "recovered_directed_changes": 6,
        "identity": "sqrt(18432/32)=24 and 24/4=6",
    }
    assert packet["reciprocity"] == {
        "forward_gain": "32",
        "inverse_gain": "1/32",
        "product": "1",
        "identity": "32 * (1/32) = 1",
    }


def test_mclxxxix_all_checks_pass() -> None:
    packet = self_entangled_emergence_roundtrip_fixed_point_packet()

    assert packet["checks"] == {
        "forward_map_matches_mclxxxvii": True,
        "inverse_map_matches_mclxxxviii": True,
        "roundtrip_seed_fixed_point": True,
        "roundtrip_directed_fixed_point": True,
        "seed_decomposes_to_directed_and_now": True,
        "recovered_seed_decomposes_same_way": True,
        "forward_gain_is_q4_edge_shell": True,
        "inverse_gain_is_shell_reciprocal": True,
        "gain_reciprocity_closes": True,
        "full_roundtrip_identity": True,
    }
    assert packet["n_verified"] == 10
