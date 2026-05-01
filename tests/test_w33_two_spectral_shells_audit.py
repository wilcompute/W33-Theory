"""Test for Part LXXXV: two spectral shells audit."""

import pytest
from scripts.w33_two_spectral_shells_audit import build_two_spectral_shells_summary


def test_two_spectral_shells_records_carrier_structure():
    """Test that the audit records the carrier dimensions."""
    summary = build_two_spectral_shells_summary()
    carrier = summary["carrier_structure"]
    
    assert carrier["light_shell_rank"] == 78
    assert carrier["heavy_shell_rank"] == 40
    assert carrier["harmonic_dimension"] == 3
    assert carrier["total_dimension"] == 121


def test_two_spectral_shells_parseval_identity():
    """Test that the Parseval identity 25 B4Bt + 8 R5Rt = 7200I - 180J holds."""
    summary = build_two_spectral_shells_summary()
    identities = summary["spectrum_algebraic_identities"]
    
    assert identities["parseval_identity_25_B4Bt_plus_8_R5Rt"]["holds"]


def test_two_spectral_shells_shell_ratio_is_2():
    """Test that sqrt(72)/sqrt(18) = 2."""
    summary = build_two_spectral_shells_summary()
    ratio_data = summary["shell_scaling_relations"]["shell_scale_ratio"]
    
    assert abs(ratio_data["ratio"] - 2.0) < 1e-9
    assert ratio_data["expected_ratio"] == 2.0


def test_two_spectral_shells_18_and_72_relations():
    """Test that 18 = 2q^2 and 72 = 8q^2 for q=3."""
    summary = build_two_spectral_shells_summary()
    relations = summary["shell_scaling_relations"]
    
    assert relations["18_equals_2q_squared"]["holds"]
    assert relations["72_equals_8q_squared"]["holds"]
    assert relations["72_equals_4_times_18"]["holds"]


def test_two_spectral_shells_chiral_decomposition():
    """Test the chiral decomposition: 59 + 59 + 3 = 121."""
    summary = build_two_spectral_shells_summary()
    chiral = summary["chiral_decomposition"]
    
    assert chiral["light_modes_per_chirality"] == 39
    assert chiral["heavy_modes_per_chirality"] == 20
    assert chiral["total_exact_modes_per_chirality"] == 59
    assert chiral["harmonic_modes"] == 3


def test_two_spectral_shells_theorem():
    """Test that all theorem statements hold."""
    summary = build_two_spectral_shells_summary()
    theorem = summary["theorem"]
    
    assert all(theorem.values()), f"Some theorem checks failed: {theorem}"


def test_part_lxxxv_note_mentions_the_executable_surface():
    """Test that the local Part LXXXV note mentions the audit."""
    try:
        with open("PART_LXXXV_TWO_SPECTRAL_SHELLS.md", "r") as f:
            content = f.read()
            assert "w33_two_spectral_shells_audit" in content or "two_spectral_shells" in content
    except FileNotFoundError:
        pytest.skip("PART_LXXXV note not yet created")
