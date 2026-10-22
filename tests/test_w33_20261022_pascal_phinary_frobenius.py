"""Independent regression tests: exact Pascal/phinary and scoped arithmetic frontiers."""
import math
import pytest
from analysis.w33_20261022_pascal_phinary_frobenius import (
    pascal_family,pascal_base,phi_representations,cyclotomic_phi_audit,
    prime_power_extension,ccm_weil_trace_audit,fp_pow_phi,all_results
)

def test_pascal_generating_function_growth_and_legacy_pi_correction():
    r=pascal_base()
    assert r["status"]=="PASS_EXACT_RECURSION"
    assert [pascal_family(m,10) for m in (1,2,3,4)]==[1024,89,28,14]
    assert "not 4*pi²/3-3!" in r["old_pascal_note_correction"]

def test_exact_base_phi_integer_expansions():
    r=phi_representations()
    assert r["unique_Bergman_forms_checked"]==41
    assert r["examples"]["2"].endswith("0100000000")
    assert "." in r["examples"]["23"]

def test_golden_gaussian_cyclotomic_and_lucas_classes():
    r=cyclotomic_phi_audit()
    assert 3 in r["sample_family_primes_below100"]
    assert 7 in r["sample_family_primes_below100"]
    assert 23 in r["sample_family_primes_below100"]
    assert fp_pow_phi(7)==(1,6)
    assert r["Lucas_pascal_checks"]==4*3240

def test_curve_prime_power_extension_parity_obstruction():
    r=prime_power_extension()
    assert r["cases"]==18
    one=next(x for x in r["cases_table"] if x["p"]==3 and x["r"]==1)
    two=next(x for x in r["cases_table"] if x["p"]==3 and x["r"]==2)
    three=next(x for x in r["cases_table"] if x["p"]==3 and x["r"]==3)
    assert one["C_Frobenius"]=="X^4+9"
    assert two["C_Frobenius"]=="(X^2+9)^2"
    assert three["C_Frobenius"]=="X^4+729"

def test_previous_arithmetic_operator_completed_Weil_and_trace():
    r=ccm_weil_trace_audit()
    assert r["status"]=="PASS_SCOPED_NUMERIC"
    assert abs(r["relative_second_trace_eta_doubled_ratio"]-4)<1e-9
    assert r["compact_smooth_Weil_smallest_eigenvalue"]>0

def test_complete_scope_firewall():
    r=all_results()
    assert r["classical_RH_proved"] is False


def test_pascal_jordan_modular_W3p_nonsemisimple():
    from analysis.w33_20261022_pascal_jordan_w3p import certificate
    r=certificate()
    assert r["status"]=="PASS_EXACT_MODULAR"
    assert [v["Jordan_size2_minus1"] for v in r["cases"]]==[4,10,35,84]
    assert [v["Jordan_size1_minus1"] for v in r["cases"]]==[6,19,85,231]
    assert all(v["B_squared_zero"] for v in r["cases"])
    assert r["classical_RH_proved"] is False
