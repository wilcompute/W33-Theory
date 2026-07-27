"""Regression tests for the exact shifted-adjacency audit."""
from analysis.w33_shifted_adjacency_spectral_audit import audit


def test_shifted_adjacency_spectral_audit() -> None:
    result = audit()
    assert result["status"] == "PASS"
    assert result["srg"]["parameters"] == [40, 12, 2, 4]
    assert result["adjacency_spectrum"] == {"12": 1, "2": 24, "-4": 15}
    assert result["shifted_spectrum"] == {"11": 1, "1": 24, "-5": 15}
    assert result["projector_ranks"] == {"11": 1, "1": 24, "-5": 15}
    assert result["historical_claim_audit"]["annihilates_D"] is False
    assert result["historical_claim_audit"]["matrix_residual_rank"] == 40
    assert result["moments_0_to_10"]["1"] == -40
    assert result["moments_0_to_10"]["2"] == 520
    assert result["moments_0_to_10"]["3"] == -520
