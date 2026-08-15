#!/usr/bin/env python3
"""Pass5404--5409: all-q unsigned apartment visibility spectrum.

Let B=|C| be the unsigned flag-edge/apartment incidence matrix of GQ(q,q).
Pass5396--5403 gives the pair overlap counts, so

  B B^T = q^4 A0 + q^3 A1 + q^2 A2 + q A3 + A4.

This script evaluates that radial kernel on the Pass5388--5395 flag distance
scheme using exact polynomial arithmetic.  The resulting eigenvalues are

  8 q^4,
  2 q^2 (q-1)(q+1 + sqrt(2q)),
  2 q^2 (q-1)^2,
  2 q^2 (q-1)(q+1 - sqrt(2q)),
  (q-1)^2(q^2+1),

with multiplicities 1, f, 2g, f, q^4 where
f=q(q+1)^2/2 and g=q(q^2+1)/2.

Every eigenvalue is positive for q>1, hence B has full row rank N.  The signed
matrix C has rank q^4, and the rank gap

  N-q^4 = 2(q+1)(q^2+1)-1

is exactly the rank of the oriented Levi incidence matrix, i.e. the cut-space
dimension.  At q=3 the spectrum is exactly BT546:
648, 144+36sqrt(6), 72, 144-36sqrt(6), 40.
"""
from __future__ import annotations

import json
from fractions import Fraction
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data/PART_W33_PASS5404_5409_ALLQ_UNSIGNED_APARTMENT_SPECTRUM.json"
ANCHORS = [2, 3, 4, 5, 7, 8, 9, 11, 13]


def trim(p: list[Fraction]) -> list[Fraction]:
    while len(p) > 1 and p[-1] == 0:
        p.pop()
    return p


def add(a: list[Fraction], b: list[Fraction]) -> list[Fraction]:
    n=max(len(a),len(b)); out=[Fraction(0) for _ in range(n)]
    for i in range(n):
        out[i]=(a[i] if i<len(a) else 0)+(b[i] if i<len(b) else 0)
    return trim(out)


def scale(a: list[Fraction], c: Fraction) -> list[Fraction]:
    return trim([c*x for x in a])


def mul(a: list[Fraction], b: list[Fraction]) -> list[Fraction]:
    out=[Fraction(0) for _ in range(len(a)+len(b)-1)]
    for i,ai in enumerate(a):
        for j,bj in enumerate(b): out[i+j]+=ai*bj
    return trim(out)


def eval_poly(p: list[Fraction], x: Fraction) -> Fraction:
    out=Fraction(0)
    for c in reversed(p): out=out*x+c
    return out


def divmod_poly(a: list[Fraction], b: list[Fraction]) -> tuple[list[Fraction],list[Fraction]]:
    a=trim(a[:]); b=trim(b[:]);
    if len(a)<len(b): return [Fraction(0)],a
    q=[Fraction(0)]*(len(a)-len(b)+1)
    while len(a)>=len(b) and any(a):
        k=len(a)-len(b); c=a[-1]/b[-1]; q[k]=c
        for j in range(len(b)): a[k+j]-=c*b[j]
        trim(a)
    return trim(q),trim(a)


def distance_polynomials(q: int) -> list[list[Fraction]]:
    # p_i(theta) is the eigenvalue of A_i on an A_1-eigenvector of eigenvalue theta.
    b=[2*q,q,q,q]
    a=[0,q-1,q-1,q-1,2*q-2]
    c=[0,1,1,1,2]
    p=[[Fraction(1)],[Fraction(0),Fraction(1)]]
    x=[Fraction(0),Fraction(1)]
    for i in range(1,4):
        # x p_i = b_{i-1} p_{i-1} + a_i p_i + c_{i+1} p_{i+1}
        lhs=mul(x,p[i])
        rhs=add(scale(p[i-1],-Fraction(b[i-1])),scale(p[i],-Fraction(a[i])))
        next_num=add(lhs,rhs)
        p.append(scale(next_num,Fraction(1,c[i+1])))
    return p


def unsigned_kernel_polynomial(q: int) -> list[Fraction]:
    p=distance_polynomials(q)
    coeff=[q**4,q**3,q**2,q,1]
    out=[Fraction(0)]
    for c,pi in zip(coeff,p): out=add(out,scale(pi,Fraction(c)))
    return out


def row(q: int) -> dict:
    assert q>1
    N=(q+1)**2*(q*q+1)
    f=q*(q+1)**2//2
    g=q*(q*q+1)//2
    U=unsigned_kernel_polynomial(q)

    lam0=8*q**4
    lammid=2*q*q*(q-1)**2
    lamterm=(q-1)**2*(q*q+1)
    assert eval_poly(U,Fraction(2*q))==lam0
    assert eval_poly(U,Fraction(q-1))==lammid
    assert eval_poly(U,Fraction(-2))==lamterm

    # On the two quadratic sectors theta satisfies
    # (theta-(q-1))^2=2q.  Reduce U modulo this polynomial.  The remainder
    # must be 2q^2(q-1)(theta+2), yielding the +/- radical pair exactly.
    minimal=[Fraction((q-1)**2-2*q),Fraction(-2*(q-1)),Fraction(1)]
    _,rem=divmod_poly(U,minimal)
    expected=[Fraction(4*q*q*(q-1)),Fraction(2*q*q*(q-1))]
    assert rem==expected

    # Positivity for q>1; the radical pair is positive because q+1>sqrt(2q).
    assert lam0>0 and lammid>0 and lamterm>0
    assert (q+1)**2>2*q

    signed_rank=q**4
    unsigned_rank=N
    cut_rank=N-signed_rank
    levi_vertices=2*(q+1)*(q*q+1)
    assert cut_rank==levi_vertices-1

    return {
        "q":q,
        "flags":N,
        "unsigned_rank":unsigned_rank,
        "signed_rank":signed_rank,
        "rank_gap_cut_space":cut_rank,
        "multiplicities":[1,f,2*g,f,q**4],
        "eigenvalues":[
            f"{8*q**4}",
            f"{2*q*q*(q-1)}*({q+1}+sqrt({2*q}))",
            f"{lammid}",
            f"{2*q*q*(q-1)}*({q+1}-sqrt({2*q}))",
            f"{lamterm}"
        ]
    }


def build_certificate() -> dict:
    anchors={str(q):row(q) for q in ANCHORS}
    q3=anchors["3"]
    assert q3["flags"]==160
    assert q3["unsigned_rank"]==160
    assert q3["signed_rank"]==81
    assert q3["rank_gap_cut_space"]==79
    assert q3["multiplicities"]==[1,24,30,24,81]
    assert q3["eigenvalues"]==[
        "648","36*(4+sqrt(6))","72","36*(4-sqrt(6))","40"
    ]
    return {
        "schema":"w33.allq_unsigned_apartment_spectrum.v1",
        "pass_range":[5404,5409],
        "status":"THEOREM_EXACT_UNSIGNED_VISIBILITY_SPECTRUM",
        "domain":"Any finite generalized quadrangle of order (q,q), q>1.",
        "gram_kernel":"B B^T=q^4A0+q^3A1+q^2A2+qA3+A4",
        "spectrum":{
            "eigenvalues":[
                "8q^4",
                "2q^2(q-1)(q+1+sqrt(2q))",
                "2q^2(q-1)^2",
                "2q^2(q-1)(q+1-sqrt(2q))",
                "(q-1)^2(q^2+1)"
            ],
            "multiplicities":["1","q(q+1)^2/2","q(q^2+1)","q(q+1)^2/2","q^4"]
        },
        "rank_complement":{
            "unsigned_rank":"N=(q+1)^2(q^2+1)",
            "signed_rank":"q^4",
            "gap":"N-q^4=2(q+1)(q^2+1)-1=rank(D_Levi)",
            "reading":"Unsigned apartment visibility spans the full flag space; alternating orientation signs project exactly onto the Levi cycle sector and remove the cut-space dimensions."
        },
        "w33_specialization":{
            "unsigned_spectrum":"648^1 + (144+36sqrt6)^24 + 72^30 + (144-36sqrt6)^24 + 40^81",
            "unsigned_rank":160,
            "signed_rank":81,
            "cut_rank":79,
            "reading":"Exactly BT546/BT549."
        },
        "anchors":anchors,
        "boundary":"This is an unsigned visibility Gram spectrum and rank-complement theorem. It is not a contextuality-degree, code-distance, or physical-noise theorem."
    }


def main()->dict:
    out=build_certificate();OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n',encoding='utf-8');print(json.dumps(out,indent=2,sort_keys=True));return out


if __name__=='__main__':main()
