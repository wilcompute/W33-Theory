from __future__ import annotations
import hashlib,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def load(name):return json.loads((ROOT/'data'/name).read_text(encoding="utf-8"))
def test_cover_augmentation_lower_bound_and_frontier():
 d=load('PART_BT3250_BT3251_COVER_AUGMENTATION_results.json');s=d['summary']
 assert s['processed_orbit_species']==10
 assert s['discovered_orbit_species']==42
 assert s['certified_distinct_exact_covers']==486000
 assert s['unprocessed_frontier_species']==32
 assert s['orbit_size_histogram']=={'6480':9,'12960':33}
 assert all(r['switch_loci']==5 and r['switch_degree']==10 for r in d['orbit_species'] if r['processed'])
def test_s3_decoder_and_fourier_shadow():
 d=load('PART_BT3252_BT3253_S3_DECODER_results.json')
 assert d['minimum_nontrivial_flat_support_weight']==2
 assert d['weight_two_flat_nongauge_assignments']==3600
 assert d['blind_guaranteed_correction_radius']==0
 assert d['character_table']['standard']==[2,0,-1]
 assert d['conjugacy_class_sizes']=={'identity':1,'three_cycle':2,'transposition':3}
def test_exact_wedderburn_compiler():
 d=load('PART_BT3254_BT3255_PORT_WEDDERBURN_results.json')
 assert d['algebra_dimension']==26 and d['center_dimension']==8
 assert d['rational_wedderburn']=='Q^6 + M2(Q) + M4(Q)'
 assert sorted(x['algebra_block_dimension'] for x in d['representation_blocks'])==[1,1,1,1,1,1,4,16]
 assert d['symmetric_psd_compiler']['symmetric_block_coordinates']==19
def test_cube_spiral_and_packet_hash():
 c=load('PART_BT3256_ADAPTIVE_CHROMATIC_CUBE_results.json');s=load('PART_BT3258_BT3259_MODULAR_SPIRAL_TOWER_results.json');p=load('PART_BT3250_BT3261_COVER_DECODER_WEDDERBURN_results.json')
 assert c['pairwise_frame_disjoint_split_edges']==list(range(8))
 assert [x['leaves'] for x in c['adaptive_levels']]==[100,1000,10000,100000,1000000,10000000]
 first={x['prime']:x for x in s['prime_table']}
 assert [(q,first[q]['rotation_order'],first[q]['even_rotation_reflection_order']) for q in (2,3,5,7)]==[(2,6,6),(3,8,8),(5,10,10),(7,16,16)]
 body=dict(p);claim=body.pop('sha256_without_hash_field')
 assert hashlib.sha256(json.dumps(body,sort_keys=True,separators=(',',':')).encode()).hexdigest()==claim
 assert all(p['checks'].values())
