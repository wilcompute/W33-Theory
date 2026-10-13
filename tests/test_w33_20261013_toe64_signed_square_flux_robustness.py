"""TOE64 source-regenerated signed-square exactness and sharpness checks."""
import sys
from pathlib import Path
import numpy as np
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"analysis"))
from w33_20261013_toe64_signed_square_flux_robustness import (
    certificate, matrices, exact_square_decomposition,
)
def test_signed_matrix_and_critical_eigenmode():
    D,M=matrices(np.array([79,77,77]),np.array([1,1,3]))
    assert np.array_equal(M,np.array([[2,1,1],[1,4,-3],[1,-3,4]]))
    q=np.array([0,1,-1])/np.sqrt(2)
    assert np.allclose((D-11*M)@q,np.zeros(3),atol=1e-12)
    assert np.linalg.eigvalsh(D-11*M)[0]>-1e-12

def test_exact_decomposition_and_critical_epsilon():
    z=certificate()
    assert z["status"]=="PASS_TOE64_SIGNED_SQUARE_FLUX_ROBUSTNESS"
    assert .1487 < z["critical_epsilon"] < .1488
    assert z["critical_epsilon"] > z["compared_to_toe63_epsilon"]
    assert z["stress_independent_coefficient_trials"]==750
    assert z["max_abs_exact_square_identity_error"]<1e-10

def test_box_sharpness_not_edge_product_claim():
    z=certificate()
    assert z["box_only_negative_energy_example"]<0
    assert "not proved optimal" in z["scope"]
