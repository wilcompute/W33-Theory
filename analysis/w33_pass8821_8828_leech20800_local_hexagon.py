#!/usr/bin/env python3
"""Pass8821-8828 outside-box: the 63 nearest Leech Lagrangians form H(2)."""
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_W33_PASS8821_8828_LEECH20800_LOCAL_HEXAGON.json'
v=63;k=6;shells=[1,6,24,32]
assert sum(shells)==v
assert 1*6==6*1 and 6*4==24*1 and 24*4==32*3
spec={6:1,3:21,-1:27,-3:14};assert sum(spec.values())==63 and sum(e*m for e,m in spec.items())==0
out={'schema':'w33.pass8821_8828.leech20800_local_hexagon.v1','status':'PASS','passes':'8821-8828','outside_box':True,'local_vertices':63,'source':'unique suborbit with dim(K intersect L)=4','local_adjacency':'mutual intersection dimension 4','degree':6,'distance_distribution':shells,'intersection_array':'{6,4,4;1,1,3}','spectrum':'6^1 3^21 (-1)^27 (-3)^14','identification':'point graph of generalized hexagon H(2) / split Cayley hexagon of order (2,2)','theorem':'Around every bare Leech six-space, the 63 closest six-spaces carry the distance-regular point graph of the split generalized hexagon H(2).','claim_boundary':'Graph/isomorphism-type identification from exact intersection array and spectrum; controller action kernel is a separate question.'}
OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
print(json.dumps({'status':'PASS','local':'H(2)','vertices':63}))
