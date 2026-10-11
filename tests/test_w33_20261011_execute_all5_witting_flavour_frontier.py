import hashlib, importlib.util, json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
SCRIPT=ROOT/"analysis"/"w33_20261011_execute_all5_witting_flavour_frontier.py"
CERT=ROOT/"data"/"w33_20261011_execute_all5_witting_flavour_frontier.json"
SPEC=importlib.util.spec_from_file_location("all5_frontier",SCRIPT)
M=importlib.util.module_from_spec(SPEC);SPEC.loader.exec_module(M)

def certificate():
    return json.loads(CERT.read_text())

def test_frozen_certificate_passes_all_fronts():
    c=certificate()
    assert c["all_checks_pass"]
    assert all(c["checks"].values())

def test_h27_intertwiner_and_cubic_obstruction_replay():
    q=M.task1_intertwiner()
    assert q["X_generator_residual"]<1e-12
    assert q["Z_generator_residual"]<1e-12
    assert q["yukawa_X_covariance_residual"]<1e-12
    assert q["yukawa_Z_covariance_residual"]<1e-12
    assert q["full_projective_sets_identical"]
    assert q["Witting_projective_order"]==q["family_projective_order"]==q["projective_matrix_intersection"]==216
    assert q["Witting_minus_family"]==q["family_minus_Witting"]==0
    assert q["H27_invariant_trilinear_dimension"]==3
    assert q["G25_invariant_trilinear_dimension"]==0

def test_bifurcation_local_logic_replay():
    q=M.task2_bifurcation()
    assert q["CW_hessian_mean"]>7
    assert q["CW_hessian_spread"]<1e-4
    assert q["competing_12_18_witness"]["phase_stable"]
    assert q["competing_12_18_witness"]["projectively_unstable"]
    assert q["zero_mode_splitting"]["remain_zero"]==4
    assert q["zero_mode_splitting"]["one_third"]==18
    assert q["zero_mode_splitting"]["one"]==2
    assert abs(q["zero_mode_splitting"]["sum_slope_squares"]-4)<1e-5

def test_heavy_frozen_results_have_expected_boundaries():
    c=certificate()
    s=c["3_gauge_invariant_source"]
    assert s["source_rank"]==3
    assert s["massless_nonmodulus_dimension"]==27
    assert s["cartan_three_leg_max"]<1e-12
    a=c["4_schmidt_adjoint"]
    assert a["combined_CKM_distance"]<.3 and a["combined_PMNS_distance"]<.35
    assert max(a["down_mass_singular_drift"],a["lepton_mass_singular_drift"])<1e-12
    l=c["5_physical_one_loop"]
    for k in ("witting","generic"):
        assert abs(l[k]["ratio_min"]-1/6)<1e-10
        assert abs(l[k]["ratio_max"]-1/6)<1e-10
        assert l[k]["operator_identity_relative_residual"]<1e-12

def test_certificate_source_bindings():
    c=certificate()
    for rel,digest in c["sources"].items():
        assert hashlib.sha256((ROOT/rel).read_bytes()).hexdigest()==digest
