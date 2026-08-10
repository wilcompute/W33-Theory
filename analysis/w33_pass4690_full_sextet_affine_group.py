#!/usr/bin/env python3
"""Pass 4690 -- recover the full affine 2^6:3.S6 structure of the corrected Golay sextet stabilizer.

Pass4633 gives the exact sextet stabilizer H of order 138240, its action on six
tetrads, and the chosen-transversal stabilizer K of order 2160.  This pass works
inside that explicit 24-point permutation group.

The kernel M of the tetrad action has order 192 and element-order census
1^1 2^63 3^128.  Identity plus the 63 involutions form a normal elementary
abelian subgroup N=C2^6.  N acts regularly on the 64 sextet transversals.  Since
N intersects K trivially and |N||K|=|H|, H=N semidirect K.

K has tetrad image S6 and kernel C3.  The C3 acts fixed-point-freely on N\{0};
the K-conjugacy orbits on the 63 nonzero translations have sizes 18 and 45,
matching the two nonzero codeword shells of the Pass4637 affine C6 model.
"""
from __future__ import annotations
import json
from collections import Counter
from pathlib import Path
import w33_pass4633_m24_sextet_section_stabilizer as p

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_W33_PASS4690_FULL_SEXTET_AFFINE_GROUP.json'
I=bytes(range(24))

def order(g):
    x=I
    for n in range(1,25):
        x=p.comp(g,x)
        if x==I:return n
    raise AssertionError('unexpected order')
def conj(g,n):return p.comp(p.comp(g,n),p.inv(g))

def main()->int:
    d=p.build();H=d['H'];K=d['K'];Hgens=d['Hgens'];Z=d['Z'];tetrads=[frozenset(x) for x in d['sextet']]
    M={g for g in H if all(p.act_set(T,g)==T for T in tetrads)};assert len(M)==192
    census=Counter(order(g) for g in M);assert census==Counter({3:128,2:63,1:1})
    N={g for g in M if order(g)<=2};assert len(N)==64
    assert all(p.comp(a,a)==I for a in N)
    assert all(p.comp(a,b)==p.comp(b,a) and p.comp(a,b) in N for a in N for b in N)
    assert all(conj(g,n) in N for g in Hgens for n in N)
    orbN={p.act_set(Z,n) for n in N};assert len(orbN)==64 and sum(p.act_set(Z,n)==Z for n in N)==1
    assert len(K)==2160 and len(N&K)==1 and len(N)*len(K)==len(H)==138240
    trans=sorted(orbN,key=lambda S:tuple(sorted(S)));tidx={S:i for i,S in enumerate(trans)}
    sig=lambda g:tuple(tidx[p.act_set(S,g)] for S in trans)
    assert len({sig(g) for g in H})==138240 and len({sig(g) for g in K})==2160
    C3={g for g in K if all(p.act_set(T,g)==T for T in tetrads)};assert len(C3)==3
    assert Counter(order(g) for g in C3)==Counter({3:2,1:1})
    assert all(sum(conj(c,n)==n for n in N)==1 for c in C3 if c!=I)
    rem=set(N)-{I};orbits=[]
    while rem:
        n=next(iter(rem));O={conj(k,n) for k in K};orbits.append(len(O));rem-=O
    assert sorted(orbits)==[18,45]
    out={'pass':4690,
      'sextet_stabilizer':{'order':138240,'tetrad_kernel_order':192,'tetrad_kernel_element_orders':{'1':1,'2':63,'3':128}},
      'translation_subgroup':{'order':64,'structure':'C2^6','construction':'identity plus the 63 involutions in the tetrad kernel','normal_in_H':True,'transversal_orbit':64,'regular_on_transversals':True},
      'point_stabilizer':{'order':2160,'intersection_with_translation_order':1,'tetrad_image':'S6','tetrad_image_order':720,'tetrad_kernel':'C3','tetrad_kernel_order':3,'C3_nonzero_translation_fixed_points':0,'nonzero_translation_orbits':[18,45]},
      'affine_action':{'faithful_H_order':138240,'faithful_K_order':2160,'factorization':'H = C2^6 semidirect K','atlas_structure':'2^6:3.S6'},
      'theorem':'The corrected M24 sextet stabilizer is internally recovered as a faithful affine group on its 64 transversals: a normal regular C2^6 translation subgroup with 2160-point stabilizer K.  K maps onto S6 with C3 kernel, and its faithful linear action on the 63 nonzero translations has the 18+45 shell split.',
      'boundary':'Exact permutation-group theorem in the repository M24 model.  The ATLAS name 2^6:3.S6 is used only after the internal normal/complement/action structure is certified.'}
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n');print(json.dumps(out,indent=2,sort_keys=True));return 0
if __name__=='__main__':raise SystemExit(main())
