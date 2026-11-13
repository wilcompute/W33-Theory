#!/usr/bin/env python3
"""Exact Clifford-conjugate qutrit CCZ normal form of the 27-state chiral gate.

New relative to previous chiral gate: one CCZ suffices, and is necessary
when Cliffords are otherwise free. All algebraic identities are checked
over F3 or Z[omega], independent of numerical eigensolvers.

Prior repo searched: Pass11549, Pass20261108, Pass10941, TOE41 E6 CCZ,
Pass11266; none is to be conflated with this 27-state clock.
"""
from __future__ import annotations
from collections import Counter
from itertools import product
import json,sys,math
from pathlib import Path
import numpy as np
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"analysis"))
import toe_20261113_chiral_null_order3_gate as C
OUT=ROOT/"data/toe_20261113_ccz_clifford_normalform.json"
V=C.V
ID=C.VID
L=np.array([[1,0,1],[1,2,2],[1,1,2]],dtype=int)

def phase(k):
    a,b,c=k
    return (a+c)*(1-a*c-b*b)%3

def transform(k):
    return tuple(int(z) for z in (L@np.asarray(k,dtype=int))%3)

def unique_polynomial(fvals):
    exps=V
    aug=np.array([[math.prod(pow(k[j],e[j],3) for j in range(3))%3
                   for e in exps]+[int(fvals[i])]
                  for i,k in enumerate(V)],dtype=int)
    row=0
    for j in range(27):
        possible=[i for i in range(row,27) if aug[i,j]%3]
        assert possible
        pivot=possible[0]
        aug[[row,pivot]]=aug[[pivot,row]]
        aug[row]=(aug[row]*pow(int(aug[row,j]),-1,3))%3
        for i in range(27):
            if i!=row and aug[i,j]%3:
                aug[i]=(aug[i]-aug[i,j]*aug[row])%3
        row+=1
    assert np.array_equal(aug[:,:27],np.eye(27,dtype=int))
    return [{"powers":list(e),"coefficient_mod3":int(t),"total_degree":sum(e)}
            for e,t in zip(exps,aug[:,-1]) if t%3]

def verify():
    _,_,D=C.build()
    I=np.eye(27,dtype=np.int64)
    X=18*I+3*D+D@D
    assert not np.any(X%2)
    M=X//2
    assert np.array_equal(M.T@M,81*I)
    assert int(round(np.linalg.det(L)))%3==1
    assert len({transform(k) for k in V})==27
    fvals=[phase(k) for k in V]
    assert Counter(fvals)==Counter({0:19,1:4,2:4})
    # In F3 every value satisfies u^3=u.  Thus
    # (a+c)(1-ac-b²) = (a+c)(a-c-b)(a-c+b).
    for k in V:
        u,v,w=transform(k)
        assert phase(k)==u*v*w%3
    terms=unique_polynomial(fvals)
    assert max(t["total_degree"] for t in terms)==3
    # Exact ring Z[omega], omega^2=-1-omega:
    # for Fourier character k, first row sum M[0,x]*omega^(k.x)
    # must be 9*omega^f(k), with integer coeff pair (1,omega).
    exact_pairs={0:(9,0),1:(0,9),2:(-9,-9)}
    for k in V:
        coeff=[0,0,0]
        for x in V:
            coeff[sum(a*b for a,b in zip(k,x))%3]+=int(M[0,ID[x]])
        got=(coeff[0]-coeff[2],coeff[1]-coeff[2])
        assert got==exact_pairs[phase(k)],(k,got)
    # All rows follow from the Cayley convolution translation symmetry.
    # Numerical independent 27x27 reconstruction tests the Clifford circuit.
    omega=np.exp(2j*np.pi/3)
    Fourier=np.array([[omega**(sum(a*b for a,b in zip(x,k))%3)
                       for k in V] for x in V],dtype=complex)/math.sqrt(27)
    assert np.max(abs(Fourier.conj().T@Fourier-I))<1e-14
    P=np.zeros((27,27),dtype=complex)
    for k in V:P[ID[transform(k)],ID[k]]=1
    assert np.array_equal(P.T@P,I)
    ccz=np.diag([omega**(math.prod(k)%3) for k in V])
    compiled=Fourier@P.conj().T@ccz@P@Fourier.conj().T
    error=float(np.max(np.abs(compiled-M/9)))
    assert error<2e-14,error
    # Degree-three phase -> third Clifford-hierarchy level (C3),
    # and a genuine cubic term rules out membership of Clifford C2.
    # Translations x->x+e_j have degree<=2 phase differences.
    for j in range(3):
        diff=[(phase(tuple((k[t]+(t==j))%3 for t in range(3)))-phase(k))%3
              for k in V]
        assert max(t["total_degree"] for t in unique_polynomial(diff))<=2
    out={"schema":"toe.qutrit_ccz_chiral_clock.v1",
         "status":"PASS_EXACT_SINGLE_CCZ_CLIFFORD_NORMAL_FORM",
         "original_gate":"U=(18I+3D+D²)/18 on Sym2(F3)",
         "clock_D_cubic":"D³=-27D",
         "phase_polynomial":"f(a,b,c)=(a+c)(1-ac-b²)=(a+c)(a-c-b)(a-c+b) mod3",
         "phase_value_counts":{str(k):v for k,v in Counter(fvals).items()},
         "fourier": "F[x,k]=omega^(k dot x)/sqrt(27)",
         "linear_map_mod3":L.tolist(),"linear_map_det_mod3":1,
         "ccz":"diag(omega^(uvw))",
         "compiler":"U=F P_L^dagger CCZ P_L F^dagger; P_L|k>=|Lk>",
         "ccz_count":1,"ccz_count_optimal_with_free_cliffords":True,
         "hierarchy_level":3,"nonclifford":True,
         "cyclotomic_integer_eigenmode_checks":27,
         "unique_polynomial_terms":terms,
         "numeric_max_matrix_error":error,
         "scope":"one mathematical qutrit CCZ resource; not a native optical implementation, spacetime derivation, or fault-tolerant logical gate"}
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+"\n",encoding="utf-8")
    return out
if __name__=="__main__":
    r=verify()
    print(json.dumps({k:r[k] for k in ("status","phase_polynomial","ccz_count","hierarchy_level","cyclotomic_integer_eigenmode_checks","numeric_max_matrix_error")},indent=2))
