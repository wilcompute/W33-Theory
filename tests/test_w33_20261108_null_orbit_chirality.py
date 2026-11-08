"""Exact rank-one null-orbit chirality and Hermitian covariance tests."""
from __future__ import annotations
import importlib.util
from pathlib import Path
import numpy as np
import pytest

P=Path(__file__).resolve().parents[1]/"analysis/w33_20261108_null_orbit_chirality.py"
spec=importlib.util.spec_from_file_location("null_orbit_chirality",P)
M=importlib.util.module_from_spec(spec);spec.loader.exec_module(M)

@pytest.fixture(scope="module")
def result():return M.produce()

@pytest.mark.parametrize("p", [3,5,7,11,13])
def test_two_equal_size_rank_one_orbits(p):
    plus,minus,d=M.two_null_classes(p)
    assert plus.shape==(p,p,p)
    assert d["two_square_class_orbit_sizes"]==[(p*p-1)//2]*2
    assert np.count_nonzero(plus&minus)==0
    assert d["generator_checks"]==3

def test_p3_chirality_4plus4_and_real_uniqueness(result):
    d=result["cases"][0]
    assert d["prime"]==3 and d["two_square_class_orbit_sizes"]==[4,4]
    assert d["inversion_swaps_square_class_orbits"]
    assert d["real_symmetric_covariant_null_weights"]==1
    assert not d["all_time_no_flat_mixing_under_these_symmetries"]

@pytest.mark.parametrize("p", [7,11])
def test_p3mod4_real_covariant_null_walk_no_go_for_higher_primes(p,result):
    d=next(x for x in result["cases"] if x["prime"]==p)
    assert d["inversion_swaps_square_class_orbits"]
    assert d["real_symmetric_covariant_null_weights"]==1
    assert d["all_time_no_flat_mixing_under_these_symmetries"]
    assert 2/p**2<p**(-1.5)

@pytest.mark.parametrize("p", [5,13])
def test_p1mod4_retains_two_real_orbital_weights(p,result):
    d=next(x for x in result["cases"] if x["prime"]==p)
    assert not d["inversion_swaps_square_class_orbits"]
    assert d["real_symmetric_covariant_null_weights"]==2
    assert not d["all_time_no_flat_mixing_under_these_symmetries"]

def test_chiral_complex_hopping_is_hermitian_but_not_real_symmetric():
    p=7
    plus,minus,_=M.two_null_classes(p)
    a=(1+.4j)*plus+(1-.4j)*minus
    inv=np.roll(a[::-1,::-1,::-1],(1,1,1),axis=(0,1,2))
    assert np.max(abs(inv-np.conj(a)))<1e-13
    assert np.max(abs(inv-a))>.1

def test_p5_independent_real_null_weights_still_symmetric():
    p=5
    plus,minus,_=M.two_null_classes(p)
    a=3.*plus+2.*minus
    inv=np.roll(a[::-1,::-1,::-1],(1,1,1),axis=(0,1,2))
    assert np.array_equal(inv,a)

def test_bounded_grid_is_not_a_no_go(result):
    c=result["p5_bounded_grid_control"]
    assert c["candidate_pairs_tested"]==1089
    assert c["grid_side"]==33
    assert c["best_max_probability_deviation"]>0
    assert "Cannot exclude" in c["warning"]

def test_scope_excludes_other_hamiltonians(result):
    assert len(result["cases"])==5
    assert "complex Hermitian" in result["limitation"]
    assert "not an emergent locality" in result["physical_scope"]
