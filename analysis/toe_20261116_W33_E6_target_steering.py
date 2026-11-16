#!/usr/bin/env python3
"""Universal exact TARGET-STATE steering via the 4-copy W33->27 Kraus map.

Any normalized desired cubic-line ket y has an explicitly constructible
normalized four-photon antecedent K† H^{-1}y / sqrt(y†H^{-1}y),
H=K K†>0. Its exact success probability is
1/(y† H^{-1} y) >= 28/55. This is a mathematical controllability
statement requiring target-specific entangled source preparation,
NOT an efficient photonic circuit.
"""
from pathlib import Path
from fractions import Fraction as F
import sys,json
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"analysis"))
from toe_20261116_W33_symmetry_minimal_fourcopy import build_geometry
OUT=ROOT/"data"/"toe_20261116_W33_E6_universal_target_steering.json"

def run():
    pts,idx,octets,SI,cliques,LI,A,adj=build_geometry()
    n=27
    I=[[F(int(i==j)) for j in range(n)] for i in range(n)]
    J=[[F(1) for j in range(n)] for i in range(n)]
    B=[[F(A[i][j]) for j in range(n)] for i in range(n)]
    def add(*terms):
        return [[sum(t[i][j] for t in terms) for j in range(n)] for i in range(n)]
    def scale(q,X):
        return [[q*X[i][j] for j in range(n)] for i in range(n)]
    def mul(X,Y):
        return [[sum(X[i][k]*Y[k][j] for k in range(n)) for j in range(n)] for i in range(n)]
    AA=mul(B,B)
    assert AA==add(scale(F(5),I),scale(F(-4),B),scale(F(5),J))
    p1=scale(F(1,27),J)
    p6=scale(F(1,18),add(scale(F(3),I),scale(F(-3),B),J))
    p20=add(I,scale(F(-1),p1),scale(F(-1),p6))
    for P,rank in ((p1,1),(p20,20),(p6,6)):
        assert mul(P,P)==P
        assert sum(P[i][i] for i in range(n))==rank
    assert mul(p1,p6)==scale(F(0),I)
    assert mul(p1,p20)==scale(F(0),I)
    assert mul(p20,p6)==scale(F(0),I)
    H=add(p1,scale(F(28,55),p20),scale(F(13,22),p6))
    inv=add(p1,scale(F(55,28),p20),scale(F(22,13),p6))
    assert mul(H,inv)==I
    for i in range(n):
        for j in range(n):
            expected=F(1440 if i==j else 24 if A[i][j] else 60,2640)
            assert H[i][j]==expected
    p_line=1/inv[0][0]
    assert p_line==F(91,170) and all(1/inv[i][i]==p_line for i in range(n))
    lo,mid,hi=F(28,55),F(13,22),F(1)
    assert lo<mid<hi
    # Any normalized target y has denominator y† inv y between
    # 1 (uniform eigenspace) and 55/28 (20-space), hence the
    # optimal achievable postselection probability lies [28/55,1].
    result={
     "status":"EXACT_W33_E6_FOURCOPY_UNIVERSAL_PURE_TARGET_STEERING",
     "output_dimension":27,
     "Schlafli_srg_parameters":[27,10,1,5],
     "projector_uniform":"P1=J/27",
     "projector_dark6":"P6=(3I-3A+J)/18, rank6",
     "projector_20":"P20=I-P1-P6, rank20",
     "success_H":"H=KKdag=P1+(28/55)P20+(13/22)P6",
     "exact_inverse":"H^-1=P1+(55/28)P20+(22/13)P6",
     "inverse_verified_by_27x27_rational_matrix_multiplication":True,
     "optimal_preimage":"psi_y=Kdag H^-1 y/sqrt(y^dag H^-1 y)",
     "success_probability":"p(y)=1/(y^dag H^-1 y) for ||y||=1",
     "worst_target_success_lower_rational":str(lo),
     "dark6_target_success":str(mid),
     "uniform_target_success":str(hi),
     "single_cubic_line_basis_target_success":str(p_line),
     "all_27_basis_labels_same_success":True,
     "limits":"Target-specific correlated four-photon antecedent. The K1 stage remains uncompiled physically. This does not supply deterministic unknown-quantum-state transfer or universal E6 gauge dynamics."
    }
    OUT.write_text(json.dumps(result,indent=2)+"\n")
    return result
if __name__=="__main__":
    d=run()
    print("PASS",d["status"],"worst",d["worst_target_success_lower_rational"],
          "one label",d["single_cubic_line_basis_target_success"],flush=True)
