#!/usr/bin/env python3
"""Pass6233-6240: audit/replay of scaffold claim tiers after Pass6189-6232."""
from pathlib import Path
import json

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data'/'PART_W33_PASS6233_6240_SCAFFOLD_CLAIM_TIER_REPAIR.json'

def rd(p): return (ROOT/p).read_text()

def main():
    status=rd('scripts/w33_ce2_k3_evidence_repair_status.py')
    trans=rd('scripts/w33_transport_cocycle_scaffold.py')
    k3=rd('scripts/w33_k3_witness_search_scaffold.py')
    summary=rd('docs/pass_6189_6232_summary.md')

    assert "ce2_global_closure='OPEN'" in status
    assert 'k3_curvature_object_loaded=False' in status
    assert 'REFUTED_FOR_DISPLAYED_BLOCKS' in status
    assert 'CONDITIONAL_SCAFFOLD_ONLY' in trans
    assert 'No actual family-flag identification' in trans
    assert 'AMBIENT_UPPER_BOUND_SCAFFOLD_ONLY' in k3
    assert 'admissible_candidate_count' in k3 and 'None' in k3
    assert 'CORRECTED BY PASS6233–6240' in summary

    out={
      'schema':'w33.pass6233_6240.scaffold_claim_tier_repair.v1',
      'status':'PASS_CORRECTION',
      'pass_6233_status_ledger':{
        'ce2_global':'OPEN','k3_object_loaded':False,'k3_scan_run':False,
        'generation_flag':'REFUTED_FOR_DISPLAYED_BLOCKS','transport_identification':'OPEN_CONDITIONAL_SCAFFOLD_ONLY'},
      'pass_6234_transport_scaffold':{
        'retained':'conditional signature comparison of a chosen positive plane and abstract hyperbolic plane',
        'withdrawn':'claim that the chosen positive plane is the actual internal generation flag or that rho is a certified external carrier parameter',
        'verdict':'CONDITIONAL_TOY_NOT_IDENTIFICATION_THEOREM'},
      'pass_6235_k3_candidate_count':{
        'ambient_single_entry_count':2428*36*2,
        'admissible_candidate_count':None,
        'verdict':'AMBIENT_UPPER_BOUND_ONLY',
        'reason':'actual K3 object, coordinate map, and deformation/cocycle constraints are not loaded'},
      'pass_6236_summary_repair':{'historical_complete_flags':['CE2 global orbit closure','K3 deformation theory'],'live_flags':['OPEN','OBJECT NOT LOADED']},
      'pass_6237_evidence_rule':{'rule':'A scaffold may parameterize a hypothetical search/comparison space, but cannot promote its inputs to certified geometry without provenance and defining equations.'},
      'pass_6238_next_ce2':'recover actual CE2 evaluator/action and enumerate rows rather than count family labels',
      'pass_6239_next_k3':'locate actual K3 cochain/curvature artifact and derive admissibility equations before candidate enumeration',
      'pass_6240_frontier':'scaffolds preserved, theorem tiers fail-closed'}
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
    print(json.dumps(out,indent=2,sort_keys=True))
    return out

if __name__=='__main__': main()
