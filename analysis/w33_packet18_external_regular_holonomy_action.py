#!/usr/bin/env python3
"""External regular holonomy action on the 18-point runtime packet space.

Parent:
  data/w33_e8_holonomy_packet18_homogeneous_bridge.json
  data/w33_e8_holonomy_c3xc6_factorization.json

Runtime:
  G = F3^2 semidirect D8, |G|=72.
  H = <R> = C4.
  X = G/H is the 18-point right-coset packet space.

The parent correctly proves that the physical holonomy-character group
  K = C3_rho x C3_a x C2_b
is NOT a subgroup of G: G has no abelian subgroup of order 18.

However, for a transitive left G-set X=G/H,
  Aut_G(X) ~= N_G(H)/H,
acting by right multiplication.

Exact computation here gives
  N_G(H) = {0} x D8,
so
  Aut_G(X) ~= D8/C4 ~= C2.
The unique nontrivial G-equivariant automorphism is right multiplication by a
reflection S; in the packet coordinates (t,sector) it fixes t in F3^2 and
swaps the two 9-point sheets.

Meanwhile the left translation kernel T=F3^2 acts freely on each sheet.
The left T action commutes with the right deck C2. Therefore
  T_left x C2_deck ~= C3^2 x C2
acts REGULARLY on all 18 packet blocks.

With the packet coordinate convention
  t=(rho,a), sheet=b,
this regular permutation group is exactly the physical holonomy-character
group K as an abstract group and as an action on its own 18 characters.

After CRT
  n=4a+3b mod6,
the physical C6 generator (a,b)=(1,1) is represented on packet18 by
  one unit translation in the a direction followed by the unique deck swap.
It has order 6 and cycle profile 6^3.
The A8 selector rho is the independent ternary translation and has profile 3^6.

What this DOES and DOES NOT repair:
  * repaired: the full holonomy group has an exact regular permutation action
    on packet18;
  * unchanged: that group is not a subgroup of the 72-element runtime group G;
  * mechanism: the missing C2 lives in Aut_G(X), a commuting RIGHT deck action,
    not in the LEFT runtime execution group;
  * no physical E8 root space is identified with an optical packet block by
    this group-theory result alone.

This is the natural left/right completion of the previous torsor bridge.
"""
from __future__ import annotations
import itertools,json
from collections import Counter
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/w33_packet18_external_regular_holonomy_action.json'

I=(1,0,0,1);R=(0,2,1,0);S=(1,0,0,2)

def mm(A,B):
    return tuple(sum(A[2*i+k]*B[2*k+j] for k in range(2))%3
                 for i in range(2) for j in range(2))
def mv(A,v):
    return ((A[0]*v[0]+A[1]*v[1])%3,(A[2]*v[0]+A[3]*v[1])%3)
def mpow(A,n):
    o=I
    for _ in range(n):o=mm(o,A)
    return o

D8=[mm(mpow(S,s),mpow(R,p)) for s in range(2) for p in range(4)]
D8=list(dict.fromkeys(D8))
C4={mpow(R,p) for p in range(4)}
T=list(itertools.product(range(3),repeat=2))

def mul(g,h):
    t,L=g;u,M=h
    Lu=mv(L,u)
    return (((t[0]+Lu[0])%3,(t[1]+Lu[1])%3),mm(L,M))

def inv(g):
    t,L=g
    Linv=next(M for M in D8 if mm(L,M)==I and mm(M,L)==I)
    u=mv(Linv,((-t[0])%3,(-t[1])%3))
    return (u,Linv)

G=[(t,L) for t in T for L in D8]
H={((0,0),C) for C in C4}

def conj(g,h):return mul(mul(g,h),inv(g))

def normalizes_H(g):
    return {conj(g,h) for h in H}==H

def right_coset(g):
    return frozenset(mul(g,h) for h in H)

def sector_of(L):return 0 if L in C4 else 1

def profile(items,act):
    idx={x:i for i,x in enumerate(items)}
    perm=[idx[act(x)] for x in items]
    seen=set();c=Counter()
    for i in range(len(items)):
        if i in seen:continue
        u=i;n=0
        while u not in seen:
            seen.add(u);n+=1;u=perm[u]
        c[n]+=1
    return dict(sorted(c.items()))

def main(write=True):
    parent=json.loads((ROOT/'data/w33_e8_holonomy_packet18_homogeneous_bridge.json').read_text())
    crt=json.loads((ROOT/'data/w33_e8_holonomy_c3xc6_factorization.json').read_text())
    assert parent['status']=='PASS_TORSOR_BRIDGE__GROUP_IDENTIFICATION_KILLED'
    assert crt['status']=='PASS_EXACT_C3_SELECTOR_X_PHYSICAL_C6_FACTORIZATION'

    # Exact normalizer.
    N=[g for g in G if normalizes_H(g)]
    assert len(N)==8
    assert all(t==(0,0) for t,L in N)
    assert {L for t,L in N}==set(D8)
    assert H.issubset(set(N))

    # The quotient N/H has two right H-cosets.
    Ncos={right_coset(n) for n in N}
    assert len(Ncos)==2

    # Build packet cosets in canonical (translation, reflection-sector) coords.
    cosets={}
    for g in G:
        C=right_coset(g)
        t,L=g
        key=(t,sector_of(L))
        cosets.setdefault(key,C)
        assert cosets[key]==C
    assert len(cosets)==18

    keys=sorted(cosets)

    # Left translation T action.
    def Lact(u,key):
        C=cosets[key]
        image=frozenset(mul((u,I),x) for x in C)
        return next(k for k,v in cosets.items() if v==image)

    # Unique nontrivial deck map: right multiplication by S.
    deck_rep=((0,0),S)
    assert normalizes_H(deck_rep)
    def deck(key):
        C=cosets[key]
        image=frozenset(mul(x,deck_rep) for x in C)
        return next(k for k,v in cosets.items() if v==image)

    for t in T:
        for b in range(2):
            assert deck((t,b))==(t,1-b)
    assert all(deck(deck(k))==k for k in keys)

    # Deck commutes with the entire left G action, not only T.
    def Gact(g,key):
        C=cosets[key]
        image=frozenset(mul(g,x) for x in C)
        return next(k for k,v in cosets.items() if v==image)
    assert all(deck(Gact(g,k))==Gact(g,deck(k)) for g in G for k in keys)

    # K = T_left x C2_deck action.
    def Kact(kappa,key):
        rho,a,b=kappa
        y=Lact((rho,a),key)
        if b:y=deck(y)
        return y

    K=list(itertools.product(range(3),range(3),range(2)))
    base=((0,0),0)
    orbit={Kact(k,base) for k in K}
    assert len(orbit)==18
    # Freeness at base => regularity since |K|=|X|.
    assert sum(Kact(k,base)==base for k in K)==1

    # Verify group law is componentwise addition.
    for x in K:
      for y in K:
        xy=((x[0]+y[0])%3,(x[1]+y[1])%3,(x[2]+y[2])%2)
        for key in keys:
            assert Kact(x,Kact(y,key))==Kact(xy,key)

    # Selector rho and physical C6 generator.
    selector=(1,0,0)
    phys=(0,1,1)
    assert profile(keys,lambda k:Kact(selector,k))=={3:6}
    assert profile(keys,lambda k:Kact(phys,k))=={6:3}

    # Physical powers obey CRT coordinate n=k mod6.
    y=base
    power=[]
    for n in range(6):
        if n==0:y=base
        elif n>0:y=Kact(phys,y)
        t,b=y
        power.append({'n':n,'rho':t[0],'a':t[1],'b':b,
                      'CRT':(4*t[1]+3*b)%6})
        assert t[0]==0 and t[1]==n%3 and b==n%2
        assert (4*t[1]+3*b)%6==n
    assert Kact(phys,Kact(phys,Kact(phys,Kact(phys,Kact(phys,Kact(phys,base))))))==base

    out={
      'schema':'w33.packet18_external_regular_holonomy_action.v1',
      'status':'PASS_EXTERNAL_REGULAR_HOLONOMY_ACTION',
      'headline':'Although K=C3_rho x C3_a x C2_b is not a subgroup of the 72-element runtime group G, packet18=X=G/C4 has Aut_G(X)=N_G(C4)/C4=C2. The unique nontrivial deck involution swaps the two regular F3^2 sheets. Combining left runtime translations T=F3^2 with this commuting right deck action gives T x C2 ~= C3^2 x C2 acting regularly on all 18 packet blocks. Under n=4a+3b mod6, the physical C6 generator is exactly one a-translation followed by the deck swap and has packet cycle profile 6^3.',
      'runtime':{
        'G':'F3^2 semidirect D8','order':72,
        'H':'C4=<R>','packet_space':'X=G/H','packet_count':18,
        'normalizer_order':len(N),
        'normalizer':'{0} x D8',
        'Aut_G_X':'N_G(H)/H ~= C2'},
      'deck':{
        'representative':'right multiplication by pure reflection S',
        'action':'(t,b) -> (t,1-b)',
        'unique_nontrivial_G_equivariant_automorphism':True,
        'commutes_with_full_left_G_action':True},
      'holonomy_action':{
        'K':'C3_rho x C3_a x C2_b',
        'realization':'left T translations on (rho,a) times right deck C2 on b',
        'order':18,'regular_on_packet18':True,
        'selector_rho_profile':{'3_cycles':6},
        'physical_C6_generator':'(rho,a,b)=(0,1,1)',
        'physical_C6_profile':{'6_cycles':3},
        'CRT':'n=4a+3b mod6',
        'physical_power_orbit':power},
      'relation_to_parent_negative_result':{
        'unchanged':'K is not a subgroup of the runtime execution group G and G contains no abelian subgroup of order18',
        'upgrade':'K nevertheless has an exact regular permutation representation on packet18, using the commuting right deck symmetry missing from the left runtime group',
        'interpretation':'the old two-sheet torsor bridge is the restriction of this full left/right regular K-action'},
      'physical_boundary':'Exact finite group/G-set theorem. It does not identify E8 eigenspaces with packet hardware modes or assert that the deck permutation is itself a dynamical optical gate.',
      'parents':['data/w33_e8_holonomy_packet18_homogeneous_bridge.json',
                 'data/w33_e8_holonomy_c3xc6_factorization.json'],
      'checks':{
        'normalizer_exact':True,
        'Aut_G_X_is_C2':True,
        'deck_swaps_sheets':True,
        'deck_commutes_with_left_G':True,
        'K_action_regular':True,
        'physical_C6_is_translation_times_deck':True,
        'physical_C6_profile_6cubed':True}}
    if write:OUT.write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps(out,indent=2));return out

if __name__=='__main__':main(True)
