"""Independent regressions for S4 harmonic characters and Gaussian q-clock duality."""
from __future__ import annotations
import importlib.util
from pathlib import Path
import pytest

SRC=Path(__file__).resolve().parents[1]/"analysis/w33_20261108_s4_harmonic_qdual.py"
spec=importlib.util.spec_from_file_location("s4_qdual",SRC)
F=importlib.util.module_from_spec(spec);spec.loader.exec_module(F)

@pytest.fixture(scope="module")
def cert():return F.produce()

def test_s4_is_exact_24_projective_matrices():
    g=F.group24()
    assert len(g)==24
    assert sorted(F.V)==sorted(set(F.V))

def test_complex_counts_and_chain_exact():
    e,f,ei,B1,B2=F.complex27()
    assert (len(e),len(f),B1.shape,B2.shape)==(108,36,(27,108),(108,36))
    assert len(ei)==108

def test_s4_conjugacy_class_sizes_and_chains(cert):
    x=cert["S4_H1"]
    assert x["class_sizes"]==[1,6,3,8,6]
    assert x["chain_traces"]["(1, 1, 1, 1)"]=={"C0":27,"C1_signed":108,"C2_signed":36,"H1":46}
    assert x["chain_traces"]["(3, 1)"]=={"C0":3,"C1_signed":3,"C2_signed":3,"H1":-2}
    assert x["H1_character"]==[46,4,-2,-2,0]

def test_exact_irreducible_decomposition(cert):
    x=cert["S4_H1"]["irreducible_multiplicities"]
    assert x=={"trivial":2,"sign":0,"standard3":7,
               "signed_standard3":5,"two_dimensional":4}
    assert 2+4*2+7*3+5*3==46

def test_two_s4_modes_but_no_translation_fixed_harmonic_mode(cert):
    x=cert["S4_H1"]
    assert x["S4_invariant_dimension"]==2
    assert x["translation_invariant_dimension"]==0
    assert x["independent_projector_max_residual"]<1e-10
    assert abs(x["independent_projector_trace"]-2)<1e-10
    assert abs(x["translation_averaged_harmonic_trace"])<1e-10

def test_translated_seed_span_is_only_18_of_46(cert):
    x=cert["S4_H1"]
    assert x["S4_seed_translation_span_dimension_numeric"]==18
    assert x["unspanned_harmonic_dimensions"]==28

def test_seed_fourier_support_orthogonality_classes(cert):
    x=cert["S4_H1"]["S4_seed_fourier_weight_by_n0"]
    assert x["4"]["characters"]==1 and abs(x["4"]["weight_per_character"])<1e-10
    assert x["1"]["characters"]==8 and abs(x["1"]["weight_per_character"])<1e-10
    assert x["2"]["characters"]==12 and x["2"]["weight_per_character"]==pytest.approx(1/12,abs=1e-10)
    assert x["0"]["characters"]==6 and x["0"]["weight_per_character"]==pytest.approx(1/6,abs=1e-10)

@pytest.mark.parametrize("p", [3,5,7,11,13,17])
def test_prime_gauss_chirp_phase_and_probability(cert,p):
    d=next(row for row in cert["q_duality"]["cases"] if row["prime"]==p)
    assert d["vertices"]==p**3
    assert d["inverse_four_coefficient"]==pow(4,-1,p)
    assert d["flat_probability_max_residual"]<1e-12
    assert d["finite_gauss_phase_max_residual"]<1e-12

def test_fixed_coordinate_self_duality_only_three(cert):
    assert [x["prime"] for x in cert["q_duality"]["cases"] if x["same_coordinate_q_star_equals_q"]]==[3]
    assert cert["q_duality"]["cases"][1]["inverse_four_coefficient"]==4

def test_nonlocal_prime_support_certificates(cert):
    assert [(x["prime"],x["nonzero_weighted_displacements"])
            for x in cert["q_duality"]["cases"]]==[(3,26),(5,100),(7,342),(11,1330),(13,2028),(17,4624)]
    assert all(x["weighted_displacements_outside_null_cone"]>0 for x in cert["q_duality"]["cases"])

def test_evidence_scope_not_particle_claim(cert):
    assert "not a TOE" in cert["claim_scope"]
    assert "not identified" in cert["S4_H1"]["boundary"]
    assert "not provide a local Lorentzian" in cert["q_duality"]["physics_limitation"]
