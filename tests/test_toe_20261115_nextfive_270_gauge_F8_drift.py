"""2026-11-15 independent next-five continued suite. Pure stdlib except pytest.

Replays exact octet intermediary, genus-six affine gauge, D9 magnetic
moment-map identity and photonic drift certificates. F8 broad census
certificate checked separately from heavy stochastic search.
"""
import importlib.util,json,math
from pathlib import Path
import pytest
ROOT=Path(__file__).resolve().parents[1]

def module(name):
  p=ROOT/"analysis"/name
  spec=importlib.util.spec_from_file_location(name.removesuffix(".py"),p)
  mod=importlib.util.module_from_spec(spec)
  spec.loader.exec_module(mod)
  return mod

@pytest.fixture(scope="module")
def comp():
  return module("toe_20261115_E6_270mode_two_stage_compiler.py").run()

@pytest.fixture(scope="module")
def affine():
  return module("toe_20261115_genus6_affine24_exact.py").run()

@pytest.fixture(scope="module")
def d9():
  return module("toe_20261115_D9_flux_compensator_SO3xSO3.py").run()

@pytest.fixture(scope="module")
def photonic():
  return module("toe_20261115_photonic_two_epoch_drift.py").run()

@pytest.fixture(scope="module")
def f8():
  return json.loads((ROOT/"data"/"toe_20261115_F8_rank5_logical_coset_census.json").read_text())

def test_two_stage_E6_full_operator_exact(comp):
  assert comp["first_stage_binary_U_shape"]==[270,22680]
  assert comp["UUT_lambda_max_exact"]==264
  assert comp["B_B_transpose_exact"]=="10 I27"
  assert comp["no_extra_postselection_penalty_due_to_two_stages"]
  assert comp["M_M_transpose_eigenvalues"]=={
    "uniform_1":2640,"schlafli_20":1344,"schlafli_dark_6":1560}

def test_E6_sparse_incidence_collisions(comp):
  assert comp["first_stage_column_decomposition_hist"]=={"1":6480,"2":16200}
  assert comp["UUT_offdiagonal_nonzero_entry_hist"]=={"2":8100}
  assert comp["UUT_offdiagonal_pairs_with_positive_overlap"]==8100
  assert comp["UUT_constant_row_sum"]==264
  assert comp["UUT_diagonal"]==144

def test_E6_full_success_entangled_resource(comp):
  assert comp["perfect_entangled_fourphoton_input_yields_success_probability"]==1
  assert comp["perfect_source_not_a_fourfold_tensor_power"]
  assert 6480+4*16200==27*2640
  assert "uniform |+27>" in comp["perfect_entangled_fourphoton_input_output"]

def test_E6_did_not_claim_a_compiled_stage1(comp):
  assert "no passive linear optics circuit" in comp["physical_compilation_stage1"]
  assert "uncompiled" in comp["scope"]

def test_genus_affine_gauge_is_24_parameters(affine):
  assert affine["original_continuous_parameters"]==36
  assert affine["affine_gauge_dimensions"]==12
  assert affine["canonical_residual_plane_parameters"]==24
  assert len(affine["canonical_remaining_eight_plane_normalized_coefficients"])==8
  assert affine["all_44_vertices_reconstructed_exactly"]

def test_genus_exact_crossings_still_eight(affine):
  assert affine["reference_tetrahedron_det_nonzero"]
  assert affine["exact_total_proper_face_crossings"]==8
  assert sum(affine["face_crossings_each_in_3d_affine_chart"])==8
  assert "does not establish realizability" in affine["scope"]

def test_D9_six_flux_gauge_compensators(d9):
  assert d9["six_massless_vector_gauge_generators"]==6
  assert d9["rational_points_checked"]==6
  assert all(x["all_three_flux_compensators_exact"] for x in d9["sample_first_sphere_checks"])
  assert "so(3)+so(3)" in d9["Lie_algebra"]

def test_D9_geometric_overlaps_not_full_KK(d9):
  assert d9["cross_sphere_moment_and_Killing_overlaps"]==0
  assert all(float(__import__("fractions").Fraction(x))>0
             for x in d9["Killing_overlap_S2xS2_coefficients_in_pi_squared"])
  assert "not a derivation of a full" in d9["scope"]

def test_F8_new_148_sample_census(f8):
  assert f8["rank5_codes_found"]==148
  assert f8["logical_count_types"]=={"3-3-3":148}
  assert f8["trials_requested"]==200
  assert "not an exhaustive classification" in f8["scope"]

def test_photonic_temporal_no_go(photonic):
  assert photonic["model_free_unbounded_drift_impossibility"]
  assert photonic["indistinguishable_endpoint_channels_with_middle_rail_error"]==1
  assert photonic["drift_bump_max_abs_second_derivative"]==pytest.approx(2*math.pi**2)

def test_photonic_two_epoch_conditional_confidence(photonic):
  assert photonic["two_epoch_16rail_calibrations"]==32
  assert photonic["total_accepted_two_epoch_calibrations"]==2103112
  assert photonic["linear_interpolation_max_curvature_error_midpoint"]==pytest.approx(.025)
  assert photonic["synthetic_fidelity_99pct_lower_with_illustrative_drift_bound"]>.9
  assert sum(photonic["confidence_failure_budget"].values())==pytest.approx(.01)

def test_photon_assumption_explicit(photonic):
  assert "independently justified" in photonic["curvature_assumption"]
  assert "not inferred" in photonic["hardware_scope"]

def test_all_five_certificates_present(comp,affine,d9,f8,photonic):
  names=[
    "toe_20261115_E6_270mode_two_stage_quantum_compiler.json",
    "toe_20261115_genus6_affine24_exact_certificate.json",
    "toe_20261115_D9_SO3xSO3_flux_moment_maps.json",
    "toe_20261115_F8_rank5_logical_coset_census.json",
    "toe_20261115_photonic_two_epoch_drift_certificates.json"]
  for name in names:
    data=json.loads((ROOT/"data"/name).read_text())
    assert data["status"]
