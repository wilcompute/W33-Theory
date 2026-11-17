"""Exact E6 27-representation Cartan invariant obstruction.

Construct all six diagonal Cartan generators as the kernel of the 45
signed cubic monomial weight-incidence equations (one equation per
nonzero term of det(A)+det(B)+det(C)-Tr(ABC)). For arbitrary symbolic
diagonal E6 adjoint H, prove
 Tr_27 H^3 = 0
 Tr_27 H^4 = (Tr_27 H^2)^2 / 12.
There is no independent quartic ADJOINT shape selector in an E6
symmetric single-adjoint potential; the analogous positive SU5
Tr Phi^4 term must arise from an E6-breaking field/portal or other
higher degree invariant. Cartan invariant theory of E6 has primitive
degrees 2,5,6,8,9,12 (Chevalley/Weyl, literature), not 3 or 4.
"""
from pathlib import Path
import itertools,json
import sympy as s
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/"data"/"toe_20261117_E6_Cartan_no_cubic_no_quartic.json"

def verify():
    import sys
    sys.path.insert(0,str(ROOT/"analysis"))
    from toe_20261116_E6_full_cubic_SM_stabilizer import cubic_monomials,hypercharge_integer_weights
    mons=cubic_monomials()
    mat=s.zeros(len(mons),27)
    for j,(triple,sign) in enumerate(sorted(mons.items())):
        for ix in triple:mat[j,ix]+=1
    basis=mat.nullspace()
    assert len(mons)==45 and len(basis)==6
    t=s.symbols("t0:6")
    h=s.Matrix.hstack(*basis)*s.Matrix(t)
    p2=s.expand(sum(z**2 for z in h))
    p3=s.expand(sum(z**3 for z in h))
    p4=s.expand(sum(z**4 for z in h))
    p5=s.expand(sum(z**5 for z in h))
    assert p3==0
    assert s.expand(p4-p2**2/s.Integer(12))==0
    assert p5!=0
    Y=hypercharge_integer_weights()
    assert mat*s.Matrix(Y)==s.zeros(len(mons),1)
    powers={k:sum(z**k for z in Y) for k in (2,3,4,5)}
    assert powers=={2:180,3:0,4:2700,5:-4320}
    # Individual basis vectors can have vanishing fifth moment; a
    # generic Cartan combination detects the first odd invariant.
    a=list(basis[0]+2*basis[1]+3*basis[2]+4*basis[3]+5*basis[4]+6*basis[5])
    assert sum(z**5 for z in a)!=0
    samples=[]
    for v in ((1,0,0,0,0,0),(1,2,3,4,5,6),(3,-2,7,0,1,-1)):
        H=s.Matrix.hstack(*basis)*s.Matrix(v)
        f=[sum(z**n for z in H) for n in (2,3,4,5)]
        assert f[2]*12==f[0]**2 and f[1]==0
        samples.append({"Cartan_coefficients":list(v),
          "Tr_H2":str(f[0]),"Tr_H3":str(f[1]),"Tr_H4":str(f[2]),"Tr_H5":str(f[3])})
    return {"status":"PASS_E6_ADJOINT_CARTAN_NO_INDEPENDENT_CUBIC_OR_QUARTIC",
        "diagonal_cubic_weight_equations":45,"Cartan_dimension":6,
        "polynomial_identity_3":"Tr27(H^3)=0 for arbitrary complex diagonal E6 Cartan H",
        "polynomial_identity_4":"Tr27(H^4)=[Tr27(H^2)]^2/12, exact polynomial in six independent symbolic Cartan parameters",
        "first_nontrivial_odd_trace":"Tr27(H^5) is not identically zero",
        "degree_list_external_group_theory":[2,5,6,8,9,12],
        "consequence":"At any E6-invariant single-adjoint quartic order, quartic terms are functions of quadratic norm only; the independent SU5 adjoint TrPhi4 shape-selector cannot be promoted to an E6-invariant pure-adjoint quartic.",
        "important_caveat":"This proves absence in the invariant polynomial ring (Cartan/Weyl restriction) for one E6 adjoint. It does not forbid quartic interactions involving additional Higgs representations or nonpolynomial quantum effective actions, and does not derive an E6 vacuum.",
        "Y_integer_weight_traces":{str(k):v for k,v in powers.items()},
        "symbolic_monomial_counts":{"TrH2":len(s.Poly(p2,*t).terms()),
                                    "TrH5":len(s.Poly(p5,*t).terms())},
        "samples":samples,
        "literature":"https://people.math.harvard.edu/~elkies/M222.23/index.html"}
if __name__=="__main__":
    z=verify();OUT.parent.mkdir(parents=True,exist_ok=True)
    OUT.write_text(json.dumps(z,indent=2,sort_keys=True)+"\n",encoding="utf8")
    print(z["status"],z["symbolic_monomial_counts"])
