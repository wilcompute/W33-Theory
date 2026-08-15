#!/usr/bin/env python3
"""Pass5351-5352: lift the Hoffman extraspecial 2-group to an explicit real two-qubit Pauli presentation and pull its commutator form onto the Klein-Latin F2^4 chart.

Pass5300 proved that the Hoffman-cover stabilizer H has a normal extraspecial
2_+^{1+4} subgroup Q of order32 and that H/Z(H) is affine-conjugate to the
even-parastrophe symmetry of the Klein order-4 Latin square. Here we make the
extraspecial identification objectwise: find four involutions X1,Z1,X2,Z2 in Q
with [Xi,Zi]=z and all other basic commutators trivial. Those are precisely the
presentation relations of the real two-qubit Pauli group (phases +/-1).

Then we transport the commutator symplectic form on Q/<z> through the explicit
Pass5300 GL4(2) conjugacy and classify the five Klein/MOLS PG(3,2) spread lines
as commuting (totally isotropic) or anticommuting (nonisotropic) Pauli triples.
This is finite group/code geometry only; it is not a physical qubit claim.
"""
from __future__ import annotations
import itertools,json
from pathlib import Path
from analysis.w33_pass5300_hoffman576_latin_group_bridge import (
    q5_hoffman,latin_groups,gl4,mcomp,minv,mapply,COVER)
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_W33_PASS5351_5352_HOFFMAN_PAULI_LATIN_SYMPLECTIC_SPREAD.json'

def comm(a,b):return (~a)*(~b)*a*b

def main():
    H,H13,Hact,Q=q5_hoffman();L,Lp,Lact=latin_groups()
    assert Q.order()==32 and Q.center().order()==2
    z=next(g for g in Q.center().generate_schreier_sims() if g!=Q.identity)
    ci={c:i for i,c in enumerate(COVER)}
    def restrict13(h):
        from sympy.combinatorics import Permutation
        return Permutation([ci[h(c)] for c in COVER])
    V=H13.derived_subgroup().derived_subgroup();assert V.order()==16 and V.is_abelian
    els=list(V.generate_schreier_sims());coord={V.identity:0};bas=[]
    for v in els:
        if v in coord:continue
        bit=1<<len(bas);old=list(coord.items())
        for g,c in old:coord[g*v]=c|bit
        bas.append(v)
    assert len(bas)==4 and len(coord)==16
    lifts={}
    for h in Q.generate_schreier_sims():
        v=restrict13(h)
        if v not in lifts or h.order()<lifts[v].order():lifts[v]=h
    assert len(lifts)==16
    # Bilinear commutator form in the Pass5300 H-coordinate basis.
    def Bv(x,y):
        a=lifts[next(g for g,c in coord.items() if c==x)]
        b=lifts[next(g for g,c in coord.items() if c==y)]
        c=comm(a,b);assert c in (Q.identity,z)
        return int(c==z)
    J=[[Bv(1<<i,1<<j) for j in range(4)] for i in range(4)]
    assert all(J[i][i]==0 for i in range(4))
    # Find a symplectic basis whose lifts are involutions: real Pauli presentation.
    nonzero=range(1,16);pb=None
    for e1,f1,e2,f2 in itertools.permutations(nonzero,4):
        if len({e1,f1,e2,f2})<4:continue
        # linear independence
        vals={0}
        for mask in range(1,16):
            x=0
            for i,v in enumerate((e1,f1,e2,f2)):
                if mask>>i&1:x^=v
            vals.add(x)
        if len(vals)!=16:continue
        if any(lifts[next(g for g,c in coord.items() if c==v)].order()!=2 for v in (e1,f1,e2,f2)):continue
        if Bv(e1,f1)!=1 or Bv(e2,f2)!=1:continue
        if any(Bv(a,b) for a,b in ((e1,e2),(e1,f2),(f1,e2),(f1,f2))):continue
        pb=(e1,f1,e2,f2);break
    assert pb is not None
    Pgens=[lifts[next(g for g,c in coord.items() if c==v)] for v in pb]
    assert comm(Pgens[0],Pgens[1])==z and comm(Pgens[2],Pgens[3])==z
    assert all(comm(Pgens[i],Pgens[j])==Q.identity for i,j in ((0,2),(0,3),(1,2),(1,3)))
    # Normal form +/- X1^a Z1^b X2^c Z2^d is bijective onto Q.
    images={}
    for bits in itertools.product((0,1),repeat=5):
        a,b,c,d,e=bits;g=Q.identity
        for bit,h in zip((a,b,c,d),Pgens):
            if bit:g=g*h
        if e:g=g*z
        images[bits]=g
    assert len(set(images.values()))==32 and set(images.values())==set(Q.generate_schreier_sims())
    # Recover the Pass5300 GL4 conjugator H-coordinates <- Latin coordinates.
    witness=None
    for P in gl4():
        Pi=minv(P)
        if {mcomp(mcomp(Pi,A),P) for A in Hact}==Lact:witness=P;break
    assert witness is not None
    def Blatin(x,y):return Bv(mapply(witness,x),mapply(witness,y))
    spread=[('row',{1,2,3}),('column',{4,8,12}),('symbol',{5,10,15}),
            ('orthogonal_mate_1',{6,11,13}),('orthogonal_mate_2',{7,9,14})]
    cls=[]
    for name,S in spread:
        a,b=sorted(S)[:2];val=Blatin(a,b)
        assert all(Blatin(x,y)==val for x,y in itertools.combinations(S,2))
        cls.append({'line':name,'points':sorted(S),'pair_commutator':val,
                    'pauli_type':'commuting/isotropic' if val==0 else 'pairwise-anticommuting/nonisotropic'})
    iso=sum(x['pair_commutator']==0 for x in cls)
    # Count all projective lines by isotropy as a sanity check: W(3,2) has 15 isotropic of 35.
    lines=[]
    for a,b in itertools.combinations(range(1,16),2):
        S=frozenset((a,b,a^b))
        if len(S)==3:lines.append(S)
    lines=set(lines);assert len(lines)==35
    n_iso=sum(Blatin(*sorted(S)[:2])==0 for S in lines);assert n_iso==15
    out={'passes':[5351,5352],
      'status':'THEOREM_HOFFMAN_EXTRASPECIAL_GROUP_HAS_EXPLICIT_REAL_TWO_QUBIT_PAULI_PRESENTATION_AND_LATIN_SPREAD_COMMUTATOR_CLASSIFICATION',
      'Q_order':32,'Q_center':2,'Q_type':'2_+^{1+4}',
      'commutator_form_matrix_H_coordinates':J,
      'pauli_symplectic_basis_H_coordinates':list(pb),
      'presentation':'Xi^2=Zi^2=z^2=1; [X1,Z1]=[X2,Z2]=z; all cross-pair commutators are1.',
      'normal_forms':32,
      'latin_to_H_change_of_basis_columns':list(witness),
      'PG3_2_lines':35,'isotropic_lines_W3_2':n_iso,
      'latin_MOLS_spread_classification':cls,
      'latin_spread_isotropic_lines':iso,'latin_spread_nonisotropic_lines':5-iso,
      'boundary':'Exact finite-group and symplectic-form identification. It does not identify the Hoffman construction with a physical two-qubit system.'}
    OUT.write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
if __name__=='__main__':main()
