"""Tests for sign-trivial unipotent holonomy witness location and properties."""

import numpy as np
from scripts.w33_holonomy_witness_location_audit import (
    sign_trivial_unipotent_witness_matrix,
    verify_witness_properties,
    locate_witness_in_transport_carrier,
    locate_witness_in_chiral_sequence,
    sign_trivial_unipotent_witness_location_packet,
)


def test_witness_matrix_is_unipotent() -> None:
    """The witness should be unipotent (all eigenvalues = 1)."""
    H = sign_trivial_unipotent_witness_matrix()
    eigenvalues = np.linalg.eigvals(H)
    
    assert np.allclose(eigenvalues, 1.0), f"Eigenvalues should be 1, got {eigenvalues}"


def test_witness_matrix_is_sign_trivial() -> None:
    """The witness should have determinant = 1 (sign-trivial)."""
    H = sign_trivial_unipotent_witness_matrix()
    det = np.linalg.det(H)
    
    assert np.isclose(det, 1.0), f"Determinant should be 1, got {det}"


def test_witness_matrix_is_nontrivial() -> None:
    """The witness should be non-identity."""
    H = sign_trivial_unipotent_witness_matrix()
    
    assert not np.allclose(H, np.eye(H.shape[0])), "Witness should be non-identity"


def test_witness_nilpotent_part_is_nilpotent() -> None:
    """The nilpotent part N = H - I should be nilpotent (N^2 = 0 for size 2)."""
    H = sign_trivial_unipotent_witness_matrix()
    N = H - np.eye(H.shape[0])
    N2 = N @ N
    
    assert np.allclose(N2, 0), f"N^2 should be zero, got {N2}"


def test_verify_witness_properties_all_pass() -> None:
    """All verification properties should pass."""
    H = sign_trivial_unipotent_witness_matrix()
    props = verify_witness_properties(H)
    
    assert props["is_unipotent"] is True
    assert props["is_sign_trivial"] is True
    assert props["is_nontrivial"] is True
    assert props["nilpotent_part_is_nilpotent"] is True


def test_transport_carrier_dimension_is_45() -> None:
    """Transport carrier should have rank 45 = 1 + 24 + 20."""
    location = locate_witness_in_transport_carrier()
    
    assert location["transport_rank"] == 45
    assert (location["representation_triangle_blocks"]["identity_point"] 
            + location["representation_triangle_blocks"]["quadratic_points"]
            + location["representation_triangle_blocks"]["line_structure"] == 45)


def test_witness_embeds_in_transport_carrier() -> None:
    """Witness should embed as 2×2 in the Q_20 → S_20 block."""
    location = locate_witness_in_transport_carrier()
    
    assert location["witness_embedding_size"] == 2
    assert location["submodule_rank"] == 2
    assert location["preserved_rank"] == 43


def test_chiral_sequence_dimension_is_121() -> None:
    """Chiral sequence should have rank 121 = 59 + 59 + 3."""
    location = locate_witness_in_chiral_sequence()
    
    assert (location["chiral_plus_rank"] 
            + location["chiral_minus_rank"]
            + location["harmonic_rank"] == 121)


def test_witness_embeds_in_chiral_sequence() -> None:
    """Witness should embed in harmonic part (3-dim) of chiral sequence."""
    location = locate_witness_in_chiral_sequence()
    
    assert location["witness_embedding_size"] == 2
    assert location["harmonic_rank"] == 3
    assert location["preserved_rank"] == 119  # 121 - 2


def test_holonomy_witness_location_packet_theorem_all_pass() -> None:
    """All theorem conditions should hold."""
    payload = sign_trivial_unipotent_witness_location_packet()
    
    theorem = payload["theorem"]
    assert theorem["witness_is_unipotent"] is True
    assert theorem["witness_is_sign_trivial"] is True
    assert theorem["witness_is_nontrivial"] is True
    assert theorem["witness_nilpotent_part_is_nilpotent"] is True
    assert theorem["witness_embeds_in_transport_carrier"] is True
    assert theorem["witness_embeds_in_chiral_sequence"] is True
    assert theorem["witness_preserves_exactness"] is True
    assert theorem["witness_activates_tail_datum"] is True
    assert theorem["smooth_realization_witness_is_constructible"] is True


def test_witness_nilpotent_part_has_rank_one() -> None:
    """The nilpotent part N should have rank 1."""
    H = sign_trivial_unipotent_witness_matrix()
    N = H - np.eye(H.shape[0])
    rank_N = np.linalg.matrix_rank(N)
    
    assert rank_N == 1, f"Rank of N should be 1, got {rank_N}"


def test_witness_is_2x2_jordan_block() -> None:
    """Verify the witness is exactly the 2×2 Jordan block."""
    H = sign_trivial_unipotent_witness_matrix()
    expected = np.array([[1.0, 1.0], [0.0, 1.0]])
    
    assert np.allclose(H, expected)
