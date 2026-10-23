"""Exact logical PSp(4,3) generators on the [[40,20,4]]_3 point CSS."""
import numpy as np
from analysis.w33_20261022_css_logical_sp43_generators import (
    certify, cycle_lengths, group_order
)


def test_all_five_generators_and_logical_homomorphism():
    r = certify()
    assert r["partial_generator_group_orders"] == [3, 24, 72, 288, 25920]
    assert r["Q_dimension"] == 20
    assert r["projective_transvection_cycle_profile"] == {"fixed":13,"3_cycles":9}
    assert r["random_word_consistency_checks"] == 100
    assert not r["physical_locality_assumed"]
    assert len(r["logical_generator_matrices"]) == 5
    for matrix in r["logical_generator_matrices"]:
        L = np.array(matrix, dtype=np.int64)
        eye = np.eye(20, dtype=np.int64)
        assert L.shape == (20, 20)
        assert np.array_equal(L @ L @ L % 3, eye)
        assert np.count_nonzero(L) >= 20
