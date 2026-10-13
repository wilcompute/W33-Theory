"""TOE62 recovery regression: exact continuous high-temperature W33 flux theorem.

This small test intentionally regenerates its certificate from native data.
The complete TOE62 seven-producer regression remains on the connected
research computer until that connection is available again.
"""
import sys
from pathlib import Path
import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "analysis"))
from w33_20261013_toe62_global_flat_flux_proof import certificate


def test_continuous_flat_flux_global_beta7_theorem():
    c = certificate()
    assert c["status"] == "PASS_TOE62_RECOVERY_GLOBAL_HIGH_T_FLUX_PROOF"
    assert c["S_pi"] == -228
    assert c["S_zero"] == 238
    assert c["strict_cosine_distance_lower_coefficients"] == [75, 69, 69]
    assert sum(c["folded_winding_fourier_coefficients"].values()) == 238
    assert c["pi_minus_zero_beta7_coefficient"] == pytest.approx(
        -0.1964781746031746
    )
    assert len(c["native_trace_and_cosine_checks"]) == 7
    assert max(abs(r["eighth_moment_residual"])
               for r in c["native_trace_and_cosine_checks"]) < 1e-6
    assert min(r["inequality_slack"]
               for r in c["native_trace_and_cosine_checks"]) > -1e-10


def test_exact_worst_case_positive_hopping_disorder_threshold():
    c = certificate()
    assert 0.14 < c["rigorous_sufficient_link_disorder_threshold"] < 0.141
    assert "does not prove every-beta" in c["scope"]
