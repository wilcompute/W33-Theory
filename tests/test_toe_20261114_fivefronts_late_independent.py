"""Independent regressions for five late TOE research fronts.

Validates full C64 witness gradient/Hessian, complete spin2 harmonic tower,
isolated clock no-go, symmetric frame Potts transition, and calibrated GHZ.
"""
import importlib.util
import json
import math
from pathlib import Path
import numpy as np
import pytest

ROOT=Path(__file__).resolve().parents[1]
SRC=ROOT/"analysis"/"toe_20261114_fivefronts_late_independent.py"

@pytest.fixture(scope="module")
def m():
    spec=importlib.util.spec_from_file_location("fivefronts_late",SRC)
    mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)
    return mod

def test_replay_5_producers(m):
    result=m.run()
    assert result["n_fronts"]==5
    assert len(result["results"])==5
    assert json.loads(m.OUT.read_text())["status"]==result["status"]

def test_F8_full_126dim_hessian_replay(m):
    r=m.f8_witness_full_hessian()
    assert r["projective_real_tangent_dim"]==126
    assert r["Pauli_labels_in_objective"]==567
    assert r["gradient_full_euclidean_residual"]<1e-10
    assert r["negative_tangent_eigenvalues"]==0
    assert r["near_zero_tangent_eigenvalues"]==2
    assert r["positive_tangent_eigenvalues"]==124
    assert r["seven_finite_difference_max_error"]<1e-4

def test_F8_exact_cyclotomic_value_consistency(m):
    r=m.f8_witness_full_hessian()
    c=(47-32*math.cos(2*math.pi/9))/9
    assert abs(r["c8"]-c)<1e-10
    assert "not global lower" in r["limitation"].lower() or "not global" in r["limitation"].lower()

def test_flat_F8_direction_nonlinear_probe(m):
    r=m.f8_witness_full_hessian()
    assert len(r["flat_geodesic_controls"])==6
    assert all(abs(row["delta_plus"])<1e-3 and abs(row["delta_minus"])<1e-3
               for row in r["flat_geodesic_controls"])

def test_spin2_tower_exact_degeneracy(m):
    r=m.spin2_and_maxwell_protected_sector()
    assert r["summed_internal_harmonic_degeneracy"]==6561
    assert r["zero_mass_spin2"]==1
    assert r["uniform_5D_abelian_vector_m2"]==0

@pytest.mark.parametrize("t", [1/100, 1/4, 1, 4, 100])
def test_spin2_KK_positive_and_minimum(t):
    lo=40*min(1,t)/(1+t)
    levels=[20*(a*(a+1)+t*b*(b+1))/(1+t) for a in range(9) for b in range(9) if a or b]
    assert all(x>0 for x in levels)
    assert min(levels)==pytest.approx(lo,abs=1e-12)

def test_exact_ring_far_site_no_go(m):
    r=m.clock_shift_far_hopping_exact()
    assert r["cycle_length"]==12
    assert r["random_branch_controls"]==100
    assert r["principal_log_opposite_site_magnitude"]==pytest.approx(math.pi/12,abs=1e-12)

def test_ring_no_go_independent_number_theory():
    n=12
    k=np.arange(n)
    for integers in (
        np.zeros(n,dtype=int),
        np.arange(n,dtype=int),
        np.array([2,-3,1,0,5,0,-1,4,1,-3,2,0])
    ):
        h=-2*np.pi*k/n+2*np.pi*integers
        far=sum(((-1)**int(j))*h[j] for j in range(n))/n
        ratio=far/(np.pi/n)
        assert abs(ratio-round(ratio))<1e-12
        assert round(ratio)%2!=0

def test_Potts_free_energy_equal_at_exact_coexistence(m):
    r=m.potts_frame_thermodynamic_selector()
    assert r["frame_count"]==1620
    assert r["permutation_invariant"] and r["PSp43_invariant"]
    assert r["free_energy_difference_exact_zero_at_coexistence"]
    assert 14<r["critical_betaJ_numeric"]<15
    assert r["uniform_spinodal_betaJ"]==1620
    assert not r["finite_M_spontaneous_selector"]

def test_Potts_critical_value_direct_numeric():
    q=1620
    beta=2*(q-1)*math.log(q-1)/(q-2)
    a=(q-1)/q
    b=1/(q*(q-1))
    Fo=a*math.log(a)+(q-1)*b*math.log(b)-.5*beta*(a*a+(q-1)*b*b)
    Fu=-math.log(q)-beta/(2*q)
    assert abs(Fo-Fu)<1e-12

def test_calibrated_GHZ_99pct_conditional_bound(m):
    r=m.calibrated_photonic_fidelity_confidence()
    assert r["physical_rails"]==16 and r["settings"]==5
    assert r["confusion_matrix_column_stochastic"]
    assert r["matrix_condition_number_1norm"]<1.2
    assert r["parity_gain"]>0
    assert r["corrected_99pct_one_sided_fidelity_lower"]>.5
    assert r["corrected_99pct_one_sided_fidelity_lower"]<r["synthetic_fidelity_estimator"]

def test_calibration_bias_bound_arithmetic(m):
    r=m.calibrated_photonic_fidelity_confidence()
    z=.5*r["assumed_column_l1_calibration_error"]
    e=2*r["assumed_each_flip_rate_calibration_error"]/r["parity_gain"]
    assert r["worst_case_calibration_bias"]==pytest.approx(
      z*r["readout_weight_max_absolute"] +e, abs=1e-13)


def test_F8_flat_quartic_numerical_factorization_and_degree8_identity(m):
    r=m.f8_witness_full_hessian()
    a,b,c=r["flat_quartic_trigonometric_coefficients"]
    assert abs(a*a-b*b-c*c)<1e-10
    assert abs(r["flat_quartic_square_discriminant"])<1e-10
    curves=r["flat_null_curved_trajectory_controls"]
    assert len(curves)==2
    for row in curves:
        assert abs(row["effective_quartic"])<1e-10
        assert row["degree8_identity_max_absolute_coefficient_residual"]<1e-10
        assert row["curve_transverse_quadratic_norm"]<1e-10
        assert all(abs(x["delta"])<1e-10 for x in row["relaxed_geodesic_values"])


def test_F8_numerical_straight_family_7_points_2_directions(m):
    r=m.f8_witness_full_hessian()
    a,b,c=r["flat_quartic_trigonometric_coefficients"]
    assert a==pytest.approx(math.hypot(b,c),abs=1e-10)
    angles=[row["angle_radians"] for row in r["flat_null_curved_trajectory_controls"]]
    assert (angles[1]-angles[0])==pytest.approx(math.pi/2,abs=1e-10)
