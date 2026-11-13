#!/usr/bin/env python3
"""Exact quadratic-polynomial E6(6) generalized Lie closure, with
nonzero-but-trivial E-bracket Jacobiator control, extending prior affine
certificate. Implements direct polynomial algebra over Z, restricted
to maximal 5D/IIB and 6D/M coordinate sections.
"""
import json,sys
from pathlib import Path
from itertools import combinations
from collections import Counter
import numpy as np
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"analysis"))
import toe_20261113_E6_exft_generalized_closure_affine as L
OUT=ROOT/"data/toe_20261113_E6_ExFT_quadratic_closure_Jacobiator.json"

def key_add(a,b):return tuple(x+y for x,y in zip(a,b))
def key_der(a,k):
    if a[k]==0:return None
    z=list(a);z[k]-=1;return tuple(z)
def add(A,B,coeff=1):
    out={k:v.copy() for k,v in A.items()}
    for k,v in B.items():
        if k in out:out[k]+=coeff*v
        else:out[k]=coeff*v.copy()
    return {k:v for k,v in out.items() if np.any(v)}

def scalef(P,n):return {k:n*v for k,v in P.items() if n and np.any(v)}
def magnitude(P):return max((int(np.max(abs(v))) for v in P.values()),default=0)

def vector_poly(rng,n,d,terms=6):
    monoms=[]
    zero=(0,)*d
    monoms.append(zero)
    for i in range(d):
        a=list(zero);a[i]=1;monoms.append(tuple(a))
    for i in range(d):
        for j in range(i,d):
            a=list(zero);a[i]+=1;a[j]+=1
            monoms.append(tuple(a))
    out={}
    for _ in range(terms):
        m=monoms[int(rng.integers(0,len(monoms)))]
        v=np.zeros(27,dtype=np.int64)
        for _ in range(2):v[int(rng.integers(0,27))]+=int(rng.choice([-2,-1,1,2]))
        if m in out:out[m]+=v
        else:out[m]=v
    return {k:v for k,v in out.items() if np.any(v)}

def generalized(X,V,S,Y):
    # derivative tensors are small and sparse. Work with monomial
    # coefficient vectors in the full 27-dimensional value fiber.
    out={}
    def put(m,v):
        if not np.any(v):return
        if m in out:out[m]+=v
        else:out[m]=v.copy()
    for k,source in enumerate(S):
        dx=[(key_der(m,k),int(m[k])*v) for m,v in X.items() if m[k]]
        dv=[(key_der(m,k),int(m[k])*v) for m,v in V.items() if m[k]]
        for mx,x in X.items():
            for mv,v in dv:
                if x[source]:put(key_add(mx,mv),int(x[source])*v)
        for mv,v in V.items():
            for mx,x in dx:
                if v[source]:put(key_add(mx,mv),-int(v[source])*x)
        mat=Y[:,source,:,:]
        for mx,x in dx:
            Z=np.einsum("mnl,l->mn",mat,x,optimize=True)
            for mv,v in V.items():
                contrib=Z@v
                put(key_add(mx,mv),contrib)
    return {k:v for k,v in out.items() if np.any(v)}

def bracket2(X,V,S,Y):
    return add(generalized(X,V,S,Y),generalized(V,X,S,Y),-1)

def closure(X,Z,V,S,Y):
    left=add(generalized(X,generalized(Z,V,S,Y),S,Y),
             generalized(Z,generalized(X,V,S,Y),S,Y),-1)
    rhs=generalized(bracket2(X,Z,S,Y),V,S,Y)
    return add(scalef(left,2),rhs,-1)

def jacobiator4(X,Z,V,S,Y):
    return add(add(bracket2(bracket2(X,Z,S,Y),V,S,Y),
                   bracket2(bracket2(Z,V,S,Y),X,S,Y)),
               bracket2(bracket2(V,X,S,Y),Z,S,Y))

def main():
    T,Y,S5,S6=L.setup()
    rng=np.random.default_rng(2026111311)
    records={}
    for S in [S5,S6]:
        trials=10
        jacobi_nonzero=0
        for _ in range(trials):
            X=vector_poly(rng,27,len(S))
            Z=vector_poly(rng,27,len(S))
            V=vector_poly(rng,27,len(S))
            C=closure(X,Z,V,S,Y)
            assert magnitude(C)==0,("CLOSURE",S,C)
            J=jacobiator4(X,Z,V,S,Y)
            if magnitude(J):jacobi_nonzero+=1
            check=generalized(J,V,S,Y)
            assert magnitude(check)==0,("JACOBIATOR_NOT_TRIVIAL",S,check)
        records[str(len(S))]={
            "section_E6_coordinates":list(S),
            "independent_quadratic_polynomial_tests":trials,
            "closure_max_integer_residual":0,
            "nonzero_Jacobiator_observed_trials":jacobi_nonzero,
            "Jacobiator_generates_zero_gauge_action_on_test_vector":True}
    out={"status":"PASS_QUADRATIC_E6_EXFT_CLOSURE_AND_TRIVIAL_JACOBIATORS",
         "records":records,
         "identity":"2[L_X,L_Z]V=L_{L_X Z-L_Z X} V for degree<=2 parameters/vectors, polynomial coefficients checked exactly",
         "E_bracket_jacobiator":"4J=[[X,Z]_2,V]_2+cyclic; it need not vanish as a parameter but its generalized action on V must vanish",
         "scope":"Finite exact polynomial tests on representative 5/6 sections only. This is not a symbolic general proof or a derivation of ExFT equations of motion.",
         "source":"Hohm Samtleben E6(6) ExFT generalized Lie derivative and E-bracket, 2014"}
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+"\n")
    print(json.dumps({k:out[k] for k in ["status","records"]},indent=2),flush=True)
    return out
if __name__=="__main__":main()
