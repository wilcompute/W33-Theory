"""Focused regressions for the five constants fronts.

No network, lab data or massive full-repository scan required for these tests.
"""
import importlib.util
from pathlib import Path

PATH = Path(__file__).resolve().parents[1]/"analysis"/"w33_20261107_constants_five_fronts.py"
spec = importlib.util.spec_from_file_location("constants_five_fronts_20261107",PATH)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

def test_qed_grid_monotonic_and_codata_reassessment():
    obj = mod.electromagnetic()
    items={x["name"]:x for x in obj["formulas"]}
    assert -4.5 < items["BT53_legacy_pdg2018_target"]["residual_CODATA22_sigma"] < -4.3
    assert items["operator_resolvent"]["residual_CODATA22_sigma"] > 200
    d=obj["electron_loop_inverse_alpha_shifts"]
    assert d[0] == 0 and d[1] < 0 and d[2] < d[1] and d[3] < d[2]
    assert obj["max_common_running_residual_error"] < 5e-14

def test_common_spurion_is_explicit_but_not_physical_solution():
    obj = mod.flavor()
    assert obj["max_unitarity_error"] < 1e-14
    assert .22 < obj["Vus_common_spurion"] < .23
    assert .05 < obj["sin2_theta12_PMNS_common_spurion"] < .06
    assert abs(obj["sin2_theta12_PMNS_common_spurion"]-.307) > .24
    assert abs(obj["Jarlskog_nonzero"]) > 1e-4

def test_scale_and_maxwell_no_go():
    obj=mod.scale()
    assert all(r["max_Gibbs_error"] < 1e-14 for r in obj["rescalings"])
    assert all(r["max_phase_error"] < 1e-14 for r in obj["rescalings"])
    coeffs=obj["maxwell_F2_action_coefficients"]
    assert coeffs["1.0"]==0.25 and coeffs["2.0"]==0.0625

def test_rational_counterfamily_and_null_sensitivity():
    obj=mod.multiplicity()
    assert obj["bounded_rational_search"][-1]["absolute_residual"]<obj["W33_absolute_residual"]
    assert obj["bounded_rational_search"][-1]["best_fraction"]=="197/852"
    vals=[x["at_least_one_match_probability"] for x in obj["uniform_null_sensitivity"]]
    assert all(0<=x<=1 for x in vals)
    assert all(a<b for a,b in zip(vals,vals[1:]))

def test_syntactic_provenance_reports_and_preserves_disagreements(tmp_path):
    (tmp_path/"first.tex").write_text(r"\alpha^{-1} = 137 + 40/1111"+"\n")
    (tmp_path/"second.py").write_text("fine-structure alpha^-1 = 137 + 1/28\n")
    (tmp_path/"weak.md").write_text("sin2thetaW = 3/13\n")
    report=mod.provenance(tmp_path)
    assert report["files_scanned"]==3
    assert report["families"]["alpha_inverse"]["distinct_line_shapes"]==2
    assert report["families"]["weak_angle"]["total_matching_lines"]>=1
    assert all(x["path"] in {"first.tex","second.py"} for x in
               report["families"]["alpha_inverse"]["example_provenance"])

def test_determinism_without_full_checkout():
    x=mod.evaluate(scan=False)
    y=mod.evaluate(scan=False)
    assert x==y
    assert x["provenance"]["status"]=="not_run_requires_full_checkout"
    assert x["scope"].startswith("Reanalysis")

def test_unbounded_archive_lines_and_explicit_size_cap(tmp_path):
    """Large one-line JSON is searched by overlapping windows, not silently skipped."""
    (tmp_path/"giant.json").write_text("x"*51000 + r" \alpha^{-1} = 137 + 40/1111"+"\n")
    all_files=mod.provenance(tmp_path)
    assert all_files["oversized_skipped"]==0
    assert all_files["files_scanned"]==1
    assert all_files["families"]["alpha_inverse"]["total_matching_lines"] >= 1
    capped=mod.provenance(tmp_path,max_bytes=1000)
    assert capped["oversized_skipped"]==1
    assert capped["files_scanned"]==0
