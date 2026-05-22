from __future__ import annotations

from analysis.w33_unified_closure_grammar import unified_closure_grammar_packet


def test_mcxcvi_packets() -> None:
    packet = unified_closure_grammar_packet()

    assert packet["emergence_kernel"] == {
        "S": 24,
        "E": 32,
        "M": 18432,
        "Delta_plus": 1568,
        "Delta_minus": 1504,
        "Sigma": 3072,
        "Kappa": 64,
        "identity": "M=E*S^2; Delta±=E(2S±1); E=Kappa/2; S=Sigma/(2Kappa)",
    }
    assert packet["horizon_reye_kernel"] == {
        "C": 8,
        "P": 12,
        "g": 6,
        "N": 72,
        "A_T": 96,
        "A_R": 576,
        "identity": "N=P*g; A_T=C*P; A_R=C*N=C*P*g",
    }
    assert packet["cross_kernel_bridges"] == {
        "E_over_C": 4,
        "S_over_P": 2,
        "M_over_A_R": 32,
        "identity": "E/C=4, S/P=2, M/A_R=32",
    }


def test_mcxcvi_all_checks_pass() -> None:
    packet = unified_closure_grammar_packet()

    assert packet["checks"] == {
        "emergence_quadratic_instance": True,
        "emergence_jump_instance_plus": True,
        "emergence_jump_instance_minus": True,
        "emergence_inverse_instance_e": True,
        "emergence_inverse_instance_s": True,
        "horizon_payload_instance": True,
        "tomotope_symmetry_instance": True,
        "reye_symmetry_instance": True,
        "reye_tomotope_ratio_instance": True,
        "kernel_bridge_ratio_e_over_c": True,
        "kernel_bridge_ratio_s_over_p": True,
        "kernel_bridge_monodromy_over_reye_symmetry": True,
    }
    assert packet["n_verified"] == 12
