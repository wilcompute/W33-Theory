#!/usr/bin/env python3
"""Pass 4767 -- the 24 explicit Leech two-neighbors carry the Golay relation code.

Pass4699 constructs one Leech 2-neighbor for each coordinate i using

  v_i=(1,...,1,3_i,1,...,1)/sqrt(2),
  chi_i(x)=(x,v_i) mod 2,
  M_i=ker chi_i.

Evaluate the 24 characters on an exact generating set of the Golay Construction-A
Niemeier lattice N: the 24 coordinate roots 2e_j/sqrt(2) and twelve lifted binary
Golay generators.  The space of binary relations among chi_0,...,chi_23 is
literally the extended Golay code G24.

Consequences: the character span has dimension 12; every <=7 characters are
independent; the first dependencies are exactly the 759 octads.  The corrected
sextet contributes its 15 unions of two tetrads as an explicit 15-subset of those
octad relations.
"""
from __future__ import annotations
import itertools,json
from collections import Counter
from pathlib import Path
import w33_pass4592_paired_axes_simplex_hexacode_golay as p4592
import w33_pass4633_m24_sextet_section_stabilizer as p4633
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_W33_PASS4767_LEECH_NEIGHBOR_GOLAY_PARITY_MATROID.json'

def basis(rows):
    piv={};out=[]
    for x in rows:
        y=int(x)
        while y:
            p=y.bit_length()-1
            if p in piv:y^=piv[p]
            else:piv[p]=y;out.append(int(x));break
    return out

def nullspace(rows,n):
    piv={}
    for x in rows:
        y=int(x)
        while y:
            p=y.bit_length()-1
            if p in piv:y^=piv[p]
            else:
                for q,z in list(piv.items()):
                    if (z>>p)&1:piv[q]=z^y
                piv[p]=y;break
    free=[j for j in range(n) if j not in piv];out=[]
    for f in free:
        x=1<<f
        for p in sorted(piv):
            if ((piv[p]&x).bit_count()&1):x|=1<<p
        out.append(x)
    assert all(all(((r&x).bit_count()&1)==0 for r in rows) for x in out)
    return out

def span(B):
    out=[0]
    for b in B:out += [x^b for x in out]
    return out

def main()->int:
    G24=set(map(int,p4592.golay24()));assert len(G24)==4096
    wh=Counter(x.bit_count() for x in G24)
    assert wh==Counter({12:2576,8:759,16:759,0:1,24:1})
    Gb=basis(sorted(G24));assert len(Gb)==12

    # Integer numerator generators of L0={a in Z^24:a mod2 in G24}; N=L0/sqrt(2).
    gens=[]
    for j in range(24):
        a=[0]*24;a[j]=2;gens.append(a)
    for g in Gb:gens.append([(g>>j)&1 for j in range(24)])
    assert len(gens)==36
    # Evaluation rows: chi_i(a/sqrt2) = (a dot v_i)/2 mod 2.
    rows=[]
    for a in gens:
        r=0
        for i in range(24):
            dot=sum(a)+2*a[i]
            assert dot%2==0
            if (dot//2)&1:r|=1<<i
        rows.append(r)
    relb=nullspace(rows,24);assert len(relb)==12
    relations=set(span(relb));assert relations==G24

    d=p4633.build();H=d['H'];sextet=[frozenset(T) for T in d['sextet']];assert len(H)==138240 and len(sextet)==6
    orbit0={g[0] for g in H};assert len(orbit0)==24
    Hi=[g for g in H if g[0]==0];assert len(Hi)==5760
    unseen=set(range(24));sub=[]
    while unseen:
        x=min(unseen);O={g[x] for g in Hi};sub.append(len(O));unseen-=O
    assert sorted(sub)==[1,3,20]
    # The sextet definition says each union of two tetrads is a Golay octad.
    pair_octads=[]
    for A,B in itertools.combinations(sextet,2):
        m=sum(1<<i for i in A|B);assert m.bit_count()==8 and m in G24;pair_octads.append(m)
    assert len(set(pair_octads))==15
    # H preserves the relation code because it is the actual M24 coordinate action.
    def actword(x,g):
        y=0
        for i in range(24):
            if (x>>i)&1:y|=1<<g[i]
        return y
    assert all(actword(x,g) in G24 for g in d['Hgens'] for x in G24)

    out={'pass':4767,'neighbors':{'count':24,'sextet_stabilizer_order':138240,'one_neighbor_stabilizer_order':5760,'point_suborbits':[1,3,20],'transitive':True},
      'parity_characters':{'count':24,'span_dimension':12,'relation_space_dimension':12,'relation_space':'extended binary Golay G24','minimum_relation_weight':8,'minimum_relations':759,
        'all_subsets_size_at_most_7_independent':True},
      'sextet_relations':{'tetrads':6,'two_tetrad_unions':15,'all_are_octad_relations':True},
      'theorem':'The 24 Leech-neighbor parity characters have exactly the extended Golay code as their binary relation space. Their first dependencies are the 759 Golay octads; the corrected sextet supplies 15 explicit two-tetrad octad relations.',
      'boundary':'Exact Construction-A/M24 lattice-character theorem. The 24 neighbors are a transitive sextet-stabilizer G-set; no physical state interpretation is inferred.'}
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n',encoding='utf-8');print(json.dumps(out,indent=2,sort_keys=True));return 0
if __name__=='__main__':raise SystemExit(main())
