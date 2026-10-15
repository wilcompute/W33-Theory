"""TOE89 exact and synthetic regression tests for all five independent tracks."""
from functools import lru_cache
import json
from pathlib import Path
import pytest
from analysis import w33_20261015_toe89_cyclic_tate_chain as T
from analysis import w33_20261015_toe89_parity_symmetry as P
from analysis import w33_20261015_toe89_complementary_css as C
from analysis import w33_20261015_toe89_heralded_mub as M
from analysis import w33_20261015_toe89_albert_product_obstruction as A

ROOT=Path(__file__).resolve().parents[1]
@lru_cache(None)
def fresh(t):
    return {"tate":T.certificate,"parity":P.certificate,
            "css":C.certificate,"mub":M.certificate,"albert":A.certificate}[t]()

def test_noncentral_C3_signed_face_Tate_decomposition_all_classes():
    x=fresh("tate")
    assert x["C2_C3_fixed_triangle_faces"]==3
    assert x["C2_C3_free_3D_modules"]==32
    assert x["C2_C3_Tate_dimension_in_each_degree"]==3
    assert x["C1_C3_free_module_count"]==45
    assert x["C0_C3_free_module_count"]==9
    classes=x["all_13_two_orbit_classes"]
    assert len(classes)==13 and sum(c["class_size"] for c in classes)==468
    assert all(all(y["fixed_oriented_triangle_faces"]==3 and
                   y["free_C3_orbits"]==32 for y in c["all_four_C3_face_decompositions"])
               for c in classes)

def test_tate_cell_isotropy_does_not_force_joint_selector():
    x=fresh("tate")
    assert x["three_orbit_extension"]["fixed_oriented_triangle_faces"]==3
    assert x["three_orbit_extension"]["free_C3_orbits"]==41
    assert x["counterexample_flat_H1_direction_rank"]==[2,2,2,2]
    assert x["counterexample_nonflat_H2_direction_rank"]==[13,12,13,13]

def test_parity_membrane_transforms_into_2D_C3_simple_module():
    x=fresh("parity")
    a=x["representatives"]
    assert len(a)==4
    assert [s["torsion_module_dimension"] for s in a]==[0,0,2,2]
    assert [s["kernel_order"] for s in a]==[27,27,9,9]
    assert a[2]["kernel_projective_Pauli_direction_index"]==0
    assert a[3]["kernel_projective_Pauli_direction_index"]==3
    assert all(s["quotient_image_is_C3"] for s in a[2:])

def test_parity_kernel_has_center_and_exact_nine_addresses():
    a=fresh("parity")["representatives"]
    for s in a[2:]:
        addresses={tuple(g) for g in s["kernel_H27_addresses"]}
        assert len(addresses)==9
        assert {(0,0,z) for z in range(3)}<=addresses

def test_css_dual_checks_commute_and_schedule():
    x=fresh("css")
    assert x["data_qutrits"]==135
    assert x["Z_face_checks"]==99 and x["X_vertex_checks"]==27
    assert x["Z_SUM_gates_per_round"]==351
    assert x["X_SUM_gates_per_round"]==270
    assert x["Z_conflict_free_layers"]==6 and x["X_conflict_free_layers"]==10
    assert x["flag_qudits_per_round_when_enabled"]==126
    assert x["flag_prepost_SUM_gates_per_round"]==252

def test_flagged_circuit_observes_hooks_without_magical_correction():
    x=fresh("css")
    a,b=x["runs"]
    assert a["shots"]==b["shots"]==144
    assert x["round_count"]==3
    assert a["flag_ancillas_enabled"] is False
    assert b["flag_ancillas_enabled"] is True
    assert a["means"]["any_flag_detected"]==0
    assert b["means"]["any_flag_detected"]>0
    assert a["means"]["raw_zero_physical_residual"]==b["means"]["raw_zero_physical_residual"]
    assert a["means"]["temporal_filtered_zero_physical_residual"]==b["means"]["temporal_filtered_zero_physical_residual"]

def test_temporal_filter_does_not_claim_fault_tolerance():
    x=fresh("css")
    # Important negative result: naive per-check filter performs worse
    # than raw final-syndrome one-site correction under this noise.
    v=x["runs"][0]["means"]
    assert v["raw_zero_physical_residual"]==pytest.approx(48/144)
    assert v["temporal_filtered_zero_physical_residual"]==pytest.approx(33/144)
    assert v["raw_zero_physical_residual"]>v["temporal_filtered_zero_physical_residual"]

def test_heralded_EB_2design_setting_blind_upper_bound():
    x=fresh("mub")
    assert x["explicit_stochastic_instrument_samples"]==96
    assert x["max_sampled_EB_conditional_survival"]<=.5+1e-12
    assert x["max_2design_identity_residual"]<1e-12
    assert x["heralding_independent_of_setting_not_required"]

def test_classical_basis_label_side_channel_remains_a_loophole():
    x=fresh("mub")
    s=x["setting_side_channel_and_postselection_spoof"]
    assert s["total_accepted_fraction"]==pytest.approx(.325)
    assert s["accepted_state_mean_fidelity"]==pytest.approx(11/13)
    assert x["reject_at_least"]==665
    assert x["null_one_sided_tail"]<=.001
    assert x["alternative_power_under_iid"]>.99

def test_albert_projected_multiplication_fails_polynomial_Jordan():
    x=fresh("albert")
    assert x["26D_binary_aug_H27_isomorphism_rank"]==26
    assert x["product_H27_equivariant_over_GF4"]
    assert x["non_Jordan_under_scalar_extension_GF4"]
    assert x["defect_support"]==[0,1,2,3,5]
    assert any(x["explicit_nonzero_Jordan_defect"])
    assert x["binary_only_test_false_negative_demonstrated"]==80

@pytest.mark.parametrize("track,file",[
    ("tate","w33_20261015_toe89_cyclic_tate_chain.json"),
    ("parity","w33_20261015_toe89_parity_symmetry.json"),
    ("css","w33_20261015_toe89_complementary_css.json"),
    ("albert","w33_20261015_toe89_albert_product_obstruction.json"),
])
def test_exact_seeded_frozen_certificate(track,file):
    frozen=json.loads((ROOT/"data"/file).read_text(encoding="utf8"))
    assert fresh(track)==frozen
