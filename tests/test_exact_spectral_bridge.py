"""
Exact spectral bridge identities for the full 4D W(3,3) clique complex.

This file sharpens the continuum-bridge story at the operator level.  It does
not claim the full refinement theorem to continuum Einstein-Hilbert + Standard
Model.  What it does close exactly is the discrete spectral side on

    C_0 ⊕ C_1 ⊕ C_2 ⊕ C_3,  dim = 480.

The full Dirac/Hodge system has a closed spectrum, closed heat traces, and an
exact McKean-Singer supertrace.  So the remaining continuum question is the
refinement/scaling bridge, not ambiguity in the discrete spectral triple.
"""

from __future__ import annotations

import math

import numpy as np

import sys as _sys
from pathlib import Path as _Path
_sys.path.insert(0, str(_Path(__file__).resolve().parent))  # tests/ is not a package (2026-10-30)
from test_continuum_limit import EULER_CHI, spectral_data  # noqa: E402


ZERO_TOL = 1e-8


def _multiplicity_map(values: np.ndarray, targets: list[float]) -> dict[float, int]:
    counts: dict[float, int] = {}
    for target in targets:
        counts[target] = int(np.sum(np.isclose(values, target, atol=ZERO_TOL)))
    return counts


def _even_heat_trace(t: float) -> float:
    return 1 + 160 * math.exp(-4 * t) + 24 * math.exp(-10 * t) + 15 * math.exp(-16 * t)


def _odd_heat_trace(t: float) -> float:
    return 81 + 160 * math.exp(-4 * t) + 24 * math.exp(-10 * t) + 15 * math.exp(-16 * t)


def _full_heat_trace(t: float) -> float:
    return 82 + 320 * math.exp(-4 * t) + 48 * math.exp(-10 * t) + 30 * math.exp(-16 * t)


class TestExactFullChainSpectrum:
    def test_full_d_squared_multiplicities(self, spectral_data):
        eigs = spectral_data["eigs_D2"]
        mults = _multiplicity_map(eigs, [0.0, 4.0, 10.0, 16.0])
        assert mults == {0.0: 82, 4.0: 320, 10.0: 48, 16.0: 30}

    def test_full_dirac_absolute_multiplicities(self, spectral_data):
        eigs = np.abs(spectral_data["eigs_D"])
        mults = _multiplicity_map(eigs, [0.0, 2.0, math.sqrt(10.0), 4.0])
        assert mults == {0.0: 82, 2.0: 320, math.sqrt(10.0): 48, 4.0: 30}

    def test_signed_dirac_spectrum_exact(self, spectral_data):
        eigs = spectral_data["eigs_D"]
        assert int(np.sum(np.isclose(eigs, 0.0, atol=ZERO_TOL))) == 82
        assert int(np.sum(np.isclose(eigs, 2.0, atol=ZERO_TOL))) == 160
        assert int(np.sum(np.isclose(eigs, -2.0, atol=ZERO_TOL))) == 160
        assert int(np.sum(np.isclose(eigs, math.sqrt(10.0), atol=ZERO_TOL))) == 24
        assert int(np.sum(np.isclose(eigs, -math.sqrt(10.0), atol=ZERO_TOL))) == 24
        assert int(np.sum(np.isclose(eigs, 4.0, atol=ZERO_TOL))) == 15
        assert int(np.sum(np.isclose(eigs, -4.0, atol=ZERO_TOL))) == 15


class TestExactHeatTraceClosure:
    def test_even_heat_trace_closed_form(self, spectral_data):
        eigs_even = np.concatenate([spectral_data["eigs_L0"], spectral_data["eigs_L2"]])
        for t in (0.01, 0.1, 0.5, 1.0, 2.0):
            lhs = float(np.sum(np.exp(-t * eigs_even)))
            rhs = _even_heat_trace(t)
            assert abs(lhs - rhs) < 1e-9

    def test_odd_heat_trace_closed_form(self, spectral_data):
        eigs_odd = np.concatenate([spectral_data["eigs_L1"], spectral_data["eigs_L3"]])
        for t in (0.01, 0.1, 0.5, 1.0, 2.0):
            lhs = float(np.sum(np.exp(-t * eigs_odd)))
            rhs = _odd_heat_trace(t)
            assert abs(lhs - rhs) < 1e-9

    def test_full_heat_trace_closed_form(self, spectral_data):
        eigs = spectral_data["eigs_D2"]
        for t in (0.01, 0.1, 0.5, 1.0, 2.0):
            lhs = float(np.sum(np.exp(-t * eigs)))
            rhs = _full_heat_trace(t)
            assert abs(lhs - rhs) < 1e-9

    def test_mcKean_singer_supertrace_is_exact(self, spectral_data):
        eigs_even = np.concatenate([spectral_data["eigs_L0"], spectral_data["eigs_L2"]])
        eigs_odd = np.concatenate([spectral_data["eigs_L1"], spectral_data["eigs_L3"]])
        for t in (0.01, 0.1, 0.5, 1.0, 2.0, 10.0):
            supertrace = float(np.sum(np.exp(-t * eigs_even)) - np.sum(np.exp(-t * eigs_odd)))
            assert abs(supertrace - EULER_CHI) < 1e-9
            assert abs(supertrace - (_even_heat_trace(t) - _odd_heat_trace(t))) < 1e-9


class TestExactEvenOddPairing:
    def test_nonzero_even_odd_d_squared_spectra_match(self, spectral_data):
        even = np.concatenate([spectral_data["eigs_L0"], spectral_data["eigs_L2"]])
        odd = np.concatenate([spectral_data["eigs_L1"], spectral_data["eigs_L3"]])
        even_nz = even[even > ZERO_TOL]
        odd_nz = odd[odd > ZERO_TOL]
        assert np.allclose(np.sort(even_nz), np.sort(odd_nz), atol=ZERO_TOL)

    def test_positive_supertrace_moments_vanish(self, spectral_data):
        for power in range(1, 6):
            even = (
                np.trace(np.linalg.matrix_power(spectral_data["L0"], power))
                + np.trace(np.linalg.matrix_power(spectral_data["L2"], power))
            )
            odd = (
                np.trace(np.linalg.matrix_power(spectral_data["L1"], power))
                + np.trace(np.linalg.matrix_power(spectral_data["L3"], power))
            )
            assert abs(even - odd) < 1e-6

    def test_zero_mode_defect_is_topological_only(self, spectral_data):
        even_zero = int(np.sum(np.isclose(spectral_data["eigs_L0"], 0.0, atol=ZERO_TOL)))
        odd_zero = int(np.sum(np.isclose(spectral_data["eigs_L1"], 0.0, atol=ZERO_TOL)))
        assert even_zero == 1
        assert odd_zero == 81
        assert even_zero - odd_zero == EULER_CHI
