"""Independent focused regressions for Forty Points five-front continuation."""
import importlib.util
from pathlib import Path
import math
from fractions import Fraction
import pytest
import numpy as np

SOURCE=Path(__file__).resolve().parents[1]/"analysis"/"w33_20261108_forty_points_fivefronts.py"
if not SOURCE.is_file():
    SOURCE=Path(__file__).resolve().parent/"w33_20261108_forty_points_fivefronts.py"
spec=importlib.util.spec_from_file_location("forty_points_20261108",SOURCE)
front=importlib.util.module_from_spec(spec)
spec.loader.exec_module(front)

@pytest.fixture(scope="module")
def bundle():
    return front.execute(SOURCE.parents[1])

def test_original_graph_and_exact_fourier_residue_counts(bundle):
    q=bundle["clock_extra"]
    assert q["vertices"]==27 and q["degree"]==8 and q["null_vectors"]==8
    assert q["exact_character_residue_counts"]=={
        "origin":[9,12,6],"null":[9,12,6],
        "q=1":[6,9,12],"q=2":[12,6,9]}
    assert q["laplacian_spectrum"]=={"0":1,"6":12,"9":8,"12":6}

def test_quadratic_butson_uniform_mixing_all_729_pairs(bundle):
    q=bundle["clock_extra"]
    assert q["numeric_flatness_residual"]<1e-13
    assert q["numeric_kernel_residual"]<1e-13
    assert q["numeric_order_three_residual"]<1e-13
    assert q["exact_uniform_probability"]=="1/27 for ALL 729 input/output pairs"

def test_change_of_chart_clifford_factorization_and_native_entanglement(bundle):
    q=bundle["clock_extra"]
    assert q["diagonal_chart_Kronecker_residual"]<1e-13
    assert q["native_a_entanglement_entropy_trits"]==1
    assert q["native_b_entanglement_entropy_trits"]==0
    # Factorization is specific to diagonalized t,x,y chart, not native a,b,c.

def test_gauge_invariant_wilson_faces_and_unfixed_coupling(bundle):
    g=bundle["front1_gauge"]
    assert (g["vertices"],g["edges"],g["oriented_faces"])==(27,108,36)
    assert g["boundary_squared_zero"] and g["cohomology_H1_dimension"]==46
    assert g["gauge_invariance_residual"]<1e-12
    assert g["maxwell_F2_action_at_supplied_g"]["1.0"] / g["maxwell_F2_action_at_supplied_g"]["2.0"]==pytest.approx(4)

def test_conditional_nelson_barr_cp_not_strong_cp(bundle):
    f=bundle["front2_flavor"]
    assert f["determinant_exact"]=="985/27"
    assert f["tree_arg_det"]==0
    assert f["effective_CP_weak_basis_invariant_float"]==pytest.approx(-0.5165489629687502,abs=1e-13)
    assert f["CP_invariant_when_row_real"]==0

def test_transmutation_retains_unfixed_continuous_parameters(bundle):
    s=bundle["front3_scale"]["example_ratios"]
    assert len(s)==9
    for b0 in (7,9,11):
        rows=[r for r in s if r["b0_input"]==b0]
        assert [r["g_squared_input"] for r in rows]==[.25,.5,1.]
        assert rows[0]["Lambda_over_mu"]<rows[1]["Lambda_over_mu"]<rows[2]["Lambda_over_mu"]

def test_safe_canonicalizer_exact_rational_aliases_and_malicious_rejection(bundle):
    assert front.safe_rational("137+40/1111")==Fraction(152247,1111)
    assert front.safe_rational("137 + 1/28 + 4/14045") == front.safe_rational("(137*28*14045+14045+112)/(28*14045)")
    assert front.safe_rational("3/13+1/2200") != front.safe_rational("197/852")
    with pytest.raises(ValueError):
        front.safe_rational("__import__('os').system('echo unsafe')")
    with pytest.raises(ValueError):
        front.safe_rational("3.14")

def test_source_catalog_conservative_status(bundle):
    p=bundle["front4_provenance"]
    assert p["status"].startswith("CANONICAL")
    if p["repository_catalog_present"]:
        assert all(r["source_catalog_exact_text_seen"] for r in p["canonicalized_candidates"] if r["name"] in {"alpha_A","alpha_B","alpha_C","weak_W33"})
    assert p["canonicalized_candidates"][0]["residual_CODATA22_sigmas"]<-4.3

def test_gauge_free_plaquette_values_and_preregistration(bundle):
    q=bundle["clock_extra"]
    plaquettes=q["phase_plaquettes"]
    assert [p["label"] for p in plaquettes]==["omega","omega2","unity"]
    assert [p["expected_root_power"] for p in plaquettes]==[1,2,0]
    r=bundle["front5_pre_registration"]
    assert r["status"]=="PREREGISTERED_SYNTHETIC_TARGET_NO_LAB_COUNTS"
    assert len(r["phase_gauge_invariants"])==3
    assert "NOT the existence of a new force" in r["identifiability"]

def test_catalog_scan_merges_exact_rational_aliases_without_executing_text():
    fake="alpha = 137+1/2\nalternate = 137+2/4\nanother = 3/13+1/2200\nbad = __import__('os').system('not executed')\n"
    scan=front.scan_catalog_rational_arithmetic(fake)
    assert scan["literal_occurrences_parsed"]==3
    assert scan["canonical_numerical_groups"]==2
    assert scan["multi_expression_groups"]>=1
    assert any(g["canonical_fraction"]=="275/2" for g in scan["largest_20_alias_groups"])
