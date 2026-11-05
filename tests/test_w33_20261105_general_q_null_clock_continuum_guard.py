"""General-q null-clock polynomial and continuum firewall regressions."""
import importlib.util
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
S=importlib.util.spec_from_file_location(
    "null_general",ROOT/"analysis"/"w33_20261105_general_q_null_clock_continuum_guard.py")
M=importlib.util.module_from_spec(S)
S.loader.exec_module(M)

def test_q3_preserves_original_clock():
    r=M.verify(3)
    assert r["adjacency_spectrum"]=={"-4":6,"-1":8,"2":12,"8":1}
    assert r["canonical_clock_order"]==3
    assert r["clock_fixed_dimension"]==9

def test_q5_exact_matrix_and_general_multiplicities():
    r=M.verify(5)
    assert r["adjacency_spectrum"]=={"-6":40,"-1":24,"4":60,"24":1}
    assert r["exact_integer_polynomial_verified"]

def test_q11_large_field_spectral_falsifier():
    r=M.verify(11)
    assert r["vertices"]==1331
    assert r["degree"]==120
    assert r["clock_fixed_dimension"]==121

def test_continuum_guard_strictly_shrinks():
    assert [1/(q-1) for q in M.PRIMES]==[0.5,0.25,1/6,0.1,1/12]
    for q in M.PRIMES:
        assert M.predicted(q)[-1]==q*q-1
