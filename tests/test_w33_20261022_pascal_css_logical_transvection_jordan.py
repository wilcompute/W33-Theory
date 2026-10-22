"""Regression checks for prime-field logical transvection Jordan census."""
import pytest

from analysis.w33_20261022_pascal_css_logical_transvection_jordan import (
    census,
    predicted_blocks,
)


@pytest.mark.parametrize("p,rank_b,logical_dim,rank_chain", [
    (2, 4, 7, [7, 2, 0]),
    (3, 10, 20, [20, 10, 3, 0]),
    (5, 35, 86, [86, 60, 37, 18, 5, 0]),
    (7, 84, 232, [232, 182, 135, 92, 55, 26, 7, 0]),
])
def test_logical_transvection_jordan(p, rank_b, logical_dim, rank_chain):
    result = census(p)
    assert result["rank_B"] == rank_b
    assert result["logical_dimension"] == logical_dim
    assert result["rank_powers_T_minus_I_on_Q"] == rank_chain
    assert result["Jordan_blocks"] == predicted_blocks(p)
    assert sum(int(j) * m for j, m in result["Jordan_blocks"].items()) == logical_dim
    assert sum(result["Jordan_blocks"].values()) == p*p + 1
    if p <= 5:
        assert result["homogeneous_degree_p_minus_1_rank"] == rank_b
