"""Independent regression assertions for eight W33 quantum/physics falsifiers."""
import math
import numpy as np
import pytest
from analysis import w33_20261031_eight_quantum_fronts_round2 as M

@pytest.fixture(scope="module")
def x():return M.build()["fronts"]

def test_mod_five_matrix_and_jordan(x):
    q=x["01_characteristic_five_module"]
    A=np.array(q["action7_GF5"],dtype=np.int64)
    assert A.shape==(7,7)
    assert np.array_equal(np.linalg.matrix_power(A,5)%5,np.eye(7,dtype=int))
    assert q["powers_of_unipotent_minus_identity_ranks"]==[7,4,2,0,0,0]

def test_seven_torsion_centralizer(x):
    q=x["01_characteristic_five_module"]
    assert q["centralizer_dimension"]==17 and q["smith_torsion_order"]==78125

def test_optics_81_unitary_and_losses(x):
    p=x["02_optical_81mode_imperfections"]
    assert p["mode_count"]==81 and p["independent_triangles"]==27
    for row in p["models"]:
        a,b=np.array(row["p_plus"]),np.array(row["p_minus"])
        assert np.all(a>=0) and np.all(b>=0)
        assert abs(a.sum()-1)<1e-12 and abs(b.sum()-1)<1e-12

def test_optics_risk_degrades_with_drift(x):
    rows=x["02_optical_81mode_imperfections"]["models"]
    assert all(rows[i]["error_1"]<rows[i+1]["error_1"]for i in range(3))
    assert rows[0]["errors"]["20"]<1e-6

def test_clock_K8_exact_one_unsatisfied(x):
    q=x["03_clock_frustration"]
    assert q["minimum_missed_bonds_among_seven_clique_extensions"]==1
    assert q["satisfied_noncommuting_bonds"]==27
    assert q["commuting_bonds"]==1
    assert abs(q["sample_bond_energy"]+16)<1e-10

def test_qca_index_no_go(x):
    q=x["04_chiral_local_index"]
    assert q["finite_depth_even_odd_swap"]=={"right":1,"left":1,"index":1}
    assert q["shift_by_one"]=={"right":1,"left":0,"index":3}

def test_symplectic_integrator_second_order(x):
    q=x["05_metric_hamiltonian"]
    assert 3.9<q["drift_ratio_coarse_to_mid"]<4.1
    assert 3.9<q["drift_ratio_mid_to_fine"]<4.1
    assert all(row["reversal_error"]<1e-12 for row in q["measurements"])

def test_two_exact_braid_parity_sectors(x):
    q=x["06_outside_braid_commutant"]
    assert q["commutant_dimension"]==2
    assert q["irreducible_sector_dimensions"]==[5,4]
    P=np.array(q["physical_parity_matrix"],dtype=int)
    assert np.array_equal(P@P,np.eye(9,dtype=int))
    assert np.trace(P)==1

def test_native_clifford_zero_mana(x):
    q=x["07_outside_wigner_magic"]["native_entangling_braid"]
    assert abs(q["mana"])<1e-12 and q["min"]>-1e-12

def test_nonclifford_magic_control(x):
    q=x["07_outside_wigner_magic"]["externally_supplied_nonclifford_phase_gate"]
    assert q["mana"]>.3 and q["min"]<-.03
    assert abs(q["sum_absolute"]-13/9)<1e-12

def test_graph_H1_has_no_integral_torsion(x):
    q=x["08_outside_homology_vs_torsion"]
    assert q["graph_h1_over_Z_free_rank"]==193
    assert q["graph_h1_integral_torsion"]==0

def test_square_filling_destroys_tested_H1(x):
    q=x["08_outside_homology_vs_torsion"]
    assert q["filled_4_cycles"]==1680
    assert q["boundary2_ranks"]=={"F2":193,"F3":193,"F5":193}
    assert set(q["filled_H1_dimensions"].values())=={0}

def test_outputs_match_frozen_artifact(x):
    import json
    d=json.loads(M.OUT.read_text())["fronts"]
    assert set(d)==set(x)
    for name in d:
        assert d[name]["status"]==x[name]["status"]

def test_interblock_crosstalk_81_detector_control(x):
    p=x["02_optical_81mode_imperfections"]["inter_triangle_81mode_crosstalk"]
    assert [row["neighbor_coupler_angle"] for row in p]==[0.0,0.025,0.1]
    assert p[0]["average_leakage_outside_injected_triangle"]<1e-12
    assert 0<p[1]["average_leakage_outside_injected_triangle"]<p[2]["average_leakage_outside_injected_triangle"]
    assert all(0<row["Bayes_one_shot_with_81_detectors_and_no_click"]<.5 for row in p)
