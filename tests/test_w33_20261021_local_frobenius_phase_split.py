"""Exact W33/Levi local Frobenius phase-order regression tests."""
import numpy as np
from analysis.w33_20261021_local_frobenius_phase_split import (
    geometry, theorem, elliptic_points
)

def test_exact_transfer_local_phase_identity():
    result=theorem()
    assert result["status"]=="PASS_EXACT_LOCAL_ARITHMETIC"
    assert result["classical_RH_proved"] is False
    levi=result["Levi_prime3"]
    assert levi["nontrivial_dimension"]==156
    assert levi["normalized_period"]==8
    assert levi["normalized_trace_cycle"]==[0,-60,0,-36,0,-60,0,156]

def test_two_ordinary_prime11_elliptic_factors():
    result=theorem()["collinearity_prime11"]
    assert result["ordinary"]
    assert result["normalized_phase_order"]=="infinite"
    assert [result["elliptic_curves"][key]["trace"] for key in ("E_plus","E_minus")]==[2,-4]
    assert elliptic_points(11,-1,0)==(12,0)

def test_geometry_provenance():
    A,N=geometry()
    assert np.array_equal(np.sum(A,axis=1),12*np.ones(40,dtype=np.int64))
    assert np.array_equal(np.sum(N,axis=1),4*np.ones(40,dtype=np.int64))
    assert np.array_equal(np.sum(N,axis=0),4*np.ones(40,dtype=np.int64))
