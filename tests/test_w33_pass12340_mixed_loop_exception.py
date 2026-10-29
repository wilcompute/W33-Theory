"""Exact arithmetic and independent complex controls for the explicit mode."""
from pathlib import Path
import sys
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'analysis'))
import w33_pass12340_mixed_loop_exception as core


def test_rational_lift_exact_ranks():
    c = core.certificate()
    assert c['exact_ranks'] == dict(short=105,mixed=107,six=108,gradient=27)
    assert c['physical_magnetic_kernel_dimension'] == 1
    assert c['six_loop_physical_magnetic_kernel_dimension'] == 0


def test_explicit_mode_is_not_gauge_and_is_lifted_by_six_flux_action():
    _,_,m0,m1,f0,f1,d0,d1,_,_ = core.operators()
    w = core.witness()
    omega = complex(-.5,np.sqrt(3)/2)
    v = np.array(w['a'],float)+omega*np.array(w['b'],float)
    v /= np.linalg.norm(v)
    F = np.array(m0,float)+omega*np.array(m1,float)
    G = np.array(d0,float)+omega*np.array(d1,float)
    F6 = np.array(f0,float)+omega*np.array(f1,float)
    assert np.max(abs(F@v)) < 1e-12
    assert np.max(abs(G.conj().T@v)) < 1e-12
    assert np.linalg.norm(F6@v) > .01
    # In a unitary Bloch character, a nonzero vector orthogonal to im G
    # cannot itself be a gradient.
    assert np.linalg.matrix_rank(G) == 27


def test_supplied_difference_loop_repair_has_same_kernel_as_six_loop():
    c = core.certificate()
    _,_,m0,m1,f0,f1,_,_,_,_ = core.operators()
    omega = complex(-.5,np.sqrt(3)/2)
    F = np.array(m0,float)+omega*np.array(m1,float)
    F6 = np.array(f0,float)+omega*np.array(f1,float)
    loops = F6[-6:]
    # One of the nonzero difference factors alone already lifts this witness;
    # the all-four-direction repair guarantees the stated kernel theorem.
    repaired = np.vstack([F,(omega-1)*loops,(omega-1)*loops])
    assert np.linalg.matrix_rank(repaired) == 108
    w = c['witness']
    vector = np.array(w['a'],float)+omega*np.array(w['b'],float)
    observed = .006*np.linalg.norm(loops@vector)**2/np.linalg.norm(vector)**2
    from fractions import Fraction
    expected = float(Fraction(c['supplied_repair']['normalized_witness_quadratic_form']))
    assert abs(observed-expected) < 1e-14 and expected > 0
