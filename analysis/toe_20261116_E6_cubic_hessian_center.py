"""Exact singlet Hessian and center-selection obstruction for cubic E6 trinification.

W(A,B,C)=det A+det B+det C-Tr(ABC).
Restrict A=a I3, B=b I3, C=c I3: W=a^3+b^3+c^3-3abc.
All computations below are algebraic in the manifest SU3^3 theory.
"""
from fractions import Fraction
from pathlib import Path
import json

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/"data"/"toe_20261116_E6_cubic_hessian_center.json"
CHARGES={"A":(1,-1,0),"B":(0,1,-1),"C":(-1,0,1)}

def allowed_monomial(letters):
    c=[sum(CHARGES[l][j] for l in letters)%3 for j in range(3)]
    return all(x==0 for x in c)

def real_singlet_hessian(s:int):
    # d^2 W = 3*s * [[2,-1,-1],[-1,2,-1],[-1,-1,2]]
    H=[[6*s if i==j else -3*s for j in range(3)] for i in range(3)]
    trace=sum(H[i][i] for i in range(3))
    trace2=sum(H[i][j]*H[j][i] for i in range(3) for j in range(3))
    det=(H[0][0]*(H[1][1]*H[2][2]-H[1][2]*H[2][1])
         -H[0][1]*(H[1][0]*H[2][2]-H[1][2]*H[2][0])
         +H[0][2]*(H[1][0]*H[2][1]-H[1][1]*H[2][0]))
    assert trace==18*s and trace2==162*s*s and det==0
    assert [sum(row) for row in H]==[0,0,0]
    # Canonical complex singlets phi_a=sqrt(3)*a because Tr|dA|²=3|da|².
    # W fermion matrix in canonically normalized fields is H/3:
    # eigenvalues 0, 3s, 3s. In unbroken global SUSY the F scalar
    # mass squares are {0,9|s|²,9|s|²} for complex singlet fluctuations.
    return {
      "s":s, "raw_W_Hessian_3x3":H, "H_trace":trace,
      "H_squared_trace":trace2, "H_det":det,
      "raw_Hessian_eigenvalues":[0,9*s,9*s],
      "canonically_normalized_superpotential_eigenvalues":[0,3*s,3*s],
      "canonically_normalized_F_scalar_mass2":[0,9*s*s,9*s*s],
      "exact_flat_direction":"(delta a, delta b, delta c) proportional (1,1,1)"
    }

def verify():
    monomial2=[{"term":u+v,"center_allowed":allowed_monomial((u,v))}
               for u in CHARGES for v in CHARGES]
    assert not any(row["center_allowed"] for row in monomial2)
    cubic=[u+v+w for u in CHARGES for v in CHARGES for w in CHARGES
           if allowed_monomial((u,v,w))]
    assert len(cubic)==9 # 3 diagonal triple + six ABC orderings
    assert {"AAA","BBB","CCC","ABC","ACB","BAC","BCA","CAB","CBA"}==set(cubic)
    rows=[real_singlet_hessian(s) for s in (1,2,3,7)]
    return {
      "status":"PASS_TRINIFICATION_CENTER_SELECTION_AND_EXACT_FLAT_DIRECTION_HESSIAN",
      "chiral_center_charges":CHARGES,
      "no_gauge_invariant_bilinear_in_one_27":True,
      "all_center_allowed_cubic_words":cubic,
      "singlet_branch":"A=B=C=s*I3 is exactly F- and D-flat for all complex s",
      "singlet_hessian_samples":rows,
      "conclusion":"The manifest SU3^3-invariant cubic alone has a complex modulus and no intrinsic scale. Three-link branch leaves diagonal SU3, not the SM. No quadratic gauge invariant exists from a lone chiral 27.",
      "limits":"Center selection alone is necessary, not sufficient, for a complete invariant; this certificate is for the restricted singlet Hessian, not all 27 complex directions or realistic soft/SUGRA corrections."
    }

if __name__=="__main__":
    cert=verify()
    OUT.parent.mkdir(parents=True,exist_ok=True)
    OUT.write_text(json.dumps(cert,indent=2)+"\n",encoding="utf-8")
    print(cert["status"])
