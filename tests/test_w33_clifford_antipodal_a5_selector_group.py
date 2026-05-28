from __future__ import annotations

from analysis.w33_clifford_antipodal_a5_selector_group import (
    clifford_antipodal_a5_selector_group_packet,
)


PACKET = clifford_antipodal_a5_selector_group_packet()


def test_mdclxxxiii_global_a5_identity() -> None:
    assert PACKET["selector_group_identity"] == "60 antipodal Clifford addresses = A5 in its degree-six action"
    assert PACKET["permutation_count"] == 60
    assert PACKET["n_verified"] == 9
    assert all(PACKET["checks"].values())


def test_mdclxxxiii_a5_order_and_parity_profiles() -> None:
    assert PACKET["order_profile"] == {"1": 1, "2": 15, "3": 20, "5": 24}
    assert PACKET["parity_profile"] == {"0": 60}
    assert PACKET["fixed_point_profile"] == {"0": 20, "1": 24, "2": 15, "6": 1}


def test_mdclxxxiii_degree_six_action_profiles() -> None:
    assert PACKET["two_transitivity_profile"] == {"2": 900}
    assert PACKET["cell_preimage_profile"] == {"10": 36}


def test_mdclxxxiii_selector_boundary() -> None:
    assert "A5 torsor" in PACKET["claim_boundary"]
    assert "does not yet construct the W33 spread selector" in PACKET["claim_boundary"]
    assert "twist this A5 torsor into the W33 spread association scheme" in PACKET["reading"]
