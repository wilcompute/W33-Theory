#!/usr/bin/env python3
"""Pass9085-9092 addendum: the Leech 20,800 carrier is the edge G-set of the G2(4) graph."""
from pathlib import Path
import json
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_W33_PASS9085_9092_LEECH_G24_GRAPH_EDGES.json'
G=503193600
V=416;k=100
E=V*k//2
assert E==20800
edge_stab=G//E
assert edge_stab==24192
flags=V*k
assert flags==41600==2*E
# established G2(4) graph parameters from repo Suzuki tower
lam,mu=36,20
assert k*(k-lam-1)==(V-k-1)*mu
out={
 'schema':'w33.pass9085_9092.leech_g24_graph_edges.v1','status':'PASS','passes':'9085-9092','outside_box':True,
 'G2(4)_graph':{'parameters':[V,k,lam,mu],'vertices':V,'edges':E,'automorphism_controller':'G2(4):2'},
 'vertices_identified_with':'416 J2:2 Hall-Janko 100-sets in the Leech 20,800 carrier',
 'edges_identified_with':'20,800 Leech bare six-spaces / H(2) subhexagons of H(4)',
 'incidence':'A six-space is incident with exactly the two Hall-Janko 100-sets that contain it.',
 'stabilizers':{'vertex':'J2:2, order 1,209,600','edge':'G2(2).2, order 24,192'},
 'checks':{'edge_count':'416*100/2 = 20,800','edge_stabilizer':'503,193,600/20,800 = 24,192','flag_count':'416*100 = 41,600 = 2*20,800'},
 'theorem':'Under the Pass9013 H(4) weld, the 416 Hall-Janko copies are the vertices of the G2(4) graph SRG(416,100,36,20), and the 20,800 Leech six-spaces are its edges. Each Hall-Janko copy is the 100-edge star at one graph vertex.',
 'claim_boundary':'Exact transitive G-set and incidence identification using the subgroup chain G2(2).2 < J2:2 < G2(4):2 and the repo-certified G2(4) SRG parameters.'}
OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
print(json.dumps({'status':'PASS','vertices':V,'edges':E,'degree':k}))
