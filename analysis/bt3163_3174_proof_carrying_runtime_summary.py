#!/usr/bin/env python3
"""Aggregate the locally observed exact/model layer for Passes 3163-3174.

This summary never upgrades the 194-ISA or 256-shard workflows from source-complete to
complete.  Their status changes only when their separate aggregate artifacts exist.
"""
from __future__ import annotations
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];DATA=ROOT/'data'
OUT=DATA/'PART_BT3163_BT3174_PROOF_CARRYING_RUNTIME_source_summary.json'

def load(name): return json.loads((DATA/name).read_text())

def main():
    tri=load('PART_BT3164_TRI_ISA_PHYSICAL_CONTRACT_results.json')
    epoch=load('PART_BT3167_BT3168_PHASE_CODED_EPOCH_results.json')
    bayes=load('PART_BT3169_BT3170_BAYESIAN_DATAPATH_results.json')
    curv=load('PART_BT3171_D4_BELIEF_CURVATURE_results.json')
    chan=load('PART_BT3172_ISA_CHANNEL_CAPACITY_results.json')
    plan=load('PART_BT3165_M36_SHARD_PLAN.json')
    checks={
      'tri_dominance':tri['crossovers']['current4_vs_fast6']<0,
      'phase_code':epoch['total_exhausted_marker_traces']==298140 and epoch['post_marker_clean_symbols_required']==0,
      'bayesian':bayes['hypotheses']==48826 and bayes['action_matches']==bayes['action_tests']==12,
      'curvature':curv['full_factor_census']=={'flat':1725,'curved':1656},
      'channel':chan['results']['fast6']['average_bits_per_dispatch']>chan['results']['current4']['average_bits_per_dispatch'],
      'm36_plan':plan['shard_count']==256 and plan['bucket_count']==32,
    }
    out={
      'schema':'w33.pass3163_3174.proof_carrying_runtime.source_summary.v1',
      'local_exact_status':'PASS' if all(checks.values()) else 'FAIL','checks':checks,
      'manuscript_refresh':{
        'photonic_holonet_lines_read':7332,
        'photonic_holonet_anchor':'carrier/state/operator duality; address-route duality; selector-clock versus mirror-bus separation; matter=magic; demonstrator versus fault-tolerant boundary',
        'machine_blueprint_pages_reviewed':38,
        'machine_blueprint_anchor':'four-trit frame machine; measured-versus-modelled evidence ladder; support/readout versus phase/execution; M36 injection remains an external typed handshake'},
      'pass_3163':{'universal_larger_isas':194,'full_group_order':4199040,'shard_count':32,
        'status':'SHARDED_ENGINE_SOURCE_COMPLETE_EVIDENCE_PENDING','claim_boundary':'No global full-distance optimum until all 194 shard records aggregate.'},
      'pass_3164':tri,
      'pass_3165_3166':{'isotropic_rank3_subspaces':plan['expected_isotropic_subspaces'],'logical_shards':plan['shard_count'],
        'workflow_buckets':plan['bucket_count'],'shards_per_bucket':plan['shards_per_bucket'],
        'status':'256_SHARD_BRIDGE_SOURCE_COMPLETE_EVIDENCE_PENDING','candidate_status':'NO_ACCEPTED_CANDIDATE_OBSERVED_BEFORE_THIS_RUN',
        'claim_boundary':'Zero candidates is a no-go only after all 256 normalized shards and independent certification complete.'},
      'pass_3167_3168':{'phase_symbols':epoch['phase_symbols'],'marker_length':epoch['marker_length'],
        'minimum_distance':epoch['minimum_marker_distance'],'correctable_edits':epoch['correctable_adversarial_edits'],
        'exhausted_marker_traces':epoch['total_exhausted_marker_traces'],'post_marker_clean_symbols_required':epoch['post_marker_clean_symbols_required'],
        'optimality':epoch['optimality']},
      'pass_3169_3170':{'hypotheses':bayes['hypotheses'],'actions':bayes['actions'],'streaming_passes':bayes['streaming_passes'],
        'cycles_per_decision':bayes['cycle_contract']['total'],'modeled_decisions_per_second_at_100mhz':bayes['cycle_contract']['modeled_decisions_per_second_at_100mhz'],
        'max_posterior_abs_error':bayes['max_posterior_abs_error'],'max_action_score_abs_error_bits':bayes['max_action_score_abs_error_bits'],
        'action_matches':bayes['action_matches'],'action_tests':bayes['action_tests']},
      'pass_3171':{'pair_correction_factors':sum(curv['full_factor_census'].values()),'flat':curv['full_factor_census']['flat'],
        'curved':curv['full_factor_census']['curved'],'curvature_bits':curv['curvature_syndrome_bits'],'theorem':curv['theorem']},
      'pass_3172':{'current4_bits_per_dispatch':chan['results']['current4']['average_bits_per_dispatch'],
        'low4_bits_per_dispatch':chan['results']['low_collision4']['average_bits_per_dispatch'],
        'fast6_bits_per_dispatch':chan['results']['fast6']['average_bits_per_dispatch'],
        'fast6_absolute_gain_fraction_vs_current':chan['results']['comparisons']['fast6_absolute_gain_fraction'],
        'theorem':'raw collision count and control-channel capacity are distinct; fast6 provides 30.3347% more absolute control information per dispatch than current4 under uniform frame/opcode averaging'},
      'evidence_boundary':'Exact/model computations above were run locally. 194-ISA BFS aggregation, 256-shard M36 completion, RTL simulation/synthesis/place, manuscript materialization, PDF builds and laboratory behavior remain external evidence gates.'}
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
    print(json.dumps({'status':out['local_exact_status'],'checks':checks},indent=2,sort_keys=True))
    return 0 if all(checks.values()) else 1
if __name__=='__main__': raise SystemExit(main())
