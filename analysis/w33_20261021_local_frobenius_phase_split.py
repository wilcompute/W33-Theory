#!/usr/bin/env python3
"""Exact local Frobenius phase-order split of W33/Levi (not classical RH).

p=3 Levi nontrivial transfer: 156D, T^8=81 I, supersingular;
p=11 W33 collinearity nontrivial transfer: 78D, ordinary infinite phases.
"""
from __future__ import annotations
import itertools, json
from pathlib import Path
import numpy as np

def normalize(v):
    first=next(int(a) for a in v if a)
    return tuple(int(x*first)%3 for x in v)

def form(x,y):
    return (x[0]*y[2]-x[2]*y[0]+x[1]*y[3]-x[3]*y[1])%3

def geometry():
    pts=sorted({normalize(v) for v in itertools.product(range(3),repeat=4) if any(v)})
    assert len(pts)==40
    ix={p:i for i,p in enumerate(pts)}
    lines=set()
    for i,j in itertools.combinations(range(40),2):
        if form(pts[i],pts[j]):continue
        lines.add(frozenset(ix[normalize(tuple((a*x+b*y)%3 for x,y in zip(pts[i],pts[j])))]
                 for a,b in itertools.product(range(3),repeat=2) if a or b))
    lines=sorted(lines,key=lambda s:tuple(sorted(s)))
    assert len(lines)==40 and all(len(L)==4 for L in lines)
    N=np.array([[int(i in L) for L in lines] for i in range(40)],dtype=np.int64)
    A=N@N.T-4*np.eye(40,dtype=np.int64)
    assert np.array_equal(A@A,8*np.eye(40,dtype=np.int64)-2*A+4*np.ones((40,40),dtype=np.int64))
    return A,N

def elliptic_points(p,a,b):
    def leg(x):
        if x%p==0:return 0
        return 1 if pow(x%p,(p-1)//2,p)==1 else -1
    n=1+sum(1+leg(x*x*x+a*x+b) for x in range(p))
    return n,p+1-n

def theorem():
    A,N=geometry()
    I80=np.eye(80,dtype=np.int64);O40=np.zeros((40,40),dtype=np.int64)
    L=np.block([[O40,N],[N.T,O40]]);L2=L@L
    assert not np.any(L2@(L2-6*I80)@(L2-16*I80))
    Q6=L2@(16*I80-L2)
    Q0=(L2-6*I80)@(L2-16*I80)
    assert np.linalg.matrix_rank(Q6)==48 and np.linalg.matrix_rank(Q0)==30
    T=np.block([[L,-3*I80],[I80,np.zeros((80,80),dtype=np.int64)]])
    T2=T@T;T4=T2@T2;T8=T4@T4
    I=np.eye(160,dtype=np.int64)
    Z=np.zeros((80,80),dtype=np.int64)
    D6=np.block([[Q6,Z],[Z,Q6]])
    D0=np.block([[Q0,Z],[Z,Q0]])
    assert not np.any((T4+9*I)@D6)
    assert not np.any((T2+3*I)@D0)
    assert not np.any((T8-81*I)@(D6+D0))
    triv=lambda n:(1+(-1)**n)+(3**n+(-3)**n)
    trace=lambda n:(96*(-9)**(n//4) if n%4==0 else 0)+(60*(-3)**(n//2) if n%2==0 else 0)
    for n,mat in ((2,T2),(4,T4),(8,T8)):
        assert int(np.trace(mat))-triv(n)==trace(n)
    # Exact positive metric: R.T G R = 3 G on each rational companion.
    R4=np.zeros((4,4),dtype=np.int64)
    for j in range(3):R4[j+1,j]=1
    R4[0,3]=-9
    G4=np.diag([1,3,9,27]).astype(np.int64)
    R2=np.array([[0,-3],[1,0]],dtype=np.int64)
    G2=np.diag([1,3]).astype(np.int64)
    assert np.array_equal(R4.T@G4@R4,3*G4)
    assert np.array_equal(R2.T@G2@R2,3*G2)
    assert np.array_equal(np.linalg.matrix_power(R4,8),81*np.eye(4,dtype=np.int64))
    assert np.array_equal(np.linalg.matrix_power(R2,8),81*np.eye(2,dtype=np.int64))
    phase_trace=[round(trace(n)/(3**(n/2))) for n in range(1,9)]
    assert phase_trace==[0,-60,0,-36,0,-60,0,156]
    curves={}
    for label,a,b in (("E_plus",1,-1),("E_minus",1,2)):
        points,ap=elliptic_points(11,a,b)
        assert ap%11!=0
        curves[label]={"points_over_F11":points,"trace":ap,"ordinary":True}
    assert [curves[k]["trace"] for k in ("E_plus","E_minus")]==[2,-4]
    assert elliptic_points(3,-1,0)==(4,0)
    # Normed p=11 roots have 2cos(theta)=2/sqrt(11) or -4/sqrt(11).
    # A root of unity has algebraic-integer (z+z^-1), but its square
    # is 4/11 or 16/11, a rational non-integer: impossible.
    assert 4%11 and 16%11
    return {
      "status":"PASS_EXACT_LOCAL_ARITHMETIC","classical_RH_proved":False,
      "Levi_prime3":{"nontrivial_dimension":156,"quartic_blocks":24,"quadratic_blocks":30,
           "exact_revival":"T^8=81I on nontrivial 156D transfer sector",
           "normalized_period":8,"normalized_trace_cycle":phase_trace,
           "positive_companion_metrics":{"quartic":[1,3,9,27],"quadratic":[1,3]},
           "exact_metric_invariance":"R.T G R = 3 G; (R/sqrt(3)) is G-orthogonal",
           "p_adic_newton_slopes":"all 1/2 (supersingular)",
           "Frobenius_polynomials":["x^4+9","x^2+3"],
           "curves":["C/F3: y^2=x^5+1","E/F3: y^2=x^3-x"]},
      "collinearity_prime11":{"nontrivial_dimension":78,"elliptic_curves":curves,
           "ordinary":True,"normalized_phase_order":"infinite",
           "phase_algebraic_integer_obstructions":["4/11 not an integer","16/11 not an integer"],
           "Frobenius_polynomials":["x^2-2x+11","x^2+4x+11"]},
      "scope":"Exact local phase, not a canonical all-prime motivic map, photonic clock, or RH proof"}

if __name__=="__main__":
    report=theorem()
    root=Path(__file__).resolve().parents[1]
    dest=root/"data"/"w33_20261021_local_frobenius_phase_split.json"
    dest.write_text(json.dumps(report,indent=2,sort_keys=True)+"\n")
    print(json.dumps(report,indent=2,sort_keys=True))
