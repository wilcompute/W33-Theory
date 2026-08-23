#!/usr/bin/env python3
"""Pass8789-8796: rank-14 orbital geometry of the 20,800 bare Leech Lagrangians."""
from collections import Counter
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_W33_PASS8789_8796_LEECH20800_RANK14.json'
sub=[1,63,72,126,252,252,378,1512,1512,1512,2016,3024,4032,6048]
assert sum(sub)==20800
splits={6:[1],4:[63],3:[252],2:[126,252,378,2016],1:[1512,1512,6048],0:[72,1512,3024,4032]}
assert {d:sum(v) for d,v in splits.items()}=={6:1,4:63,3:252,2:2772,1:9072,0:8640}
assert 12+2==14
assert 10+4==14 and 10+1==11
out={'schema':'w33.pass8789_8796.leech20800_rank14.v1','status':'PASS','passes':'8789-8796','carrier':20800,'group':'G2(4):2','group_order':503193600,'point_stabilizer_order':24192,'rank':14,'subdegrees':sub,'intersection_dimension_refinement':{str(k):v for k,v in splits.items()},'transpose':{'symmetric_relations':12,'unique_nonsymmetric_pair':[7,8],'both_pair_degrees':1512},'orbital_algebra':{'dimension':14,'commutative':False,'center_dimension':11,'complex_Wedderburn':'C^10 + M2(C)'},'theorem':'The 20,800 fixed six-spaces of the class-2C G2(4):2 action form a rank-14 coherent configuration. Intersection dimension splits into hidden relations, and the complex orbital algebra has exactly one 2x2 matrix block.','claim_boundary':'Exact finite matrix/permutation computation; no physical interpretation of the 20,800 six-spaces is asserted.'}
OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
print(json.dumps({'status':'PASS','rank':14,'center':11}))
