#!/usr/bin/env python3
"""Pass5078: exhaustive local K_(q+1) cut/switching decoder."""
from itertools import combinations
from collections import Counter
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_W33_PASS5078_LOCAL_CUT_DECODER.json'

def solve(q):
    n=q+1; edges=list(combinations(range(n),2)); m=len(edges)
    cuts=[]
    for mask in range(1<<q):
        a=[0]+[(mask>>(i-1))&1 for i in range(1,n)]
        cuts.append(sum((a[i]^a[j])<<e for e,(i,j) in enumerate(edges)))
    tris=[(0,i,j) for i in range(1,n) for j in range(i+1,n)]
    edge_index={e:i for i,e in enumerate(edges)}
    def syn(word):
        s=0
        for k,(a,b,c) in enumerate(tris):
            ii=[edge_index[tuple(sorted(x))] for x in ((a,b),(a,c),(b,c))]
            if sum((word>>e)&1 for e in ii)&1:s|=1<<k
        return s
    leaders={}; ambient=Counter()
    for w in range(1<<m):
        d=min((w^c).bit_count() for c in cuts); ambient[d]+=1; s=syn(w)
        if s not in leaders or d<leaders[s][0]:leaders[s]=(d,w)
    assert len(leaders)==1<<(q*(q-1)//2)
    sh=Counter(d for d,_ in leaders.values())
    return {'q':q,'n_geodesics':n,'local_bits':m,'code_dimension':q,'codewords':len(cuts),
            'syndrome_rank':q*(q-1)//2,'distinct_syndromes':len(leaders),
            'covering_radius':max(sh),'syndrome_coset_leader_weight_hist':dict(sorted(sh.items())),
            'ambient_nearest_cut_distance_hist':dict(sorted(ambient.items())),
            'rom_entries':len(leaders),'rom_address_bits':q*(q-1)//2,'exact_reconstruction_bits':q}

def main():
    out={'pass':5078,'status':'PASS','decoder':'nearest K_(q+1) cut / switching decoder',
         'theorem':'An independent syndrome basis is the triangle set (0,i,j), rank q(q-1)/2.',
         'q':{str(q):solve(q) for q in range(2,6)},
         'hardware_boundary':'Exact local lookup counts only; no global decoder/noise threshold.'}
    OUT.write_text(json.dumps(out,indent=2)+'\n'); print(json.dumps(out,indent=2))
if __name__=='__main__':main()
