import hashlib,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def digest(d):
 z=dict(d);z.pop('sha256_without_hash_field',None);return hashlib.sha256(json.dumps(z,sort_keys=True,separators=(',',':')).encode()).hexdigest()
def load(name):
 d=json.loads((ROOT/'data'/name).read_text(encoding="utf-8"));assert digest(d)==d['sha256_without_hash_field'];return d
def test_five_frontier_certificates():
 a=load('w33_pass2430_labelled_tomotope_group_obstruction.json');b=load('w33_pass2431_u6_singleton_identifiability.json');c=load('w33_pass2432_signature_pair_obstruction.json');d=load('w33_pass2433_exact_commutative_fusion_lattice.json');e=load('w33_pass2434_c5_split_hom.json')
 assert a['comparison']['wd4plus_matches']==0
 assert b['exact_second_moment_sum_m2_n_m']==3697497150640
 assert c['exact_pair_test']['disjoint_pairs']==0
 assert d['finest_commutative_fusion']['rank']==9
 assert e['restriction']['Hom_C5_E8_to_coexact90_dimension']==144
def test_publication_hooks_and_boundaries():
 for f in ('w33_paper.tex','photonic_holonet.tex'):
  assert 'analysis/BT2435_five_frontiers_insert' in (ROOT/f).read_text(encoding="utf-8")
 release=(ROOT/'PASS2430_2435_FIVE_FRONTIERS_RELEASE.md').read_text(encoding="utf-8")
 assert 'GLOBAL_U6_SINGLETON_UNION_BOUNDARY' in release
 assert 'chi(H)=9` remains open' in release
