"""2026-11-08 five deep W33 gates: independent structural, numerical and provenance checks."""
from __future__ import annotations
import importlib.util,subprocess
from pathlib import Path
import pytest

ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location("w33_deep_five",ROOT/"analysis/w33_20261108_deep_fivefronts.py")
M=importlib.util.module_from_spec(spec)
spec.loader.exec_module(M)

@pytest.fixture(scope="module")
def certificate():
    return M.produce(ROOT)

def test_native_e6_full_record_tensor_not_toy(certificate):
    a=certificate["native_e6"]
    assert a["signed_tensor_records"]==1620
    assert a["e6_irrep_generators"] in {0,78} and a["block_count"]==729
    assert a["block_rank_census"]=={"0":459,"2":270}
    assert a["max_block_antisymmetry_residual"]<1e-12

def test_no_direct_rank3_generation_projection(certificate):
    a=certificate["native_e6"]
    if a["generator_basis_status"]=="DESKTOP_78_BASIS_CHECKED":
        assert a["fiber_projectors_tested"]==27
        assert a["all_fiber_projectors_break_full_E6"] is True
        assert a["min_commutator_norm_squared"]>0
    else:
        assert a["generator_basis_status"]=="NOT_CHECKED_78_BASIS_ABSENT"
        assert a["fiber_projectors_tested"]==0
        assert a["all_fiber_projectors_break_full_E6"] is None
    assert "Mixed E6-coordinate projectors" in a["limits"]

@pytest.mark.parametrize("p", [3,5,7,11])
def test_weighted_nonlocal_chirps_are_exactly_flat(certificate,p):
    row=next(x for x in certificate["weighted"]["cases"] if x["prime"]==p)
    assert row["vertices"]==p**3
    assert row["flatness_max_abs_probability_residual"]<1e-12
    assert abs(row["sum_probabilities"]-1)<1e-12

def test_weighted_escape_is_not_a_null_local_continuum(certificate):
    rows=certificate["weighted"]["cases"]
    assert [r["nonzero_offdiagonal_weighted_differences"] for r in rows]==[26,100,342,1330]
    assert [r["off_null_support_differences"] for r in rows]==[18,84,294,1210]
    assert all(r["off_null_support_differences"]>0 for r in rows)
    assert "not a controlled smooth Lorentz" in rows[1]["physical_boundary"]

def test_gauge_exact_harmonic_leverage(certificate):
    d=certificate["gauge"]
    assert (d["vertices"],d["edges"],d["faces"],d["harmonic_rank"])==(27,108,36,46)
    assert d["projector_idempotence_and_closure_residual"]<1e-10
    assert d["exact_single_edge_leverage"]=="23/54"
    assert abs(d["single_oriented_edge_harmonic_leverage_squared"]-23/54)<1e-11
    assert d["per_edge_uniformity_deviation"]<1e-11

def test_charge_gradients_are_orthogonal_to_harmonic_sector(certificate):
    d=certificate["gauge"]
    assert d["gradient_charge_harmonic_norm"]<1e-11
    assert d["single_triangle_boundary_harmonic_norm"]<1e-11
    assert d["conserved_nonlocal_cycle_divergence"]<1e-11

def test_historical_tool_is_explicitly_scoped(certificate):
    d=certificate["provenance"]
    assert len(d["candidates"])==5
    assert all(x["status"] in {"file_history_pickaxe","history_not_complete_or_shallow_checkout",
                                "timeout_bounded_no_inferred_first_owner","path_absent","git_log_failed"} for x in d["candidates"])
    assert "not first discovery" in d["scope"]

def test_git_pickaxe_really_finds_introduction(tmp_path):
    path=tmp_path/"claims.txt"
    subprocess.run(["git","init","-q",str(tmp_path)],check=True)
    subprocess.run(["git","-C",str(tmp_path),"config","user.email","test@example.invalid"],check=True)
    subprocess.run(["git","-C",str(tmp_path),"config","user.name","TOE Probe"],check=True)
    path.write_text("fixture\n")
    subprocess.run(["git","-C",str(tmp_path),"add","claims.txt"],check=True)
    subprocess.run(["git","-C",str(tmp_path),"commit","-qm","initial"],check=True)
    path.write_text("fixture\n137+880/24445\n")
    subprocess.run(["git","-C",str(tmp_path),"commit","-qam","add candidate"],check=True)
    r=M.git_pickaxe("claims.txt","137+880/24445",root=tmp_path)
    assert r["status"]=="file_history_pickaxe"
    assert r["changes_count"]==1
    assert r["first_change_on_file_history"]["message"]=="add candidate"

def test_optical_exact_27_port_permutations(certificate):
    a=certificate["optical"]
    assert a["matrix_max_residual"]<1e-12
    assert a["sum_permutation_networks"]==4
    assert a["tritters"]==27
    assert a["max_two_mode_beamsplitters_excluding_permutation_routing"]==81
    assert a["generic_unitary_two_mode_bound"]==351
    for x in a["permutation_stages"]:
        assert sorted(y["to"] for y in x["map"])==list(range(27))
    for x in a["tritter_layers"]:
        assert len(set(x["ports"]))==3

def test_optical_loss_crosstalk_calibration_is_synthetic(certificate):
    d=certificate["optical"]["calibration"]
    assert len(d["detector_efficiency"])==27
    assert min(d["detector_efficiency"])>0
    assert d["postselected_bias_before_correction"]>1e-5
    assert d["bias_after_exact_synthetic_calibration"]<1e-12
    assert sum(d["first_input_synthetic_click_counts"])==d["per_input_accepted_counts"]==5000
    assert "not a lithographic layout" in certificate["optical"]["scope"]
