"""Five TOE research fronts and independent algebra/topology controls.

Run in isolation with --noconftest. All producers execute from scratch;
a stale JSON certificate cannot make a test pass.
"""
from __future__ import annotations
from pathlib import Path
import importlib.util,math,sys
import pytest
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"analysis"))
sys.path.insert(0,str(ROOT))
def calculate(name):
    file=ROOT/"analysis"/name
    spec=importlib.util.spec_from_file_location(file.stem,file)
    mod=importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod.main()
@pytest.fixture(scope="module")
def r():
    return {
      "gauge":calculate("toe_20261105_s3_algebra_square_followthrough.py"),
      "h27":calculate("toe_20261105_h27_gauge_generator_comparison.py"),
      "lorentz":calculate("toe_20261105_lorentzian_freudenthal_causal.py"),
      "mub":calculate("toe_20261105_mub_qutrit_memory_witness.py"),
      "index":calculate("toe_20261105_overlap_4d_su2_cartan.py")
    }

def test_s3_original_not_full_algebra(r):
    a=r["gauge"]["operator_algebra"]
    assert not a["original_symmetric_generators"]["scalar_commutant_numerically_supported"]
    assert a["exchange_broken_generators"]["graph_component_sizes"]==[18,4,4,1]
    assert a["exchange_broken_generators"]["generic_simple_spectral_gap"]>.001

def test_s3_gauge_projector_spatial_square(r):
    s=r["gauge"]["mobile_square"]
    assert s["invariant_dimension"]==36
    assert s["gauge_fixed_dimension"]==288
    assert s["raw_unfixed_dimension"]==6**5*8
    assert s["gauge_trace_census"]==[-36,-36,0,0,0,288]

def test_s3_gauge_covariant_square_hopping_spectra(r):
    s=r["gauge"]["mobile_square"]
    assert s["electric_transport_noncommutation"]
    assert s["electric_magnetic_noncommutation"]
    assert all(x["gauss_error"]<1e-11 for x in s["scans"])
    assert s["scans"][1]["gap"]>.1

def test_H27_regular_not_identical_to_three_qutrit_full_algebra(r):
    H=r["h27"]["H27"]
    assert H["H27_order"]==27
    assert H["H27_left_regular_associative_algebra_dimension"]==27
    assert H["full_Mat27_dimension"]==H["three_qutrit_Weyl_operator_basis_dimension"]==729
    assert sorted(H["H27_center_eigenspace_dimensions"].values())==[9,9,9]

def test_extra_gauge_invariant_generator_family_numerically_irreducible(r):
    P=r["h27"]["S3_gauge"]
    last=next(x for x in P["records"] if x["name"]=="full_10_operator_family")
    assert last["components"]==[27]
    assert last["generic_simple_spectral_gap"]>.01
    assert last["commutant_scalar_if_simple_and_connected"]

def test_minimum_extra_generators_for_current_search(r):
    p=r["h27"]["S3_gauge"]
    assert p["smallest_irreducibility_addition_size"]==2
    assert any(x["added_generators"]==["Ccross","Nielsen_shear"]
               for x in p["minimal_irreducible_additions"])
    assert len(p["minimal_ensemble_robustness"])==3
    assert all(x["commutant_scalar_if_simple_and_connected"]
               for x in p["minimal_ensemble_robustness"])

def test_H27_probe_cannot_be_misread_on_degenerate_spectrum(r):
    a=next(x for x in r["h27"]["S3_gauge"]["records"] if x["name"]=="original_EMC")
    assert not a["connected_component_decomposition_interpretable"]

def test_lorentzian_discrete_4d_refinements(r):
    rows=r["lorentz"]["rows"]
    assert len(rows)==6
    assert all(row["euler_characteristic"]==1 for row in rows)
    assert all(row["metric_signatures"]==[[1,3]] for row in rows)
    assert [(x["n"],x["four_simplices"]) for x in rows[::2]]==[(1,24),(2,384),(3,1944)]

def test_lorentzian_mesh_artifact_not_physical_arrow(r):
    rows=r["lorentz"]["rows"]
    assert all(x["timelike_edges_with_spatial_transport"]==0 for x in rows if x["metric_timestep"]<1)
    assert all(x["negative_spatial_future_steps"]==0 for x in rows)
    assert all(x["positive_spatial_future_steps"]>0 for x in rows if x["metric_timestep"]>1)

def test_s4_lorentzian_topology_obstruction(r):
    s=r["lorentz"]
    assert s["curved_regge_S4_euler_characteristic"]==2
    assert s["curved_regge_S4_closed_f_vector"]==[6,15,20,15,6]

def test_lorentzian_massless_scalar_fem_convergence(r):
    s=r["lorentz"]
    assert abs(s["massless_scalar_FEM_continuum_action"]-math.pi**2/16)<1e-12
    fem=s["massless_scalar_FEM_refinement"]
    assert len(fem)==4
    assert all(a["absolute_error"]>b["absolute_error"] for a,b in zip(fem[:-1],fem[1:]))
    assert fem[-1]["absolute_error"]<.021

def test_mub_Bell_matching_formula_and_separable_bound(r):
    m=r["mub"]
    assert m["qutrit_MUB_bases"]==4
    assert m["rank_one_measurement_projectors"]==12
    assert m["matching_operator_exact_identity"]=="C=(I9+3 Bell3)/4"
    assert m["separable_match_probability_upper_bound"]==.5
    assert m["alternative_match_probability"]==pytest.approx((1+2*.35)/3)

def test_mub_gate_compilation_is_four_rail(r):
    m=r["mub"]
    assert m["four_rail_compiler_blocks_per_side_max"]<=6
    assert m["four_rail_nontrivial_two_mode_mixers_per_side_max"]<=3
    assert m["local_measurement_setting_pairs"]==4

def test_mub_exact_detection_sample_sizes(r):
    m=r["mub"]
    loss=m["exact_binomial_loss_adjusted_MUB_design"]
    ideal=m["exact_binomial_perfect_detector_MUB_design"]
    globalideal=m["ideal_global_entangling_Bell_projection_comparator"]
    assert loss["shots"]==1612 and ideal["shots"]==891 and globalideal["shots"]==472
    for x in (loss,ideal,globalideal):
        assert x["exact_false_alarm"]<=.01 and x["model_power"]>=.95
    assert len(m["static_mesh_calibrations"])==4

def test_four_dimensional_Wilson_overlap_flux_index(r):
    q=r["index"]
    assert len(q["scans"])==14
    assert q["L3_recovers_unit_product_flux_index"]
    assert q["coarse_L2_nonzero_flux_index_collapses_to_zero"]
    lookup={(x["L"],x["Q01"],x["Q23"],x["Wilson_negative_mass_parameter"]):x["overlap_index"] for x in q["scans"]}
    assert lookup[(3,1,1,1)]==1
    assert lookup[(3,1,-1,1)]==-1
    assert lookup[(2,1,1,1)]==0
    assert lookup[(3,1,1,3)]==-3
    assert lookup[(3,1,1,5)]==3
    assert lookup[(3,1,1,7)]==-1

def test_four_dimensional_overlap_exact_GW(r):
    q=r["index"]
    selected=[x for x in q["scans"] if "Ginsparg_Wilson_max_residual" in x]
    assert len(selected)==2
    assert all(x["Ginsparg_Wilson_max_residual"]<4e-12 for x in selected)

def test_reducible_SU2_not_nonabelian_instanton(r):
    q=r["index"]
    assert q["su2_reducible_fundamental_index"]==2
    assert not q["su2_is_truly_noncommuting_gauge_background"]
    assert "No noncommuting SU2 instanton" in q["boundary"]
