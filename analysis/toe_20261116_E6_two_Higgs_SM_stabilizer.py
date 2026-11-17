"""Exact two-bifundamental trinification stabilizer and gauge mass certificate.

Two 27 Higgses have L_i in (1,3,bar3) with L1=e3 e3^T,
L2=e3 e2^T. Their conjugate 27bar partners cancel all D-terms.
Assume a purely cubic E6 Higgs superpotential restricted to these fields,
without bilinear 27bar*27 mass terms or other nonzero sectors.

Exact results concern the manifest su3_L+su3_R subalgebra;
the other 54 E6 generators, hypercharge normalization, chirality,
and vacuum stability of every fluctuation are NOT solved.
"""
from pathlib import Path
import json
import sympy as S
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/"data"/"toe_20261116_E6_two_Higgs_SM_stabilizer.json"

def gellmann():
    I=S.I
    B=[]
    for a,b in ((0,1),(0,2),(1,2)):
        R=S.zeros(3);R[a,b]=R[b,a]=S.Rational(1,2);B.append(R)
        J=S.zeros(3);J[a,b]=-I/2;J[b,a]=I/2;B.append(J)
    B.extend((S.diag(1,-1,0)/2,S.diag(1,1,-2)/(2*S.sqrt(3))))
    assert len(B)==8
    assert all(S.simplify(S.trace(A*T)-(S.Rational(1,2) if i==j else 0))==0
               for i,A in enumerate(B) for j,T in enumerate(B))
    return B

def fields():
    V=S.zeros(3);V[2,2]=1
    W=S.zeros(3);W[2,1]=1
    return V,W

def exact_certificate():
    G=gellmann()
    V,W=fields()
    derivs=[[X*A for X in G]+[-A*X for X in G] for A in (V,W)]
    coeff=[]
    for ds in derivs:
        for i in range(3):
            for j in range(3):
                coeff.extend(([S.re(z[i,j]) for z in ds],
                              [S.im(z[i,j]) for z in ds]))
    C=S.Matrix(coeff)
    assert C.shape==(36,16) and C.rank()==12
    basis=C.nullspace()
    assert len(basis)==4
    # Gauge-boson mass Gram uses real bilinear because A^a are real.
    M=S.zeros(16)
    for ds in derivs:
        for i in range(16):
            for j in range(i,16):
                v=S.simplify(S.re(S.trace(ds[i].conjugate().T*ds[j])))
                M[i,j]+=v
                if i!=j:M[j,i]+=v
    charpoly=S.factor(M.charpoly().as_expr())
    lam=S.Symbol("lambda")
    target=lam**4*(2*lam-1)**7*(4*lam-1)**4*(6*lam-5)/196608
    assert S.factor(charpoly-target)==0
    # Two conjugate vectorlike Higgs VEVs contribute twice the Gram.
    # Gauge-boson mass squared = 2 g^2 * (two-copy Gram) =4 g^2 v^2 M.
    spectrum=[("0",4),("g^2*v^2",4),("2*g^2*v^2",7),("10*g^2*v^2/3",1)]
    assert sum(n for _,n in spectrum)==16
    # Explicit surviving SU2_L generators T0, T1 and T6.
    for j in (0,1,6):assert all(y==0 for y in C[:,j])
    # Surviving U1 left diag(1,1,-2), right diag(4,-2,-2).
    X=S.diag(1,1,-2);Y=S.diag(4,-2,-2)
    assert X*V==V*Y and X*W==W*Y
    assert S.trace(X)==S.trace(Y)==0
    # Adjugates of every combination vanish -> all polarized det F-terms.
    t,u=S.symbols("t u")
    T=t*V+u*W
    assert T.rank()==1 and all(entry==0 for entry in T.adjugate())
    assert S.expand(T.det())==0
    # D term of the conjugate representation is exactly opposite.
    # For each compact E6 generator T the contribution of conjugate
    # VEV V* to the dual rep is negative of the original generator
    # expectation, so it cancels pairwise, including beyond SU3^3.
    return {"status":"PASS_TWO_RANKONE_27_PLUS_27BAR_MANIFEST_SM_GAUGE_STABILIZER",
      "source_sector":"Two Higgs 27s in (1,3,bar3), plus their aligned conjugate 27bar partners",
      "Higgs_VEV_matrices":[[list(map(int,row)) for row in A.tolist()] for A in (V,W)],
      "manifest_generator_count":16,"manifest_broken_generator_count":12,
      "manifest_stabilizer_dimension":4,
      "manifest_stabilizer":"su(2)_L + u(1)",
      "exact_stabilizer_generator":{"left":str(X),"right":str(Y)},
      "mass_gram_charpoly":str(charpoly),
      "mass2_spectrum_equal_couplings_with_two_conjugate_pairs":spectrum,
      "all_Higgs_polarized_cubic_det_F_terms_zero":True,
      "D_flatness":"Pairwise compact-group moment maps cancel for 27 VEV and aligned 27bar conjugate partner.",
      "unproven":"Extra 54 E6 generators' stabilizer; identification and normalization of U1_Y; full SUSY superpotential F-terms with mass/singlet terms; scalar Hessian and all 3 family chirality.",
      "scale_note":"VEV v is arbitrary here, not dynamically determined.",
      "phenomenological_boundary":"Matching SM Lie-algebra subgroup is NOT derivation of the Standard Model or TOE."}

def run():
    cert=exact_certificate()
    OUT.parent.mkdir(parents=True,exist_ok=True)
    OUT.write_text(json.dumps(cert,indent=2)+"\n",encoding="utf8")
    print(cert["status"],cert["manifest_stabilizer"],cert["mass2_spectrum_equal_couplings_with_two_conjugate_pairs"])
    return cert

if __name__=="__main__":run()
