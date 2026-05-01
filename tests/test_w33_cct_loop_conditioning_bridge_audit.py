from __future__ import annotations

from scripts.w33_cct_loop_conditioning_bridge_audit import (
    cct_loop_conditioning_bridge_summary,
)


def test_remote_loop_stack_first_realization_probability_and_action() -> None:
    summary = cct_loop_conditioning_bridge_summary()

    assert summary["efficient_loop_language_packet"] == {
        "directed_edges": 480,
        "branch_count": 11,
        "trit_loop_length": 3,
        "local_words_at_first_loop": 1331,
        "realized_triangle_closures_per_directed_edge": 2,
        "first_loop_probability": "2/1331",
        "weighted_language_rule": "uniform cost gives closed_histories / 11^n",
    }
    assert summary["pel_action_packet"]["first_realization_action"] == "log_3(1331/2)"
    assert summary["pel_action_packet"]["equilibrium_action_limit"] == "log_3(480)"


def test_remote_loop_stack_primitive_thermodynamic_and_parry_packets() -> None:
    summary = cct_loop_conditioning_bridge_summary()

    assert summary["primitive_semantics_packet"]["first_primitive_layer"] == 320
    assert summary["primitive_semantics_packet"]["triangle_count_factorization"] == (
        480,
        2,
        3,
        320,
    )
    assert summary["prime_thermodynamics_packet"] == {
        "top_hashimoto_eigenvalue": 11,
        "entropy": "log(11)",
        "trit_entropy": "log_3(11)",
        "critical_beta": 1,
        "top_ihara_pole": "u = 1/11",
        "primitive_asymptotic": "N_n ~ 11^n / n",
    }
    assert summary["parry_kms_packet"]["stationary_distribution"] == "1/480"
    assert summary["parry_kms_packet"]["loop_return_probability_length_3"] == "2/1331"


def test_doob_bridge_and_quasicrystal_alignment_are_boundary_explicit() -> None:
    summary = cct_loop_conditioning_bridge_summary()

    assert summary["doob_bridge_packet"]["first_step_unconditioned_options"] == 11
    assert summary["doob_bridge_packet"]["first_step_loop_compatible_options"] == 2
    assert summary["doob_bridge_packet"]["open_turns_killed"] == 9
    assert summary["quasicrystal_loop_alignment_packet"] == {
        "quasicrystal_neighbor_packet": 8,
        "hashimoto_branch_packet": 11,
        "qutrit_slack": 3,
        "count_identity": "K - 1 = (K - mu) + q = 8 + 3 = 11",
        "interpretation_boundary": (
            "exact count alignment only: quasicrystal trit-savings remains "
            "an empire-overlap argmax rule, while Doob conditioning is a "
            "future-loop path-measure reweighting"
        ),
    }
    assert all(summary["theorem"].values())
