"""
Refinement/scaling firewall for the exact W(3,3) spectral closure.

These checks formalize the obstruction that remains after the exact finite
Dirac/Hodge package is closed: a fixed finite spectrum cannot itself be the
full 4D continuum theorem. To get an actual Einstein-Hilbert plus Standard
Model limit, the project still needs a genuine refinement family or an
almost-commutative product with a 4D continuum geometry.
"""

from __future__ import annotations

import numpy as np

import sys as _sys
from pathlib import Path as _Path
_sys.path.insert(0, str(_Path(__file__).resolve().parent))  # tests/ is not a package (2026-10-30)
from test_continuum_limit import DIM_TOTAL, E, spectral_data  # noqa: E402


ZERO_TOL = 1e-12


def _heat_trace(eigs: np.ndarray, t: float) -> float:
    return float(np.sum(np.exp(-t * eigs)))


def _spectral_zeta(eigs: np.ndarray, s: float) -> float:
    nonzero = eigs[eigs > ZERO_TOL]
    return float(np.sum(nonzero ** (-s)))


def _counting_function(eigs: np.ndarray, cutoff: float) -> int:
    return int(np.sum(eigs <= cutoff + ZERO_TOL))


class TestFixedSpectrumFirewall:
    def test_full_chain_heat_trace_has_finite_origin(self, spectral_data):
        eigs = spectral_data["eigs_D2"]
        values = [_heat_trace(eigs, t) for t in (1e-4, 1e-5, 1e-6)]
        assert values[0] < values[1] < values[2] < DIM_TOTAL + 1e-9
        assert abs(values[-1] - DIM_TOTAL) < 0.01

    def test_full_chain_has_no_four_dimensional_heat_singularity(self, spectral_data):
        eigs = spectral_data["eigs_D2"]
        scaled = [t * t * _heat_trace(eigs, t) for t in (1e-3, 1e-4, 1e-5)]
        assert scaled[0] > scaled[1] > scaled[2] > 0.0
        assert scaled[-1] < 1e-6

    def test_l1_zeta_is_finite_at_candidate_four_dimensional_pole(self, spectral_data):
        zeta_at_two = _spectral_zeta(spectral_data["eigs_L1"], 2.0)
        assert np.isfinite(zeta_at_two)
        assert zeta_at_two > 0.0

    def test_l1_zeta_converges_to_a_finite_limit_at_s_equal_2(self, spectral_data):
        eigs = spectral_data["eigs_L1"]
        zeta_at_two = _spectral_zeta(eigs, 2.0)
        near = [_spectral_zeta(eigs, 2.0 + eps) for eps in (1e-1, 1e-2, 1e-3)]
        assert near[0] < near[1] < near[2] < zeta_at_two + 1e-2
        assert abs(near[-1] - zeta_at_two) < 2e-2

    def test_true_weyl_counting_function_saturates_after_the_top_eigenvalue(self, spectral_data):
        eigs = spectral_data["eigs_L1"]
        counts = [_counting_function(eigs, cutoff) for cutoff in (20.0, 40.0, 80.0, 160.0)]
        assert counts == [E, E, E, E]

    def test_true_weyl_ratio_decays_to_zero_once_the_spectrum_saturates(self, spectral_data):
        eigs = spectral_data["eigs_L1"]
        ratios = [_counting_function(eigs, cutoff) / (cutoff * cutoff) for cutoff in (20.0, 40.0, 80.0, 160.0)]
        assert ratios[0] > ratios[1] > ratios[2] > ratios[3] > 0.0
        assert ratios[-1] < 0.01
