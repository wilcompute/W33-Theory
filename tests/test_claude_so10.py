"""Tests that capture Claude's SO(10) claims (smoke / deterministic).

- Verifies the E6 27 -> 16 + 10 + 1 decomposition via Q_psi charges.
- Verifies the Weinberg-angle derivation sin^2(theta_W) = 3/8.

These are compact, deterministic checks that codify Claude's outputs into CI tests.
"""

from __future__ import annotations

import math
from pathlib import Path

import pytest

from scripts.w33_weinberg_dirac import weinberg_angle_derivation

# repository modules (tools/scripts are importable in the test environment)
from tools import toe_sm_cubic_firewall_analysis as sm

CARTAN_MATS_PATH = (
    Path(__file__).resolve().parents[1]
    / "artifacts"
    / "e6_27rep_basis_export"
    / "Cartan_mats.npy"
)


@pytest.mark.skipif(
    not CARTAN_MATS_PATH.exists(),
    reason="SO(10) Q_psi decomposition requires optional E6 Cartan_mats.npy export",
)
def test_so10_qpsi_decomposition_counts():
    """Check Q_psi pattern: 16 (Q_psi=1), 10 (Q_psi=-2), 1 (Q_psi=4)."""
    w27 = sm._compute_weights_27()
    omega_psi = sm._fund_coweight(0)  # fundamental coweight that yields Q_psi

    qpsi_fracs = [sm._dot_frac(w27[i], omega_psi) for i in range(27)]
    qpsi3 = [int(x * 3) for x in qpsi_fracs]

    assert qpsi3.count(1) == 16
    assert qpsi3.count(-2) == 10
    assert qpsi3.count(4) == 1
    assert sum(qpsi3.count(v) for v in (1, -2, 4)) == 27


def test_weinberg_angle_is_3_over_8():
    """Weinberg-angle derivation (W33 / E6 context) should give 3/8 at GUT scale."""
    out = weinberg_angle_derivation()
    assert math.isclose(
        out.get("sin2_theta_W", 0.0), 3.0 / 8.0, rel_tol=0, abs_tol=1e-15
    )
