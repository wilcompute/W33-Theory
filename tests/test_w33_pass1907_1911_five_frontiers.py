import hashlib,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];DATA=ROOT/'data'
def load(n,s):return json.loads((DATA/f'w33_pass{n}_{s}.json').read_text(encoding="utf-8"))
def chash(d):x=dict(d);x.pop('sha256_without_hash_field',None);return hashlib.sha256(json.dumps(x,sort_keys=True,separators=(',',':')).encode()).hexdigest()
def test_canonical_hashes_and_statuses():
 files={1907:'u6_exact_shard_and_resource',1908:'complete_mixed_trivariate_certificate_v2',1909:'complete_s6_subgroup_phase_poset_certificate',1910:'gaussian_lines_sigma_phase_cuts',1911:'stabilizer_weighted_primitive_holonomy'}
 for n,s in files.items():
  d=load(n,s);assert chash(d)==d['sha256_without_hash_field'];assert d['status'].startswith('PASS')
def test_critical_theorems():
 a=load(1907,'u6_exact_shard_and_resource');assert a['completed_exact_pilot_shard']['nonlower_singletons_within_shard']==1349896
 b=load(1908,'complete_mixed_trivariate_certificate_v2');assert b['words']==2**45 and b['nonzero_bins']==7355 and b['complement_subcode']['structure']=='C2 x C2'
 c=load(1909,'complete_s6_subgroup_phase_poset_certificate');assert c['subgroup_class_count']==56 and c['counts']=={'j114':12,'j24':26,'j90':22,'pairedV9':56};assert c['j_reconciliation']['quaternionic'] is False
 d=load(1910,'gaussian_lines_sigma_phase_cuts');assert d['spread_K10_audit']['upper_13_proved'] is False and d['checks']['false_bound_excluded']
 e=load(1911,'stabilizer_weighted_primitive_holonomy');assert sum(e['v9_shared_channel']['sector_dimensions'])==36 and sum(e['hashimoto_complement']['sector_dimensions'])==54
