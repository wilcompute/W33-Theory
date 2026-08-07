from __future__ import annotations
import importlib.util, pathlib, math, pytest

ROOT=pathlib.Path(__file__).resolve().parents[1]
MOD=ROOT/"analysis/w33_pass4169_4176_discrete_c2_hawking_backreaction_gray_levi_casimir_axion.py"
spec=importlib.util.spec_from_file_location("p4169_4176",MOD)
m=importlib.util.module_from_spec(spec); spec.loader.exec_module(m)

@pytest.fixture(scope="session",autouse=True)
def full_verify():
    assert m.verify()

def test_semantic_hash():
    assert m.semantic_hash(m.CERT)==m.CERT["semantic_sha256"]

def test_all_passes_true():
    assert m.CERT["all_checks_hold"] and all(m.CERT["checks"].values())

def test_second_chern_compiler():
    p=m.CERT["pass4169_discrete_c2_compiler"]
    assert p["exact_second_chern"]==1 and p["first_mesh_below_5pct_error_among_audited"][0]==29

def test_hawking_continuous_disorder():
    p=m.CERT["pass4170_continuous_hawking_disorder"]
    assert p["gaussian_logneg_min"]>0 and p["qp_logneg_min"]>0
    assert p["baseline_thermal_mobility_edges"]["0.01"]>0.57

def test_backreaction_saddle_node():
    p=m.CERT["pass4171_scale_geometry_backreaction"]
    assert p["g1_derivatives"][0]<0<p["g1_derivatives"][1]
    assert 1.12<p["critical_g"]<1.13

def test_gray_locality_reduction():
    p=m.CERT["pass4172_locality_reduced_gray_clock"]
    assert p["original_locality"]==7 and p["exact_reduced_locality"]==4 and p["total_and_ancillas"]==72

def test_levi_erratum_and_cover_obstruction():
    p=m.CERT["pass4173_levi_cover_critical_sequence"]
    assert p["degree"]==4 and p["cycle_parity_augmented_rank"]==p["cycle_parity_rank"]+1
    assert abs(p["beta_c_J"]-.5*math.log(2))<1e-15

def test_three_bonkers_boundaries():
    a=m.CERT["pass4174_hawking_erasure_channel"]
    b=m.CERT["pass4175_spectral_casimir"]
    c=m.CERT["pass4176_axion_dimensional_reduction"]
    assert a["patterns_Q_positive"]+a["patterns_Q_zero"]==512
    assert all(x<0 for x in b["interaction_energy"].values())
    assert c["theta_winding"]=="2pi" and c["chern_simons_level_shift"]==1

def test_spectral_casimir_exact_green_data():
    p=m.CERT["pass4175_spectral_casimir"]
    assert p["green_diagonal"]=="211/855"
    assert p["green_by_distance"]=={"1":"10/171","2":"13/855","3":"1/171","4":"4/855"}
