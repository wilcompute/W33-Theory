from pathlib import Path
import json,math
from analysis.bt3155_3158_factor_epoch import factor_schedule,marker_proof,MARKER,SYNC
from analysis.bt3160_adaptive_dual_isa import threshold,choose,effective_collision_cost

ROOT=Path(__file__).resolve().parents[1]

def test_factor_schedule_exact():
    schedule,pairs=factor_schedule()
    assert len(schedule)==528
    assert len(pairs)==len(set(pairs))==69
    assert schedule[0]['address']==0 and schedule[44]['address']==44
    assert schedule[45]['kind']=='pair' and schedule[-1]['address']==527
    assert 7*528+1==3697

def test_epoch_marker_and_spacing():
    spacing=marker_proof()
    assert set(MARKER).isdisjoint(set(SYNC))
    assert len({(SYNC[i],SYNC[(i+1)%12]) for i in range(12)})==12
    assert spacing[2]['payload_symbols']==48
    assert math.isclose(spacing[2]['overhead_fraction'],5/53)

def test_dual_isa_hysteresis():
    assert math.isclose(threshold(),3.741933823529581)
    assert math.isclose(threshold(.25,'up'),4.640798576082018)
    assert math.isclose(threshold(.25,'down'),2.843069070977144)
    assert choose('current4',5.0)=='low_collision4'
    assert choose('low_collision4',2.0)=='current4'
    assert effective_collision_cost(1,1,0,.99)>1

def test_source_summary_boundaries():
    d=json.loads((ROOT/'data/PART_BT3153_BT3160_ADAPTIVE_EPOCH_FACTOR_ENGINE_source_summary.json').read_text())
    assert d['pass_3153_3154']['five_six_subsets']==462
    assert d['pass_3153_3154']['universal_subsets']==194
    assert d['pass_3155_3156']['sweep_cycles']==528
    assert d['pass_3157_3158']['radius_two_false_acquisition']=='IMPOSSIBLE'
    assert d['pass_3159']['current_candidate_status']=='NO_ACCEPTED_CANDIDATE_OBSERVED'
    assert 'unobserved' in d['pass_3155_3156']['boundary']

def test_rtl_and_integrity_sources_exist():
    factor=(ROOT/'rtl/w33_pass3155_sparse_factor_engine.sv').read_text()
    ctrl=(ROOT/'rtl/w33_pass3157_3160_epoch_dual_isa.sv').read_text()
    assert 'bank6' in factor and "cycle_o==10'd527" in factor
    assert "5'd1" in ctrl and "5'd22" in ctrl
    assert 'UP_THRESHOLD' in ctrl and 'DOWN_THRESHOLD' in ctrl
