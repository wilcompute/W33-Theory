"""W33 40 four-port buses form the Q(4,3) dual point graph, with rank-8 phase mask."""
import sys,math
from pathlib import Path
import numpy as np
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'analysis'))
from w33_linebus_dual_q43_phase_geometry_20261023 import bus_dual,certificate
from w33_linebus_q43_address_bridge_codegen_20261023 import produce
from w33_fractal_linebus_switch_matrix_20261023 import LINES,THROUGH
from w33_phase_oracle_mod_local_gauge_rank14_20261023 import rank_factor,centered
from w33_q43_cospectral_mode_entanglement_phase_complexity_20261023 import graphs
def test_line_bus_geometry_is_four_rails_and_four_buses_per_point():
    assert len(LINES)==40 and all(len(x)==4 for x in LINES)
    assert len(THROUGH)==40 and all(len(x)==4 for x in THROUGH.values())
def test_exact_point_line_dual_has_srg_parameters_and_quadratic_eigenvalues():
    E=bus_dual()
    assert E.shape==(40,40) and np.array_equal(E,E.T)
    assert np.all(E.sum(axis=1)==12)
    assert np.allclose(np.linalg.eigvalsh(E),np.array([-4]*15+[2]*24+[12]))
def test_line_bus_dual_is_explicitly_isomorphic_to_Q43():
    x=certificate()
    E=np.asarray(x['bus_intersection_adjacency_E'])
    mp=x['bus_to_parabolic_quadric_point_permutation']
    assert sorted(mp)==list(range(40))
    Q=graphs()[1]
    assert np.array_equal(E,Q[np.ix_(mp,mp)])
def test_dual_line_bus_eight_term_vs_w33_point_fourteen_term():
    E=bus_dual()
    W=graphs()[0]
    assert rank_factor(E)[0].shape[1]==10
    assert rank_factor(centered(E))[0].shape[1]==8
    assert rank_factor(centered(W))[0].shape[1]==14
def test_interface_bridge_generated_native_bus_permutation_no_optical_cz():
    j=produce()
    assert j['logical_nonlocal_binary_phase_terms']==8
    assert j['physical_W33_bus_ids']==40
    assert j['valid_test_pairs']==1600 and j['invalid_test_pairs']==2496
    rtl=Path(__file__).resolve().parents[1]/j['RTL']
    x=rtl.read_text()
    assert 'q43_phase_oracle_rank8_20261023 target(' in x
    assert "default:to_q43=6'd63" in x
    assert 'no coherent' in j['limitation'].lower() or 'optical' in j['limitation'].lower()
def test_all_intersections_shared_one_point_and_registered_phases_match():
    E=bus_dual()
    for i in range(40):
        for j in range(40):
            if i!=j:
                assert int(E[i,j])==len(set(LINES[i])&set(LINES[j]))

def test_native_bus_direct_eight_term_deletes_runtime_lookup_overhead():
    from w33_linebus_q43_direct_rank8_RTL_codegen_20261023 import produce as direct
    cert=direct()
    assert cert['direct_W33_bus_numbering']
    assert cert['dynamic_bus_to_Q43_lookups']==0
    assert cert['cross_register_phase_terms']==8
    generated=Path(__file__).resolve().parents[1]/cert['rtl']
    s=generated.read_text()
    assert "cross_comb=da[7:0]&db[7:0]" in s
    assert 'to_q43' not in s
    testbench=(generated.parent/'tb_w33_linebus_dual_rank8_direct_20261023.sv').read_text()
    assert 'valid_cases!=1600||invalid_cases!=2496' in testbench
