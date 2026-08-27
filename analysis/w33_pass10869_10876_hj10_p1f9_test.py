#!/usr/bin/env python3
"""Pass10869-10876: extend the HJ 32-cycle quotient through C13:C12 and test P1(F9).

Pass10797 gives the inner C6 action on the 32 C13-orbit labels of the
416-point G2(4)/J2 carrier.  The full graph automorphism group is G2(4):2 and
the order-13 torus normalizer extends to C13:C12.  Let t generate the C12
complement, with t^2=n the inner C6 generator.

ATLAS class fusion through L2(13):2 and J2:2 gives the power classes
  t   : 12E,  t^2:6B, t^3:4E, t^4:3B, t^6:2B
in G2(4):2.  Centralizer ratios against the corresponding J2:2 classes give
fixed-point counts on the 416 cosets

  Fix(t,t^2,t^3,t^4,t^6) = 1,1,4,5,16.

Because t^d normalizes C13 with nontrivial automorphism whenever needed, each
stable 13-orbit contains a unique fixed point, so these are also fixed counts
on the 32 C13-orbit labels.  Möbius inversion for a cyclic C12 action forces
cycle profile

  1^1 3^1 4^1 6^2 12^1.

The inner C6=<t^2> has the already-certified ten orbit states.  The residual
C2=C12/C6 acts on those ten states as 1^2 2^4.

This distinguishes two natural P1(F9) involutions:
* field Frobenius z->z^3 fixes P1(F3): profile 1^4 2^3, so it is NOT the HJ
  residual involution;
* split projective involution z->-z fixes 0 and infinity: profile 1^2 2^4,
  exactly matching the HJ residual C2-set.

Since P1(F9) is also the standard ten-point carrier of Q^-(3,3), the HJ ten
states are compatible with the elliptic-quadric carrier at the C2-set level,
but no full projective-line cross-ratio/orthogonal structure is claimed.
"""
from __future__ import annotations
import json
from collections import Counter
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_W33_PASS10869_10876_HJ10_P1F9_TEST.json'

def cycles(p):
    seen=set();C=[]
    for x in range(len(p)):
      if x in seen:continue
      y=x;n=0
      while y not in seen:seen.add(y);n+=1;y=p[y]
      C.append(n)
    return Counter(C)

def main():
    # ATLAS centralizers and class fusion for the degree-416 coset action.
    G={'12E':12,'6B':24,'4E':96,'3B':360,'2B':7680}
    J={'12BC':12,'6B':24,'4C':24,'3B':72,'2B':480}
    fixed=[G['12E']//J['12BC'],G['6B']//J['6B'],G['4E']//J['4C'],G['3B']//J['3B'],G['2B']//J['2B']]
    assert fixed==[1,1,4,5,16]
    f1,f2,f3,f4,f6=fixed
    # For generator t of C12: Fix(t^m)=sum_{d|m} d*c_d.
    c1=f1
    c2=(f2-c1)//2
    c3=(f3-c1)//3
    c4=(f4-c1-2*c2)//4
    c6=(f6-c1-2*c2-3*c3)//6
    c12=(32-c1-2*c2-3*c3-4*c4-6*c6)//12
    profile={1:c1,2:c2,3:c3,4:c4,6:c6,12:c12}
    assert profile=={1:1,2:0,3:1,4:1,6:2,12:1}
    assert sum(d*n for d,n in profile.items())==32
    assert sum(profile.values())==6

    # C6=<t^2> orbit profile derived from each C12 cycle.
    c6prof=Counter()
    for d,m in profile.items():
      if not m:continue
      g=__import__('math').gcd(d,2)
      c6prof[d//g]+=m*g
    assert c6prof==Counter({3:5,2:2,6:2,1:1})
    assert sum(c6prof.values())==10
    # residual t mod <t^2> on the ten C6 orbits: odd C12 cycles contribute one fixed orbit;
    # even cycles split into two C6 orbits exchanged by residual C2.
    residual_fixed=sum(m for d,m in profile.items() if d%2==1)
    assert residual_fixed==2
    residual_pairs=(10-residual_fixed)//2;assert residual_pairs==4

    # Explicit P1(F9)=F9 union infinity involution profiles.
    # F9 elements encoded (a,b) for a+b*i, i^2=-1 over F3.
    F9=[(a,b) for a in range(3) for b in range(3)];INF=('inf',)
    P=F9+[INF];idx={x:i for i,x in enumerate(P)}
    frob=[];neg=[]
    for x in P:
      if x==INF:frob.append(idx[INF]);neg.append(idx[INF])
      else:
        a,b=x
        frob.append(idx[(a,(-b)%3)])  # z^3 = conjugation
        neg.append(idx[((-a)%3,(-b)%3)])
    assert cycles(frob)==Counter({1:4,2:3})
    assert cycles(neg)==Counter({2:4,1:2})

    out={
      'schema':'w33.pass10869_10876.hj10_p1f9_test.v1','status':'PASS','passes':'10869-10876',
      'ATLAS_input':{
        'group':'G2(4):2 on 416 cosets of J2:2','torus_normalizer':'C13:C12','power_classes':{'t':'12E','t^2':'6B','t^3':'4E','t^4':'3B','t^6':'2B'},
        'G2d2_centralizers':G,'J2d2_centralizers':J,'fixed_points_416':{'t':1,'t2':1,'t3':4,'t4':5,'t6':16}},
      'C12_on_32_C13_cycles':{'cycle_profile':{'1':1,'3':1,'4':1,'6':2,'12':1},'full_normalizer_orbits':6},
      'C6_quotient':{'states':10,'orbit_size_profile_on_32':{'1':1,'2':2,'3':5,'6':2}},
      'residual_outer_C2_on_10':{'profile':{'1':2,'2':4},'fixed_states':2,'paired_states':8},
      'P1F9_comparison':{
        'carrier_size':10,'also':'Q^-(3,3) point carrier under the standard PSL2(9) ~= POmega^-(4,3) action',
        'field_Frobenius_profile':{'1':4,'2':3},'matches_HJ':False,
        'split_projective_involution_z_to_minus_z_profile':{'1':2,'2':4},'matches_HJ':True},
      'theorem':'The full C13:C12 normalizer acts on the 32 Hall-Janko C13 cycles with profile 1^1 3^1 4^1 6^2 12^1. The ten-state inner-C6 quotient therefore carries a residual involution of type 1^2 2^4. This rules out F9/F3 Frobenius on P1(F9), but exactly matches a split projective involution on the ten-point P1(F9) ~= Q^-(3,3) carrier.',
      'boundary':'The ATLAS centralizer-ratio computation and P1(F9) involution profiles are exact. Matching the residual C2-set does not yet identify a projective-line cross-ratio, PGL2(9) action, or Q^-(3,3) polarity on the HJ ten states.'}
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
    print(json.dumps({'status':'PASS','C12_profile':'1^1 3^1 4^1 6^2 12^1','HJ10_C2':'1^2 2^4','P1F9':'split yes, Frobenius no'}))
if __name__=='__main__':main()
