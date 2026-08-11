#!/usr/bin/env python3
"""Pass4943 — explicit common-S6 crosswalk between two previously distinct carriers.

Pass4869: after marking one double-six, the 35-vertex residue is the 15 duads
plus 20 triads of six columns, with symmetry S6 x C2 (triad complement).
Pass1848: the 15 duads map to the 15 synthemes through the exceptional outer
automorphism of S6.  This pass puts both constructions on the same literal
six-label set and proves exactly what is shared and what cannot be extended.
"""
from __future__ import annotations
import itertools,json
from collections import deque
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
INP=ROOT/'data/w33_pass1848_duad_syntheme_transfer.json'
OUT=ROOT/'data/PART_W33_PASS4943_COMMON_S6_CARRIER_CROSSWALK.json'

def comp(p,q):return tuple(p[q[i]] for i in range(len(q)))
def closure(gens,n):
    I=tuple(range(n));S={I};D=deque([I])
    while D:
        a=D.popleft()
        for g in gens:
            z=comp(g,a)
            if z not in S:S.add(z);D.append(z)
    return S

def center(G):
    return [a for a in G if all(comp(a,b)==comp(b,a) for b in G)]

def main()->int:
    prior=json.loads(INP.read_text());assert prior['status']=='PASS'
    duads=list(itertools.combinations(range(6),2));triads=list(itertools.combinations(range(6),3))
    synthemes=[]
    for m in itertools.permutations(range(6)):
        S=tuple(sorted(tuple(sorted(x)) for x in ((m[0],m[1]),(m[2],m[3]),(m[4],m[5]))))
        if S not in synthemes:synthemes.append(S)
    synthemes=sorted(synthemes);assert len(synthemes)==15
    di={d:i for i,d in enumerate(duads)};ti={t:i for i,t in enumerate(triads)};si={s:i for i,s in enumerate(synthemes)}
    labels35=[('d',d) for d in duads]+[('t',t) for t in triads];li35={x:i for i,x in enumerate(labels35)}
    labels30=[('d',d) for d in duads]+[('s',s) for s in synthemes];li30={x:i for i,x in enumerate(labels30)}
    def act_subset(S,p):return tuple(sorted(p[i] for i in S))
    def act_synth(S,p):return tuple(sorted(tuple(sorted((p[a],p[b]))) for a,b in S))
    # Adjacent transpositions generate the same literal inner S6 on both carriers.
    s6gens=[]
    for k in range(5):
        p=list(range(6));p[k],p[k+1]=p[k+1],p[k];p=tuple(p);s6gens.append(p)
    inner35=[];inner30=[]
    for p in s6gens:
        inner35.append(tuple(li35[(typ,act_subset(S,p))] for typ,S in labels35))
        inner30.append(tuple(li30[(typ,act_subset(S,p) if typ=='d' else act_synth(S,p))] for typ,S in labels30))
    G35inner=closure(inner35,35);G30inner=closure(inner30,30);assert len(G35inner)==len(G30inner)==720
    # The marked-residue extra involution fixes every duad and complements every triad.
    c35=tuple(li35[(typ,S if typ=='d' else tuple(i for i in range(6) if i not in S))] for typ,S in labels35)
    Gcentral=closure(inner35+[c35],35);assert len(Gcentral)==1440 and len(center(Gcentral))==2
    # Pass1848's exact duad->syntheme table defines the exceptional swap on 30 objects.
    d2s={}
    for key,val in prior['duad_to_syntheme_outer_map'].items():
        d=tuple(map(int,key));s=tuple(sorted(tuple(x) for x in val));assert d in di and s in si;d2s[d]=s
    assert len(d2s)==15 and len(set(d2s.values()))==15
    s2d={s:d for d,s in d2s.items()}
    tau=[]
    for typ,S in labels30:
        tau.append(li30[('s',d2s[S])] if typ=='d' else li30[('d',s2d[S])])
    tau=tuple(tau);assert comp(tau,tau)==tuple(range(30))
    Gouter=closure(inner30+[tau],30);assert len(Gouter)==1440 and len(center(Gouter))==1
    # Literal common core: all six-label S6 elements induce the same permutation on the first 15 duad coordinates.
    for a,b in zip(inner35,inner30):assert a[:15]==b[:15]
    assert c35[:15]==tuple(range(15))
    assert any(tau[i]>=15 for i in range(15))
    out={
      'pass':4943,
      'common_core':{'group':'S6','order':720,'coordinate_set':'the same six labels 0..5',
        'shared_duad_carrier':'15 two-subsets; adjacent-transposition generators agree coordinate-for-coordinate',
        'marked_residue_extra_orbit':'20 three-subsets (triads)'},
      'marked_double_six_extension':{'group':'S6 x C2','order':1440,'center_order':2,
        'extra_involution':'fixes all 15 duads and complements every 3-subset triad'},
      'duad_syntheme_extension':{'group':'Aut(S6)=S6:2','order':1440,'center_order':1,
        'outer_involution':'Pass1848 exact bijection swaps the 15 duads with the 15 synthemes'},
      'crosswalk':{'inner_S6_intertwiner':'identity on the six labels, hence identity on the 15 duads',
        'extends_to_order1440_groups':False,
        'obstruction':'the marked-residue involution centralizes S6 and fixes the duad orbit; the exceptional involution is noncentral and swaps duads with synthemes'},
      'theorem':'The Pass4869 marked-double-six shell and the Pass1848 duad-syntheme construction have a literal common S6 core, not merely an equal-order resemblance: after using the same six column labels, their S6 generators agree exactly on all 15 duads. The extensions diverge at the extra involution. One is the central triad-complement extension S6 x C2 on 15+20 objects; the other is the exceptional outer extension Aut(S6) on 15 duads plus 15 synthemes. Therefore the common S6 carrier is explicit, but no crosswalk fixing that carrier can identify the two order-1440 groups.',
      'boundary':'Finite marked-coordinate crosswalk. Choosing the marked double-six and an ordering of its six opposite columns is extra coordinate data.'}
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n');print(json.dumps(out,indent=2,sort_keys=True));return 0
if __name__=='__main__':raise SystemExit(main())
