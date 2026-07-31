#!/usr/bin/env python3
"""Pass 1533: exact audit of what the current cover-orbit frontier proves."""
from __future__ import annotations
import argparse,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
SAT=ROOT/'data'/'w33_pass1510_bidirectional_cover_saturation.json'
DIS=ROOT/'data'/'w33_pass1511_1515_cover_resolution_frontiers.json'
def certificate()->dict:
 a=json.loads(SAT.read_text());b=json.loads(DIS.read_text());hist={int(k):int(v) for k,v in a['union']['stabilizer_order_histogram'].items()};order=25920
 orbit_sum=sum(n*(order//s) for s,n in hist.items())
 checks={
  'same_327_orbits_both_directions':a['checks']['same_327_complete_orbits'],
  'raw_prefixes_disjoint':a['checks']['raw_prefixes_disjoint'],
  'orbit_sum_3547800':orbit_sum==3547800==a['union']['certified_cover_lower_bound'],
  'all_327_have_disjoint_partner':b['checks']['pass1512_all_327_orbits_have_disjoint_partner'],
  'disjoint_partner_count_13648':b['pass1512_disjoint_partner_frontier']['distinct_disjoint_covers']==13648,
  'frozen_disjoint_graph_clique_3':b['pass1513_disjointness_graph_and_four_packing']['graph']['clique_number']==3,
  'four_packing_exact':b['checks']['pass1513_four_packing_exact'],
 }
 checks={k:bool(v) for k,v in checks.items()};assert all(checks.values())
 return {'schema':'w33.pass1533.cover_orbit_frontier_audit.v1','status':'PASS',
  'hoffman_coclique_statement':'Every 60-frame maximum independent set of H is an exact cover; therefore cover orbit classification is maximum-Hoffman-coclique classification.',
  'frozen_frontier':{'psp_order':order,'orbit_types':327,'stabilizer_order_histogram':hist,'certified_cover_lower_bound':orbit_sum,
    'disjoint_partners_of_canonical_cover':13648,'disjointness_graph_clique_number':3},
  'quantifier_audit':{
    'proved':'Both opposite DFS prefixes meet the same 327 complete PSp orbits; all 327 have a disjoint partner; the frozen disjointness graph is exhaustively computed.',
    'not_proved':'The 327 orbits are not proved to be all global cover orbits, and clique number three in the canonical-cover link is not the global packing number.',
    'reason':'Both enumerations are finite prefixes. Agreement under branch reversal is saturation evidence, not an exhaustion certificate.'},
  'checks':checks,
  'boundary':'Global classification of all maximum cocliques remains open until canonical augmentation or an exhaustive solver produces a completeness certificate.'}
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--output',type=Path);ap.add_argument('--check',action='store_true');a=ap.parse_args();r=certificate();t=json.dumps(r,indent=2,sort_keys=True)+'\n'
 if a.output:a.output.write_text(t)
 if not a.check or not a.output:print(t,end='')
if __name__=='__main__':main()
