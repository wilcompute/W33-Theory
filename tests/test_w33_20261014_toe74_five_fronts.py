"""TOE74 regression gates: exact structure, rotor, cover neighbors and matter."""
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"analysis"))
from w33_20261014_toe74_exact_gates import certificate as exact
from w33_20261014_toe74_unconditional_gauge_bound import certificate as gauge
from w33_20261014_toe74_quantum_neighbors import certificate as quantum
from w33_20261014_toe74_u1_manybody_finite_t import certificate as matter

def test_exact_hessian_unique_witness_block_rational_psd():
    c=exact()["disorder"]
    assert c["status"]=="PASS_TOE74_EXACT_WITNESS_HESSIAN_SYMMETRIC_BLOCK"
    assert c["exact_symmetric_positive_on_bracket"]
    assert c["signs_antisymmetric_at_bracket"]==[1,-1]
    assert c["epsilon_exact_bracket"]==["12230759/50000000","24461519/100000000"]
    assert "not all" in c["scope"].lower()

def test_graph_euler_dirac_is_not_4d_chiral_spin_dirac():
    c=exact()["dirac"]
    assert c["rank_coboundary_over_Z"]==79
    assert c["graph_D_zero_modes_even"]==1
    assert c["graph_D_zero_modes_odd"]==81
    assert c["graph_Euler_Dirac_superindex"]==-80
    assert c["W33_squared_4D_deRham_Euler_index"]==25600
    assert c["W33_squared_4D_untwisted_spin_Dirac_index"]==0

def test_unconditional_unbounded_two_loop_exact_rational_E0_bracket():
    c=gauge()
    assert c["status"]=="PASS_TOE74_UNCONDITIONAL_TWO_LOOP_ROTOR_GROUND_ENCLOSURE"
    assert c["P_dimension"]==22638
    assert c["Q_exact_gershgorin_spectral_lower"]=="2833/200"
    assert c["interface_exact_squared_norm_upper"]=="6411/3200"
    assert c["numeric_display_only_E0_interval"][0]<-3.1898474481159673
    assert c["numeric_display_only_E0_interval"][1]>-3.1898474481159673
    assert c["spectral_gap_certified"] is False

def test_seven_cover_seed_actual_second_order_pair_flip_graph():
    c=quantum()
    assert c["known_distinct_PGSp_orbits"]==7
    assert c["total_pair_flip_tests"]==88480
    assert len(c["neighborhood_summary"])==7
    assert all(z["local_20_loop_degree"]>=1 for z in c["neighborhood_summary"])
    assert c["distinct_second_order_neighbor_covers_over_seven_seeds"]>=7
    assert c["compressed_star_is_full_induced_seven_orbit_graph"] is False

def test_interacting_native_U1_two_loop_rephasing_and_finite_temperature():
    c=matter()
    assert c["Fock_dim"]==462
    assert len(c["V_scans"])==4
    assert all(len(row["grid_5x5"])==25 for row in c["V_scans"])
    assert all(len(row["full_spectrum_four_corner_free_energies"])==4 for row in c["V_scans"])
    assert c["gauge_rephasing_spectrum_invariance"]
    assert c["time_reversal_spectrum_invariance"]
    assert all(row["min_grid_holonomy"]["ritz_residual"]<1e-7 for row in c["V_scans"])
