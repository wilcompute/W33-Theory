from __future__ import annotations

from analysis.w33_self_entangled_emergence_inverse_lock import (
    self_entangled_emergence_inverse_lock_packet,
)


def test_mclxxxviii_recovered_seed_packet() -> None:
    packet = self_entangled_emergence_inverse_lock_packet()

    assert packet["emergent_input"] == {
        "monodromy": 18432,
        "q4_edges": 32,
        "identity": "18432 = S^2*32",
    }
    assert packet["recovered_seed"] == {
        "seed_square": 576,
        "seed": 24,
        "now_rays": 4,
        "recovered_directed_changes": 6,
        "identity": "S = sqrt(18432/32) = 24, D = 24/4 = 6",
    }


def test_mclxxxviii_all_checks_pass() -> None:
    packet = self_entangled_emergence_inverse_lock_packet()

    assert packet["checks"] == {
        "monodromy_divides_by_q4_edges": True,
        "seed_square_is_576": True,
        "seed_square_is_perfect_square": True,
        "recovered_seed_is_24": True,
        "recovered_directed_is_integer": True,
        "recovered_directed_is_6": True,
        "recovered_directed_matches_mclxiii": True,
        "inverse_forward_consistency": True,
        "factor_identity": True,
    }
    assert packet["n_verified"] == 9
