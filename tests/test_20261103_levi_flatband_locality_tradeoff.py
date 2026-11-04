"""Regression tests for the general W(3,q) Levi flat-band locality firewall."""
from pathlib import Path
import importlib.util
import json
import math
import numpy as np
import pytest

ROOT=Path(__file__).resolve().parents[1]
SRC=ROOT/"analysis"/"2026_11_03_levi_flatband_locality_tradeoff.py"
spec=importlib.util.spec_from_file_location("levi_locality",SRC)
mod=importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

@pytest.fixture(scope="module")
def results():
    mod.main()
    return json.loads(mod.OUT.read_text(encoding="utf8"))

def test_full_producer_replays_and_passes(results):
    assert results["status"].startswith("PASS_")
    assert len(results["cases"])==4

@pytest.mark.parametrize("q,v,e,beta",[
    (2,15,45,16),(3,40,160,81),(4,85,425,256),(5,156,936,625)])
def test_finite_fields_exact_counts_and_hodge_dimension(results,q,v,e,beta):
    row=next(c for c in results["cases"] if c["q"]==q)
    assert row["points"]==row["lines"]==v
    assert row["levi_vertices"]==2*v
    assert row["flags"]==e
    assert row["cycle_rank"]==beta==e-2*v+1
    assert row["flat_band_adjacency_eigenvalue"]==-2
    assert row["distance_shells"]==[1,2*q,2*q*q,2*q**3,q**4]

def test_gf4_is_an_extension_field_not_integer_mod_four(results):
    q=4
    assert mod.field_add(2,3,q)==1
    assert mod.field_mul(2,2,q)==3 # omega^2 = omega+1
    assert mod.field_mul(2,3,q)==1
    assert mod.normalize((2,0,0,0),q)==(1,0,0,0)
    assert next(c for c in results["cases"] if c["q"]==4)["cycle_rank"]==256

def test_projector_never_has_zeros_and_local_defect_spreads(results):
    for c in results["cases"]:
        assert c["all_projected_defect_matrix_entries_nonzero"]
        assert all(a!=0 for a in c["integer_projector_coefficients"])
        assert math.isclose(sum(c["projected_defect_radial_probability"]),1,abs_tol=1e-14)
        p=c["cycle_rank"]/c["flags"]
        assert math.isclose(c["projection_onto_defect"],p,rel_tol=1e-15)
        assert math.isclose(c["defect_cut_leakage_amplitude"],math.sqrt(p*(1-p)),rel_tol=1e-14)

def test_qutrit_protected_radial_probability_is_exact(results):
    row=next(c for c in results["cases"] if c["q"]==3)
    assert row["integer_projector_coefficients"]==[81,-27,9,-3,1]
    assert row["distance_shells"]==[1,6,18,54,81]
    assert np.allclose(row["projected_defect_radial_probability"],
                       [81/160,54/160,18/160,6/160,1/160],atol=1e-15)
    assert math.isclose(row["leakage_to_band_split_ratio"],math.sqrt(79/81),rel_tol=1e-14)

def test_diagonal_perturbation_cannot_preserve_all_cycles():
    _,_,flags,neighbors,_,_=mod.geometry(3)
    d=mod.all_distances(neighbors)
    P=np.array([81,-27,9,-3,1])[d]/160.
    v=np.zeros(len(flags));v[0]=1
    comm=v[:,None]*P-P*v[None,:]
    assert np.max(abs(comm))>0.1
    # Pairwise nonzero P entries force v_e-v_f=0 for a diagonal
    # Hamiltonian commuting with P.
    assert np.min(abs(P))==1/160
    assert not np.allclose(comm,0)
    assert np.allclose((2*np.eye(len(flags)))@P-P@(2*np.eye(len(flags))),0)

def test_all_adjacency_polynomials_flat_on_cycle_space():
    _,_,flags,neighbors,_,_=mod.geometry(3)
    d=mod.all_distances(neighbors)
    K=np.array([81,-27,9,-3,1],dtype=np.int64)[d]
    A=np.zeros_like(K)
    for i,neigh in enumerate(neighbors):A[i,neigh]=1
    assert np.array_equal(A@K,-2*K)
    assert np.array_equal((A@A+3*A+5*np.eye(len(flags),dtype=np.int64))@K,
                          ((-2)**2+3*(-2)+5)*K)

def test_qutrit_two_flag_bond_leaks(results):
    v=results["q3_dynamical_controls"]
    assert np.allclose(v["adjacent_bond_projected_eigenvalues"],
                       [54/160,-108/160])
    assert all(x>0.46 for x in v["adjacent_bond_cut_leakage_amplitudes"])

def test_onsite_local_unitary_short_time_leakage(results):
    vals=results["q3_dynamical_controls"]["finite_time_tests"]
    assert len(vals)==3
    assert all(v["cut_leakage_probability"]>0 for v in vals)
    assert all(abs(v["relative_error"])<.002 for v in vals)
    assert abs(vals[0]["relative_error"])<abs(vals[-1]["relative_error"])
