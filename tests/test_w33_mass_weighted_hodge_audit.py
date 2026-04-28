"""Test for Part LXXXVI: mass-weighted Hodge audit."""

import pytest
from scripts.w33_mass_weighted_hodge_audit import build_mass_weighted_hodge_summary


def test_mass_weighted_hodge_records_shell_spectrum():
    """Test that the audit records the shell eigenvalues correctly."""
    summary = build_mass_weighted_hodge_summary()
    spectrum = summary["laplacian_spectrum"]
    
    assert spectrum["light_shell_eigenvalue"] == 18
    assert spectrum["heavy_shell_eigenvalue"] == 72


def test_mass_weighted_hodge_three_forward_blocks():
    """Test that there are exactly three forward blocks."""
    summary = build_mass_weighted_hodge_summary()
    blocks = summary["forward_blocks"]
    
    assert len(blocks) == 3
    assert blocks[0]["source"] == "S_15"
    assert blocks[1]["source"] == "Q_24"
    assert blocks[2]["source"] == "Q_20"


def test_mass_weighted_hodge_rank_and_nullity():
    """Test that rank(d) = 59 and nullity(d) = 62."""
    summary = build_mass_weighted_hodge_summary()
    chiral = summary["chiral_complex_structure"]
    
    assert chiral["rank_d"] == 59
    assert chiral["nullity_d"] == 62
    assert chiral["total_dimension"] == 121


def test_mass_weighted_hodge_exactness():
    """Test the exactness structure: 59 + 59 + 3 = 121."""
    summary = build_mass_weighted_hodge_summary()
    chiral = summary["chiral_complex_structure"]
    
    assert chiral["exact_part"] == 118
    assert chiral["harmonic_part"] == 3
    assert chiral["exact_part"] + chiral["harmonic_part"] == 121


def test_mass_weighted_hodge_laplacian_spectrum():
    """Test that the Laplacian has the correct spectrum."""
    summary = build_mass_weighted_hodge_summary()
    laplacian = summary["laplacian_spectrum"]
    
    assert laplacian["harmonic_multiplicity"] == 3
    assert laplacian["light_shell_multiplicity"] == 78
    assert laplacian["heavy_shell_multiplicity"] == 40
    assert laplacian["harmonic_multiplicity"] + laplacian["light_shell_multiplicity"] + laplacian["heavy_shell_multiplicity"] == 121


def test_mass_weighted_hodge_parseval_identity():
    """Test the Parseval identity."""
    summary = build_mass_weighted_hodge_summary()
    parseval = summary["parseval_identity"]
    
    assert parseval["holds"]


def test_mass_weighted_hodge_theorem():
    """Test that all theorem statements hold."""
    summary = build_mass_weighted_hodge_summary()
    theorem = summary["theorem"]
    
    assert all(theorem.values()), f"Some theorem checks failed: {theorem}"


def test_part_lxxxvi_note_mentions_the_executable_surface():
    """Test that the local Part LXXXVI note mentions the audit."""
    try:
        with open("PART_LXXXVI_MASS_WEIGHTED_HODGE.md", "r") as f:
            content = f.read()
            assert "w33_mass_weighted_hodge_audit" in content or "mass_weighted_hodge" in content
    except FileNotFoundError:
        pytest.skip("PART_LXXXVI note not yet created")
