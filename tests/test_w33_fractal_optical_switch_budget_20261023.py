"""Tests of explicitly hypothetical W33 optical selector model."""
import math,sys
from pathlib import Path
import pytest
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'analysis'))
from w33_fractal_optical_switch_budget_20261023 import (
    mzi,tree_transfer,single_link_budget,route_budget,build)
from w33_fractal_four_lane_scheduler_20261023 import sparse_route
import numpy as np
def test_mzi_is_unitary():
    for phase in (0,.05,math.pi/2,math.pi,2*math.pi):
        U=mzi(phase)
        assert np.linalg.norm(U.conj().T@U-np.eye(2))<1e-13
def test_lossless_one_to_three_exact_routing():
    for out in range(3):
        s=tree_transfer(out,0.0,0.0)
        assert s['target_probability']==pytest.approx(1.,abs=1e-13)
        assert s['wrong_port_probability']==pytest.approx(0.,abs=1e-13)
        assert s['absorbed_probability']==pytest.approx(0.,abs=1e-13)
def test_tree_has_branch_dependent_loss():
    single=10**(-.2/10)
    assert tree_transfer(0,0,.2)['target_probability']==pytest.approx(single)
    for out in (1,2):
        assert tree_transfer(out,0,.2)['target_probability']==pytest.approx(single**2)
    assert single_link_budget(0,0,.2,.1)['switch_mzi_stages_across_both_endpoints']==2
    assert single_link_budget(2,0,.2,.1)['switch_mzi_stages_across_both_endpoints']==4
def test_off_state_leaks_light():
    a=tree_transfer(1,.05,.2)
    assert a['wrong_port_probability']>0
    assert a['absorbed_probability']>0
    assert sum(a['powers'])<1
def test_route_loss_is_positive_and_counts_reconcile():
    r=sparse_route((5,6,7),(18,22,25))
    q=route_budget(r)
    assert q['hops']==len(r)-1
    assert q['interchild_hops']+q['local_hops']==q['hops']
    assert sum(q['interchild_slots'].values())==q['interchild_hops']
    assert 0<q['selected_path_survival']<1
def test_repeatability_and_guardrails():
    a=build(3)
    assert build(3)['sha256']==a['sha256']
    assert a['status'].startswith('HYPOTHETICAL')
    with pytest.raises(ValueError):tree_transfer(3)
    with pytest.raises(ValueError):single_link_budget(0,0,-1,.1)
