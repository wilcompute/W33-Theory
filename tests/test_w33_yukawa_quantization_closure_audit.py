"""Tests for Yukawa quantization closure and smooth realization exactness."""

from scripts.w33_yukawa_quantization_closure_audit import (
    yukawa_base_coupling_from_coherence_law,
    yukawa_under_holonomy_amplitude,
    mass_hierarchy_under_holonomy_amplitude,
    coherence_law_and_holonomy_consistency_check,
)


def test_base_yukawa_coupling_is_positive() -> None:
    """Base Yukawa coupling should be positive."""
    coupling = yukawa_base_coupling_from_coherence_law()
    assert coupling > 0


def test_yukawa_at_zero_amplitude_equals_base() -> None:
    """At epsilon=0, Yukawa should equal base coupling."""
    base = yukawa_base_coupling_from_coherence_law()
    at_zero = yukawa_under_holonomy_amplitude(0.0)
    
    assert abs(at_zero - base) < 1e-10


def test_yukawa_increases_monotonically_with_holonomy_amplitude() -> None:
    """Yukawa should increase monotonically with holonomy amplitude."""
    epsilons = [0.0, 0.01, 0.05, 0.1, 0.15]
    couplings = [yukawa_under_holonomy_amplitude(eps) for eps in epsilons]
    
    for i in range(len(couplings) - 1):
        assert couplings[i] <= couplings[i+1], (
            f"Not monotone: {couplings[i]} > {couplings[i+1]}"
        )


def test_mass_hierarchy_electron_muon() -> None:
    """Muon mass should exceed electron mass."""
    masses = mass_hierarchy_under_holonomy_amplitude(0.0)
    assert masses["muon"] > masses["electron"]


def test_mass_hierarchy_muon_tau() -> None:
    """Tau mass should exceed muon mass."""
    masses = mass_hierarchy_under_holonomy_amplitude(0.0)
    assert masses["tau"] > masses["muon"]


def test_mass_hierarchy_preserved_at_all_amplitudes() -> None:
    """Mass hierarchy should be preserved under all holonomy amplitudes."""
    epsilons = [0.0, 0.01, 0.05, 0.1, 0.15]
    
    for eps in epsilons:
        masses = mass_hierarchy_under_holonomy_amplitude(eps)
        assert masses["hierarchy_preserved"], f"Hierarchy broken at epsilon={eps}"


def test_coherence_law_coupling_always_positive() -> None:
    """Yukawa coupling should be positive at all holonomy amplitudes."""
    payload = coherence_law_and_holonomy_consistency_check()
    
    assert payload["consistency_checks"]["coupling_always_positive"] is True


def test_coherence_law_coupling_monotone() -> None:
    """Yukawa coupling should be monotone increasing with holonomy."""
    payload = coherence_law_and_holonomy_consistency_check()
    
    assert payload["consistency_checks"]["coupling_monotone_increasing_with_holonomy"] is True


def test_holonomy_commutes_with_mass_sector() -> None:
    """2×2 holonomy witness should commute with mass sector."""
    payload = coherence_law_and_holonomy_consistency_check()
    
    assert payload["consistency_checks"]["holonomy_witness_commutes_with_mass_sector"] is True


def test_smooth_realization_closure_is_complete() -> None:
    """Smooth realization closure condition should be satisfied."""
    payload = coherence_law_and_holonomy_consistency_check()
    
    assert payload["closure_condition"]["is_closure_complete"] is True


def test_smooth_realization_is_exact() -> None:
    """Smooth realization should achieve exactness."""
    payload = coherence_law_and_holonomy_consistency_check()
    
    theorem = payload["theorem"]
    assert theorem["yukawa_coherence_law_is_consistent"] is True
    assert theorem["holonomy_witness_is_consistent_with_mass_generation"] is True
    assert theorem["no_obstruction_between_transport_and_masses"] is True
    assert theorem["smooth_realization_is_exact"] is True
