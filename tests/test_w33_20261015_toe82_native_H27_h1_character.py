"""Regression tests for TOE82 native H27 homology character."""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "analysis"))
from w33_20261015_toe82_native_H27_h1_character import certificate, mul


def test_h27_exponent_and_noncommutativity():
    e = (0, 0, 0)
    elements = [(a, b, c) for a in range(3) for b in range(3) for c in range(3)]
    assert all(mul(mul(g, g), g) == e for g in elements)
    assert mul((1, 0, 0), (0, 1, 0)) != mul((0, 1, 0), (1, 0, 0))


def test_native_h1_character_and_irreducible_decomposition():
    r = certificate()
    assert r["complex"] == {
        "vertices": 27, "edges": 135, "faces": 45,
        "boundary_ranks_F2": [26, 45], "H1_dimension": 64}
    assert r["H27_character_values"] == {
        "identity": 64, "two_nonidentity_central_elements": -8,
        "twenty_four_noncentral_elements": -2}
    assert r["H27_invariant_H1_dimension_characteristic_zero"] == 0
    assert r["linear_character_multiplicities"]["0,0"] == 0
    assert sorted(r["linear_character_multiplicities"].values()) == [0] + [2] * 8
    assert set(r["schrodinger_3d_irrep_multiplicities"].values()) == {8}
