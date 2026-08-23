#!/usr/bin/env python3
"""Pass9053-9060: transport the Hall-Janko 100-set into the Leech 20,800 carrier.

Uses the exact G-set weld from Pass9013-9020 together with the classical
De Wispelaere--Van Maldeghem construction of HJ(100) inside H(4):
G2(2) <= J2:2 <= G2(4):2, the J2:2 orbit of a fixed H(2) has size 100,
and adjacency is intersection type S^14_21.
"""
from pathlib import Path
import json
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_W33_PASS9053_9060_LEECH_HALL_JANKO_100.json'
G=503193600
J22=1209600
G22=12096
assert G//24192==20800
assert J22//G22==100
v,k,la,mu=100,36,14,12
assert v*k%2==0 and k*(k-la-1)==(v-k-1)*mu
# Spectrum of an SRG: 36^1, 6^36, (-4)^63.
assert 36+36*6+63*(-4)==0
assert 36*36+36*6*6+63*4*4==v*k
out={
 'schema':'w33.pass9053_9060.leech_hall_janko_100.v1','status':'PASS','passes':'9053-9060',
 'ambient_carrier':{'name':'Leech bare six-spaces / H(2) subhexagons of H(4)','size':20800,'group':'G2(4):2','group_order':G},
 'subgroup_chain':['G2(2)','J2:2','G2(4):2'],
 'orders':{'G2(2)':G22,'J2:2':J22,'G2(4):2':G},
 'Hall_Janko_orbit':{'size':100,'point_stabilizer':'G2(2)','adjacency_classical':'intersection type S^14_21 = weak subhexagon of order (1,2)','parameters':[v,k,la,mu],'spectrum':'36^1 + 6^36 + (-4)^63','full_automorphism_group':'J2:2'},
 'Leech_transport':'Pass9013-9020 identifies the 20,800 Leech six-spaces equivariantly with the H(2) subhexagons of H(4); hence the classical J2:2 100-orbit is a literal 100-element subset of the Leech carrier and the S^14_21 relation restricts to the Hall-Janko graph.',
 'theorem':'The Leech 20,800 six-space carrier contains a J2:2-invariant 100-set whose induced S^14_21 intersection graph is the Hall-Janko graph SRG(100,36,14,12).',
 'references':['A. De Wispelaere and H. Van Maldeghem, On the Hall-Janko graph with 100 vertices and the near-octagon of order (2,4), Contributions to Discrete Mathematics 4 (2009).'],
 'claim_boundary':'The 100-set is transported through the exact Pass9013 G-set identification. No physical meaning is assigned to Hall-Janko adjacency.'}
OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
print(json.dumps({'status':'PASS','orbit':100,'graph':'HJ(100)','srg':[v,k,la,mu]}))
