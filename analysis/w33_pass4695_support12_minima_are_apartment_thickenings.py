#!/usr/bin/env python3
"""Pass 4695 -- the 1620 support-12 minima are exactly corner-star thickenings of the 1620 W33 apartments.

For an apartment A (an induced C4 of four W33 lines), let its four corner points
be the consecutive line intersections.  Define T(A) to be all W33 lines through
those four corner points.  Since W33 has four lines through each point and each
selected apartment line contains two corners, T(A) has 4+4*2=12 lines.

Every one of the 1620 T(A) is distinct and its XOR of apartment-incidence rows
has weight 608.  Pass4693 proves there are exactly 1620 support-12 coefficient
sets of weight 608, so these are all minima.

The selected apartment is intrinsic to T(A).  T(A) contains 11 apartments.  One
has overlap profile with the other ten {2:8,0:2}; eight have
{2:4,1:4,0:2}; two have {2:4,0:6}.  Thus the original A is uniquely recovered
without coordinates, giving an exact PGSp-equivariant bijection between the
support-12 minimum shell and the apartment set.
"""
from __future__ import annotations
import itertools,json
from collections import Counter
from pathlib import Path
import numpy as np
from w33_pass4495_4502_distance_prism_reconstruction import geometry
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_W33_PASS4695_SUPPORT12_MINIMA_APARTMENT_THICKENINGS.json'

def thickening(ap,lines):
    ap=list(ap);corners=set()
    for i,j in itertools.combinations(ap,2):
        z=lines[i]&lines[j]
        if z:corners|=z
    assert len(corners)==4
    T=frozenset(i for i,L in enumerate(lines) if L&corners)
    assert len(T)==12
    return T,tuple(sorted(corners))
def row_masks(H):
    out=[]
    for i in range(40):
        m=0
        for j in np.flatnonzero(H[i]):m|=1<<int(j)
        out.append(m)
    return out
def xor_weight(T,rows):
    x=0
    for i in T:x^=rows[i]
    return x.bit_count()
def overlap_profile(A,contained):return dict(sorted(Counter(len(A&B) for B in contained if B!=A).items()))

def main()->int:
    pts,pidx,lines,Astar,apartments,apmasks,H=geometry();assert len(apartments)==1620
    rows=row_masks(H);Ts={};weights=Counter()
    for ap in apartments:
        T,c=thickening(ap,lines);assert T not in Ts;Ts[T]=(frozenset(ap),c);weights[xor_weight(T,rows)]+=1
    assert len(Ts)==1620 and weights==Counter({608:1620})
    old=json.loads((ROOT/'data/PART_W33_PASS4693_SUPPORT12_TRANSITIVITY_EXACT.json').read_text(encoding='utf-8'))
    assert old['minimum_weight']==608 and old['minimum_count']==1620
    repT=next(iter(Ts));repA,_=Ts[repT]
    contained=[frozenset(ap) for ap in apartments if set(ap)<=repT];assert len(contained)==11
    profiles=Counter(tuple(overlap_profile(A,contained).items()) for A in contained)
    expected=Counter({((0,2),(2,8)):1,((0,2),(1,4),(2,4)):8,((0,6),(2,4)):2})
    assert profiles==expected and overlap_profile(repA,contained)=={0:2,2:8}
    selected=[A for A in contained if overlap_profile(A,contained)=={0:2,2:8}];assert selected==[repA]
    deg=Counter(sum(int(Astar[i,j]) for j in repT) for i in repT);assert deg==Counter({4:8,6:4})
    out={'pass':4695,'objects':{'apartments':1620,'support12_minima':old['minimum_count'],'thickenings_distinct':len(Ts)},'corner_star_thickening':{'definition':'all W33 lines through the four corner points of an apartment','size':12,'extra_lines_per_corner':2,'apartment_code_weight':608,'all_1620_have_weight_608':True,'induced_line_graph_degree_census':{'4':8,'6':4}},'intrinsic_inverse':{'contained_apartments':11,'overlap_profile_multiplicities':{'{0:2,2:8}':1,'{0:2,1:4,2:4}':8,'{0:6,2:4}':2},'selected_apartment_profile':'{0:2,2:8}','unique':True},'theorem':'The exact support-12 minimum shell is precisely the 1620 corner-star thickenings T(A) of W33 apartments.  The original apartment is uniquely reconstructible from its 12-line minimum support, so the shell and apartment set are canonically PGSp-equivariantly bijective.','boundary':'Exact finite W33 code/building theorem.  The equality 1620 is used only after the explicit thickening map, weight-608 verification, exact minimum-shell count, and intrinsic inverse are certified.'}
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n');print(json.dumps(out,indent=2,sort_keys=True));return 0
if __name__=='__main__':raise SystemExit(main())
