#!/usr/bin/env python3
"""Explicit Weyl conjugator between physical theta^3 parity and Qpsi matter parity.

The physical parity is reconstructed in the regular SU(9) model of E8 used by
w33_physical_holonomy_e8_chevalley_lift.py.  Its 112 even roots form D8.
The Qpsi parity is reconstructed in the standard doubled E8 gauge as the square
of the Kummer Z4 grading: coefficient on the mark-4 node modulo two.

First an exact root-lattice isometry transports the SU(9) E8 root system into
the standard doubled-coordinate E8 gauge by matching the two E8 simple systems.
Then a BFS over the finite Weyl orbit of D8 subsystems finds a 10-reflection
word sending the physical D8 fixed roots to the Qpsi D8 fixed roots.  On all
240 root spaces it sends physical parity b exactly to Qpsi mod2.
"""
from __future__ import annotations
import importlib.util, itertools, json, sys
from collections import Counter, deque
from fractions import Fraction as F
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/"data/w33_physical_theta3_qpsi_d8_weyl_conjugator.json"
EXPECTED_WORD=(0,3,2,1,4,3,2,5,4,3)
JOINT=[((0,0),3),((0,1),2),((1,0),1),((1,1),1),((2,0),1),((2,1),1)]

def load(path,name):
    spec=importlib.util.spec_from_file_location(name,path); assert spec and spec.loader
    m=importlib.util.module_from_spec(spec); sys.modules[name]=m; spec.loader.exec_module(m); return m

def dot(a,b): return sum(x*y for x,y in zip(a,b))

def simple_roots_any(R,h):
    P={r for r in R if dot(r,h)>0}; assert len(P)*2==len(R)
    out=[]
    for r in sorted(P):
        if not any(tuple(r[i]-a[i] for i in range(len(r))) in P for a in P): out.append(r)
    return out

def main(write=True):
    old=load(ROOT/"analysis/w33_pass7081_7096_e8_z3_z4_z12_common_refinement.py","old_d8conj")
    R=old.e8_roots_doubled(); h8=(1,3,9,27,81,243,729,2187)
    simp8=old.simple_roots(R,h8); cm=old.coeff_map(R,simp8)
    A8=old.cartan(simp8)

    chars=[]
    for ch,n in JOINT: chars += [ch]*n
    roots9=[]; parity9=[]
    for i in range(9):
        for j in range(9):
            if i==j: continue
            v=[F(0)]*9; v[i]=1; v[j]=-1
            roots9.append(tuple(v)); parity9.append((chars[i][1]-chars[j][1])%2)
    for S in itertools.combinations(range(9),3):
        v=[F(-1,3)]*9
        for i in S: v[i]+=1
        b=sum(chars[i][1] for i in S)%2
        roots9.append(tuple(v)); parity9.append(b)
        roots9.append(tuple(-x for x in v)); parity9.append((-b)%2)
    assert len(roots9)==len(set(roots9))==240

    h9=tuple(F(3**i) for i in range(9))
    simp9=simple_roots_any(roots9,h9); assert len(simp9)==8
    A9=[[int(dot(a,b)) for b in simp9] for a in simp9]

    perm=None
    for p in itertools.permutations(range(8)):
        if all(A9[i][j]==A8[p[i]][p[j]] for i in range(8) for j in range(8)):
            perm=p; break
    assert perm==(5,4,3,2,1,0,6,7)

    I9=old.inverse_fraction(A9)
    def map9(r):
        d=[dot(r,a) for a in simp9]
        c=[sum(I9[i][j]*d[j] for j in range(8)) for i in range(8)]
        assert all(x.denominator==1 for x in c)
        ci=[int(x) for x in c]
        return tuple(sum(ci[i]*simp8[perm[i]][k] for i in range(8)) for k in range(8))
    mapped=[map9(r) for r in roots9]
    assert set(mapped)==set(R)

    physical=frozenset(mapped[i] for i,b in enumerate(parity9) if b==0)
    qpsi=frozenset(r for r in R if cm[r][3]%2==0)
    assert len(physical)==len(qpsi)==112
    overlap=len(physical&qpsi); assert overlap==56

    def refl(x,a):
        q=old.dot(x,a); assert q%4==0; k=q//4
        return tuple(x[i]-k*a[i] for i in range(8))
    dq=deque([physical]); prev={physical:(None,None)}
    while dq:
        S=dq.popleft()
        if S==qpsi: break
        for gi,a in enumerate(simp8):
            N=frozenset(refl(x,a) for x in S)
            if N not in prev: prev[N]=(S,gi); dq.append(N)
    assert qpsi in prev
    word=[]; cur=qpsi
    while prev[cur][0] is not None:
        p,gi=prev[cur]; word.append(gi); cur=p
    word=tuple(reversed(word)); assert word==EXPECTED_WORD

    def act(x):
        for gi in word: x=refl(x,simp8[gi])
        return x
    assert frozenset(act(x) for x in physical)==qpsi
    census=Counter()
    for rr,b in zip(mapped,parity9):
        census[(b,cm[act(rr)][3]%2)]+=1
    assert census==Counter({(0,0):112,(1,1):128})

    parent=json.loads((ROOT/"data/w33_physical_holonomy_e8_chevalley_lift.json").read_text())
    assert parent["fixed_algebras"]["order2_theta3"]["dimension"]==120

    out={
      "schema":"w33.physical_theta3_qpsi_d8_weyl_conjugator.v1",
      "status":"PASS_EXPLICIT_D8_INVOLUTION_WEYL_CONJUGATOR",
      "headline":"The physical theta^3 parity and Qpsi matter parity are explicitly Weyl-conjugate E8 involutions. After an exact SU(9)-to-standard-E8 root-lattice isometry, a 10-simple-reflection Weyl word sends the 112 physical even roots to the 112 Qpsi-even roots and sends all 128 odd roots to odd roots. Thus their common D8 fixed type is realized by an explicit conjugator, not inferred only from dimensions.",
      "SU9_to_standard_simple_permutation":list(perm),
      "preconjugation_even_root_intersection":overlap,
      "D8_orbit_states_seen":len(prev),
      "weyl_word_zero_based":list(word),
      "weyl_word_one_based":[i+1 for i in word],
      "word_length":len(word),
      "root_parity_census":{"physical_even_to_qpsi_even":112,"physical_odd_to_qpsi_odd":128},
      "interpretation":"The two involutions occupy the same E8 Weyl conjugacy class. Their associated order-six extensions can still differ, as the previously frozen C6 trace fingerprints prove.",
      "boundary":"Conjugacy of the involutions does not identify the full FI x parity Z6 with the flagship geometric/holonomy Z6; their order-six eigenspace multiplicities remain different.",
      "checks":{"SU9_root_model_to_standard_E8":True,"D8_to_D8_word":True,"all_240_parities_match":True}}
    if write: OUT.write_text(json.dumps(out,indent=2)+"\n")
    print(json.dumps({k:out[k] for k in ("status","word_length","weyl_word_zero_based","root_parity_census")},indent=2))
    return out
if __name__=="__main__": main(True)
