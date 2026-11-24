#!/usr/bin/env python3
"""Pass5151: second-moment/curvature inequality for theta-even apartment supports."""
from __future__ import annotations
import itertools,json
from collections import Counter
from pathlib import Path
from analysis.w33_pass5074_gauge_active_chart_tester import build_W,chamber_stars
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_W33_PASS5151_THETA_CURVATURE_SECOND_MOMENT.json'

def checks(G):
    q=G['q'];o=set()
    for _,loc in G['charts']:
        for i,j,k in itertools.combinations(range(q+1),3):o.add(tuple(sorted((loc[(i,j)],loc[(i,k)],loc[(j,k)]))))
    return sorted(o)

def adj(G,C):
    A=[0]*len(G['apartments'])
    for T in C:
        for a,b in itertools.combinations(T,2):A[a]|=1<<b;A[b]|=1<<a
    return A

def basis(rows):
    piv={};out=[]
    for r0 in rows:
        r=r0
        while r:
            p=r.bit_length()-1
            if p in piv:r^=piv[p]
            else:piv[p]=r;out.append(r);break
    return out

def star_anchor(q):
    G=build_W(q);C=checks(G);A=adj(G,C);z=chamber_stars(G)[0];S={i for i in range(len(A)) if (z>>i)&1};k=4*(q-1)
    H=Counter((A[v]&z).bit_count() for v in range(len(A)) if v not in S)
    moment=sum((A[v]&z).bit_count()**2 for v in range(len(A)))
    assert moment==k*(k+2)*len(S);assert {x for x,c in H.items() if x and c}=={2}
    return {'q':q,'weight':len(S),'k':k,'second_moment':moment,'moment_per_selected':moment//len(S),
            'outside_neighbor_hist':{str(x):c for x,c in sorted(H.items()) if c}}

def q2_exhaustive():
    G=build_W(2);C=checks(G);A=adj(G,C);B=basis(chamber_stars(G));assert len(B)==16;k=4
    z=0;eq=0;minpos=None;eqw=Counter();joint=Counter()
    for i in range(1,1<<16):
        g=i^(i>>1);h=(i-1)^((i-1)>>1);z^=B[(g^h).bit_length()-1];w=z.bit_count()
        moment=sum((A[v]&z).bit_count()**2 for v in range(len(A)));d=moment-k*(k+2)*w
        assert d>=0 and d%8==0;joint[(w,d)]+=1
        if d==0:eq+=1;eqw[w]+=1
        elif minpos is None or d<minpos:minpos=d
    assert eq==45 and eqw==Counter({16:45}) and minpos==64
    return {'dimension':16,'nonzero_words':65535,'curvature_zero_words':45,'curvature_zero_weight':16,'minimum_positive_defect':64,'joint_classes':len(joint)}

def main():
    out={'pass':5151,'status':'THEOREM_THETA_SECOND_MOMENT_CURVATURE',
         'theorem':'Let k=4(q-1), A be theta adjacency, x=1_S for a nonzero codeword. Then x^T A^2 x >= k(k+2)|S|.',
         'proof':'Selected vertices have exactly k selected neighbors. For an unselected vertex, theta parity makes its selected-neighbor count t even. Since sum_out t=k|S| and t^2>=2t for even t>=0, the inequality follows.',
         'defect':'Delta=x^T A^2 x-k(k+2)|S|=sum_out t(t-2) lies in 8 Z_{>=0}. Equality iff every exterior boundary vertex has exactly two selected neighbors.',
         'star_anchors':{str(q):star_anchor(q) for q in (2,3,4,5)},
         'q2_exhaustive':q2_exhaustive(),
         'boundary':'At q=2 curvature equality classifies the complete minimum shell. For larger q, equality classification beyond known chamber stars is not claimed.'}
    OUT.write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
if __name__=='__main__':main()
