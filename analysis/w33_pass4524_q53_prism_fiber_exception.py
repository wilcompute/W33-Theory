#!/usr/bin/env python3
"""Pass 4524 -- Q(5,3) prism lift and the failure of the W33 nine-sheet law.

For Q(5,3)=GQ(3,9), every noncollinear point pair x,y has t+1=10 common
neighbors. Choosing three produces the three rectangular apartment faces of a
triangular prism on the six lines xz_i,yz_i.  There are
4536*C(10,3)=544320 such prisms.

Project the six-line indicator b through the line-intersection adjacency A_*.
Unlike W33, the map is injective on all 544,320 prisms and every image has
ambient weight 104.

The reason is structural. The XOR of all ten rung pairs is the union of the
complete line-stars at x and y and lies in ker(A_*) over F2. Hence a chosen
3-rung prism has the same image as its complementary 7-rung fan.  In W33 t=3,
there are only four rungs, so the complement of three is one rung and the map
collapses nine prisms onto a line-graph edge. For t=9 the complement has seven
rungs and no such edge collapse occurs.
"""
from __future__ import annotations
import itertools,json
from collections import Counter
from pathlib import Path
import numpy as np

from w33_pass4448_4450_q53_floquet_tanner import build_q53

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data'/'PART_W33_PASS4524_Q53_PRISM_FIBER_EXCEPTION.json'


def main()->int:
    pts,lines=build_q53(); P,L=len(pts),len(lines)
    assert (P,L)==(112,280)
    N=np.zeros((P,L),dtype=np.uint8)
    pair_line={}
    for j,line in enumerate(lines):
        N[list(line),j]=1
        for a,b in itertools.combinations(sorted(line),2):pair_line[(a,b)]=j
    Astar=(N.T@N)%2; np.fill_diagonal(Astar,0)
    Ap=np.zeros((P,P),dtype=np.uint8)
    for line in lines:
        for a,b in itertools.combinations(line,2):Ap[a,b]=Ap[b,a]=1
    colmask=[]
    for j in range(L):
        m=0
        for i in np.flatnonzero(Astar[:,j]):m|=1<<int(i)
        colmask.append(m)
    def apply_A(mask:int)->int:
        y=0;x=int(mask)
        while x:
            b=x&-x;i=b.bit_length()-1;y^=colmask[i];x-=b
        return y

    noncol=[(x,y) for x,y in itertools.combinations(range(P),2) if not Ap[x,y]]
    assert len(noncol)==4536
    images=Counter(); image_weights=Counter(); fan_kernel=0; complement_checks=0
    for x,y in noncol:
        common=np.flatnonzero(Ap[x]&Ap[y]).tolist(); assert len(common)==10
        rungs=[]
        for z in common:
            lx=pair_line[tuple(sorted((x,z)))];ly=pair_line[tuple(sorted((y,z)))]
            rungs.append((1<<lx)|(1<<ly))
        fan=0
        for r in rungs:fan^=r
        assert apply_A(fan)==0; fan_kernel+=1
        for comb in itertools.combinations(range(10),3):
            b=rungs[comb[0]]^rungs[comb[1]]^rungs[comb[2]]
            img=apply_A(b)
            images[img]+=1;image_weights[img.bit_count()]+=1
            comp=fan^b
            assert comp.bit_count()==14 and apply_A(comp)==img
            complement_checks+=1
    assert fan_kernel==4536
    assert complement_checks==544320
    assert len(images)==544320 and set(images.values())=={1}
    assert image_weights==Counter({104:544320})
    out={
      'pass':4524,
      'geometry':{'points':112,'lines':280,'noncollinear_point_pairs':4536,'common_neighbors_per_pair':10},
      'prisms':{'count':544320,'formula':'4536*C(10,3)','rungs_chosen':3},
      'protected_map':{'map':'b -> A_* b','distinct_images':544320,'injective':True,'image_weight':104},
      'fan_kernel':{'full_rungs':10,'verified_pairs':4536,'identity':'A_*(xor of all 10 rung pairs)=0'},
      'complement_duality':{'three_rungs':'same image as complementary seven rungs','verified_prisms':544320},
      'W33_comparison':{'t':3,'rungs':4,'three_rung_complement':1,'consequence':'nine-sheet collapse to the omitted-rung line-graph edge'},
      'Q53_comparison':{'t':9,'rungs':10,'three_rung_complement':7,'consequence':'no edge collapse; prism map is injective'},
      'boundary':'Exact finite-geometry negative/generalization result. The W33 9-sheet edge fiber is not extrapolated to Q(5,3).'}
    OUT.parent.mkdir(exist_ok=True)
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n',encoding='utf-8')
    print(json.dumps(out,indent=2,sort_keys=True));return 0

if __name__=='__main__': raise SystemExit(main())
