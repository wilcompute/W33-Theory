from __future__ import annotations

from scripts.w33_cct_trit_savings_global_lift_audit import (
    cct_trit_savings_global_lift_summary,
)


def test_base_monodromy_obstruction_has_no_one_turn_fixed_selector() -> None:
    summary = cct_trit_savings_global_lift_summary()
    base = summary["base_monodromy_packet"]

    assert base["one_turn_map"] == "c -> 1-c"
    assert base["fixed_points"] == ()
    assert "no one-turn fixed selector" in base["obstruction_statement"]


def test_lift_packet_has_two_turn_identity_and_period_two_orbit() -> None:
    summary = cct_trit_savings_global_lift_summary()
    lift = summary["lift_packet"]

    assert lift["lift_group"] == "Z2"
    assert lift["two_turn_map"] == "identity"
    assert len(lift["two_step_fixed_points"]) == 4
    orbit = lift["example_period_2_orbit"]
    assert orbit[0] == orbit[2]
    assert orbit[0] != orbit[1]


def test_holonomy_packet_makes_minimality_explicit() -> None:
    summary = cct_trit_savings_global_lift_summary()
    holonomy = summary["holonomy_packet"]

    assert holonomy["coefficient_group"] == "Z2"
    assert holonomy["one_turn_holonomy_class"] == 1
    assert holonomy["odd_turn_fixed_points"] == {1: (), 3: (), 5: ()}
    assert holonomy["minimal_consistent_turns"] == 2
    assert "first global consistency period" in holonomy["minimality_statement"]


def test_global_lift_theorem_bundle_is_true_and_boundary_explicit() -> None:
    summary = cct_trit_savings_global_lift_summary()

    assert all(summary["theorem"].values())
    assert summary["w33_alignment_packet"]["neighbor_packet"] == 8
    assert "does not claim full global selector closure" in summary["w33_alignment_packet"]["boundary"]
