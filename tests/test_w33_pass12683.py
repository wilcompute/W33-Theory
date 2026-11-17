"""Pass 12683: orbit-A degree 8 converged (not tight), global degree 8 at q = 4 (not tight), E6 -> SU(5) -> SM replication and its
two-qutrit frame shadow."""
import json, os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
C8 = 2.4985086466880784


def load(name):
    return json.load(open(os.path.join(ROOT, "data", name)))


def test_orbitA_degree8_converged_and_feasible():
    rows = load("w33_f8_orbitA_sos8_clarabel_sweep.json")
    best = max(r["bound"] for r in rows if r["status"] == "Solved")
    assert all(r["min_cone_eigenvalue"] > 0 and r["max_equality_residual"] < 1e-7 for r in rows)
    assert 2.44 < best < 2.447 and C8 - best > 0.05      # degree 8 is not tight on orbit A


def test_T_clarabel_control():
    d = load("w33_f8_symmetric_sos8_T_clarabel.json")
    assert abs(d["bound"] - C8) < 1e-6 and d["identity_error"] < 1e-10


def test_global_q4_degree8_not_tight():
    d = load("w33_f8_symmetric_sos8_Q4_clarabel.json")
    assert d["group_order"] == 360 and d["c8"] == 1.0 and "Solved" in d["status"]
    assert 0.95 < d["bound"] < 0.975 and d["identity_error"] < 1e-5


def test_e6_replication():
    d = load("w33_pass12683_e6_su5_sm_replication.json")
    assert (d["derivations"], d["stabilizer_two_singlet_pairs"], d["stabilizer_with_adjoint_Y"]) == (78, 24, 12)
    assert abs(d["trace_X3_normalised"]) < 1e-12 and d["Y_annihilates_vevs"]
    assert d["Y_spectrum"] == {"-6.0": 1, "-3.0": 2, "-2.0": 6, "-1.0": 6, "0.0": 2, "2.0": 3, "3.0": 4, "4.0": 3}


def test_su5_vacuum_is_a_skew_frame_pair():
    d = load("w33_pass12683_su5_vacuum_skew_frames.json")
    c = d["partA_classes"]
    assert c["meets both (transversal)"]["content"] == {"H_u (1,2)_1/2": 2, "D (3,1)_-1/3": 3}
    assert c["meets F1 only"]["content"] == c["meets F2 only"]["content"] == {"L (1,2)_-1/2": 2, "d^c (3b,1)_1/3": 3}
    assert c["skew to both"]["size"] == 10 and c["skew to both"]["content"]["Q (3,2)_1/6"] == 6
    assert d["psp43_order"] == d["frame_action_order"] == 25920
    assert d["ordered_skew_pair_stabiliser"] == 60 and d["action_on_transversals"] == 60 and d["action_on_transversals_even"]
    assert d["transversal_factorisation_bijection"] and d["doublet_choice_orbit"] == 10 and d["doublet_choice_stabiliser"] == 6


def test_doublet_triplet_split_is_a_measurement_context():
    d = load("w33_pass12683_doublet_triplet_contexts.json")
    assert d["special_contexts"] == 10 and d["distinct_weak_pairs"] == 10
    assert d["scan"]["isotropic line 6 (2, 3)"] == 10 and d["scan"]["isotropic line 2 (1, 2, 2)"] == 30
    assert d["weak_factorisations_product_basis"] and d["colour_factorisations_maximally_entangled"]
