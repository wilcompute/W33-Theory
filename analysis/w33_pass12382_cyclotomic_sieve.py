"""Exact exclusions by finite-field quadratic elimination and cyclotomic recheck.

If Q vanishes in Z[zeta_n], it vanishes under every good reduction zeta_n->r.
Enumerate n^3 triples, solve Q as a quadratic in the fourth coordinate mod p,
and retain only roots in mu_n. Nonzero reductions certify exclusion. A second
prime rejects spurious survivors; final candidates are checked in Q[x]/Phi_n.
This certifies the declared grids only, not all 464 candidate orders.
"""
from pathlib import Path
from itertools import product
from math import gcd
import json,sys,hashlib,time
import numpy as np
import sympy as s

def field(n,start):
    p=int(s.nextprime(start))
    while (p-1)%n or p%4!=3:p=int(s.nextprime(p))
    primitive=int(s.primitive_root(p));r=pow(primitive,(p-1)//n,p)
    assert pow(r,n,p)==1 and all(pow(r,n//q,p)!=1 for q in s.factorint(n))
    return p,r

def pow_array(a,e,p):
    result=np.ones_like(a);base=a%p
    while e:
        if e&1:result=result*base%p
        base=base*base%p;e//=2
    return result

def residues(points,n,p,r):
    roots=np.array([pow(r,i,p) for i in range(n)],dtype=np.int64)
    a,b,c,d=roots[np.asarray(points,dtype=np.int64)].T
    return (5*a*a-5*a*b+a*c-6*a*d+5*b*b-5*b*c+6*b*d-6*b+5*c*c-6*c*d+6*d*d-6*d+6)%p

def census(n):
    assert n%4!=0
    p,r=field(n,1000000);q,t=field(n,p+10000)
    roots=np.array([pow(r,i,p) for i in range(n)],dtype=np.int64)
    order=np.argsort(roots);sorted_roots=roots[order]
    bc=np.array(list(product(range(n),repeat=2)),dtype=np.int64)
    hits=[];inverse=pow(12,-1,p)
    for i in range(n):
        a=roots[i];b=roots[bc[:,0]];c=roots[bc[:,1]]
        B=(-6*a+6*b-6*c-6)%p
        C=(5*a*a-5*a*b+a*c+5*b*b-5*b*c-6*b+5*c*c+6)%p
        D=(B*B-24*C)%p;root=pow_array(D,(p+1)//4,p);valid=root*root%p==D
        for sign in [1,-1]:
            z=(-B+sign*root)*inverse%p;ix=np.searchsorted(sorted_roots,z);ix=np.minimum(ix,n-1)
            good=valid&(sorted_roots[ix]==z)
            for j in np.flatnonzero(good):hits.append([i,int(bc[j,0]),int(bc[j,1]),int(order[ix[j]])])
    first=sorted({tuple(v) for v in hits});second=[]
    if first:
        vals=residues(first,n,q,t)
        second=[list(v) for v,z in zip(first,vals) if z==0]
    x=s.Symbol('x');phi=s.Poly(s.cyclotomic_poly(n,x),x);exact=[]
    for v in second:
        a,b,c,d=[x**j for j in v]
        Q=5*a*a-5*a*b+a*c-6*a*d+5*b*b-5*b*c+6*b*d-6*b+5*c*c-6*c*d+6*d*d-6*d+6
        if s.rem(Q,phi.as_expr(),x)==0:exact.append(v)
    return {'n':n,'characters_certified':n**4,'quadratic_triples':n**3,
            'primes_and_primitive_roots':[[p,r],[q,t]],'first_prime_survivors':len(first),
            'second_prime_survivors':len(second),'exact_h_exponents':exact,
            'exact_orders':sorted({n//gcd(n,gcd(gcd(v[0],v[1]),gcd(v[2],v[3]))) for v in exact})}

def run(orders,target):
    out={'method':'Exact finite-field elimination followed by exact cyclotomic remainders','orders':[],
         'scope':'Complete declared grids; no claim of complete464-order classification',
         'producer_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
    for n in orders:
        start=time.time();row=census(n);row['elapsed_seconds']=time.time()-start;out['orders'].append(row)
        Path(target).write_text(json.dumps(out,indent=2)+'\n');print(n,len(row['exact_h_exponents']),row['elapsed_seconds'],flush=True)
    return out

if __name__=='__main__':run([int(v) for v in sys.argv[1].split(',')],sys.argv[2])
