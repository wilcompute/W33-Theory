#!/usr/bin/env python3
"""Odd-prime Weyl transvection theorem + exact W33/Holotrade ABI bridge.

THEOREM (algebraic, not empirical). Let p be any odd prime, V=F_p^(2n) with
standard symplectic form <.,.>, h=2^{-1} mod p, and choose the Weyl convention

    D_(q,r) = omega^(h q.r) X^q Z^r.

Then

    D_u D_v = omega^(-h<u,v>) D_(u+v),
    D_v^k = D_(kv),                 D_v^dag = D_(-v).

For lambda != 0 and the transvection

    T_(v,lambda)(x) = x + lambda <x,v> v,

put a=-(2 lambda)^(-1) and

    G_(v,lambda) = p^(-1/2) sum_k omega^(a k^2) D_(kv).

Then G is unitary and

    G D_x G^dag = D_(T_(v,lambda)x)

with zero residual Weyl/Pauli phase, for every n and every odd prime p.

PROOF. Weyl multiplication follows by commuting Z^r through X^q and using
1-h=h because 2h=1. Hence D_(kv) D_x = omega^(k<x,v>) D_x D_(kv). Writing
s=<x,v> and m=lambda s,

  G D_x = D_x sum_j c_j omega^(js) D_(jv)
  D_(x+mv) G = omega^(h lambda s^2) D_x sum_j c_(j-m) D_(jv).

The coefficients agree identically because, for c_j=omega^(a j^2),

    -2 a lambda = 1,
    h lambda + a lambda^2 = 0.

For unitarity, on a D_v eigenvalue omega^r the scalar is the normalized
quadratic Gauss sum p^(-1/2) sum_k omega^(a k^2+r k). Its squared modulus is
p^(-1) sum_(k,l) omega^(a(k^2-l^2)+r(k-l)); writing d=k-l, the inner sum over
l vanishes for every d!=0 because 2ad!=0 in odd characteristic, leaving only
d=0 and norm one. No classification theorem is required.

CROSS-REPO ABI. W33's existing qutrit implementation uses spectral calculus

    U_spec = sum_r omega^(h lambda r^2) P_r(D_v),
    P_r(D_v)=p^-1 sum_t omega^(-rt) D_(tv).

Completing the square gives

    h lambda r^2-r t = h lambda (r-t/lambda)^2 - h t^2/lambda,

so

    U_spec = gamma_p(lambda) G_(v,lambda),
    gamma_p(lambda)=p^-1/2 sum_r omega^(h lambda r^2).

Thus the W33 spectral lift and Holotrade's direct Weyl Gauss lift are the SAME
Clifford operator up to the explicit global Gauss phase. At p=3,n=2 this file
checks that statement for all 40 axes x 2 lambdas = 80 W33 primitive opcodes.
"""
from __future__ import annotations
import cmath,itertools,json,math,sys
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'analysis'))
import w33_qutrit_clifford_phase_displacement_lift as w33


def primes_upto(n):
    out=[]
    for x in range(3,n+1,2):
        if all(x%d for d in range(2,int(x**0.5)+1)):out.append(x)
    return out

def algebra_sanity(p):
    h=pow(2,-1,p)
    if (1-h)%p!=h:return False
    for lam in range(1,p):
        a=(-pow(2*lam,-1,p))%p
        if (-2*a*lam)%p!=1:return False
        if (h*lam+a*lam*lam)%p!=0:return False
        # Exhaustive coefficient identity over F_p; this is a finite sanity
        # check of the general symbolic cancellation in the proof above.
        for s in range(p):
            m=lam*s%p
            for j in range(p):
                lhs=(a*j*j+j*s)%p
                rhs=(h*lam*s*s+a*(j-m)*(j-m))%p
                if lhs!=rhs:return False
        # Exact character-sum cancellation encoded by exponent multiplicities:
        # for d!=0, l -> 2*a*d*l is a permutation of F_p.
        for d in range(1,p):
            if len({(2*a*d*l)%p for l in range(p)})!=p:return False
    return True

def cmatmul(A,B):
    return tuple(tuple(sum(A[i][k]*B[k][j] for k in range(len(B))) for j in range(len(B[0]))) for i in range(len(A)))
def cadd(*As):
    return tuple(tuple(sum(A[i][j] for A in As) for j in range(len(As[0][0]))) for i in range(len(As[0])))
def cscale(z,A):return tuple(tuple(z*x for x in r) for r in A)
def normalize_global(A):
    flat=[x for r in A for x in r];i=next(i for i,x in enumerate(flat) if abs(x)>1e-9);z=flat[i]/abs(flat[i]);return cscale(z.conjugate(),A)
def close(A,B,tol=1e-8):return max(abs(A[i][j]-B[i][j]) for i in range(len(A)) for j in range(len(A[0])))<tol

def direct_gauss(v,lam):
    p=w33.Q;h=pow(2,-1,p);a=(-pow(2*lam,-1,p))%p;D=w33.weyl(v);powers=[w33.eye()]
    for _ in range(1,p):powers.append(cmatmul(powers[-1],D))
    U=tuple(tuple(0j for _ in range(w33.DIM)) for _ in range(w33.DIM))
    for k in range(p):U=cadd(U,cscale((w33.OMEGA**((a*k*k)%p))/math.sqrt(p),powers[k]))
    return U

def gauss_phase(lam):
    p=w33.Q;h=pow(2,-1,p)
    return sum(w33.OMEGA**((h*lam*r*r)%p) for r in range(p))/math.sqrt(p)

def q3_bridge():
    rows=[];all_ok=True
    for axis,v in enumerate(w33.GEOMETRY.points):
        for lam in (1,2):
            S=w33.transvection_unitary(v,lam);G=direct_gauss(v,lam);gam=gauss_phase(lam)
            exact=close(S,cscale(gam,G));projective=close(normalize_global(S),normalize_global(G));unit=abs(abs(gam)-1)<1e-8
            ok=exact and projective and unit;all_ok&=ok
            rows.append({'axis':axis,'lambda':lam,'gaussPhaseReal':round(gam.real,12),'gaussPhaseImag':round(gam.imag,12),'exactAfterGaussPhase':exact,'sameModuloGlobalPhase':projective})
    return all_ok,rows

def main():
    tested=primes_upto(43);sanity={str(p):algebra_sanity(p) for p in tested};bridge,rows=q3_bridge()
    checks={
      'generic_algebra_sanity_all_odd_primes_through_43':all(sanity.values()),
      'w33_q3_all_80_equal_direct_gauss_up_to_explicit_global_phase':bridge,
      'w33_q3_gauss_phase_has_unit_norm':all(abs(r['gaussPhaseReal']**2+r['gaussPhaseImag']**2-1)<1e-9 for r in rows),
      'all_80_w33_primitive_opcodes_checked':len(rows)==80,
    }
    out={
      'schema':'w33.odd-prime-weyl-transvection-theorem.v1','status':'PASS' if all(checks.values()) else 'FAIL','checks':checks,
      'theorem':{'scope':'all odd primes p, arbitrary n','weyl':'D_(q,r)=omega^(2^-1 q.r) X^q Z^r','transvection':'T(x)=x+lambda<x,v>v','directGaussCoefficient':'a=-(2 lambda)^-1','unitaryAndExactConjugation':True,'proofMethod':'coefficient cancellation plus exact quadratic-character orthogonality; see module docstring'},
      'crossRepoABI':{'statement':'W33 spectral transvection lift = explicit normalized quadratic Gauss phase times the direct Weyl Gauss lift used by Holotrade','p':3,'n':2,'primitiveOpcodes':80,'allVerified':bridge,'rows':rows},
      'finiteSanityPrimes':sanity,
      'boundary':'The theorem is algebraic for odd prime fields. Composite dimensions/rings and characteristic two require separate treatment. The p=3,n=2 numerical matrices verify the existing W33 implementation, not the general proof.'
    }
    if '--write' in sys.argv:(ROOT/'data'/'w33_odd_prime_weyl_transvection_theorem.json').write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
    print(json.dumps(out,indent=2,sort_keys=True));return 0 if out['status']=='PASS' else 1
if __name__=='__main__':raise SystemExit(main())
