#!/usr/bin/env python3
"""Pass5612: classify minimum supports of the binary projectivity codes.

Pass5604 proved d=q+1.  Here a counting equality proves that every weight-(q+1)
word is the graph of a permutation pi of P1(q).  Orthogonality to the opposite
determinant PGL coset then says that no nonsquare projectivity agrees with pi on
three points.  Equivalently, pi preserves the PSL two-colouring of ordered
triples.  The standard projective-line automorphism identification gives the
colour-preserving group P-Sigma-L_2(q)=PSL_2(q):Gal(F_q/F_p).

Thus the minimum supports are semilinear projectivities, not merely PSL rows at
extension fields.  In particular Frobenius is a new minimum word at q=9.

This verifier exhausts all permutations for q=3,5,7 and directly checks the q=9
Frobenius/semilinear phenomenon over GF(9).
"""
from __future__ import annotations

import itertools
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "PART_W33_PASS5612_PROJECTIVITY_MINWORDS_SEMILINEAR.json"


def normp(v, q):
    v = tuple(x % q for x in v)
    for a in v:
        if a:
            z = pow(a, -1, q)
            return tuple(z*x % q for x in v)
    raise ValueError


def p1p(q):
    return [(1,t) for t in range(q)] + [(0,1)]


def applyp(m, v, q):
    a,b,c,d=m
    return normp((a*v[0]+b*v[1], c*v[0]+d*v[1]), q)


def pgl_psl_prime(q):
    P=p1p(q); idx={x:i for i,x in enumerate(P)}
    sq={x*x%q for x in range(1,q)}
    mats=set(); plus=set()
    for m in itertools.product(range(q), repeat=4):
        a,b,c,d=m; det=(a*d-b*c)%q
        if det==0: continue
        k=normp(m,q); mats.add(k)
        a,b,c,d=k
        if (a*d-b*c)%q in sq: plus.add(k)
    conv=lambda M: sorted({tuple(idx[applyp(m,x,q)] for x in P) for m in M})
    return conv(mats),conv(plus)


def bits(g):
    n=len(g); z=0
    for i,j in enumerate(g): z |= 1 << (i*n+j)
    return z


def compose(a,b): return tuple(a[b[i]] for i in range(len(a)))


def qualifies(pi, minus_bits):
    z=bits(pi)
    return all(((z & h).bit_count() & 1)==0 for h in minus_bits)


def exhaustive_prime(q):
    PGL,PSL=pgl_psl_prime(q); ps=set(PSL)
    minus=[g for g in PGL if g not in ps]; mb=[bits(g) for g in minus]
    good=[]
    for pi in itertools.permutations(range(q+1)):
        if qualifies(pi,mb): good.append(pi)
    assert set(good)==ps
    return {"q":q,"all_permutations_checked":len(list(itertools.permutations(range(q+1)))),
            "qualifying_minimum_graphs":len(good),"PSL2_order":len(PSL),"equals_PSL2":True}


class GF9:
    """F3[w]/(w^2-2), encoded a+3b."""
    p=3; q=9; d=2
    @staticmethod
    def pair(x): return x%3,x//3
    @staticmethod
    def enc(a,b): return (a%3)+3*(b%3)
    @classmethod
    def add(cls,x,y):
        a,b=cls.pair(x);c,d=cls.pair(y);return cls.enc(a+c,b+d)
    @classmethod
    def neg(cls,x):
        a,b=cls.pair(x);return cls.enc(-a,-b)
    @classmethod
    def sub(cls,x,y): return cls.add(x,cls.neg(y))
    @classmethod
    def mul(cls,x,y):
        a,b=cls.pair(x);c,e=cls.pair(y);return cls.enc(a*c+2*b*e,a*e+b*c)
    @classmethod
    def inv(cls,x):
        a,b=cls.pair(x); den=(a*a-2*b*b)%3; z=pow(den,-1,3)
        return cls.enc(a*z,-b*z)
    @classmethod
    def pow(cls,x,n):
        r=1
        while n:
            if n&1:r=cls.mul(r,x)
            x=cls.mul(x,x);n//=2
        return r


def normF(v,F):
    for a in v:
        if a:
            z=F.inv(a);return tuple(F.mul(z,x) for x in v)
    raise ValueError


def p1F(F): return [(1,t) for t in range(F.q)]+[(0,1)]

def applyF(m,v,F):
    a,b,c,d=m
    return normF((F.add(F.mul(a,v[0]),F.mul(b,v[1])),F.add(F.mul(c,v[0]),F.mul(d,v[1]))),F)


def pgl_psl_F(F):
    P=p1F(F);idx={x:i for i,x in enumerate(P)};sq={F.mul(x,x) for x in range(1,F.q)}
    mats=set();plus=set()
    for m in itertools.product(range(F.q),repeat=4):
        a,b,c,d=m;det=F.sub(F.mul(a,d),F.mul(b,c))
        if det==0:continue
        k=normF(m,F);mats.add(k)
        a,b,c,d=k;det=F.sub(F.mul(a,d),F.mul(b,c))
        if det in sq:plus.add(k)
    conv=lambda M: sorted({tuple(idx[applyF(m,x,F)] for x in P) for m in M})
    return conv(mats),conv(plus)


def q9_semilinear_check():
    F=GF9;P=p1F(F);idx={x:i for i,x in enumerate(P)}
    PGL,PSL=pgl_psl_F(F);ps=set(PSL);minus=[g for g in PGL if g not in ps];mb=[bits(g) for g in minus]
    frob=tuple(idx[normF((F.pow(v[0],3),F.pow(v[1],3)),F)] for v in P)
    assert frob not in set(PGL)
    assert qualifies(frob,mb)
    pSigma={compose(frob,g) for g in PSL}|set(PSL)
    assert len(pSigma)==2*len(PSL)==720
    assert all(qualifies(g,mb) for g in pSigma)
    h=minus[0]
    bad=compose(h,frob)
    assert not qualifies(bad,mb)
    hist={}
    z=bits(frob)
    for m in mb:
        k=(z&m).bit_count();hist[k]=hist.get(k,0)+1
    assert set(hist)<= {0,2}
    return {"q":9,"PSL2_order":len(PSL),"PGL2_order":len(PGL),"P_Sigma_L2_constructed_order":len(pSigma),
            "Frobenius_is_projectivity":False,"Frobenius_is_minimum_word":True,
            "Frobenius_opposite_coset_intersection_histogram":hist,
            "nonsquare_projectivity_after_Frobenius_fails":True}


def main():
    primes=[exhaustive_prime(q) for q in (3,5,7)]
    ext=q9_semilinear_check()
    out={
      "pass":5612,"status":"MINIMUM_SUPPORTS_REDUCE_TO_PSIGMAL2_TRIPLE_COLOUR_AUTOMORPHISMS",
      "parameters":"[(q+1)^2,(q+1)^2/2,q+1]_2",
      "counting_proof":{
        "opposite_projectivities_through_one_cell":"a=q(q-1)/2",
        "through_two_compatible_cells":"b=(q-1)/2",
        "even_intersection_inequality":"C(m,2)>=m/2 for even m",
        "equality_conclusion":"a weight q+1 support has every pair compatible, hence is exactly one cell per row and column; all opposite-coset intersections are 0 or 2"
      },
      "triple_colour_reduction":"the unique PGL interpolation on every ordered triple of a minimum permutation lies in PSL, so the permutation preserves the two PSL orbits on ordered triples",
      "classification":"Min(C_plus)=P-Sigma-L2(q)=PSL2(q):Gal(F_q/F_p); Min(C_minus) is the other determinant coset inside P-Gamma-L2(q)",
      "important_extension_field_correction":"minimum words are not only PSL rows when f>1; Frobenius supplies new minimum words",
      "exhaustive_prime_anchors":primes,
      "extension_anchor":ext,
      "literature_boundary":"the last identification uses the standard projective-line/PSL switching automorphism classification; the counting and parity reduction are proved directly here",
      "physics_reading":"minimum information carriers are semilinear projective histories; extension-field Frobenius is an allowed minimum carrier, so field automorphisms are information symmetries rather than extra noise"
    }
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+"\n",encoding="utf-8")
    print(json.dumps(out,indent=2,sort_keys=True))

if __name__=="__main__": main()
