"""Five-front Walsh-qutrit design: physically honest executable regressions."""
import json,math,os,sys
from pathlib import Path
import numpy as np
import pytest
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'analysis'))
os.environ.setdefault('W33_GDSTK_PATH',r'C:\Temp\w33_gdstk_isolated')
from w33_walsh_qutrit_lab_ref_layout_20261023 import optical_target,make
from w33_walsh_qutrit_phase_noise_falsification_20261023 import prediction,decode_counts,simulation,analyze_real_csv
from w33_walsh_qutrit_160_incidence_transfer_20261023 import incidence_graph,transfer,report as route_report
from w33_walsh_two_qutrit_entangler_target_20261023 import report as entangle_report,gate,negativity

def test_gds_is_generated_and_clearly_not_manufacturable(tmp_path):
    x=make(tmp_path)
    assert x['gds_bytes']>1200
    assert len(x['stages'])==5
    assert not x['PDK_selected'] and not x['tapeout_ready'] and not x['LVS_passed']
    assert 'SCHEMATIC' in x['photonic_nets_status']

def test_8_ideal_unitary_cells_keep_auxiliary_walsh_mode_isolated():
    for m in range(4):
        for cyc in (False,True):
            U=optical_target(m,cyc)
            assert np.linalg.norm(U.conj().T@U-np.eye(4))<1e-11
            assert abs(U[0,0]-1)<1e-11
            assert np.linalg.norm(U[0,1:])+np.linalg.norm(U[1:,0])<1e-11

def test_correlated_gaussian_law_and_noise_identifiability():
    for sigma in (.0,.05,.1,.3):
        assert prediction(sigma,1)==0
        assert prediction(sigma,.5)==pytest.approx(prediction(sigma/math.sqrt(2),0))
    o=simulation(shots=5000,phase_samples=600)
    assert len(o['conditions'])==12 and o['DATA_TYPE'].startswith('SYNTHETIC')
    assert 'Only sigma*sqrt(1-rho)' in o['identifiability']

def test_calibrated_count_inversion_and_real_csv_parser(tmp_path):
    a=decode_counts(1000,100000,efficiency=.75,dark_prob=.001)
    assert a['inferred_auxiliary_leakage']>0
    with pytest.raises(ValueError):decode_counts(5,4)
    csv=tmp_path/'actual_counts.csv'
    csv.write_text('sigma_per_rail_rad,common_mode_correlation_rho,clicks,shots,detector_efficiency,dark_false_click_probability\n0.1,0,1000,100000,0.75,0.001\n')
    record=analyze_real_csv(csv)
    assert len(record['inference'])==1
    assert record['inference'][0]['inferred_auxiliary_leakage']==pytest.approx(a['inferred_auxiliary_leakage'])

def test_160_distinct_incidence_ports_and_780_four_rail_targets():
    adjacency,by_point=incidence_graph()
    assert len(adjacency)==160 and len(by_point)==40
    assert all(len(x)==6 for x in adjacency)
    rep=route_report()
    assert rep['line_pairs_checked']==780
    assert rep['intersections']=={0:540,1:240}
    for a,b in [(0,1),(0,20),(12,39)]:
        x=transfer(a,b)
        assert len(x['four_pair_swaps'])==4
        assert len(set(x['source_160_incidence_rails']+x['destination_160_incidence_rails']))==8
        assert x['qutrit_transfer_residual']<1e-12
        assert x['number_of_distinct_physical_rail_swaps']==4

def test_two_qutrit_controlled_phase_is_entangling_local_circuit_not():
    p=entangle_report()
    assert np.linalg.norm(gate().conj().T@gate()-np.eye(9))<1e-12
    assert p['partial_transpose_negativity']==pytest.approx(1)
    assert p['reduced_purity']==pytest.approx(1/3)
    assert p['von_neumann_entanglement_bits']==pytest.approx(math.log2(3))
    assert not p['local_F3_R_operations_entangle'] and not p['current_device_has_entangler']

def test_yosys_gatelevel_source_is_tech_independent_and_latch_free():
    p=ROOT/'data/w33_walsh_qutrit_frame_gatelevel_20261023.json'
    if not p.exists():pytest.skip('gate-level netlist not present on this checkout')
    mod=json.loads(p.read_text())['modules']['w33_walsh_qutrit_frame']
    types=[cell['type'] for cell in mod['cells'].values()]
    assert len(types)==24
    assert sum(t.startswith('$_DFFE') for t in types)==8
    assert not any(t.startswith('$_DLATCH') for t in types)
