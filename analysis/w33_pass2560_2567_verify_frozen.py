#!/usr/bin/env python3
from pathlib import Path
import json,hashlib
ROOT=Path(__file__).resolve().parents[1]
FILES=[
'data/w33_pass2560_u6_singleton_orbit_harvest.json',
'data/w33_pass2561_chromatic_interval_10_11.json',
'data/w33_pass2562_exact_character_fusion.json',
'data/w33_pass2563_full_group_nonlinear_covariants.json',
'data/w33_pass2564_joint_octet_fourier_macwilliams.json',
'data/w33_pass2565_abstract_schlaefli_incidence.json',
'data/w33_pass2566_mod3_signature_quotient.json']
def dig(d):
 x=dict(d);x.pop('sha256_without_hash_field',None);return hashlib.sha256(json.dumps(x,sort_keys=True,separators=(',',':')).encode()).hexdigest()
def main():
 D=[];hs=[];checks=0
 for f in FILES:
  d=json.loads((ROOT/f).read_text());h=dig(d);assert h==d['sha256_without_hash_field'];assert all(d['checks'].values());D.append(d);hs.append(h);checks+=1+len(d['checks'])
 agg=hashlib.sha256(json.dumps(hs,separators=(',',':')).encode()).hexdigest()
 a,b,c,e,f,g,h=D
 assert a['orbit_classification']['certified_singleton_lower_bound']==13633920
 assert b['chromatic']['proved_lower_bound']==10 and b['chromatic']['explicit_upper_bound']==11
 assert c['exact_submodule_assignment']['135']=='60+15+30+30'
 assert e['full_group_covariant_dimensions']['7']==1 and e['full_group_covariant_dimensions']['3']==0
 assert [x['signatures'] for x in f['shells']]==[45,270,135,270]
 assert g['line_graph']['parameters']==[27,10,1,5]
 assert h['rank_H_mod3']==44
 checks+=7
 print(json.dumps({'status':'PASS','checks':checks,'aggregate_sha256':agg},sort_keys=True));return agg
if __name__=='__main__':main()
