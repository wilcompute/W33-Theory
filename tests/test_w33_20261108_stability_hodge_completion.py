"""W33 full-affine stability and minimal H1 polarization-completion regressions."""
from __future__ import annotations
import importlib.util,math
from pathlib import Path
import pytest

PATH=Path(__file__).resolve().parents[1]/"analysis/w33_20261108_stability_hodge_completion.py"
S=importlib.util.spec_from_file_location("w33_stability_bundle",PATH)
M=importlib.util.module_from_spec(S);S.loader.exec_module(M)

@pytest.fixture(scope="module")
def cert():return M.produce()

@pytest.mark.parametrize("q", [3,5,7,11,13,17])
def test_group_twirling_bound_is_exact_five_orbit_count(cert,q):
    c=next(x for x in cert["robust_affine"]["cases"] if x["prime"]==q)
    assert c["five_orbit_coefficients"]==[1,(q-1)//2,(q-1)//2,
             -q if q%4==1 else 0,-q if q%4==3 else 0]
    assert math.isclose(c["contraction_commutant_amplitude_upper"],2/q**2,rel_tol=0,abs_tol=1e-15)
    assert c["forbidden_if_fully_affine_covariant"]==(q>=5)

@pytest.mark.parametrize("q",[5,7,11,13,17])
def test_flatness_enforces_nonzero_symmetry_defect(cert,q):
    c=next(x for x in cert["robust_affine"]["cases"] if x["prime"]==q)
    delta=q**-1.5-2/q**2
    assert delta>0
    assert c["guaranteed_operator_norm_twirl_defect_if_flat"]==pytest.approx(delta,abs=1e-15)
    assert c["guaranteed_max_group_commutator_if_flat"]==pytest.approx(delta,abs=1e-15)
    assert c["max_symmetric_output_probability"]<c["exact_flat_output_probability"]

def test_q3_does_not_require_symmetry_break(cert):
    x=cert["robust_affine"]["cases"][0]
    assert x["guaranteed_operator_norm_twirl_defect_if_flat"]==0

def test_Hamiltonian_Duhamel_version_keeps_time_and_norm(cert):
    x=cert["robust_affine"]
    assert "delta_q/|t|" in x["hamiltonian_version"]
    assert "max(0,delta_q-epsilon)" in x["approximate_flatness"]

def test_actual_q5_gaussian_chirp_breaks_full_affine_symmetry(cert):
    x=cert["p5_isometry_chirp"]
    assert x["group_orbit_dimensions"]==[1,12,12,60,40]
    assert x["original_flat_amplitude"]==pytest.approx(1/math.sqrt(125),abs=1e-12)
    assert x["full_operator_norm_twirl_difference"]==pytest.approx(math.sin(2*math.pi/5),abs=1e-12)
    assert x["selected_entry_twirl_difference"]>x["general_proven_minimum"]
    assert x["twirled_selected_amplitude"]<2/25

def test_group_commutant_amplitude_ceiling_is_sharp_but_not_flat(cert):
    w=cert["p5_isometry_chirp"]
    assert w["selected_output_bound_is_sharp_among_affine_invariant_unitaries"]
    assert w["affine_invariant_involution_selected_amplitude"]==pytest.approx(2/25,abs=1e-12)
    assert w["saturating_involution_is_flat"] is False

def test_H1_momentum_dimension_census_exact(cert):
    b=cert["h1_bundle"]
    assert b["vertices"]==27 and b["null_graph_degree"]==8 and b["h1_dimension"]==46
    assert b["h1_momentum_rank_multiplicities"]=={"0":1,"1":12,"2":8,"3":6}
    assert b["adjacency_eigenvalue_multiplicities"]=={"-4":6,"-1":8,"2":12,"8":1}

def test_auxiliary_rank_two_repair_minimality(cert):
    b=cert["h1_bundle"]
    assert not b["rank_two_every_nonzero_momentum_possible_with_H1_alone"]
    assert b["momentum_rank_deficit_for_two_polarizations"]==12
    assert b["minimal_selective_auxiliary_dimension"]==12
    assert b["minimum_completed_H1_dimension"]==58
    assert b["rank_two_nonzero_momentum_subbundle_dimension"]==52
    assert b["remaining_modes_after_minimal_completion"]==6
    assert b["onsite_uniform_scalar_auxiliary_dimension"]==27

def test_deficiency_projector_exact_cubic_and_symmetric(cert):
    b=cert["h1_bundle"]
    assert b["deficient_orbit_spectral_projector"].startswith("P_2=(8I-A)")
    assert b["deficient_orbit_projector_convolution_kernel_9x_values"]=={"-1":12,"0":6,"1":8,"4":1}
    assert b["spatial_kernel_nonzero_displacement_types"]==20
    assert b["graph_distance_upper_bound_for_polynomial"]==3

def test_no_physical_photon_or_alpha_claim(cert):
    assert "not the space of physical Maxwell" in cert["h1_bundle"]["physical_boundary"]
    assert "no empirically verified TOE" in cert["scientific_boundary"]
    assert "not a locality solution" in cert["p5_isometry_chirp"]["interpretation"]
