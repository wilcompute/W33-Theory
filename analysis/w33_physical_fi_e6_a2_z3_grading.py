#!/usr/bin/env python3
"""Physical FI projection realizes the E8 -> E6 x A2 Z3 grading.

The certified physical anomalous-U(1) generator has a projection t_A into the
flagship A5/hypercharge-organizer E8 factor.  Its hypercharge component is zero
and its A4 coefficients are (-5/3,-2/3,-1/3,-2).

This verifier exponentiates that *recorded physical projection* as an E8 Cartan
element.  It proves that it has order three in the adjoint action and that its
root grading is exactly 78+81+81, with the 78 neutral roots splitting as
72(E6)+6(A2).  Thus the long-standing abstract E6 x A2 grading in W33 receives
an explicit physical-FI Cartan representative.

Scope: this concerns the organizer-E8 projection t_A, not the other-E8
component of the full anomalous generator and not a solved D/F-flat vacuum.
"""
from __future__ import annotations
import itertools,json
from collections import Counter
from fractions import Fraction as F
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/"data/w33_physical_fi_e6_a2_z3_grading.json"

A4=(
 (F(0),F(0),F(0),F(-1),F(0),F(1),F(0),F(0)),
 (F(-1,2),F(1,2),F(1,2),F(1,2),F(-1,2),F(-1,2),F(-1,2),F(1,2)),
 (F(0),F(0),F(0),F(0),F(1),F(0),F(1),F(0)),
 (F(1,2),F(-1,2),F(-1,2),F(-1,2),F(-1,2),F(-1,2),F(-1,2),F(1,2)),
)
COEFF=(F(-5,3),F(-2,3),F(-1,3),F(-2))

def dot(a,b):return sum(x*y for x,y in zip(a,b))
def lin(B,c):return tuple(sum(c[i]*B[i][j] for i in range(len(B))) for j in range(len(B[0])))
def roots_e8():
    out=[]
    for i,j in itertools.combinations(range(8),2):
        for a in (1,-1):
            for b in (1,-1):
                v=[F(0)]*8;v[i]=F(a);v[j]=F(b);out.append(tuple(v))
    for s in itertools.product((1,-1),repeat=8):
        if sum(x<0 for x in s)%2==0:out.append(tuple(F(x,2) for x in s))
    assert len(out)==len(set(out))==240
    return out
def matrix_rank(rows):
    A=[list(map(F,r)) for r in rows]
    if not A:return 0
    m,n=len(A),len(A[0]);rr=0
    for c in range(n):
        p=next((i for i in range(rr,m) if A[i][c]),None)
        if p is None:continue
        A[rr],A[p]=A[p],A[rr];z=A[rr][c]
        A[rr]=[x/z for x in A[rr]]
        for i in range(m):
            if i!=rr and A[i][c]:
                z=A[i][c];A[i]=[A[i][j]-z*A[rr][j] for j in range(n)]
        rr+=1
    return rr
def root_components(R):
    adj=[set() for _ in R]
    for i,j in itertools.combinations(range(len(R)),2):
        if dot(R[i],R[j])!=0:
            adj[i].add(j);adj[j].add(i)
    seen=set();out=[]
    for i in range(len(R)):
        if i in seen:continue
        todo=[i];seen.add(i);cc=[]
        while todo:
            x=todo.pop();cc.append(x)
            for y in adj[x]:
                if y not in seen:seen.add(y);todo.append(y)
        roots=[R[k] for k in cc]
        out.append((len(roots),matrix_rank(roots)))
    return sorted(out)
def standard_a4_diagonal(pairings):
    # h_i-h_{i+1}=pairing_i, sum h_i=0.
    offs=[F(0)]
    for p in pairings:offs.append(offs[-1]-p)
    x=-sum(offs)/5
    return tuple(x+o for o in offs)

def main(write=True):
    t=lin(A4,COEFF)
    assert dot(t,t)==F(32,3)
    pairings=tuple(dot(t,a) for a in A4)
    assert pairings==(F(-8,3),F(2,3),F(2),F(-11,3))
    h=standard_a4_diagonal(pairings)
    assert h==(F(-5,3),F(1),F(1,3),F(-5,3),F(2))
    assert tuple(3*x for x in h)==(-5,3,1,-5,6)
    phases=tuple(x%1 for x in h)
    assert Counter(phases)=={F(1,3):3,F(0):2}

    R=roots_e8()
    grades=Counter(dot(t,r)%1 for r in R)
    assert grades=={F(0):78,F(1,3):81,F(2,3):81}
    neutral=[r for r in R if dot(t,r)%1==0]
    comps=root_components(neutral)
    assert comps==[(6,2),(72,6)]
    assert matrix_rank(neutral)==8

    # Restrict to the organizer A4 root subsystem.
    # Its roots are exactly the roots in span(A4), equivalently those generated
    # by the A4 simple roots. A root lies in that span iff its orthogonal
    # projection residual is zero; here rank membership suffices exactly.
    a4roots=[]
    for r in R:
        if matrix_rank(list(A4)+[r])==4:a4roots.append(r)
    assert len(a4roots)==20
    a4grades=Counter(dot(t,r)%1 for r in a4roots)
    assert a4grades=={F(0):8,F(1,3):6,F(2,3):6}
    assert root_components([r for r in a4roots if dot(t,r)%1==0])==[(2,1),(6,2)]

    out={
      "schema":"w33.physical_fi_e6_a2_z3_grading.v1",
      "status":"PASS_PHYSICAL_FI_REALIZES_E6_A2_Z3_GRADING",
      "headline":"The physical FI projection t_A exponentiates to an order-three inner Cartan action on the organizer E8. Its 240 roots grade exactly 78+81+81; the 78 neutral roots split into connected root systems 72(rank6)+6(rank2), hence E6+A2. On the organizer A4 itself the same element has defining phases 3+2 and root grading 8+6+6, giving centralizer A2+A1+u(1). Thus the physical FI ray supplies an explicit Cartan representative of the repository's canonical E8 -> E6 x A2 Z3 grading.",
      "physical_FI_projection":{
        "A4_coefficients":[str(x) for x in COEFF],
        "E8_coordinates":[str(x) for x in t],"norm2":"32/3",
        "A4_simple_pairings":[str(x) for x in pairings],
        "standard_A4_diagonal":[str(x) for x in h],
        "three_times_diagonal":[int(3*x) for x in h]},
      "organizer_SU5":{
        "defining_phase_multiplicities":{"omega":3,"one":2},
        "root_grades":{"0":8,"1/3":6,"2/3":6},
        "neutral_root_components":[{"roots":6,"rank":2,"type":"A2"},{"roots":2,"rank":1,"type":"A1"}],
        "connected_centralizer":"S(U(3)xU(2)) up to the standard finite quotient",
        "lie_dimension":12},
      "E8":{
        "root_grades":{"0":78,"1/3":81,"2/3":81},
        "neutral_root_components":[{"roots":72,"rank":6,"type":"E6"},{"roots":6,"rank":2,"type":"A2"}],
        "fixed_lie_algebra":"E6 + A2","fixed_dimension":86,
        "adjoint_branching":"248=(78,1)+(1,8)+(27,3)+(27bar,3bar)"},
      "bridge_to_existing_W33":"The repo already has an abstract/canonical 240=72+6+81+81 E6+A2 root refinement. This theorem identifies a concrete physically measured anomalous-U(1) FI projection whose inner Z3 grading realizes exactly that pattern.",
      "boundary":"The full anomalous generator also has a nonzero component in the other E8 factor. This theorem concerns only its certified A5-organizer-factor projection t_A. Exponentiating the charge generator is a Lie-theoretic grading construction; it is not a proof that the FI vacuum dynamically turns on this holonomy, and it does not solve D/F flatness.",
      "checks":{"physical_star_recovered":True,"order3_phase_3_plus_2":True,
        "organizer_A4_grades_8_6_6":True,"all_E8_grades_78_81_81":True,
        "neutral_components_E6_A2":True,"adjoint_dimension_248":78+8+81+81==248}}
    if write:OUT.write_text(json.dumps(out,indent=2)+"\n")
    print(json.dumps(out,indent=2));return out
if __name__=="__main__":main(True)
