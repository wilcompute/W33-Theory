"""TOE71 independent regression of all five physics frontiers.

These tests deliberately require exact witness checks while refusing to
upgrade numerical MILP / sparse Ritz / HF convergence to formal theorems.
"""
import sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"analysis"))
from w33_20261014_toe71_global_disorder_milp import certificate as disorder
from w33_20261014_toe71_two_loop_gap_bound import certificate as gap
from w33_20261014_toe71_quantum_pairing import certificate as loops
from w33_20261014_toe71_4d_holonomy_and_index import certificate as geometry
from w33_20261014_toe71_sitewise_hartree_fock import certificate as mass

def test_global_160_link_mixed_integer_fixed_direction():
    c=disorder()
    assert c["status"]=="PASS_TOE71_GLOBAL_INTEGER_PROGRAM_SOLVER"
    assert all(z["solver_status"]=="optimal" for z in c["tested_global_corner_optima"])
    assert len(c["tested_global_corner_optima"])==5
    assert c["tested_global_corner_optima"][0]["integer_variables"]==1591
    assert len(c["tested_global_corner_optima"][0]["optimal_high_native_edges"])==17
    assert int(c["tested_global_corner_optima"][0]["exact_winner_numerator"])<0
    assert int(c["tested_global_corner_optima"][2]["exact_winner_numerator"])>0
    assert "not formal exact proof" in c["qualification"]

def test_two_loop_unbounded_rotor_schur_minmax_inputs():
    c=gap()
    assert c["native_patch"]==[11,12,5]
    assert abs(c["exact_diagonal_Q_min"]-18.215)<1e-12
    assert abs(c["Q_spectral_lower_bound"]-7.94)<1e-12
    assert abs(c["interface_norm_squared_upper"]-3.51125)<1e-12
    assert c["conditional_full_spectral_gap_lower"]>.62
    assert "CONDITIONAL" in c["important_limitation"]

def test_full_PGSp_equivariant_quantum_pairings_and_two_flip_tunneling():
    c=loops()
    assert c["full_model_Hilbert_dimension"]=="3^80"
    assert c["single_vertex_new_loop_counts"]=={"19":160}
    assert c["two_vertex_new_loop_counts"]=={"18":12628,"19":6,"20":6}
    assert len(c["two_vertex_new_twenty_loop_configurations"])==6
    assert abs(next(x["ground_energy_over_J"] for x in c["restricted_quantum_sectors"]
        if x["states"]==81 and x["t_over_J"]==.2)+20.35959179422655)<1e-9
    assert "NOT symmetry invariant" in c["qualification"]

def test_closed_spin_W33_handlebody_preserves_flat_deck_but_index_needs_curvature():
    c=geometry()
    assert c["handlebody_retraction_H1_rank"]==81
    assert c["selected_flat_three_deck_edges"]==[59,93,139]
    assert c["inclusion_boundary_to_handlebody_H1_surjective"]
    assert c["M4_betti"]==[1,164,326,164,1]
    assert c["untwisted_spin_Dirac_index"]==0
    assert c["flat_holonomy_alone_index"]==0
    assert c["line_bundle_twist_examples"][3]["unit_charge_spin_Dirac_index"]==1
    assert c["line_bundle_twist_examples"][3]["five_charge_total_index"]==220

def test_site_resolved_hartree_and_exchange_self_consistency():
    c=mass()
    assert c["status"]=="PASS_TOE71_UNRESTRICTED_LOCAL_SELF_CONSISTENT_HF"
    assert len(c["runs"])==8
    assert all(r["max_fixed_point_residual"]<1e-11 for r in c["runs"])
    assert all(r["energy_gain_vs_symmetric_trial"]>0 for r in c["runs"])
    assert all(r["quasiparticle_gap"]>0 for r in c["runs"])
    assert abs(c["at_V_0p2_HF_quasiparticle_gap"]-.2404442056)<1e-7
    assert "not a proof" in c["scope"].lower()
