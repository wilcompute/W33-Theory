#!/usr/bin/env python3
"""Physical Chevalley-level lift of the flagship commuting holonomies to all of E8.

This is the correct replacement for trying to realise the physical parity as
the Coxeter-fiber half-turn.

External classical input:
  E8 restricted to its regular maximal A8=SU(9) subgroup branches as
      248 = 80 + 84 + 84bar
          = sl(9) + Lambda^3(9) + Lambda^6(9).
  (Slansky, Phys. Rep. 79 (1981), Table 53.)

Flagship input (Holotrade w33_holonomy_pair_is_cz_parity):
on the fundamental 9, the commuting order-(3,2) holonomies have joint character
multiplicities
  (0,+):3, (0,-):2,
  (1,+):1, (1,-):1,
  (2,+):1, (2,-):1,
where a in Z3 is the Wilson-line character and b in Z2 is theta^3 parity.

Because these are INNER SU(9) torus elements, they automatically act on all of
E8 through the A8 embedding.  No Weyl/root permutation is required.

This certificate reconstructs the 240 E8 roots explicitly in the A8 model:
  * 72 roots e_i-e_j;
  * 84 weights sum_{i in S} e_i - (1/3)sum_i e_i, |S|=3;
  * their 84 negatives.
Every vector has norm 2 and the set has 240 distinct roots.

The exact E8 adjoint joint multiplicities are
  (0,+):44, (0,-):48,
  (1,+):38, (1,-):40,
  (2,+):38, (2,-):40.
Equivalently the product C6 character multiplicities (exponent 2a+3b mod6) are
  [44,40,38,48,38,40].

Neutral-root classification:
  order-3 Wilson line: 84 roots, one rank-7 component => D7, plus U(1);
      fixed algebra D7 + u1, dim 92.
  order-2 physical theta^3: 112 roots, one rank-8 component => D8;
      fixed algebra D8, dim 120.
  order-6 product: 36 roots split 24(rank4)+12(rank3) => D4 + A3,
      with one residual u1; fixed algebra D4 + A3 + u1, dim 44.

Thus the physical holonomies DO possess an exact E8/Chevalley lift, but it is a
diagonal inner automorphism of E8 root spaces, not a root permutation.  This
explains the earlier 40-versus-36 firewall: the Coxeter antipode was simply
the wrong category of lift.

Scope:
  This proves the finite Lie-algebra/character lift for the recorded flagship
  joint spectrum. It does not claim the SU(9) embedding/basis is uniquely
  selected by W33 alone, nor does it identify the separate Coxeter-fiber C6
  root permutation with the physical holonomy.
"""
from __future__ import annotations
import itertools,json
from collections import Counter
from fractions import Fraction as F
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/w33_physical_holonomy_e8_chevalley_lift.json'

JOINT=[((0,0),3),((0,1),2),((1,0),1),((1,1),1),((2,0),1),((2,1),1)]

def rank(rows):
    A=[list(r) for r in rows if any(r)]
    if not A:return 0
    m,n=len(A),len(A[0]);r=0
    for c in range(n):
        p=next((i for i in range(r,m) if A[i][c]),None)
        if p is None:continue
        A[r],A[p]=A[p],A[r];z=A[r][c];A[r]=[x/z for x in A[r]]
        for i in range(m):
            if i!=r and A[i][c]:
                z=A[i][c];A[i]=[A[i][j]-z*A[r][j] for j in range(n)]
        r+=1
    return r

def dot(a,b):return sum(x*y for x,y in zip(a,b))

def main(write=True):
    chars=[]
    for ch,n in JOINT:chars += [ch]*n
    assert len(chars)==9

    roots=[];rch=[]
    # A8 roots.
    for i in range(9):
      for j in range(9):
        if i==j:continue
        v=[F(0)]*9;v[i]=F(1);v[j]=F(-1)
        roots.append(tuple(v))
        rch.append(((chars[i][0]-chars[j][0])%3,(chars[i][1]-chars[j][1])%2))
    # Lambda^3 9 and its dual.
    for S in itertools.combinations(range(9),3):
        v=[F(-1,3)]*9
        for i in S:v[i]+=1
        ch=(sum(chars[i][0] for i in S)%3,sum(chars[i][1] for i in S)%2)
        roots.append(tuple(v));rch.append(ch)
        roots.append(tuple(-x for x in v));rch.append(((-ch[0])%3,(-ch[1])%2))
    assert len(roots)==len(set(roots))==240
    assert all(dot(r,r)==2 for r in roots)
    assert set(dot(a,b) for a in roots for b in roots)<=set((F(-2),F(-1),F(0),F(1),F(2)))

    # Cartan is 8-dimensional and always joint-neutral.
    joint=Counter(rch);joint[(0,0)]+=8
    expected={(0,0):44,(0,1):48,(1,0):38,(1,1):40,(2,0):38,(2,1):40}
    assert dict(joint)==expected and sum(joint.values())==248

    c6=Counter()
    for (a,b),n in joint.items():c6[(2*a+3*b)%6]+=n
    assert [c6[i] for i in range(6)]==[44,40,38,48,38,40]

    def neutral(kind):
        out=[]
        for i,(a,b) in enumerate(rch):
            ok=(a==0) if kind=='order3' else ((b==0) if kind=='order2' else ((2*a+3*b)%6==0))
            if ok:out.append(i)
        return out

    def comps(ids):
        rem=set(ids);out=[]
        while rem:
            i=rem.pop();C=[i];stack=[i]
            while stack:
                u=stack.pop()
                ns=[v for v in list(rem) if dot(roots[u],roots[v])!=0]
                for v in ns:rem.remove(v);stack.append(v);C.append(v)
            out.append(C)
        return out

    n3,n2,n6=neutral('order3'),neutral('order2'),neutral('order6')
    c3,c2,c6r=comps(n3),comps(n2),comps(n6)
    sig3=sorted((len(C),rank([roots[i] for i in C])) for C in c3)
    sig2=sorted((len(C),rank([roots[i] for i in C])) for C in c2)
    sig6=sorted((len(C),rank([roots[i] for i in C])) for C in c6r)
    assert sig3==[(84,7)]       # D7
    assert sig2==[(112,8)]      # D8
    assert sig6==[(12,3),(24,4)]# A3 + D4

    # Fundamental and Lambda^3 character controls.
    fund=Counter(chars)
    lam3=Counter()
    for S in itertools.combinations(range(9),3):
        lam3[(sum(chars[i][0] for i in S)%3,sum(chars[i][1] for i in S)%2)]+=1
    assert fund==Counter({(0,0):3,(0,1):2,(1,0):1,(1,1):1,(2,0):1,(2,1):1})
    assert lam3==Counter({(0,1):16,(0,0):14,(1,1):14,(2,1):14,(1,0):13,(2,0):13})

    parent=json.loads((ROOT/'data/w33_e8_cz_parity_c6_root_lift.json').read_text())
    assert parent['status']=='PASS_LABEL_LIFT__PHYSICAL_PARITY_FIREWALL'

    out={
      'schema':'w33.physical_holonomy_e8_chevalley_lift.v1','status':'PASS_PHYSICAL_INNER_CHEVALLEY_LIFT',
      'headline':'The flagship commuting (order3,order2) holonomy pair has an exact physical inner lift to all of E8 through the regular SU(9) subgroup. Using E8=sl9+Lambda^3(9)+Lambda^6(9), its full 248-dimensional joint character is 44,48,38,40,38,40. The fixed algebras are D7+u1 (dim92) for the Wilson line, D8 (dim120) for physical theta^3 parity, and D4+A3+u1 (dim44) for their order-six product.',
      'branching':{'E8_under_SU9':'248 = 80 + 84 + 84bar = sl9 + Lambda^3(9) + Lambda^6(9)',
                   'classical_reference':'Slansky, Phys.Rept.79 (1981), Table 53'},
      'fundamental_joint_multiplicities':{f'{a},{b}':n for (a,b),n in JOINT},
      'full_E8_joint_multiplicities':{f'{a},{b}':joint[(a,b)] for a in range(3) for b in range(2)},
      'physical_C6_eigenvalue_multiplicities':[c6[i] for i in range(6)],
      'fixed_algebras':{
        'order3_W3':{'neutral_roots':84,'component_signature':sig3,'type':'D7 + u1','dimension':92},
        'order2_theta3':{'neutral_roots':112,'component_signature':sig2,'type':'D8','dimension':120},
        'order6_product':{'neutral_roots':36,'component_signature':sig6,'type':'D4 + A3 + u1','dimension':44}},
      'resolution':{
        'parity_firewall':'resolved by changing category: physical holonomies act diagonally on E8 root spaces as inner torus automorphisms, not as Weyl permutations of the roots',
        'coxeter_label_lift':'remains a separate exact combinatorial root-permutation theorem; it is not the physical parity lift'},
      'checks':{
        '240_root_A8_model':True,'all_roots_norm2':True,'joint_sum248':True,
        'C6_character':[c6[i] for i in range(6)]==[44,40,38,48,38,40],
        'order3_D7':sig3==[(84,7)],'order2_D8':sig2==[(112,8)],
        'order6_D4_A3':sig6==[(12,3),(24,4)],
        'physical_parity_firewall_parent_loaded':True}}
    if write:OUT.write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps(out,indent=2));return out

if __name__=='__main__':main(True)
