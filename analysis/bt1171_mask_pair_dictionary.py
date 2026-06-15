#!/usr/bin/env python3
import itertools, json
masks=list(range(1,16))
pairs=list(itertools.combinations(range(6),2))
lookup={str(m):list(p) for m,p in zip(masks,pairs)}
out={'bt':1171,'dictionary':lookup,'mask_count':len(masks),'pair_count':len(pairs),'status':'fixed lexicographic dictionary after labels are chosen','all_checks_pass':len(masks)==len(pairs)==15 and lookup['1']==[0,1] and lookup['15']==[4,5]}
print(json.dumps(out,indent=2,sort_keys=True))
