from __future__ import annotations
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
RESULT=ROOT/'data/PART_4019_4024_PHOTONIC_FLAT_BAND_H1.json'
SHA='e7746ea1730daea1b29d0e7831bc627c4d115ee0ccf1c81441796363101aa59f'
def load():return json.loads(RESULT.read_text(encoding='utf-8'))
def test_certificate():
 x=load();assert x['status']=='PASS_EXACT_PHOTONIC_LINE_GRAPH_FLAT_BAND_H1';assert x['semantic_sha256']==SHA;assert all(x['checks'].values())
def test_flat_band_and_apartments():
 x=load();f=x['pass4020_h1_is_minus2_flat_band'];a=x['pass4021_apartment_compact_localized_states']
 assert f['flat_band_eigenvalue']==-2 and f['multiplicity']==81
 assert a['apartments']==1620 and a['support_per_state']==8 and a['span_rank']==81
def test_tight_frame_and_address_law():
 x=load();t=x['pass4022_apartment_unit_norm_tight_frame'];l=x['pass4023_local_address_law']
 assert t['frame_bound']==20 and t['redundancy']==20 and t['unit_vectors']==1620
 assert l['apartments_per_secondary_site']==81 and l['double_count']=='160*81=1620*8=12960'
def test_disorder_boundary():
 p=load()['pass4024_perturbation_boundary']
 assert '81/160' in p['single_site_onsite_perturbation']
 assert 'not generically immune' in p['honest_boundary']
