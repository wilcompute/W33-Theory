from __future__ import annotations

from scripts.w33_q3_smooth_realization_witness_audit import (
    analyze,
    verify_witness_embedding,
    verify_witness_existence,
    verify_witness_uniqueness,
)


def test_witness_existence_packet_verifies_unipotent_nontrivial_sign_trivial_matrix() -> None:
    packet = verify_witness_existence()

    assert packet["canonical_holonomy"] == [[1, 1], [0, 1]]
    assert packet["determinant"] == 1
    assert packet["is_nontrivial"] is True
    assert packet["is_sign_trivial"] is True
    assert packet["is_unipotent"] is True
    assert packet["nilpotent_increment"] == [[0, 1], [0, 0]]
    assert packet["nilpotent_square"] == [[0, 0], [0, 0]]
    assert packet["nilpotent_square_is_zero"] is True
    assert packet["witness_existence_verified"] is True


def test_witness_uniqueness_packet_is_gauge_equivalent_pair() -> None:
    packet = verify_witness_uniqueness()

    assert packet["nontrivial_sign_trivial_holonomies"] == [
        [[1, 1], [0, 1]],
        [[1, 2], [0, 1]],
    ]
    assert packet["expected_two_holonomies"] == [
        [[1, 1], [0, 1]],
        [[1, 2], [0, 1]],
    ]
    assert packet["gauge_conjugated_matrix"] == [[1, 2], [0, 1]]
    assert packet["theorem_gauge_equivalent"] is True
    assert packet["witness_uniqueness_verified"] is True


def test_witness_embedding_packet_targets_fixed_45_point_carrier() -> None:
    packet = verify_witness_embedding()

    assert packet["quotient_point_carrier_size"] == 45
    assert packet["k3_chart_target"]["target_coordinate"] == "dC"
    assert packet["k3_chart_target"]["required_value"] == "14105"
    assert packet["affine_target_theorem"] is True
    assert packet["shared_transport_theorem"] is True
    assert packet["witness_embedding_verified"] is True


def test_q3_smooth_realization_predicate_passes() -> None:
    payload = analyze()
    theorem = payload["q3_smooth_realization_witness_theorem"]

    assert theorem["witness_existence_verified"] is True
    assert theorem["witness_uniqueness_verified"] is True
    assert theorem["witness_embedding_verified"] is True
    assert theorem["smooth_realization_predicate_passes"] is True
