"""Tests for tomotope perturbation response law under CKM alignment."""

from scripts.w33_tomotope_perturbation_law_audit import (
    e_sector_base_split,
    tomotope_imbalance,
    tomotope_imbalance_under_alignment,
    tomotope_perturbation_response_law,
)


def test_base_tomotope_split_is_correct() -> None:
    """Base tomotope split from Part CXXVII should be exact."""
    split = e_sector_base_split()
    
    # Check pair counts
    total_pairs = sum(split.values())
    assert total_pairs == 192, f"Expected 192 pairs, got {total_pairs}"
    
    # Check split
    assert split["same_four_overlap"] == 36
    assert split["same_one_overlap"] == 60
    assert split["opposite_four_overlap"] == 60
    assert split["opposite_one_overlap"] == 36


def test_base_imbalance_is_positive_24() -> None:
    """Imbalance should be +24 (opposite_four - same_four)."""
    split = e_sector_base_split()
    imbalance = tomotope_imbalance(split)
    
    assert imbalance == 24, f"Expected +24, got {imbalance}"


def test_alignment_zero_gives_base_imbalance() -> None:
    """At alignment=0, imbalance should equal base imbalance of 24."""
    imbalance = tomotope_imbalance_under_alignment(0.0)
    assert abs(imbalance - 24.0) < 0.1


def test_alignment_one_gives_zero_imbalance() -> None:
    """At alignment=1, imbalance should approach zero."""
    imbalance = tomotope_imbalance_under_alignment(1.0)
    assert abs(imbalance) < 0.1


def test_quadratic_model_is_monotone_decreasing() -> None:
    """As alignment increases, imbalance should monotonically decrease."""
    alignments = [0.0, 0.2, 0.4, 0.6, 0.8, 1.0]
    imbalances = [tomotope_imbalance_under_alignment(a, power=2) for a in alignments]
    
    # Should be monotone decreasing
    for i in range(len(imbalances) - 1):
        assert imbalances[i] >= imbalances[i + 1], (
            f"Not monotone at step {i}: {imbalances[i]} > {imbalances[i+1]}"
        )


def test_intermediate_alignments_give_intermediate_imbalances() -> None:
    """At intermediate alignment (e.g., 0.5), imbalance should be intermediate."""
    imb_0 = tomotope_imbalance_under_alignment(0.0, power=2)
    imb_50 = tomotope_imbalance_under_alignment(0.5, power=2)
    imb_100 = tomotope_imbalance_under_alignment(1.0, power=2)
    
    # Intermediate should be between endpoints
    assert imb_0 >= imb_50 >= imb_100


def test_perturbation_response_law_all_theorems_pass() -> None:
    """All theorem conditions of the law should hold."""
    payload = tomotope_perturbation_response_law()
    
    theorem = payload["theorem"]
    assert theorem["tomotope_imbalance_responds_to_alignment"] is True
    assert theorem["quadratic_model_is_monotone_decreasing"] is True
    assert theorem["alignment_zero_recovers_base_imbalance"] is True
    assert theorem["alignment_one_approaches_zero_imbalance"] is True


def test_response_law_provides_finite_packets() -> None:
    """Response law should generate finite/checkable packets."""
    payload = tomotope_perturbation_response_law()
    
    # Check structure
    assert "alignment_scan_points" in payload
    assert "imbalance_curves" in payload
    assert "quadratic_model_properties" in payload
    
    # Check data completeness
    assert len(payload["alignment_scan_points"]) == 11
    assert len(payload["imbalance_curves"]) == 3  # three power laws
    
    # Check quadratic properties
    props = payload["quadratic_model_properties"]
    assert "is_monotone_decreasing" in props
    assert "range" in props
    assert props["is_monotone_decreasing"] is True
