"""Frobenius phase and finite-rank W33/arithmetic integration regression tests."""
import numpy as np
from analysis.w33_20261021_local_frobenius_phase_split import theorem,geometry,elliptic_points
from analysis.w33_20261021_rank_two_arithmetic_interface import certificate

def test_levi_eight_step_local_arithmetic_clock():
    r=theorem()
    assert r["status"]=="PASS_EXACT_LOCAL_ARITHMETIC"
    assert r["classical_RH_proved"] is False
    assert r["Levi_prime3"]["nontrivial_dimension"]==156
    assert r["Levi_prime3"]["normalized_trace_cycle"]==[0,-60,0,-36,0,-60,0,156]

def test_p11_ordinary_nonperiodic_obstruction():
    r=theorem()["collinearity_prime11"]
    assert r["ordinary"] and r["normalized_phase_order"]=="infinite"
    assert r["elliptic_curves"]["E_plus"]["trace"]==2
    assert r["elliptic_curves"]["E_minus"]["trace"]==-4
    assert elliptic_points(11,-1,0)==(12,0)

def test_w33_geom():
    A,N=geometry()
    assert A.shape==N.shape==(40,40)
    assert np.all(A.sum(axis=0)==12)
    assert np.all(N.sum(axis=0)==4)
    assert np.all(N.sum(axis=1)==4)

def test_rank_two_coupling_interlacing_and_dark_modes():
    r=certificate()
    assert r["classical_RH_proved"] is False
    assert r["offdiagonal_rank"]==2
    assert r["bright_internal_dimensions"]==2
    assert r["dark_internal_dimensions"]==37
    assert all(abs(v["difference"])<=41 for v in r["count_checks"].values())

def test_schur_determinant_ratio():
    r=certificate()
    for v in r["determinant_checks"].values():
        assert abs(v["Feshbach"]-v["full_matrix"])<1e-8
