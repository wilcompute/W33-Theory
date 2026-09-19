#!/usr/bin/env python3
"""The E8 Z12 cocycle refines the 80-state cover to the full signed Pauli symplectic orientation.

Parents:
  data/PART_W33_PASS7163_7170_E8_HEXAGONAL_LIFT.json
  data/w33_e8_c3_quotient_signed_pauli_cover.json

Pass 7168 assigns every oriented W33 nonedge x->y an odd phase
    phi_xy = 2 s_xy + 1 mod 12,
with reversal phi_yx=-phi_xy and fiber-origin gauge law
    phi_xy -> phi_xy + 2(a_y-a_x),  a_x in Z6.

Define the binary sign
    eps_xy = (-1)^s_xy.
Then:
  eps_yx = -eps_xy,
and under gauge shift
  eps_xy -> (-1)^(a_x+a_y) eps_xy.
This is exactly the switching law obtained by changing signed projective
representatives v_x -> eta_x v_x, eta_x=+/-1.

This certificate reconstructs the deterministic Pass-7164 E8 fibers, builds
the canonical PG(3,3) symplectic model, and freezes one explicit base
isomorphism plus one switching gauge.  For every one of the 540 W33 nonedges:
    eps_E8(x,y)
      = eta_x eta_y sign( omega(v_f(x),v_f(y)) ).

The explicit base isomorphism f (E8-fiber index -> canonical PG index) is:
  [0,1,39,32,34,30,23,27,22,28,26,33,38,31,35,37,36,24,29,25,
   3,16,4,12,15,8,20,9,14,19,5,18,10,21,11,7,17,6,13,2].

The switching gauge eta is:
  [+,-,+,-,-,+,-,-,+,-,+,+,-,-,+,+,-,+,-,+,
   -,-,+,+,-,+,-,-,+,+,-,+,-,-,+,+,-,+,-,-].

Lift the two C3-orbit sheets t=0,1 over each E8 fiber by
    (x,t) -> eta_x (-1)^t v_f(x).
This is a bijection onto all 80 nonzero vectors of F3^4 and verifies
objectwise:
  sheet flip <-> vector negation,
  W33 adjacency <-> symplectic product 0,
  E8 cocycle sign on nonedges <-> symplectic product +1/-1.

Therefore the previously fused 54-class splits exactly into 27+27 at every
oriented Pauli vector.  The switching CLASS is canonical from the E8 cocycle;
the displayed f and eta are one witness gauge, not unique.

This resolves the open 27+27 boundary in
  data/w33_e8_c3_quotient_signed_pauli_cover.json.

Still open:
this does NOT yet prove that the heterotic CZ-parity C6 action lifts to an
automorphism of the full 240-root E8 Coxeter-fiber structure.  It proves that
the underlying oriented 80-state Pauli carrier, including its symplectic sign,
is already encoded by the E8 C6/Z12 phase data.
"""
from __future__ import annotations
import itertools, json
from collections import Counter
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/w33_e8_z12_to_pauli_symplectic_sign.json'

SIMPLES=[
(1,-1,-1,-1,-1,-1,-1,1),
(2,2,0,0,0,0,0,0),
(-2,2,0,0,0,0,0,0),
(0,-2,2,0,0,0,0,0),
(0,0,-2,2,0,0,0,0),
(0,0,0,-2,2,0,0,0),
(0,0,0,0,-2,2,0,0),
(0,0,0,0,0,-2,2,0)]

ISO=[0,1,39,32,34,30,23,27,22,28,26,33,38,31,35,37,36,24,29,25,
     3,16,4,12,15,8,20,9,14,19,5,18,10,21,11,7,17,6,13,2]
ETA=[1,-1,1,-1,-1,1,-1,-1,1,-1,1,1,-1,-1,1,1,-1,1,-1,1,
     -1,-1,1,1,-1,1,-1,-1,1,1,-1,1,-1,-1,1,1,-1,1,-1,-1]

def dot(a,b):return sum(x*y for x,y in zip(a,b))

def roots_e8():
    R=[]
    for i,j in itertools.combinations(range(8),2):
        for si in (1,-1):
            for sj in (1,-1):
                x=[0]*8;x[i]=2*si;x[j]=2*sj;R.append(tuple(x))
    for bits in itertools.product((1,-1),repeat=8):
        if sum(x==-1 for x in bits)%2==0:R.append(tuple(bits))
    assert len(R)==len(set(R))==240
    return R

def refl(x,r):
    q=dot(x,r);assert q%4==0;k=q//4
    return tuple(x[i]-k*r[i] for i in range(8))

def cox(x):
    y=x
    for r in SIMPLES:y=refl(y,r)
    return y

def canon(v):
    i=next(i for i,x in enumerate(v) if x)
    inv=pow(v[i],-1,3)
    return tuple((x*inv)%3 for x in v)

def symp(v,w):
    return (v[0]*w[2]+v[1]*w[3]-v[2]*w[0]-v[3]*w[1])%3

def scale(sign,v):
    s=1 if sign==1 else 2
    return tuple((s*x)%3 for x in v)

def main(write=True):
    assert sorted(ISO)==list(range(40))
    assert len(ETA)==40 and set(ETA)=={-1,1}

    R=roots_e8();I={r:i for i,r in enumerate(R)}
    cp=[I[cox(r)] for r in R]
    d=list(range(240))
    for _ in range(5):d=[cp[i] for i in d]

    seen=set();fib=[]
    for i in range(240):
        if i in seen:continue
        o=[];j=i
        while j not in o:
            o.append(j);seen.add(j);j=d[j]
        assert len(o)==6
        fib.append(tuple(o))
    assert len(fib)==40
    phase=[{v:k for k,v in enumerate(F)} for F in fib]

    # E8 base adjacency and Z12 midpoint phase.
    badj=[set() for _ in range(40)]
    e8sign={}
    phi={}
    for a,b in itertools.combinations(range(40),2):
        E=[(u,v) for u in fib[a] for v in fib[b] if dot(R[u],R[v])==4]
        if not E:
            badj[a].add(b);badj[b].add(a)
            continue
        assert len(E)==12
        D={(phase[b][v]-phase[a][u])%6 for u,v in E}
        assert len(D)==2
        ss=[s for s in D if (s+1)%6 in D]
        assert len(ss)==1
        s=ss[0]
        p=(2*s+1)%12
        phi[(a,b)]=p;phi[(b,a)]=(-p)%12
        sig=1 if s%2==0 else -1
        e8sign[(a,b)]=sig;e8sign[(b,a)]=-sig

    assert all(len(x)==12 for x in badj)
    assert len(phi)==1080 and len(e8sign)==1080

    # Gauge covariance of the binary reduction, exhaustively in Z6.
    for s in range(6):
        old=1 if s%2==0 else -1
        for ax in range(6):
            for ay in range(6):
                sp=(s+ay-ax)%6
                new=1 if sp%2==0 else -1
                assert new==((-1)**(ax+ay))*old

    # Canonical symplectic PG(3,3).
    V=[v for v in itertools.product(range(3),repeat=4) if any(v)]
    PP=sorted({canon(v) for v in V})
    assert len(PP)==40

    padj=[set() for _ in range(40)]
    psign={}
    for i,j in itertools.combinations(range(40),2):
        s=symp(PP[i],PP[j])
        if s==0:
            padj[i].add(j);padj[j].add(i)
        else:
            sig=1 if s==1 else -1
            psign[(i,j)]=sig;psign[(j,i)]=-sig

    # Explicit base graph isomorphism.
    for a,b in itertools.combinations(range(40),2):
        assert (b in badj[a])==(ISO[b] in padj[ISO[a]])

    # Explicit switching equivalence on all 540 nonedges.
    for a,b in itertools.permutations(range(40),2):
        if b in badj[a]:continue
        assert e8sign[(a,b)]==ETA[a]*ETA[b]*psign[(ISO[a],ISO[b])]

    # Switching-invariant triangle products: balanced 1620/1620.
    tri=Counter()
    for a,b,c in itertools.combinations(range(40),3):
        if (a,b) in e8sign and (b,c) in e8sign and (c,a) in e8sign:
            tri[e8sign[(a,b)]*e8sign[(b,c)]*e8sign[(c,a)]]+=1
    assert tri==Counter({1:1620,-1:1620})

    # Full 80-state lift.
    M={}
    for a in range(40):
        for t in (0,1):
            M[(a,t)]=scale(ETA[a]*((-1)**t),PP[ISO[a]])
    assert len(set(M.values()))==80

    for a in range(40):
        assert M[(a,1)]==tuple((-x)%3 for x in M[(a,0)])

    outdegree=Counter()
    for a in range(40):
        for ta in (0,1):
            c=Counter()
            va=M[(a,ta)]
            for b in range(40):
                if b==a:continue
                for tb in (0,1):
                    vb=M[(b,tb)]
                    s=symp(va,vb)
                    if b in badj[a]:
                        assert s==0
                        c['commuting']+=1
                    else:
                        expected=e8sign[(a,b)]*((-1)**(ta+tb))
                        actual=1 if s==1 else -1
                        assert actual==expected
                        c['plus' if actual==1 else 'minus']+=1
            assert c==Counter({'plus':27,'minus':27,'commuting':24})
            outdegree[tuple(sorted(c.items()))]+=1
    assert outdegree==Counter({(('commuting',24),('minus',27),('plus',27)):80})

    out={
      'schema':'w33.e8_z12_to_pauli_symplectic_sign.v1',
      'status':'PASS',
      'headline':'The Pass-7168 E8 Z12 midpoint cocycle canonically refines the 80-state antipodal cover to the full two-qutrit symplectic sign structure. The binary reduction eps_xy=(-1)^s for phi_xy=2s+1 transforms by projective switching, and an explicit W33 base isomorphism plus switching gauge identifies it with sign(omega(v_x,v_y)) on every one of the 540 nonedges. The two C3-orbit sheets then map bijectively to all 80 nonzero F3^4 vectors, splitting the fused noncommuting class exactly as 27+27.',
      'binary_reduction':{
        'definition':'phi_xy=2s_xy+1 mod12 -> eps_xy=(-1)^s_xy',
        'reversal':'eps_yx=-eps_xy',
        'gauge_law':'eps_xy -> (-1)^(a_x+a_y) eps_xy',
        'interpretation':'exact projective switching law'},
      'explicit_witness':{
        'base_isomorphism_E8fiber_to_PGindex':ISO,
        'switching_eta':ETA,
        'equation':'eps_E8(x,y)=eta_x eta_y sign(omega(v_f(x),v_f(y))) on all 540 W33 nonedges'},
      'full_80_map':{
        'formula':'(x,t) -> eta_x (-1)^t v_f(x)',
        'bijection_to_F3four_nonzero':True,
        'sheet_flip_is_vector_negation':True,
        'commuting_degree':24,
        'positive_symplectic_degree':27,
        'negative_symplectic_degree':27},
      'switching_invariants':{
        'complement_triangles':3240,
        'triangle_product_plus':1620,
        'triangle_product_minus':1620},
      'closure':{
        'resolves':'the open 27+27 sign refinement in data/w33_e8_c3_quotient_signed_pauli_cover.json',
        'now_proved':'the E8 C6/Z12 phase data encode the full signed Pauli carrier up to switching gauge and W33 base automorphism',
        'still_open':'whether the heterotic/Clifford CZ-parity C6 action lifts through this identification to an automorphism of the full 240-root E8 Coxeter-fiber structure'},
      'parents':['data/PART_W33_PASS7163_7170_E8_HEXAGONAL_LIFT.json','data/w33_e8_c3_quotient_signed_pauli_cover.json']
    }
    if write:OUT.write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps(out,indent=2))
    return out

if __name__=='__main__':main(True)
