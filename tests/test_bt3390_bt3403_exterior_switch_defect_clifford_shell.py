from __future__ import annotations
import importlib.util
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('runner',ROOT/'analysis/bt3390_3401_validated_runner.py')
runner=importlib.util.module_from_spec(spec);assert spec.loader;spec.loader.exec_module(runner)
core=runner.core

def test_exterior_census_and_cap():
    x=core.exterior_audit()
    assert x['residual_sheet_census']==x['known_sheet']
    assert x['exceptional_cap']['stab'][8]==15

def test_defect_templates_and_common_local_witness():
    ts=core.split_templates();w=core.local_witness()
    assert len(ts)==15
    assert len({tuple(t['spectrum']) for t in ts})==11
    assert w['status']=='PASS_COMMON_45_BLOCK_BALANCED_WITNESS'
    assert w['local_pair_max'] < min(v for t in ts for v in t['edge_counts'].values())

def test_fail_closed_sidecars():
    x=core.sidecars()
    assert x['leaves']==100 and x['live_boundary']=='10 <= chi(H) <= 11'

def test_clifford_source_bound():
    x=core.clifford_resources()
    assert x['table_lookup']['toffoli_upper_bound']==56700
    assert x['table_lookup']['standard_7T_upper_bound']==396900

def test_shell_theorem_and_macwilliams():
    x=runner.shell_theorem(6)
    assert x['instances'][2]['quotient_shells']==[135,207,144,48,9,1]
    assert x['instances'][2]['tau_invariant_multiplicities']==[1,9,48,144,207,135]
    m=core.macwilliams_bridge()
    assert m['span_size']==2048

def test_branched_skeleton_boundary():
    x=core.branched_skeleton()
    assert x['two_regular_sheets']+x['branch_cap']==327
    assert x['cap_stabilizers'][8]==15
