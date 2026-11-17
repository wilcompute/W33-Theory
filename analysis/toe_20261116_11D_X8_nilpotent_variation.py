"""Exact curvature-matrix nilpotency on AdS5 x S2 x S2 x T2.

For a product of constant-sectional-curvature blocks, the
orthonormal-frame curvature 2-form is R^a_b=K e^a wedge e^b
within each factor (and zero between factors).
As a MATRIX of differential forms, (R wedge R)^a_c=0
identically because every summand contains e^b twice.

Consequences, for any first-order perturbation delta R:
 tr R0^2 = tr R0^4 = 0;
 delta tr R^4 = 4 tr R0^3 deltaR = 0;
 delta [(tr R^2)^2]=0 because tr R0^2=0.
Thus X8(R0)=0 and delta X8(R0)=0 for ALL first
curvature variations, not only radius-preserving variations.
This does NOT imply delta^2 X8=0, nor that the full
R^4+G4 mixed eight-derivative action has no effects.

This program verifies curvature 2-form wedge nilpotency
exactly via integer bitset exterior algebra, not a
floating point Riemann contraction proxy.
"""
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/"data"/"toe_20261116_11D_X8_linear_variation_nilpotent.json"
N=11
BLOCKS=[(tuple(range(0,5)),-1),(tuple(range(5,7)),6),
        (tuple(range(7,9)),6),(tuple(range(9,11)),0)]
def wedge_mask(u,v):
    if u & v:return None
    crossings=sum((v & ((1<<i)-1)).bit_count() for i in range(N) if u & (1<<i))
    return (-1 if crossings%2 else 1),u|v
def wedge(A,B):
    out={}
    for u,x in A.items():
        for v,y in B.items():
            t=wedge_mask(u,v)
            if t is None:continue
            s,w=t
            out[w]=out.get(w,0)+s*x*y
    return {w:v for w,v in out.items() if v}
def form(i,j):
    t=wedge_mask(1<<i,1<<j)
    return {} if t is None else {t[1]:t[0]}
def curvature():
    R=[[{} for _ in range(N)] for _ in range(N)]
    for block,K in BLOCKS:
        for a in block:
            for b in block:
                if a!=b and K:R[a][b]={mask:K*val for mask,val in form(a,b).items()}
    return R
def multiply(A,B):
    C=[[{} for _ in range(N)] for _ in range(N)]
    for a in range(N):
        for b in range(N):
            if not A[a][b]:continue
            for c in range(N):
                if B[b][c]:
                    for w,v in wedge(A[a][b],B[b][c]).items():
                        C[a][c][w]=C[a][c].get(w,0)+v
    return [[{w:v for w,v in C[a][c].items() if v}
           for c in range(N)] for a in range(N)]
def trace(A):
    s={}
    for i in range(N):
        for w,v in A[i][i].items():
            s[w]=s.get(w,0)+v
    return {w:v for w,v in s.items() if v}
def verify():
    R=curvature()
    RR=multiply(R,R)
    assert all(not z for row in RR for z in row)
    assert trace(RR)=={}
    # Perturb two antisymmetric curvature entries by algebraic 2forms.
    # They are arbitrary so only demonstrate that delta trR²
    # is NOT universally zero; not a physical Riemann variation.
    D=[[{} for _ in range(N)] for _ in range(N)]
    for a,b,u,v in [(0,1,2,3),(5,6,7,8)]:
        D[a][b]=form(u,v)
        D[b][a]={w:-z for w,z in form(u,v).items()}
    linear_R2=trace(multiply(R,D))
    linear_R2_second=trace(multiply(D,R))
    total={}
    for F in (linear_R2,linear_R2_second):
        for mask,c in F.items():total[mask]=total.get(mask,0)+c
    assert total and linear_R2==linear_R2_second
    # d/dt trace(R+tD)^4 = 4 trace(R^3 D) =0
    # since R^2=0 identically.
    assert all(not x for row in multiply(RR,R) for x in row)
    assert wedge(trace(RR),total)=={}
    # Although dX8=0, its quadratic variation NEED NOT vanish.
    # The d(trR²) wedge d(trR²) part is nonzero in this toy
    # 2-form variation, so cannot set X8 fluctuations to zero.
    second_trR2sq=wedge(total,total)
    assert second_trR2sq
    return {"status":"PASS_11D_X8_FIRST_VARIATION_EXACT_ZERO",
      "factors":[{"dimension":len(ids),"sectional_curvature_Lminus2":K} for ids,K in BLOCKS],
      "matrix_curvature_wedge_square_zero":True,
      "pointwise_tr_R2_and_tr_R4_zero":True,
      "first_variation_tr_R4_zero":True,
      "first_variation_of_X8_zero_for_arbitrary_deltaR":True,
      "sample_delta_tr_R2_nonzero":True,
      "sample_delta_tr_R2_squared_nonzero":True,
      "example_delta_tr_R2":{str(mask):c for mask,c in total.items()},
      "example_wedge_square":{str(mask):c for mask,c in second_trR2sq.items()},
      "local_C3_X8_consequence":"No background X8 and no deltaC3 wedge deltaX8 quadratic mixed term in local fluctuation expansion. But background C3 wedge delta²X8 may contribute, and full supersymmetric R4/flux terms certainly need calculation.",
      "global_and_physical_caveat":"This is an exact exterior-algebra identity for the unwarped constant-curvature product. The sample deltaR is algebraic and not asserted to be a realizable linearized Levi-Civita curvature; no 11D corrected KK eigenmass is derived."}
if __name__=="__main__":
    z=verify();OUT.parent.mkdir(parents=True,exist_ok=True)
    OUT.write_text(json.dumps(z,indent=2,sort_keys=True)+"\n",encoding="utf8")
    print(z["status"],z["example_delta_tr_R2"])
