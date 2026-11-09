"""Regression checks for 2026-11-08 five-gate extension and H27 audit."""
from __future__ import annotations
import importlib.util
import math
from pathlib import Path
import pytest

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location(
    "physics_extension", ROOT / "analysis/w33_20261108_five_gate_extensions.py")
M = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(M)

@pytest.fixture(scope="module")
def cert():
    return M.produce(ROOT)

def test_weighted_faces_do_not_remove_harmonics(cert):
    g=cert["geometry"]
    assert g["native_complex"] == [27,108,36]
    assert g["gauge_gradients"] == 26
    assert g["weighted_magnetic_rank"] == 36
    assert g["harmonic_modes_after_arbitrary_face_weight"] == 46

def test_four_dimension_rank_lift_loses_at_least_42_harmonics(cert):
    g=cert["geometry"]
    assert g["conditional_H27_rank_cap"] == 4
    assert g["illustrative_lift_rank"] == 40
    assert g["harmonic_zero_modes_after_rank4_lift"] == 42
    assert "NOT been shown" in g["warning"]

def test_time_dependent_duhamel_bound(cert):
    s=cert["quantum_walk"]["q_values"]
    assert s["3"]["necessary_integrated_operator_norm"] == 0
    assert math.isclose(s["5"]["necessary_integrated_operator_norm"],
                        (math.sqrt(5)-2)/25,rel_tol=1e-13)
    assert all(s[str(q)]["necessary_integrated_operator_norm"]>0
               for q in (5,7,11,13))

def test_e6_native_rank_three_determinant_exact_product(cert):
    e=cert["e6"]
    assert e["native_alternating_rank"]==78 and e["completed_rank"]==81
    assert len(e["checks"])==4
    assert all(c["identity_log_error"]<1e-6 for c in e["checks"])
    assert all(c["identity_phase_complex_error"]<1e-6 for c in e["checks"])
    assert abs(e["native_coefficient_phase_radians"])>0.01

def test_e6_mass_phase_is_not_claimed_as_strong_cp_solution(cert):
    assert "NOT theta_bar" in cert["e6"]["physical_limit"]
    assert cert["e6"]["augmented_determinant_is_pfaffian_square"]

def test_optical_common_phase_is_invisible(cert):
    c=cert["photonic"]["correlated_phase_results"]
    assert abs(c["1.0"]["simulated_conditional_fidelity"]-1)<1e-12
    assert c["0.0"]["analytic_conditional_fidelity"] < c["0.9"]["analytic_conditional_fidelity"] < 1
    assert cert["photonic"]["synthetic"]

def test_correlation_simulation_matches_gaussian_expectation(cert):
    for v in cert["photonic"]["correlated_phase_results"].values():
        assert abs(v["analytic_conditional_fidelity"]-v["simulated_conditional_fidelity"])<.002
        assert v["equal_rail_survival_eta07_unconditional_success_weighted_fidelity"] < v["analytic_conditional_fidelity"]

def test_cosmology_shapley_and_interaction_recomputed(cert):
    for v in cert["cosmology"]["surveys"].values():
        a=v["all"]
        assert abs(a["shapley_power"]+a["shapley_geometry"]-a["delta_chi2_CPL_minus_fading"])<1e-9
        assert a["nonadditive_interaction"]!=0
        assert abs(a["nonadditive_subblock_difference"])>.1

def test_shear_not_treated_as_independent_block_sum_or_sigma(cert):
    x=cert["cosmology"]
    assert "must not" in x["inference_boundary"]
    assert x["surveys"]["des"]["high"]["delta_chi2_CPL_minus_fading"] > 0
    assert x["surveys"]["kids"]["all"]["delta_chi2_CPL_minus_fading"] > 0

def test_h27_integer_smith_lattice_replay(cert):
    a=cert["extra_h27"]["orbits"]
    assert len(a)==4
    assert [len(x["integer_charge_snf"]) for x in a]==[2,2,4,4]
    assert a[2]["integer_charge_snf"]==[1,1,1,1]

def test_h27_generalized_mass_eigenvalues_replay(cert):
    a=cert["extra_h27"]["orbits"]
    assert a[0]["generalized_mass_eigenvalues"]==[0,0,round(2/9,12),round(2/9,12)]
    assert a[2]["generalized_mass_eigenvalues"]==[round(2/27,12)]*2+[round(1/9,12)]*2

def test_six_distinct_scoped_fronts(cert):
    assert {"geometry","quantum_walk","e6","photonic","cosmology","extra_h27"} <= set(cert)
    assert "no unified physics" in cert["scientific_status"]
