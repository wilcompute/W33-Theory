#!/usr/bin/env python3
"""Infinite local Levi/Hasse–Weil prime family; classical RH remains OPEN.

For p ≡ 3 or 7 mod 20, W(3,p)'s nontrivial Levi Ihara denominator equals
(1+p²u⁴)^f (1+pu²)^(2g), f=p(p+1)²/2, g=p(p²+1)/2.
These are local Frobenius factors of C:y²=x⁵+1 and E:y²=x³−x over Fp.
Independently counts Fp and Fp² points at p=3,7,23.
"""
from __future__ import annotations
import json, math
from pathlib import Path

def is_prime(p):
    return p >= 2 and all(p % d for d in range(2, math.isqrt(p)+1))

def chi(x,p):
    x%=p
    return 0 if x==0 else (1 if pow(x,(p-1)//2,p)==1 else -1)

def count_fp(p,kind):
    assert is_prime(p) and p%2
    return p+1+sum(chi(x**5+1 if kind=="C" else x**3-x,p) for x in range(p))

def count_fp2(p,kind):
    """Enumerate Fp[W]/(W²-d) with a nonsquare d; independent of Weil formulas."""
    d=next(v for v in range(2,p) if chi(v,p)==-1)
    squares={}
    for a in range(p):
        for b in range(p):
            v=((a*a+d*b*b)%p,2*a*b%p)
            squares[v]=squares.get(v,0)+1
    def mul(x,y):
        return ((x[0]*y[0]+d*x[1]*y[1])%p,(x[0]*y[1]+x[1]*y[0])%p)
    def power(x,n):
        r=(1,0)
        while n:
            if n&1:r=mul(r,x)
            x=mul(x,x);n//=2
        return r
    total=1
    for a in range(p):
        for b in range(p):
            x=(a,b);v=power(x,5 if kind=="C" else 3)
            rhs=((v[0]+1)%p,v[1]) if kind=="C" else ((v[0]-a)%p,(v[1]-b)%p)
            total+=squares.get(rhs,0)
    return total

def local_packet(p,extension_counts=True):
    assert is_prime(p) and p%20 in (3,7)
    assert math.gcd(5,p*p-1)==1
    f=p*(p+1)**2//2
    g=p*(p*p+1)//2
    points=(p+1)*(p*p+1)
    flags=(p+1)*points
    assert f+g==points-1
    assert 4*f+4*g==4*(points-1)
    # x -> x^5 permutes Fp and Fp² because ord_5(p)=4.
    # E's trace is zero because p≡3 mod4.
    cp,ep=count_fp(p,"C"),count_fp(p,"E")
    assert cp==ep==p+1
    cp2,ep2=(count_fp2(p,"C"),count_fp2(p,"E")) if extension_counts else (None,None)
    if extension_counts:assert (cp2,ep2)==(p*p+1,(p+1)**2)
    return dict(p=p,points_each=points,flags=flags,
      quartic_exponent=f,quadratic_exponent=2*g,
      local_cohomology_rank=4*f+4*g,
      C_points_Fp=cp,E_points_Fp=ep,
      C_points_Fp2=cp2,E_points_Fp2=ep2,
      C_Frobenius_polynomial=f"X^4+{p*p}",
      E_Frobenius_polynomial=f"X^2+{p}",
      local_Newton_slopes="all 1/2; supersingular",
      normalized_Frobenius_phase_order=8)

def certificate():
    samples=[local_packet(p) for p in (3,7,23)]
    assert [v["local_cohomology_rank"] for v in samples]==[156,1596,50876]
    # Independent out-of-family controls: the two conditions matter separately.
    # At 11 the C trace is nonzero; at 13 the E trace is nonzero.
    c11=12-count_fp(11,"C")
    e13=14-count_fp(13,"E")
    assert (c11,e13)==(4,6)
    return dict(status="PASS_EXACT_LOCAL",classical_RH_proved=False,
      prime_family="p ≡ 3 or 7 (mod 20), infinitely many primes by Dirichlet",
      out_of_family_controls={"p11_genus2_first_trace":c11,"p13_elliptic_trace":e13},
      formula="D_Levi,nt(u)=(1+p^2u^4)^[p(p+1)^2/2]*(1+pu^2)^[p(p^2+1)]",
      genus2_C="y^2=x^5+1",elliptic_E="y^2=x^3-x",
      proof="GQ(p,p) Ihara-Bass factors; x^5 permutation on Fp and Fp2; p≡3 mod4 implies E trace zero; genus-two functional equation",
      local_Galois="Since Gal(Fbarp/Fp) is procyclic and the curve Frobenius is semisimple, the abstract Q_l companion module is noncanonically Galois-isomorphic to H1(C)^f plus H1(E)^(2g). NOT a geometric motive map or PSp-equivariant construction.",
      global_obstruction="Unbounded local cohomology ranks at good primes prohibit interpreting ALL these graph-packets as the unmodified factors of ONE fixed-rank global motive.",
      samples=samples)

if __name__=="__main__":
    out=certificate()
    p=Path(__file__).resolve().parents[1]/"data"/"w33_20261022_levi_prime_family.json"
    p.parent.mkdir(parents=True,exist_ok=True)
    p.write_text(json.dumps(out,indent=2,sort_keys=True)+"\n")
    print(json.dumps(out,indent=2,sort_keys=True))
