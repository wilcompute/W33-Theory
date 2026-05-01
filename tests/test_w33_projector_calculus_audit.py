"""Test for Part LXXXVIII: projector calculus and finite propagator."""

import pytest
from scripts.w33_projector_calculus_audit import build_projector_calculus_summary


def test_projector_calculus_idempotence():
    """Test that all three shell projectors are idempotent (P^2 = P)."""
    summary = build_projector_calculus_summary()
    checks = summary["checks"]

    assert checks["P0_idempotent"]
    assert checks["P_light_idempotent"]
    assert checks["P_heavy_idempotent"]


def test_projector_calculus_completeness():
    """Test that P0 + P_light + P_heavy = I."""
    summary = build_projector_calculus_summary()
    assert summary["checks"]["completeness_holds"]


def test_projector_calculus_orthogonality():
    """Test that shell projectors are mutually orthogonal."""
    summary = build_projector_calculus_summary()
    checks = summary["checks"]

    assert checks["P0_orthogonal_to_P_light"]
    assert checks["P0_orthogonal_to_P_heavy"]
    assert checks["P_light_orthogonal_to_P_heavy"]


def test_projector_calculus_ranks():
    """Test that projector ranks match the known shell multiplicities."""
    summary = build_projector_calculus_summary()
    ranks = summary["projector_ranks"]

    assert ranks["rank_P0_full"] == 3
    assert ranks["rank_P_light_full"] == 78
    assert ranks["rank_P_heavy_full"] == 40
    assert ranks["rank_P0_full"] + ranks["rank_P_light_full"] + ranks["rank_P_heavy_full"] == 121


def test_projector_calculus_functional_calculus():
    """Test that f(H^2) = f(0)P0 + f(18)P_light + f(72)P_heavy recovers H^2."""
    summary = build_projector_calculus_summary()
    assert summary["checks"]["functional_calculus_recovers_H2"]


def test_projector_calculus_heat_kernel():
    """Test that the heat kernel exp(-tH^2) is symmetric positive semi-definite."""
    summary = build_projector_calculus_summary()
    propagators = summary["finite_propagators"]

    assert propagators["heat_kernel_is_symmetric"]
    assert propagators["heat_kernel_is_positive"]


def test_projector_calculus_green_kernel():
    """Test that the Green kernel trace is consistent with spectral formula."""
    summary = build_projector_calculus_summary()
    assert summary["finite_propagators"]["green_kernel_trace_consistent"]


def test_projector_calculus_theorem():
    """Test that all Part LXXXVIII theorem statements hold."""
    summary = build_projector_calculus_summary()
    theorem = summary["theorem"]

    assert theorem["projector_calculus_is_closed"]
    assert theorem["finite_propagator_system_complete"]
    assert theorem["H_determines_all_propagators"]


def test_projector_calculus_links_to_prior_parts():
    """Test that projector calculus is consistent with Parts LXXXV and LXXXVI."""
    summary = build_projector_calculus_summary()
    links = summary["link_to_prior_parts"]

    assert links["two_spectral_shells_parseval_holds"]
    assert links["mass_weighted_hodge_rank_d"] == 59
    assert links["three_shell_projectors_span_H2_spectrum"]
