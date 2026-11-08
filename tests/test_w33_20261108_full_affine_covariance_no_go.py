"""Proof regressions for the five-class affine congruence no-go."""
import importlib.util
from pathlib import Path
import pytest
P=Path(__file__).resolve().parents[1]/"analysis/w33_20261108_full_affine_covariance_no_go.py"
spec=importlib.util.spec_from_file_location("affine_mixing",P)
M=importlib.util.module_from_spec(spec)
spec.loader.exec_module(M)

@pytest.mark.parametrize("p", [3,5,7,11,13,17])
def test_exact_orbit_coefficients(p):
    x=M.certify(p)
    assert x["orbit_character_coefficients_at_010"]==[1,(p-1)//2,(p-1)//2,
         -p if p%4==1 else 0,-p if p%4==3 else 0]
    assert sum(abs(z) for z in x["orbit_character_coefficients_at_010"])==2*p
    assert sum(c["dimension"] for c in x["dual_orbits"])==p**3

@pytest.mark.parametrize("p", [3,5,7,11,13,17])
def test_finite_additive_character_phase_counts(p):
    x=M.certify(p)
    for o in x["dual_orbits"]:
        assert o["count_phase_zero"]+(p-1)*o["count_each_nonzero_phase"]==o["dimension"]
        assert o["count_phase_zero"]-o["count_each_nonzero_phase"]==o["fourier_coefficient_at_010"]

@pytest.mark.parametrize("p", [5,7,11,13,17])
def test_global_all_time_bound_is_strict(p):
    x=M.certify(p)
    assert x["max_unitary_transition_amplitude"] < x["uniform_amplitude_required"]
    assert x["uniform_mixing_forbidden"]

def test_p3_is_not_excluded():
    x=M.certify(3)
    assert not x["uniform_mixing_forbidden"]
    assert x["max_unitary_transition_amplitude"]>x["uniform_amplitude_required"]

@pytest.mark.parametrize("p", [3,5,7,11,13])
def test_correct_group_is_not_projective_GL_for_high_fields(p):
    x=M.certify(p)
    assert x["GL2_mod_pm_identity_order"]==x["PGL2_order"]*(p-1)//2
    assert x["distinct_from_PGL2"]==(p>3)

def test_all_symmetry_assumptions_visible():
    z=M.build()
    assert "translations and GL2(q) congruences" in z["theorem"]
    assert "not PGL2(q)" in z["group_correction"]
    assert "not measured physics" in z["scope"]
