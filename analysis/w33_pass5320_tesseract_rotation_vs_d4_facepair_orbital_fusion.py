#!/usr/bin/env python3
"""Pass5320: distinguish the two order-192 tesseract covers on the same 12 face pairs.

Pass5310 proves that the orientation-preserving tesseract group R and W(D4)=D
are nonisomorphic order-192 subgroups of B4, although R/Z and D/Z are abstractly
isomorphic order-96 groups.  Pass5319 identifies the natural D/Z action on the
12 antipodal square-face pairs with the published tomotope action.

Here both groups are placed on those SAME 12 objects.  Their permutation
representations differ sharply:

  D/Z (tomotope): orbital rank 5 = diagonal + 3 perfect matchings + residual;
  R/Z           : orbital rank 4 = diagonal + 1 perfect matching + one 2-factor + residual.

The 2-factor is exactly the fusion of two D/tomotope matching orbitals.  Thus the
uncolored 3K4 skeleton is common, but the tomotope keeps all three matching
colors while the rotational action fuses two of them.
"""
from __future__ import annotations
import itertools,json
from collections import Counter
from pathlib import Path

from analysis.w33_pass5310_tesseract_rotation_d4_tomotope_doublecovers import signed_groups
from analysis.w33_pass5319_d4_tesseract_facepairs_tomotope_action import build_face_pairs,induced

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_W33_PASS5320_TESSERACT_ROTATION_VS_D4_FACEPAIR_ORBITAL_FUSION.json'

def orbitals(G,n=12):
    els=list(G.generate_schreier_sims());rem=set(itertools.product(range(n),repeat=2));O=[]
    while rem:
        p=next(iter(rem));orb={(g(p[0]),g(p[1])) for g in els};O.append(orb);rem-=orb
    return sorted(O,key=len)

def cycle_type(g,n=12):
    seen=set();L=[]
    for i in range(n):
        if i in seen:continue
        j=i;l=0
        while j not in seen:
            seen.add(j);l+=1;j=g(j)
        L.append(l)
    return tuple(sorted(L))

def hist(G):return Counter(cycle_type(g) for g in G.generate_schreier_sims())

def small_graph_components(orbs,n=12):
    # all non-diagonal orbitals except the degree-8 residual of size96
    E=set()
    for O in orbs:
        if len(O)>=96 or all(a==b for a,b in O):continue
        E|={tuple(sorted((a,b))) for a,b in O if a!=b}
    nbr=[set() for _ in range(n)]
    for a,b in E:nbr[a].add(b);nbr[b].add(a)
    comps=[];seen=set()
    for i in range(n):
        if i in seen:continue
        C={i};Q=[i];seen.add(i)
        while Q:
            x=Q.pop()
            for y in nbr[x]:
                if y not in seen:seen.add(y);C.add(y);Q.append(y)
        comps.append(sorted(C))
    return sorted(comps),sorted(len(nbr[i]) for i in range(n)),len(E)

def orbital_profile(orbs):
    out=[]
    for O in orbs:
        if all(a==b for a,b in O):out.append({'size':len(O),'relation':'diagonal','degree':1});continue
        deg=len({b for a,b in O if a==0})
        if len(O)==12:kind='perfect_matching'
        elif len(O)==24:kind='2_factor'
        elif len(O)==96:kind='residual_degree8'
        else:kind='other'
        out.append({'size':len(O),'relation':kind,'degree':deg})
    return out

def main():
    V,vi,B,R,D=signed_groups();faces,pairs,_=build_face_pairs(V,vi)
    R12=induced(R,faces,pairs);D12=induced(D,faces,pairs)
    assert R12.order()==D12.order()==96
    OR=orbitals(R12);OD=orbitals(D12)
    assert [len(x) for x in OD]==[12,12,12,12,96]
    assert [len(x) for x in OR]==[12,12,24,96]

    cD,degD,eD=small_graph_components(OD);cR,degR,eR=small_graph_components(OR)
    assert cD==cR==[[0,1,10,11],[2,3,8,9],[4,5,6,7]]
    assert degD==degR==[3]*12 and eD==eR==18

    hD=hist(D12);hR=hist(R12);assert hD!=hR
    # D/tomotope keeps three global 1-factors; R keeps one and fuses the other two.
    assert sum(1 for x in orbital_profile(OD) if x['relation']=='perfect_matching')==3
    assert sum(1 for x in orbital_profile(OR) if x['relation']=='perfect_matching')==1
    assert sum(1 for x in orbital_profile(OR) if x['relation']=='2_factor')==1

    out={'pass':5320,'status':'THEOREM_ROTATION96_IS_ORBITAL_FUSION_OF_D4_TOMOTOPE_FACEPAIR_SCHEME',
      'same_12_objects':'antipodal pairs of the 24 tesseract square faces',
      'abstract_group_orders':{'R_over_center':96,'WD4_over_center':96},
      'WD4_tomotope_action':{'orbital_rank':len(OD),'orbitals':orbital_profile(OD),
        'cycle_type_histogram':{str(k):v for k,v in sorted(hD.items())}},
      'rotation_action':{'orbital_rank':len(OR),'orbitals':orbital_profile(OR),
        'cycle_type_histogram':{str(k):v for k,v in sorted(hR.items())}},
      'common_uncolored_small_relation':{'graph':'3 K4','components':cD,'edges':18,'degree':3},
      'fusion':'The rotational action preserves one of the three tomotope perfect-matching orbitals and fuses the other two into a degree-2 relation (three C4 cycles).',
      'nonconjugacy_certificate':'Orbital ranks differ: tomotope/D4 rank5 versus rotation rank4; therefore the two degree-12 permutation representations are not conjugate.',
      'boundary':'R/Z and D/Z are abstractly isomorphic order96 groups, but this theorem distinguishes their natural square-face-pair permutation representations.'}
    OUT.write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
if __name__=='__main__':main()
