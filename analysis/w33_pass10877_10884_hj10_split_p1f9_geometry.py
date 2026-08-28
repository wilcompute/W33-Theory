#!/usr/bin/env python3
"""Pass10877-10884: sharpen the HJ ten-state P1(F9) comparison.

Pass10869-10876 proved that the residual outer involution on the ten HJ states
has cycle profile 1^2 2^4.  This pass classifies the matching projective-line
involution exactly rather than stopping at the cycle count.

On P1(F9), j:z -> -z is a split projective involution.  It fixes the two poles
0,infinity and pairs the eight nonzero affine points.  Its centralizer in
PGL2(9) is

    F9^x : <z->1/z> ~= C8:C2 = D16,

of order 16.  The moving-point quotient is canonically
F9^x/{+/-1} ~= C4.  Hence

    P1(F9)/<j> = {0, infinity} disjoint-union C4,

six states in total.  This matches the HJ full C13:C12 quotient count: the ten
inner-C6 states modulo the residual C2 also give two fixed states and four
paired-state classes, hence six full-normalizer states.

By contrast field Frobenius z->z^3 fixes P1(F3), four points, and has profile
1^4 2^3.  Therefore the outer HJ bit is projective/diagonal rather than Galois
at the ten-state carrier level.

The theorem deliberately does NOT put a C4 operation on the four moving HJ
classes; that extra projective-line structure remains a transporter target.
"""
from __future__ import annotations
import itertools,json
from collections import Counter
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_W33_PASS10877_10884_HJ10_SPLIT_P1F9_GEOMETRY.json'

# F9 = F3[i], i^2=-1. element=(a,b).
def add(x,y): return ((x[0]+y[0])%3,(x[1]+y[1])%3)
def neg(x): return ((-x[0])%3,(-x[1])%3)
def mul(x,y):
    a,b=x;c,d=y
    return ((a*c-b*d)%3,(a*d+b*c)%3)
def pow9(x,n):
    r=(1,0)
    while n:
      if n&1:r=mul(r,x)
      x=mul(x,x);n//=2
    return r
def inv(x):
    assert x!=(0,0)
    return pow9(x,7)

F=[(a,b) for a in range(3) for b in range(3)]
NZ=[x for x in F if x!=(0,0)]
INF=('inf',)
P=F+[INF]

def cycles(perm):
    seen=set();out=[]
    for x in P:
      if x in seen:continue
      y=x;C=[]
      while y not in seen:
        seen.add(y);C.append(y);y=perm[y]
      out.append(C)
    return Counter(map(len,out))

def main():
    # Find a primitive generator of F9^x=C8.
    primitive=next(x for x in NZ if len({pow9(x,k) for k in range(8)})==8)
    assert len({pow9(primitive,k) for k in range(8)})==8
    minus_one=(2,0)
    assert pow9(primitive,4)==minus_one

    j={INF:INF}
    frob={INF:INF}
    for z in F:
      j[z]=neg(z)
      frob[z]=pow9(z,3)
    assert cycles(j)==Counter({2:4,1:2})
    assert cycles(frob)==Counter({1:4,2:3})
    assert {z for z in P if frob[z]==z}=={(0,0),(1,0),(2,0),INF}

    # Quotient moving points by +/-1 is cyclic C4 via exponents modulo 4.
    antipodal=[];seen=set()
    for z in NZ:
      if z in seen:continue
      C=frozenset((z,neg(z)));seen|=set(C);antipodal.append(C)
    assert len(antipodal)==4
    exp={pow9(primitive,k):k for k in range(8)}
    labels=sorted({min(exp[z]%4 for z in C) for C in antipodal})
    assert labels==[0,1,2,3]

    # Explicit centralizer of j in PGL2(9): scalings z->a z (8) and
    # inversion-scalings z->a/z (8).  All commute with z->-z.
    maps=[]
    for a in NZ:
      f={INF:INF,(0,0):(0,0)}
      for z in NZ:f[z]=mul(a,z)
      maps.append(f)
      g={INF:(0,0),(0,0):INF}
      for z in NZ:g[z]=mul(a,inv(z))
      maps.append(g)
    keys={tuple(m[x] for x in P) for m in maps};assert len(keys)==16
    for m in maps:
      assert all(m[j[x]]==j[m[x]] for x in P)
    # scaling by primitive has order 8; inversion has order2 and conjugates it to inverse.
    rot=maps[0]  # not guaranteed primitive scaling; build explicitly
    rot={INF:INF,(0,0):(0,0),**{z:mul(primitive,z) for z in NZ}}
    refl={INF:(0,0),(0,0):INF,**{z:inv(z) for z in NZ}}
    def compose(a,b):return {x:a[b[x]] for x in P}
    def ppower(a,n):
      r={x:x for x in P}
      for _ in range(n):r=compose(r,a)
      return r
    assert ppower(rot,8)=={x:x for x in P} and ppower(rot,4)!={x:x for x in P}
    assert ppower(refl,2)=={x:x for x in P}
    assert compose(compose(refl,rot),refl)==ppower(rot,7)

    old=json.loads((ROOT/'data/PART_W33_PASS10869_10876_HJ10_P1F9_TEST.json').read_text())
    assert old['residual_outer_C2_on_10']['profile']=={'1':2,'2':4}
    assert old['C12_on_32_C13_cycles']['full_normalizer_orbits']==6

    out={
      'schema':'w33.pass10877_10884.hj10_split_p1f9_geometry.v1','status':'PASS','passes':'10877-10884',
      'HJ':{'inner_C6_quotient_states':10,'residual_C2_profile':'1^2 2^4','full_C13_C12_quotient_states':6},
      'P1F9':{
        'points':10,'primitive_F9_unit':list(primitive),'F9x':'C8',
        'split_involution':'j:z->-z','j_profile':'1^2 2^4','fixed_poles':['0','infinity'],
        'moving_quotient':'F9^x/{+/-1} ~= C4','full_j_quotient':'{0,infinity} disjoint-union C4, six states',
        'centralizer_in_PGL2_9':'C8:C2 ~= D16','centralizer_order':16,
        'field_Frobenius':'z->z^3','Frobenius_profile':'1^4 2^3','Frobenius_fixed_set':'P1(F3)'},
      'theorem':'The HJ ten-state residual outer involution is compatible with the split projective involution z->-z on P1(F9), not with F9/F3 Frobenius. The matching projective model has two fixed poles and four antipodal moving classes F9^x/{+/-1}=C4, so its six-state involution quotient exactly matches the six full C13:C12 Hall-Janko normalizer orbits.',
      'boundary':'The P1(F9) classification is exact. Only the C2-set and six-state quotient are identified; no canonical C4 operation, cross-ratio, PGL2(9) action or Q^-(3,3) polarity has yet been transported to the HJ ten states.'}
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
    print(json.dumps({'status':'PASS','HJ10':'1^2 2^4','P1F9':'split projective','quotient':'2 poles + C4','centralizer':'D16'}))
if __name__=='__main__':main()
