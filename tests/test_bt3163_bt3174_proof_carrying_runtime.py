from __future__ import annotations
import json, math, sys
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))

from analysis.bt3164_tri_isa_physical_contract import cross, cost
from analysis.bt3167_3168_phase_coded_epoch import PHASE_SYMBOLS, PAYLOAD, edit_ball, lev
from analysis.bt3169_3170_bayesian_datapath import build_tables
from analysis.bt3171_d4_belief_curvature import comm
from analysis.bt3172_isa_channel_capacity import metrics


def load(name: str):
    return json.loads((ROOT/'data'/name).read_text())


def test_tri_isa_exact_runtime_law():
    assert cross('current4','fast6') < 0
    assert math.isclose(cross('fast6','low4'),16.701642492779975)
    for c in (0,1,10):
        assert cost('fast6',c)<cost('current4',c)
    assert cost('low4',25)<cost('fast6',25)


def test_phase_code_is_optimal_and_disjoint():
    assert len(PHASE_SYMBOLS)==12 and len(set(PHASE_SYMBOLS))==12
    assert set(PHASE_SYMBOLS).isdisjoint(set(PAYLOAD))
    words=[(u,)*5 for u in PHASE_SYMBOLS]
    assert min(lev(a,b) for i,a in enumerate(words) for b in words[i+1:])==5
    balls=[edit_ball(w,2) for w in words]
    assert sum(map(len,balls))==298140
    seen=set()
    for b in balls:
        assert seen.isdisjoint(b);seen.update(b)


def test_bayesian_hypothesis_and_factor_counts():
    u1,u2,ci,outcomes,pairs=build_tables()
    assert len(u1)==len(u2)==len(ci)==outcomes.shape[0]==48826
    assert len(pairs)==69
    assert int((ci>=0).sum())==3381
    d=load('PART_BT3169_BT3170_BAYESIAN_DATAPATH_results.json')
    assert d['action_matches']==d['action_tests']==12
    assert d['cycle_contract']['total']==98387
    assert not d['dense_posterior_ram_required']


def test_curvature_and_channel_theorems():
    assert comm((1,0),(0,1))==(2,0)
    c=load('PART_BT3171_D4_BELIEF_CURVATURE_results.json')
    assert c['ordered_label_pair_census']=={'curved':24,'flat':25}
    assert c['full_factor_census']=={'curved':1656,'flat':1725}
    current=metrics(['F_p','CX_pf','CX_fp','Z1'])
    fast=metrics(['F_f','CX_pf','CX_fp','Z0','Z1','Z3'])
    assert fast['average_bits_per_dispatch']>current['average_bits_per_dispatch']


def test_source_summary_and_pending_boundaries():
    d=load('PART_BT3163_BT3174_PROOF_CARRYING_RUNTIME_source_summary.json')
    assert d['local_exact_status']=='PASS'
    assert d['pass_3163']['status'].endswith('EVIDENCE_PENDING')
    assert d['pass_3165_3166']['status'].endswith('EVIDENCE_PENDING')
    assert d['pass_3167_3168']['post_marker_clean_symbols_required']==0
    assert 'RTL simulation' in d['evidence_boundary']


def test_rtl_and_publication_sources_are_typed():
    epoch=(ROOT/'rtl/w33_pass3168_phase_epoch_decoder.sv').read_text()
    enum=(ROOT/'rtl/w33_pass3169_hypothesis_enumerator.sv').read_text()
    stream=(ROOT/'rtl/w33_pass3169_3170_bayesian_stream.sv').read_text()
    assert "5'd17" in epoch and 'ambiguous_o' in epoch
    assert "16'd48825" in enum and 'correction_index_o' in enum
    assert '23 packed 3-bit D4 outcomes' in stream and 'MIN_LOGW' in stream
    report=(ROOT/'analysis/BT3163_BT3174_proof_carrying_runtime.md').read_text()
    assert 'not a no-go' in report and 'what is not built' in report.lower()
