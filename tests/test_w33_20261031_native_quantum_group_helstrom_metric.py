"""Regression on native quantum-group gates, field-nine lift, optics and dynamic metric."""
import json, math
import pytest
from analysis import w33_20261031_native_tlj_metaplectic_chain as T
from analysis import w33_20261031_q9_torsion_ambient_lift as Q
from analysis import w33_20261031_helstrom_optical_braid_readout as O
from analysis import w33_20261031_dynamic_native_metric_backreaction as G

@pytest.fixture(scope="module")
def packet():
    return {"tl":T.build(),"q9":Q.build(),"optics":O.build(),"gravity":G.build()}

def test_120_pauli_projectors_and_TL_native(packet):
    p=packet["tl"]
    assert p["projector_pairs"]=={"noncommuting_pairs":540,"commuting_pairs":240}
    assert len(p["concrete_Pauli_indices"])==5
    assert p["native_tick_count"]==120

def test_root_of_unity_five_strand_jw_truncation(packet):
    p=packet["tl"]
    assert [x["rank"] for x in p["JW_projectors"]]==[6,3,1,0]
    assert p["full_40_point_Pauli_conjugacy_verified"]
    assert "finite" not in p["root_of_unity"] or p["status"].startswith("PASS")

def test_regular_25920_symplectic_chain_torsor(packet):
    d=packet["tl"]["ordered_TL5_paths"]
    assert (d["length4"],d["length5"],d["length6"])==(25920,25920,0)
    assert d["projective_symplectic_orbit_size"]==25920 and d["regular_PSp43_torsor"]

def test_braid_prepares_maximally_entangled_qutrits(packet):
    d=packet["tl"]["maximally_entangling_native_braid"]
    assert all(abs(x-1/3)<1e-12 for x in d["Schmidt_probabilities"])
    assert abs(d["von_Neumann_entropy_nats"]-math.log(3))<1e-12

def test_w33_noncommuting_packing_limit(packet):
    d=packet["tl"]["spatial_graph_packing"]
    assert d["maximum_pairwise_noncommuting_Pauli_directions"]==7
    assert (d["number_maximal_independent_sets_7"],d["number_maximal_independent_sets_4"])==(2880,90)

def test_q9_ambient_pgsp_lift_full_geometry(packet):
    d=packet["q9"]
    assert d["status"]=="PASS_GF9_AMBIENT_SEMILINEAR_LIFT"
    m=d["point_map"]
    assert m["all_projective_points_permuted"]==820 and m["all_isotropic_lines_permuted"]==820
    assert m["full_ambient_PGSp_certificate"] and m["generator_order"]==5
    assert m["fifth_power_scalar_GF9"]!=0

def test_q9_lift_agrees_with_incidence_and_torsion(packet):
    m=packet["q9"]["point_map"]
    assert m["projective_points_certified"]==240 and m["all_selected_line_images_certified"]
    previous=json.loads((Q.ROOT/"data/w33_20261031_torsion_order5_probe.json").read_text())
    assert previous["nilpotent_image_ranks"]==[7,4,2,0,0,0]

def test_real_three_mode_helstrom_error(packet):
    d=packet["optics"]
    assert abs(d["one_photon_Helstrom_optimal_error"]-(1-2*math.sqrt(10)/7)/2)<1e-13
    assert d["one_photon_Helstrom_optimal_error"]<d["one_photon_fixed_port_error"]
    assert len(d["analyzer_two_mode_Givens_angles"])==3

def test_local_photon_repetition_vs_collective_measurement(packet):
    p=packet["optics"]["IID_local_vs_collective_test"]
    assert (p["0.001"]["local_interferometer_IID_shots"],p["0.001"]["collective_ideal_copies"])==(7,4)
    assert (p["1e-06"]["local_interferometer_IID_shots"],p["1e-06"]["collective_ideal_copies"])==(13,8)
    assert all(p[x]["local_error"]<float(x) for x in ("0.001","1e-06"))

def test_positive_native_metric_backreaction_and_conservation(packet):
    g=packet["gravity"];assert g["status"].startswith("PASS")
    assert all(max(abs(row["relative_energy_drift"]) for row in r["snapshots"])<.001
               for r in g["runs"])
    assert all(r["snapshots"][-1]["metric_field_norm"]>1e-5 for r in g["runs"] if r["alpha"]>.1)
    assert all(r["snapshots"][-1]["metric_field_norm"]==0 for r in g["runs"] if r["alpha"]==0)

def test_metric_force_finite_difference_controls(packet):
    checks=packet["gravity"]["force_gradient_verification"]
    assert max(checks.values())<1e-7

def test_reproducible_frozen_certificates(packet):
    loc={
        "tl":T.OUT,"q9":Q.OUT,"optics":O.OUT,"gravity":G.OUT}
    for key,path in loc.items():
        assert json.loads(path.read_text())["status"]==packet[key]["status"]
