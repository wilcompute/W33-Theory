"""PIC comparison: exact target gates, reference-GDS integrity, and scenario sensitivity."""
import os,sys
from pathlib import Path
import numpy as np
import pytest
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'analysis'))
os.environ.setdefault('W33_GDSTK_PATH',r'C:\Temp\w33_gdstk_isolated')
from w33_pic_xor_walsh_pareto_20261023 import (
 H4,target,walsh_target,xor_target,monte_carlo,device_loss_scenarios,make_layout)
def test_both_switches_implement_all_four_exact_masks():
    for k in range(4):
        P=target(k)
        assert np.linalg.norm(walsh_target(k)-P)<1e-12
        assert np.linalg.norm(xor_target(k)-P)<1e-12
def test_walsh_modes_are_unitary_under_phase_error():
    for k in range(4):
        U=walsh_target(k,[.02,-.03,.04,.01])
        assert np.linalg.norm(U.conj().T@U-np.eye(4))<1e-12
def test_loss_comparison_is_not_prejudged():
    scenarios=device_loss_scenarios()
    assert any(v['preferred_by_simple_path_loss']=='XOR' for v in scenarios)
    assert any(v['preferred_by_simple_path_loss']=='Walsh' for v in scenarios)
def test_monte_carlo_determinism_and_leakage():
    a=monte_carlo(draws=12)
    assert a==monte_carlo(draws=12)
    for key,row in a.items():
        assert row['sample_count']==48
        assert 0<row['mean_unitary_overlap']<=1
        assert row['mean_worst_port_wrong_probability']>0
def test_gds_readback_and_incomplete_physical_signoff(tmp_path):
    v=make_layout(tmp_path/'test.gds',tmp_path/'test.svg')
    assert v['forty_macro_references']==40 and v['symbolic_mzi_total']==160
    assert v['cell_names']==['W33_40BUS_PHOTONIC_REF','W33_FOUR_MZI_SYMBOL','W33_WALSH_SYMBOL']
    assert v['unrouted_second_stage_pairs']==[[0,2],[1,3]]
    assert v['gds_size_bytes']>2000
    assert (tmp_path/'test.svg').stat().st_size>100
    assert 'DRC_LVS_NOT_RUN' in v['status']
