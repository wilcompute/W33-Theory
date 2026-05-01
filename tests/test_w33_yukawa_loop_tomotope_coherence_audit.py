"""Tests for Yukawa-loop-tomotope coherence law bridging frontier to smooth realization."""

from scripts.w33_yukawa_loop_tomotope_coherence_audit import (
    tomotope_imbalance_response_factor,
    zeta_loop_ramanujan_noise_amplitude,
    transport_scale_affine_coherence,
    yukawa_loop_tomotope_coherence_packet,
)


def test_tomotope_response_factor_at_zero_alignment() -> None:
    """At perfect alignment (a=1), tomotope response should be zero."""
    response = tomotope_imbalance_response_factor(1.0)
    assert response < 0.1, f"Expected near-zero at a=1.0, got {response}"


def test_tomotope_response_factor_at_misaligned() -> None:
    """At misaligned (a=0), tomotope response should be 24."""
    response = tomotope_imbalance_response_factor(0.0)
    assert abs(response - 24.0) < 0.1, f"Expected 24 at a=0.0, got {response}"


def test_tomotope_response_is_monotone_decreasing() -> None:
    """Tomotope response should decrease monotonically with alignment."""
    values = [tomotope_imbalance_response_factor(a) for a in [0.0, 0.25, 0.5, 0.75, 1.0]]
    for i in range(len(values) - 1):
        assert values[i] >= values[i+1], f"Not monotone: {values}"


def test_zeta_loop_noise_is_positive() -> None:
    """Zeta-loop Ramanujan noise amplitude should be positive."""
    noise = zeta_loop_ramanujan_noise_amplitude(3)
    assert noise > 0, f"Expected positive noise, got {noise}"


def test_affine_coherence_is_positive() -> None:
    """Affine coherence factor should be positive."""
    coherence = transport_scale_affine_coherence()
    assert float(coherence) > 0, f"Expected positive coherence, got {coherence}"


def test_coherence_relates_to_kernel_regularity() -> None:
    """Affine coherence should be expressed relative to kernel k=12."""
    coherence = transport_scale_affine_coherence()
    # 217/12 / 12 = 217/144 ≈ 1.507
    expected_approx = 217 / 144
    assert abs(float(coherence) - expected_approx) < 0.01


def test_yukawa_coupling_emerges_from_product() -> None:
    """Yukawa coupling should be positive and emerge from component product."""
    payload = yukawa_loop_tomotope_coherence_packet()
    comp = payload['component_values']
    coup = payload['yukawa_coupling_prediction']['coupling_strength_base']
    
    # Coupling = (tomotope_norm) * (zeta_norm) * (coherence)
    expected_approx = (comp['tomotope_imbalance_response_normalized'] 
                      * comp['zeta_noise_normalized']
                      * comp['affine_coherence'])
    
    assert coup > 0
    assert abs(coup - expected_approx) < 1e-10


def test_mass_hierarchy_tau_greater_than_muon() -> None:
    """Tau Yukawa should exceed muon Yukawa (mass hierarchy)."""
    payload = yukawa_loop_tomotope_coherence_packet()
    yuk = payload['yukawa_coupling_prediction']
    
    assert yuk['tau_yukawa'] > yuk['muon_yukawa'], (
        f"tau {yuk['tau_yukawa']} should exceed muon {yuk['muon_yukawa']}"
    )


def test_mass_hierarchy_muon_greater_than_electron() -> None:
    """Muon Yukawa should exceed electron Yukawa."""
    payload = yukawa_loop_tomotope_coherence_packet()
    yuk = payload['yukawa_coupling_prediction']
    
    assert yuk['muon_yukawa'] > yuk['electron_yukawa'], (
        f"muon {yuk['muon_yukawa']} should exceed electron {yuk['electron_yukawa']}"
    )


def test_coherence_law_all_theorems_pass() -> None:
    """All theorem conditions should hold."""
    payload = yukawa_loop_tomotope_coherence_packet()
    
    theorem = payload["theorem"]
    assert theorem["tomotope_response_is_nonzero"] is True
    assert theorem["zeta_noise_is_nonzero"] is True
    assert theorem["affine_coherence_is_positive"] is True
    assert theorem["yukawa_coupling_emerges_from_product"] is True
    assert theorem["mass_hierarchy_is_captured_in_ratios"] is True
