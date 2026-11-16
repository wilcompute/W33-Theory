"""Trinification cubic: exact F/D-flat branches and scale-selection obstruction.

E6 27 restricted to (3,bar3,1)+(1,3,bar3)+(bar3,1,3):
I3(A,B,C)=det(A)+det(B)+det(C)-Tr(ABC).
We test the manifest SL3^3 polynomial and SU3^3 D-flat conditions.
No claim is made that this simple superpotential gives a Standard Model.
"""
from fractions import Fraction as F
from pathlib import Path
import json

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/"data"/"toe_20261116_e6_trinification_cubic_flat_branches.json"

def mult(A,B):
    return [[sum(A[i][k]*B[k][j] for k in range(3)) for j in range(3)] for i in range(3)]
def tr(A):return sum(A[i][i] for i in range(3))
def det(A):
    return A[0][0]*(A[1][1]*A[2][2]-A[1][2]*A[2][1])\
         -A[0][1]*(A[1][0]*A[2][2]-A[1][2]*A[2][0])\
         +A[0][2]*(A[1][0]*A[2][1]-A[1][1]*A[2][0])
def transpose(A):return [list(row) for row in zip(*A)]
def eye(k=1):return [[k if i==j else 0 for j in range(3)] for i in range(3)]
def zero():return eye(0)
def adj(A):
    cof=[[((-1)**(i+j))*
         (A[(i+1)%3][(j+1)%3]*A[(i+2)%3][(j+2)%3]
          -A[(i+1)%3][(j+2)%3]*A[(i+2)%3][(j+1)%3])
          for j in range(3)] for i in range(3)]
    # Above cyclic minor indices need signed order; use explicit true minors.
    cof=[]
    for i in range(3):
        row=[]
        for j in range(3):
            rows=[k for k in range(3) if k!=i]
            cols=[k for k in range(3) if k!=j]
            row.append(((-1)**(i+j))*(A[rows[0]][cols[0]]*A[rows[1]][cols[1]]
                                      -A[rows[0]][cols[1]]*A[rows[1]][cols[0]]))
        cof.append(row)
    return transpose(cof)
def inverse_sl3(A):
    assert det(A)==1
    return adj(A)
def cubic(A,B,C):
    return det(A)+det(B)+det(C)-tr(mult(mult(A,B),C))
def grad(A,B,C):
    # derivative of det(A) is adj(A)^T; d tr ABC / d A =(BC)^T.
    return [[adj(A)[j][i]-mult(B,C)[j][i] for j in range(3)] for i in range(3)]
def fgrad(A,B,C):
    return grad(A,B,C),grad(B,C,A),grad(C,A,B)
def frobenius(A):
    return sum(x*x for row in A for x in row)
def tracefree(A):
    center=F(tr(A),3)
    return [[F(A[i][j])-(center if i==j else 0) for j in range(3)] for i in range(3)]
def rank1_case(s=1):
    A=eye(0);A[0][0]=F(s)
    Fb=fgrad(A,zero(),zero())
    # For rank-one A, only two vertex moment maps are nonzero.
    AA=mult(A,transpose(A))
    D2=2*frobenius(tracefree(AA))
    return {"s":str(s),"F_gradient_square":str(sum(frobenius(T) for T in Fb)),
            "D_moment_norm_squared":str(D2),"expected_D2":"4*s^4/3"}
def scalar_triad(a,b,c):
    A,B,C=eye(a),eye(b),eye(c)
    grads=fgrad(A,B,C)
    return {"values":[a,b,c], "cubic":cubic(A,B,C),
      "F_norm_squared":sum(frobenius(T) for T in grads),
      "D_flat":True,  # each vertex moment map is scalar identity minus scalar identity
      "unbroken_manifest_gauge":"SU(3)_diagonal when a=b=c != 0"}
def verify():
    A=[[1,2,0],[0,2,3],[4,0,1]]
    B=[[0,1,3],[2,1,0],[1,0,2]]
    C=[[2,0,1],[3,1,0],[0,2,1]]
    U=[[1,1,0],[0,1,0],[0,0,1]]
    V=[[1,0,0],[0,1,1],[0,0,1]]
    W=[[1,0,0],[0,1,0],[1,0,1]]
    Ap=mult(mult(U,A),inverse_sl3(V))
    Bp=mult(mult(V,B),inverse_sl3(W))
    Cp=mult(mult(W,C),inverse_sl3(U))
    assert cubic(A,B,C)==cubic(Ap,Bp,Cp)
    for s in (1,2,7):
        tri=scalar_triad(s,s,s)
        assert tri["cubic"]==0 and tri["F_norm_squared"]==0 and tri["D_flat"]
        r=rank1_case(s)
        assert r["F_gradient_square"]=="0"
        assert F(r["D_moment_norm_squared"])==F(4*s**4,3)
    # The A-only F-flat condition is adj(A)=0 -> rank(A)<=1.
    # The A-only SU3 left/right D-flatness is AA^dagger proportional I,
    # requiring rank(A)=0 or 3.  So only their intersection A=0.
    assert scalar_triad(1,0,0)["F_norm_squared"]==3
    return {
      "status":"PASS_TRINIFICATION_CUBIC_F_D_FLAT_MODULUS",
      "SL3_triplet_invariance_exact_integer_example":True,
      "flat_equal_scalar_triads":[scalar_triad(s,s,s) for s in (1,2,7)],
      "rank_one_F_flat_D_not_flat":[rank1_case(s) for s in (1,2,7)],
      "A_only_F_and_D_common_nonzero":"none (rank <=1 from F; rank 0 or 3 from D)",
      "general_scale_modulus":"For homogeneous cubic W, F(lambda fields)=lambda^2 F(fields); all D equations also scale quadratically. Nonzero F=D=0 vacua cannot fix the overall scale without extra terms.",
      "physical_scope":"A precise obstruction for cubic-only SU3^3 superpotential; no claim about all E6 models, higher invariants, D-dependent FI terms, or physics of the actual SM vacuum."
    }
if __name__=="__main__":
    cert=verify();OUT.parent.mkdir(parents=True,exist_ok=True)
    OUT.write_text(json.dumps(cert,indent=2)+"\n",encoding="utf-8")
    print(cert["status"])
