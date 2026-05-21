from __future__ import annotations

from analysis.w33_self_entangled_emergence_quantized_increment import (
    self_entangled_emergence_quantized_increment_packet,
)


def test_mcxc_packets() -> None:
    packet = self_entangled_emergence_quantized_increment_packet()

    assert packet["baseline"] == {
        "seed": 24,
        "q4_edges": 32,
        "monodromy": 18432,
        "identity": "18432 = 32*24^2",
    }
    assert packet["quantized_jumps"] == {
        "delta_plus": 1568,
        "delta_minus": 1504,
        "mean_jump": 1536,
        "asymmetry": 64,
        "identity": "Delta+=1568, Delta-=1504, mean=1536, asymmetry=64",
    }
    assert packet["invertibility"] == {
        "m_plus": 20000,
        "m_minus": 16928,
        "seed_plus": 25,
        "seed_minus": 23,
        "identity": "M+Delta+=32*25^2 and M-Delta-=32*23^2",
    }


def test_mcxc_all_checks_pass() -> None:
    packet = self_entangled_emergence_quantized_increment_packet()

    assert packet["checks"] == {
        "baseline_identity": True,
        "delta_plus_formula": True,
        "delta_minus_formula": True,
        "mean_jump_is_48_times_32": True,
        "jump_asymmetry_is_2_edges": True,
        "forward_plus_step_is_exact": True,
        "forward_minus_step_is_exact": True,
        "inverse_plus_recovers_seed_plus_one": True,
        "inverse_minus_recovers_seed_minus_one": True,
        "all_packets_integral": True,
    }
    assert packet["n_verified"] == 10
