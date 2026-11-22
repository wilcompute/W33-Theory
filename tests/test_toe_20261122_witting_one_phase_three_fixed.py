"""Exact tests for one-phase three-fixed-mirror Witting controllability."""
from __future__ import annotations
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'analysis'))
import toe_20261122_witting_one_phase_three_fixed as witness

def test_qomega_exact_mirror_action():
    d=witness.verify()
    assert d['fixed_mirror_actions_are_permutations_of_all_40_rays']
    assert d['fixed_mirror_orders']==[3,3,3]
    assert d['fixed_subgroup_permutation_order']==648
    assert d['fixed_subgroup_orbit_sizes']==[27,12,1]

def test_one_phase_orbit_controllability():
    d=witness.verify()
    assert d['orbit_size']==27
    assert d['target_four_ray_subset']==[0,2,7,20]
    assert d['target_lie_rank_layers']==[4,8,14,16]
    assert all(q['Lie_rank']==16 for q in d['target_modular_certificates'])
    assert all(int(j) in d['orbit_indices'] for j in d['target_four_ray_subset'])
