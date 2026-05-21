from __future__ import annotations

from analysis.w33_self_entangled_emergence_discrete_curvature_inversion import (
    self_entangled_emergence_discrete_curvature_inversion_packet,
)


def test_mcxci_packets() -> None:
    packet = self_entangled_emergence_discrete_curvature_inversion_packet()

    assert packet["jump_packet"] == {
        "delta_plus": 1568,
        "delta_minus": 1504,
        "sigma": 3072,
        "kappa": 64,
        "identity": "Sigma=3072, Kappa=64 from (1568,1504)",
    }
    assert packet["recovered_packets"] == {
        "edge_shell": 32,
        "seed": 24,
        "monodromy": 18432,
        "identity": "E=Kappa/2=32, S=Sigma/(2Kappa)=24, M=E*S^2=18432",
    }


def test_mcxci_all_checks_pass() -> None:
    packet = self_entangled_emergence_discrete_curvature_inversion_packet()

    assert packet["checks"] == {
        "sigma_is_3072": True,
        "kappa_is_64": True,
        "kappa_is_twice_edge_shell": True,
        "sigma_is_four_edge_seed": True,
        "edge_shell_recovered_integral": True,
        "seed_recovered_integral": True,
        "seed_recovered_is_24": True,
        "monodromy_reconstructed_from_recovered_packets": True,
        "jump_pair_consistency_plus": True,
        "jump_pair_consistency_minus": True,
    }
    assert packet["n_verified"] == 10
