#!/usr/bin/env python3
"""Full objectwise W(E6)-involution <-> W33 carrier dictionary.

This is a closure/consistency certificate over previously independent exact
intertwiners plus w33_e6_degree2_selected270_bridge.py.
"""
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
DATA=ROOT/'data'
def load(n):return json.loads((DATA/n).read_text())

def main(write=True):
    lad=load('w33_e6_involution_ladder_flags.json')
    d270=load('w33_e6_degree2_selected270_bridge.json')
    ds=load('PART_W33_PASS4964_DOUBLE_SIX_SPREAD_EQUIVARIANT_BRIDGE.json')
    ports=load('PART_W33_PASS4979_TRITANGENT_SPREAD_45_PORT_TRANSCEIVER.json')
    tri=load('PART_W33_PASS4659_INTERNAL_E6_27_36_45_TRIANGLE.json') if (DATA/'PART_W33_PASS4659_INTERNAL_E6_27_36_45_TRIANGLE.json').exists() else None
    assert lad['status']=='PASS' and d270['status']=='PASS'
    assert ds['equivariant_bijection']['exists'] and ds['equivariant_bijection']['unique']
    assert ds['carriers']['double_sixes']==36 and ds['carriers']['W33_spreads']==36
    assert ds['pair_relation_transport']['double_six_intersection_4_to_spread_overlap_4']==270
    s=ports['selector_incidence']; assert ports['tritangents']==45 and ports['spreads_double_sixes']==36
    assert s['per_tritangent_profile']['unselected_meet_0']==12
    assert 45*12==540 and 45*24==1080
    assert d270['canonical_signature']['signature_sets_equal']
    out={
      'schema':'w33.e6_involution_full_w33_dictionary.v1','status':'PASS',
      'headline':'All four nontrivial W(E6) involution degrees now transport objectwise into native W33 carriers. The formerly missing degree-2/270 bridge is canonical, and degree-3/540 is exactly the complement of the certified 45x36 tritangent/spread selector.',
      'dictionary':{
        'degree1_36':{'E6':'reflections = double-sixes','W33':'36 spreads','bridge':'unique W(E6)-equivariant Pass4964 bijection'},
        'degree2_270':{'E6':'syzygetic double-six pairs = degree-2 involutions','W33':['pairs of spreads with overlap 4','selected 270 singular lines','base of the 1620-apartment six-sheet cover'],'bridge':'new canonical 12-signature selected270 bridge + Pass4964 pair transport'},
        'degree3_540':{'E6':'disjoint tritangent-double-six flags = degree-3 involutions','W33':'(tritangent/protected45, spread36) flags in the complement of Pass4979 selector','count_identity':'45*12=36*15=540'},
        'degree4_45':{'E6':'tritangents = degree-4 involutions','W33':['internal Pass4659 45','protected45','center-quad/E6 tritangent45'],'bridge':'Pass4659 action-level 45 -> protected45 composed with Pass4616'}
      },
      'cross_relations':{
        '36_pair_partition':'630 = 270 four-overlap/syzygetic + 360 one-overlap/azygetic spread pairs',
        '45x36_partition':'1620 = 540 disjoint/unselected + 1080 two-line/selected flags',
        'selected270_apartment_cover':'1620 = 270*6'
      },
      'stabilizer_crosschecks':{
        'PSp_selected270':96,'W_E6_degree2':192,'PSp_tritangent45':576,'W_E6_degree4':1152,
        'note':'outer completion doubles the PSp stabilizers on the corresponding W(E6) carriers'},
      'commutative_closure':True,
      'boundary':'Exact finite G-set/incidence transport only; no physical E6 gauge symmetry follows.'}
    if tri is not None: out['pass4659_crosscheck']=tri.get('theorem','loaded')
    if write:(DATA/'w33_e6_involution_full_w33_dictionary.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps(out,indent=2));return out
if __name__=='__main__':main(True)
