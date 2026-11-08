"""Finite isometric chirp: exact escape from the full GL2 obstruction."""
import importlib.util
from pathlib import Path
import pytest
P=Path(__file__).resolve().parents[1]/"analysis/w33_20261108_lorentz_chirp_escape.py"
spec=importlib.util.spec_from_file_location("lorentz_chirp_escape",P)
M=importlib.util.module_from_spec(spec);spec.loader.exec_module(M)

@pytest.fixture(scope="module")
def cert():return M.produce()

@pytest.mark.parametrize("p", [3,5,7,11,13,17])
def test_flat_gaussian_chirp_is_unitary(p):
    d=M.certify(p)
    assert d["spectral_unitarity_error"]<1e-12
    assert d["vertices"]==p**3

@pytest.mark.parametrize("p", [3,5,7,11,13,17])
def test_correct_isometry_subgroup_index(p):
    d=M.certify(p)
    assert d["full_GL2_order"]//d["determinant_pm1_isometry_subgroup_order"]==(p-1)//2
    assert d["isometry_symmetry_is_full_congruence"]==(p==3)
    assert (d["GL2_nonisometric_example_diag_r"] is None)==(p==3)

def test_p5_index_two_is_minimal_nontrivial_group_reduction(cert):
    x=next(d for d in cert["cases"] if d["prime"]==5)
    assert x["minimal_symmetry_breaking_index_for_this_chirp"]==2
    assert x["determinant_pm1_isometry_subgroup_order"]*2==x["full_GL2_order"]

@pytest.mark.parametrize("p", [3,5,7,11,13,17])
def test_principal_log_generator_is_not_null_local(p):
    d=M.certify(p)
    assert d["principal_log_generator_is_nonlocal"]
    assert d["principal_log_generator_off_null_support"]>0

def test_not_physical_lorentz_or_new_qm(cert):
    assert "no physical continuum" in cert["connection"]
    assert "Does not guarantee locality" in cert["no_go_comparison"]
