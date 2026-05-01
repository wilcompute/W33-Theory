from __future__ import annotations

from w33_k3_integral_h2_lattice_bridge import (
    build_k3_integral_h2_lattice_bridge_summary,
)


def test_k3_integral_h2_lattice_bridge_recovers_even_unimodular_k3_lattice() -> None:
    summary = build_k3_integral_h2_lattice_bridge_summary()
    assert summary["status"] == "ok"

    profile = summary["integral_lattice_profile"]
    assert profile["h2_rank"] == 22
    assert profile["cocycle_rank"] == 127
    assert profile["exact_rank"] == 105
    assert profile["smith_zero_count"] == 22
    assert profile["smith_unit_count"] == 105
    assert profile["determinant"] == -1
    assert profile["positive_directions"] == 3
    assert profile["negative_directions"] == 19
    assert profile["diagonal_even"] is True
    assert profile["unimodular"] is True

    theorem = summary["integral_h2_lattice_theorem"]
    assert theorem["smith_diagonal_has_22_zeros_and_105_units"] is True
    assert theorem["integral_h2_rank_is_22"] is True
    assert theorem["intersection_form_is_even"] is True
    assert theorem["intersection_form_is_unimodular"] is True
    assert theorem["intersection_form_has_signature_3_19"] is True
    assert theorem["explicit_k3_seed_realizes_full_even_unimodular_k3_lattice"] is True


def test_k3_integral_h2_lattice_bridge_selects_primitive_hyperbolic_plane() -> None:
    summary = build_k3_integral_h2_lattice_bridge_summary()
    plane = summary["primitive_hyperbolic_plane"]

    assert plane["gram_matrix"] == [[0, 1], [1, 0]]
    assert plane["primitive_minor_gcd"] == 1
    assert len(plane["isotropic_vector_support"]) >= 1
    assert len(plane["companion_vector_support"]) >= 1

    theorem = summary["integral_h2_lattice_theorem"]
    assert theorem["canonical_primitive_plane_is_hyperbolic_U"] is True
    assert theorem["canonical_primitive_plane_is_primitive"] is True


def test_k3_integral_h2_lattice_bridge_exposes_continuum_lift_checklist_and_diagnostics() -> None:
    summary = build_k3_integral_h2_lattice_bridge_summary()

    checklist = summary["continuum_lift_checklist"]
    assert checklist["integral_h2_rank_is_22"] is True
    assert checklist["smith_rank_profile_is_22_plus_105"] is True
    assert checklist["intersection_is_even_unimodular"] is True
    assert checklist["intersection_signature_is_3_19"] is True
    assert checklist["primitive_hyperbolic_plane_U_present"] is True
    assert checklist["primitive_hyperbolic_plane_is_primitive"] is True
    assert checklist["continuum_lift_predicate_passes"] is True

    diagnostics = summary["runtime_diagnostics"]
    assert isinstance(diagnostics["gp_available"], bool)
    assert diagnostics["gp_timeout_seconds"] > 0
    assert diagnostics["pytest_timeout_fallback_env"] == "W33_USE_PRECOMPUTED_ON_GP_TIMEOUT"

    theorem = summary["integral_h2_lattice_theorem"]
    assert theorem["continuum_lift_predicate_passes"] is True
