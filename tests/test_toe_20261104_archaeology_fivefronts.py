"""Cross-history W33 five-front falsification regression, with exact layer fences."""
import importlib.util
import json
import math
from pathlib import Path
import pytest

ROOT=Path(__file__).resolve().parents[1]
def importer(name,path):
    spec=importlib.util.spec_from_file_location(name,ROOT/path)
    mod=importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod

@pytest.fixture(scope="module")
def results():
    r=importer("archctrl","analysis/toe_20261104_archaeological_fivefront_controls.py")
    return r.main()

@pytest.fixture(scope="module")
def sparse():
    r=importer("archsparse","analysis/toe_20261104_c3_orbit_sparsification.py")
    return r.run()

def test_search_census_records_hundreds_of_prior_hits():
    j=json.loads((ROOT/"data"/"toe_20261104_corpus_archaeology.json").read_text())
    assert j["repo_files"]>=40000 and j["commit_count"]>=20000
    for front in ("dimension","symmetry","gravity","flavor","hardware"):
        x=j["fronts"][front]
        assert x["tracked_text_path_hits"]>=100
        assert len(x["all_matching_paths"])==x["tracked_text_path_hits"]
        assert x["commit_subject_matches_before_october_count"]>0
        assert x["search_limitations"].startswith("Path hits")

def test_ko_dimension_congruence_does_not_fix_four(results):
    d=results["dimension"]
    assert d["allowed_spacetime_dimensions_up_to_64"]==[4,12,20,28,36,44,52,60]
    assert d["historic_python_sets_KO_signs_by_literal_assignment"]
    assert d["n_distinct_solutions_up_to_64"]==8

def test_symmetry_sparse_c3_preserves_rank_and_decreases_condition(sparse):
    assert sparse["status"]=="PASS_EXACT_C3_ORBIT_FRAME_SPARSIFICATION"
    vals=sparse["comparison"]
    assert [v["orbit_count"] for v in vals]==[27,36,54,81,108,135,162,216,270,405,540]
    assert all(v["full_basis_protected_rank"]==81 for v in vals)
    assert all(v["cycle_count"]==3*v["orbit_count"] for v in vals)
    assert all(v["nonzero_positive_min"]>0 for v in vals)
    assert vals[-1]["condition_number"]<1+1e-10

def test_symmetry_specific_sparse_pareto(sparse):
    vals={r["orbit_count"]:r for r in sparse["comparison"]}
    assert 2.99<vals[108]["condition_number"]<3.10
    assert vals[108]["undirected_hoppings"]==5546
    assert vals[216]["condition_number"]<1.92
    assert vals[216]["undirected_hoppings"]==8225
    assert vals[540]["undirected_hoppings"]==12720
    assert vals[108]["max_flag_neighbors"]==75
    assert vals[81]["undirected_hoppings"]==4650

def test_c3_nested_orbit_supports(sparse):
    vals={r["orbit_count"]:r for r in sparse["comparison"]}
    previous=set()
    for m in (27,81,108,216,540):
        o=vals[m]["selected_orbit_indices"]
        assert len(o)==m and len(set(o))==m
        assert previous.issubset(set(o))
        previous=set(o)

def test_indefinite_candidate_has_nontrivial_zeros_but_bracket_obstruction(results):
    g=results["gravity"]
    assert g["gauss_dp_zero_exact"] and g["two_indefinite_constraints_zero_exact"]
    assert g["two_constraint_Poisson_bracket_exact"]=="-8"
    assert g["full_common_indefinite_constraint_surface_has_nonpure_gauge_cycle_point"]

def test_weak_cp_symmetric_toy_is_not_tree_strong_cp_solution(results):
    f=results["flavor"]
    assert f["previous_symmetric_4x4_toy_determinant"]=="12 - 4*I"
    assert math.isclose(f["previous_symmetric_toy_arg_det_radians"],-math.atan(1/3),abs_tol=1e-12)
    assert f["previous_symmetric_toy_weak_CP_cubed_trace"]=="1600"
    assert not f["previous_symmetric_toy_strong_CP_safe_if_bare_theta_zero"]
    assert f["historic_11951_triangular_determinant_exact"]=="14"
    assert f["historic_11951_nonzero_Jarlskog_like_triple"]=="119/64"

def test_one_aligned_vectorlike_row_cannot_induce_cp(results):
    f=results["flavor"]
    assert f["aligned_diagonal_real_bare_Y_and_single_B_triplet_imaginary_invariant_exact"]=="0"

def test_interrogation_time_changes_hardware_depth_choice(results):
    h=results["hardware"]
    assert h["best_sampled_steps"]==8 and h["best_sampled_pulses"]==24
    rows={r["steps"]:r for r in h["shot_and_latency_budgets"]}
    assert rows[1]["approximate_5sigma_shots_per_flux_setting"] is None
    assert rows[8]["idealized_total_interrogation_time_for_both_flux_settings"]<rows[16]["idealized_total_interrogation_time_for_both_flux_settings"]
    assert rows[8]["approximate_5sigma_shots_per_flux_setting"]>rows[16]["approximate_5sigma_shots_per_flux_setting"]
    assert rows[64]["idealized_total_interrogation_time_for_both_flux_settings"]>rows[8]["idealized_total_interrogation_time_for_both_flux_settings"]
