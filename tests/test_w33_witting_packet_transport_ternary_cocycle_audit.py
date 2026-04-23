from __future__ import annotations

from scripts.w33_witting_packet_transport_ternary_cocycle_audit import analyze


def test_packet_extension_cocycle_is_exact_and_not_a_coboundary() -> None:
    payload = analyze()
    theorem = payload["packet_transport_ternary_cocycle_theorem"]
    cocycle = payload["extension_cocycle"]
    operator = payload["fiber_nilpotent_operator"]
    matter = payload["matter_extension_operator"]

    assert theorem["the_packet_extension_cocycle_is_exact_and_not_a_coboundary"] is True
    assert theorem["the_packet_fiber_shift_realizes_the_extension_operatorially"] is True
    assert theorem["the_packet_matter_extension_operator_has_rank_81_and_square_zero"] is True
    assert (
        theorem[
            "the_packet_cocycle_and_nilpotent_operator_recover_the_same_exact_extension_package_as_the_centerquad_route"
        ]
        is True
    )
    assert theorem["the_witting_packet_layer_carries_the_exact_transport_twisted_ternary_cocycle_package"] is True

    assert cocycle == {
        "field": "F3",
        "adapted_group_order": 6,
        "adapted_matrices_upper_triangular": True,
        "twisted_cocycle_identity_exact": True,
        "cocycle_values_on_sign_trivial_subgroup": [0, 1, 2],
        "cocycle_values_on_sign_nontrivial_coset": [0, 1, 2],
        "cocycle_is_not_a_coboundary": True,
    }
    assert operator == {
        "matrix": [[0, 1], [0, 0]],
        "rank": 1,
        "square_zero": True,
        "kernel_equals_image_equals_invariant_line": True,
        "left_action_fixes_shift": True,
        "right_action_twists_by_sign": True,
    }
    assert matter == {
        "dimension": 162,
        "rank": 81,
        "nullity": 81,
        "square_zero": True,
        "image_dimension": 81,
        "kernel_dimension": 81,
        "image_equals_kernel": True,
        "logical_qutrits": 81,
    }
