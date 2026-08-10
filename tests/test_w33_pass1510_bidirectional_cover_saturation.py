import hashlib,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
P=ROOT/'data'/'w33_pass1510_bidirectional_cover_saturation.json'
def cert():return json.loads(P.read_text(encoding="utf-8"))
def test_frozen_certificate_passes():
 p=cert();assert p['status']=='PASS';assert all(p['checks'].values());assert len(p['checks'])==13
def test_objectwise_saturation_frontier():
 p=cert();u=p['union'];assert u['raw_overlap']==0;assert u['union_size']==u['union_marked']==200000;assert u['distinct_full_orbits']==327;assert u['certified_cover_lower_bound']==3547800;assert u['stabilizer_order_histogram']=={'2':228,'4':84,'8':15}
def test_sampler_bias_numbers():
 h=cert()['hit_profile'];assert h['equal_orbit_hit_counts']==7;assert h['l1_redistribution']==10244;assert h['squared_redistribution']==463520;assert h['max_orbit_hit_difference']==98;assert h['pearson_components']=={'numerator':964601357,'forward_variance_factor':994717730,'reverse_variance_factor':1086056024}
def test_binary_and_canonical_hashes():
 p=cert();assert p['forward']['binary_sha256']=='ee6a429279fece6c4cd917acf2a07fdec2e9f8b66ebe9f7aa0db328ee6ed0172';assert p['reverse']['binary_sha256']=='e28c3c6c7d5869f93b04c3fc34320f60e65383f82cb3c2484978f46e73bfca5d';assert p['hit_profile']['canonical_orbit_representatives_sha256']=='223be23d50147437acfa18cc8f4cea43083c6b87066fe6e26812d0de50c8abb4'
def test_source_hashes():
 for name,digest in cert()['source_sha256'].items():assert hashlib.sha256((ROOT/name).read_bytes()).hexdigest()==digest
