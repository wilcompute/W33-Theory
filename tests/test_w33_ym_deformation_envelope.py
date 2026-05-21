"""Tests for Part MCLXII: Yang-Mills gap-shell deformation envelope."""

from fractions import Fraction

from analysis.w33_ym_deformation_envelope import (
    DAVIS_KAHAN_COEFFICIENT,
    E8_RANK,
    E8_RANK_CHANNEL_RADIUS,
    EPS_CRITICAL,
    NU_GAP,
    S_HOLO,
    gap_lower_bound,
    normalized_spectrum_counts,
    uniform_rescale_errors,
    ym_deformation_envelope_packet,
)


PACKET = ym_deformation_envelope_packet()


def test_normalized_laplacian_spectrum_counts_are_canonical():
    assert normalized_spectrum_counts() == {"0": 1, "5/6": 24, "4/3": 15}
    assert PACKET["checks"]["gap_multiplicity_is_24"]


def test_gap_shell_ratio_locks_to_gap_multiplicity():
    assert S_HOLO == 20
    assert NU_GAP == Fraction(5, 6)
    assert S_HOLO / NU_GAP == 24
    lock = PACKET["gap_shell_lock"]
    assert lock["S_holo_over_nu_gap"]["fraction"] == "24"
    assert lock["gap_multiplicity"] == 24
    assert lock["dim_su5_adjoint"] == 24
    assert lock["lock_verified"] is True


def test_deformation_envelope_constants():
    assert DAVIS_KAHAN_COEFFICIENT == Fraction(3, 5)
    assert EPS_CRITICAL == Fraction(25, 18)
    assert E8_RANK == 8
    assert E8_RANK_CHANNEL_RADIUS == Fraction(25, 144)


def test_rank_channel_radius_is_not_the_one_parameter_closure():
    envelope = PACKET["deformation_envelope"]
    assert envelope["one_parameter_critical_radius"]["fraction"] == "25/18"
    assert envelope["rank_distributed_per_channel_radius"]["fraction"] == "25/144"
    assert envelope["eight_channels_saturate_exact_radius"]["fraction"] == "25/18"
    assert "strict safe radius" in envelope["classification"]


def test_gap_lower_bound_at_safe_radius():
    assert gap_lower_bound(E8_RANK_CHANNEL_RADIUS) == Fraction(35, 48)
    assert PACKET["deformation_envelope"]["gap_lower_at_rank_channel_radius"]["fraction"] == "35/48"
    assert PACKET["checks"]["safe_radius_keeps_positive_gap"]


def test_gap_lower_bound_closes_at_exact_radius():
    assert gap_lower_bound(EPS_CRITICAL) == 0


def test_uniform_edge_scaling_leaves_normalized_laplacian_invariant():
    errors = uniform_rescale_errors()
    assert errors == {"1/2": "0.0e+00", "4/3": "0.0e+00", "3": "0.0e+00", "25/18": "0.0e+00"}
    assert PACKET["uniform_scaling"]["invariant"] is True


def test_packet_metadata_and_boundary():
    assert PACKET["part"] == "MCLXII"
    assert PACKET["theorem"] == "Yang-Mills gap-shell deformation envelope"
    assert "finite W33" in PACKET["claim_boundary"]
    assert "continuum Yang-Mills remains" in PACKET["claim_boundary"]


def test_all_checks_pass():
    failed = [name for name, value in PACKET["checks"].items() if not value]
    assert failed == []
    assert PACKET["n_verified"] == len(PACKET["checks"])
