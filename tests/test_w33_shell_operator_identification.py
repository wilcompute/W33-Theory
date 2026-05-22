from __future__ import annotations

from analysis.w33_shell_operator_identification import (
    shell_operator_identification_packet,
)


def test_mcc_packets() -> None:
    packet = shell_operator_identification_packet()

    assert packet["packets"] == {
        "E_shell": 32,
        "F_operator": 32,
        "C": 8,
        "s": 4,
        "A0": 576,
        "S": 24,
        "M": 18432,
    }
    assert packet["identification"] == {
        "identity": "F=C*s=8*4=32=E and M=F*A0=E*S^2=18432",
    }


def test_mcc_all_checks_pass() -> None:
    packet = shell_operator_identification_packet()

    assert packet["checks"] == {
        "emergence_shell_is_32": True,
        "operator_factor_is_32": True,
        "operator_factor_equals_shell": True,
        "operator_factor_decomposes_as_8_times_4": True,
        "monodromy_from_operator_form": True,
        "monodromy_from_emergence_form": True,
        "operator_emergence_forms_match": True,
        "a0_is_576": True,
        "s_square_is_576": True,
        "base_equivalence_a0_equals_s_square": True,
    }
    assert packet["n_verified"] == 10
