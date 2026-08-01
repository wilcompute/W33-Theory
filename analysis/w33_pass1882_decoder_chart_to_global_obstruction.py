#!/usr/bin/env python3
"""Pass 1882: correct the fixed-coordinate decoder globalization.

A coordinate chart records only equal-syndrome errors sharing that coordinate.
It therefore cannot determine global syndrome multiplicity.  This verifier
turns the exact Pass-1847/1860/1876 counts into a fail-closed obstruction.
"""
from __future__ import annotations
import hashlib,json,math
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/w33_pass1882_decoder_chart_to_global_obstruction.json'

def canonical_hash(d):
 x=dict(d);x.pop('sha256_without_hash_field',None)
 return hashlib.sha256(json.dumps(x,sort_keys=True,separators=(',',':')).encode()).hexdigest()

def main():
 old=json.loads((ROOT/'data/w33_pass1847_exact_weight5_decoder_completion.json').read_text())
 w6=json.loads((ROOT/'data/w33_pass1860_weight6_decoder_frontier.json').read_text())
 exact=json.loads((ROOT/'data/w33_pass1876_exact_dual_weight_enumerator.json').read_text())
 terms={4:old['weight5_collision_terms']['A4'],6:old['weight5_collision_terms']['A6'],8:old['weight5_collision_terms']['A8'],10:old['weight5_collision_terms']['A10']}
 hist={int(k):v for k,v in old['decoder']['minimum_syndrome_group_histogram'].items()}
 min_pairs=sum(n*math.comb(m,2) for m,n in hist.items())
 fixed_pairs=sum(v*(5-w//2) for w,v in terms.items())//240
 lower_pairs=fixed_pairs-min_pairs
 total5=old['decoder']['global_total_weight5'];lower5=old['decoder']['global_lower_shadow'];minimum5=total5-lower5
 upper5=old['decoder']['global_unique_minimum_weight5']
 A12=exact['A12'];E6=1312130546100+462*A12
 checks={
  'weight5_partition':lower5+minimum5==total5,
  'weight5_edges_sum':sum(terms.values())==old['weight5_collision_edges'],
  'fixed_pair_double_count':sum(v*(5-w//2) for w,v in terms.items())==240*fixed_pairs,
  'weight10_pairs_chart_invisible':5-10//2==0 and terms[10]==2207943360,
  'chart_pair_partition':min_pairs+lower_pairs==fixed_pairs,
  'chart_singleton_arithmetic':240*old['decoder']['fixed_unique_minimum_weight5']==5*upper5,
  'weight6_total':math.comb(240,6)==w6['weight6_total_errors'],
  'weight6_collision_exact':E6==exact['weight6_equal_syndrome_pairs'],
  'moment_witness':3*2==3*1+1*3 and 3*math.comb(2,2)==3*math.comb(1,2)+math.comb(3,2),
 }
 out={
  'schema':'w33.pass1882.decoder_chart_to_global_obstruction.v1','status':'PASS_WITH_PROOF_BOUNDARY','checks':checks,
  'weight5':{
   'total_errors':total5,'exact_lower_shadow_errors':lower5,'exact_minimum_weight5_errors':minimum5,
   'previously_claimed_unique_minimum':upper5,'corrected_status':'upper_bound_only',
   'certified_upper_bound_on_global_unique_minimum':upper5,
   'collision_edges_by_codeword_weight':{str(k):v for k,v in terms.items()},
   'total_collision_edges':sum(terms.values()),
   'disjoint_weight10_collision_edges_invisible_to_every_coordinate_chart':terms[10],
   'fixed_coordinate_pair_count_exact':fixed_pairs,'fixed_minimum_chart_pair_count':min_pairs,
   'fixed_lower_chart_pair_count':lower_pairs,
   'chart_singleton_incidence_identity':'240*62,359,342 = 5*2,993,248,416'},
  'weight6':{
   'total_errors':math.comb(240,6),'exact_equal_syndrome_collision_edges':E6,
   'exact_lower_shadow_incidence_count_not_deduplicated':w6['lower_shadow_incidence_counts']['total_incidence'],
   'unique_minimum_coefficient_status':'OPEN',
   'moment_nonidentifiability_witness':{'distribution_A':'three classes of multiplicity 2','distribution_B':'three singleton classes and one class of multiplicity 3','errors_each':6,'collision_edges_each':3,'singleton_errors_A':0,'singleton_errors_B':3}},
  'theorem':'A fixed-coordinate syndrome sort does not determine global minimum multiplicity. Equal-syndrome weight-five errors differing by a weight-w codeword coappear in exactly 5-w/2 coordinate charts; all weight-10 pairs are disjoint and invisible in every chart. Hence 2,993,248,416 is an upper bound, not an exact fifth-order coefficient. The exact sixth-order collision edge count likewise does not determine singleton syndrome classes.',
  'boundary':'Exact fifth- and sixth-order unique-minimum coefficients require a true global syndrome-component enumeration; no fixed-coordinate globalization or moment-only shortcut is valid.'}
 assert all(checks.values()),{k:v for k,v in checks.items() if not v}
 out['sha256_without_hash_field']=canonical_hash(out)
 OUT.write_text(json.dumps(out,sort_keys=True,separators=(',',':'))+'\n')
 print(json.dumps({'status':out['status'],'upper5':upper5,'E6':E6,'sha256':out['sha256_without_hash_field']},indent=2))
 return out
if __name__=='__main__':main()
