"""New finite-field, resource, topology and geometry falsifier regression."""
import json,math
import pytest
import numpy as np
from analysis import w33_20261031_six_orthogonal_falsifiers as M

@pytest.fixture(scope="module")
def packet():
    return M.build()["results"]

def test_actual_a5_7d_invariant_quadratic_space(packet):
    f=packet["01_GF5_A5_quadratic_invariants"]["invariant_form_spaces"]
    assert f["symmetric"]["dimension"]==3
    assert f["alternating"]["dimension"]==0
    assert f["symmetric"]["basis_ranks"].count(7)>=1

def test_invariant_quadratic_witnesses_exact_mod5(packet):
    d=json.loads((M.ROOT/"data/w33_20261031_full_subgroup_GF5_representation.json").read_text())
    g=[np.array(d["GF5_generator_actions"][str(k)],dtype=int)for k in (2,3,5)]
    forms=packet["01_GF5_A5_quadratic_invariants"]["invariant_form_spaces"]["symmetric"]["basis_matrices"]
    assert all(np.array_equal((A.T@np.array(F)@A)%5,np.array(F)%5)for F in forms for A in g)

def test_ancilla_unitary_heralding_probability(packet):
    x=packet["02_ancilla_QND_strange_instrument"]
    assert abs(x["success_probability_for_stabilizer_input_1"]-.5)<1e-12
    assert abs(x["ideal_output_wigner"]["mana"]-math.log(5/3))<1e-12
    assert x["ideal_output_wigner"]["min"]<0

def test_strange_depolarization_magic_threshold(packet):
    scan=packet["02_ancilla_QND_strange_instrument"]["depolarization_scan"]
    assert scan[0]["min"]<0
    assert scan[-1]["mana"]<1e-12
    assert abs(scan[4]["min"])<1e-12

def test_local_clock_exact_40_by_40_transfer_spectrum(packet):
    x=packet["03_40state_local_clock_transfer"]
    for row in x["rows"]:
        assert row["lambda0"]>abs(row["lambda2_mult24"])
        assert row["lambda0"]>abs(row["lambda_minus4_mult15"])
        assert row["xi_sites"]>0
    assert abs(x["large_beta_limiting_correlation_length"]-1/math.log(9))<1e-13

def test_81dim_w33_harmonic_and_pauli_labels_not_equivariant(packet):
    d=packet["04_81mode_steinberg_vs_Pauli_obstruction"]
    assert d["nonzero_Pauli_F3_4_orbit"]==80
    assert d["Pauli_81_permutation_module_invariant_dimension"]==2
    assert d["Steinberg_81_invariant_dimension"]==0

def test_indefinite_lorentz_SO13_gauge_ward(packet):
    x=packet["05_SO13_noncompact_gauge_Ward"]
    assert x["gauge_action_invariance_abs_error"]<1e-10
    assert x["holonomy_trace_invariance_max_error"]<1e-10
    assert x["finite_difference_local_Ward_error"]<1e-8
    assert x["action_indefinite"] is True

def test_index_survives_unitary_dressing_not_nonunitary_noise(packet):
    d=packet["06_Floquet_edge_unitary_vs_noise"]
    assert d["GNVW_boundary_index"]==3
    assert d["edge_cycle_checks"]==[(4,7),(6,11),(8,15)]
    s=d["noisy_layers_control"]
    assert abs(s[1]["52_layer_survival_control"]-.999**52)<1e-14
    assert s[3]["52_layer_survival_control"]<.6

def test_frozen_json_reproducibility(packet):
    assert M.OUT.exists()
    stored=json.loads(M.OUT.read_text())
    assert set(stored["results"])==set(packet)
    for key in packet:
        assert stored["results"][key]["status"]==packet[key]["status"]


def test_random_coherent_SU3_floquet_dressing_exact_information_routing():
    from analysis import w33_20261031_floquet_coherent_dressing as D
    d=D.build()
    assert d["status"]=="PASS_FLOQUET_RANDOM_LOCAL_SU3_DRESSING_EXACT_ROUTE_AND_RECOVERY"
    assert len(d["rows"])==12
    for row in d["rows"]:
        assert row["bulk_permutation_identity"]
        assert row["maximum_recovered_infidelity"]<1e-12
        if row["periodic"]:assert row["boundary_shift_orbit_length"]==0
        else:assert row["boundary_shift_orbit_length"]==2*row["side"]-1
    assert any(row["mean_uncalibrated_infidelity"]>.2 for row in d["rows"] if row["epsilon_random_local_SU3"]==.5)
    assert json.loads(D.OUT.read_text())["status"]==d["status"]
