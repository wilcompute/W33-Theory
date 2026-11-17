"""SU(5) adjoint F-flat hypercharge stabilizer and three-family E6 cubic mass audit.

EXACTLY PROVED: after E6 -> SU5 Higgsing, an SU5-invariant
W_eff = (lambda*v/2) tr Phi^2 + (lambda/3) tr Phi^3
has Phi0=v diag(2,2,2,-3,-3) F-flat. Its 24-dimensional
adjoint fermion Hessian has 12 Goldstone zero modes, 11
nonzero masses of magnitude 5*lambda*v and one of lambda*v.
The three former SU5 Cartan flat directions are therefore lifted.
E6 has NO cubic adjoint Casimir: this is an effective SU5
construction, and its E6 UV embedding is NOT derived.

Additionally the E6 cubic Yukawa tensor with three matter 27s
and common-row rank-one Higgs vevs generically gives 30 massive
and 51 kernel directions; this is a representation-level test,
not a complete physical fermion spectrum.
"""
from pathlib import Path
import importlib.util, json
import sympy as S
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/"data"/"toe_20261116_SU5_adjoint_spectral_lifting_3families.json"
sp=importlib.util.spec_from_file_location("higgs",ROOT/"analysis"/"toe_20261116_E6_Yukawa_superpotential_flat.py")
higgs=importlib.util.module_from_spec(sp);sp.loader.exec_module(higgs)

def su5_adjoint_spectral():
    D=S.diag(2,2,2,-3,-3)
    mu=lam=v=S.Integer(1)
    assert S.trace(D)==0
    centered=D**2-S.eye(5)*S.trace(D**2)/5
    assert mu*D+lam*centered==S.zeros(5)
    # Trace invariant Newton identities fix eigenvalue multiset EXACTLY.
    tr={k:S.trace(D**k) for k in range(1,6)}
    assert tr=={1:0,2:30,3:-30,4:210,5:-390}
    t=S.symbols("t")
    characteristic=(t-2)**3*(t+3)**2
    assert S.expand(characteristic)==t**5-15*t**3+10*t**2+60*t-72
    # Lie-algebra tangent map to F term
    def response(B):
        raw=mu*B+lam*(D*B+B*D-2*S.eye(5)*S.trace(D*B)/5)
        assert S.trace(raw)==0
        return raw
    G=[]
    for i in range(5):
        for j in range(5):
            if i!=j:
                E=S.zeros(5);E[i,j]=1;G.append(E)
    for i in range(4):
        E=S.zeros(5);E[i,i]=1;E[4,4]=-1;G.append(E)
    assert len(G)==24
    coeff=[]
    for A in G:
        R=response(A)
        v=S.Matrix([R[i,j] for i in range(5) for j in range(5)])
        coeff.append(v)
    H=S.Matrix.hstack(*coeff)
    assert H.rank()==12
    # Spectral decomposition of tangent map:
    # 8 generators of su3 block and 3 of su2: magnitude 5;
    # 1 hypercharge Cartan mode: magnitude 1; and
    # 12 Goldstone root generators: eigenvalue 0.
    eigen=H # H is 25x24 non-square; reconstruct square coordinates
    basis=S.Matrix.hstack(*[S.Matrix([E[i,j] for i in range(5) for j in range(5)]) for E in G])
    square=basis.gauss_jordan_solve(H)[0]
    assert square.shape==(24,24)
    assert square.eigenvals()=={S.Integer(0):12,S.Integer(5):8,S.Integer(-5):3,S.Integer(-1):1}
    W=S.Rational(1,2)*S.trace(D**2)+S.Rational(1,3)*S.trace(D**3)
    assert W==S.Integer(5)
    # With only 4 singlet multipliers imposing the SU5 power sums,
    # eigenvalues are fixed modulo Weyl, but gradients at D rank1
    # on the traceless Cartan: isolated with Hessian flat directions.
    diagdirs=[]
    for i in range(4):
        E=S.zeros(5);E[i,i]=1;E[4,4]=-1
        diagdirs.append(E)
    jac=S.Matrix([[k*S.trace(D**(k-1)*E) for E in diagdirs] for k in range(2,6)])
    assert jac.rank()==1
    return {
        "status":"PASS_EXACT_SU5_EFFECTIVE_SUPERPOTENTIAL_CARTAN_LIFT",
        "adjoint_vacuum":"Phi0=v diag(2,2,2,-3,-3)",
        "effective_superpotential":"W_eff=lambda*v/2 Tr(Phi^2)+lambda/3 Tr(Phi^3)",
        "F_flat":True,
        "traces_1_to_5":{str(k):int(n) for k,n in tr.items()},
        "characteristic_polynomial":str(S.expand(characteristic)),
        "F_term_linearization_rank":12,
        "Hessian_eigenvalues_lambda_v_1":{"0":12,"+5":8,"-5":3,"-1":1},
        "unbroken_sm_adjoint_complex_dim":12,
        "broken_complex_goldstone_count":12,
        "previous_3_complex_Cartan_moduli_lifted":True,
        "Casimir_constraint_Cartan_gradient_rank_at_hypercharge":1,
        "IMPORTANT_UV_CAVEAT":"SU5 permits cubic tr Phi^3 but E6 has no degree-3 adjoint invariant. No E6 invariant UV operator inducing this effective superpotential has been derived; consistency of heavy E6 fields and scalar vacuum remains open."
    }

def competing_SU5_F_flat_vacua():
    """All 2-eigenvalue SU5 adjoint F-flat branches at mu=lambda*v=1."""
    branches=[]
    for m in range(1,5):
        x=S.Rational(5-m,2*m-5)
        y=S.Rational(-m,2*m-5)
        # m eigenvalues x and (5-m) eigenvalues y, up to permutation
        V=S.diag(*([x]*m+[y]*(5-m)))
        assert S.trace(V)==0
        F=V+V**2-S.eye(5)*S.trace(V**2)/5
        assert F==S.zeros(5)
        branches.append({"multiplicity_first":m,"first_eigenvalue":str(x),
            "second_eigenvalue":str(y),
            "centralizer":"S(U(%d) x U(%d))"%(m,5-m),
            "superpotential_value":str(S.trace(V**2)/2+S.trace(V**3)/3),
            "globally_SUSY_zero_F_energy":True})
    assert branches[2]["centralizer"]=="S(U(3) x U(2))"
    assert branches[3]["centralizer"]=="S(U(4) x U(1))"
    return {"origin":"Phi=0 (unbroken SU5)",
        "two_eigenvalue_branches":branches,
        "nonuniqueness":"Global N=1 SUSY F/D potential vanishes on all F=D=0 vacua. The cubic SU5 superpotential does not energetically prefer the SM branch over the origin or SU4xU1."}

def three_family_cubic():
    M7=higgs.mass_hessian(1,0)
    M8=higgs.mass_hessian(0,1)
    L1=S.diag(1,2,3)
    L2=S.Matrix([[1,1,0],[1,2,1],[0,1,3]])
    mass=S.kronecker_product(L1,M7)+S.kronecker_product(L2,M8)
    assert mass==mass.T and mass.shape==(81,81)
    rank=mass.rank()
    assert rank==30,rank
    assert mass.nullspace().__len__()==51
    # Decompose SU5 under existing unbroken weights.
    return {"status":"PASS_THREE_FAMILY_GENERIC_CUBIC_RANK30_NULLITY51",
        "matter_families":3,"vector_components":81,
        "independent_symmetric_yukawa_matrices":[[[int(v) for v in row] for row in T.tolist()] for T in (L1,L2)],
        "mass_matrix_rank":rank,"remaining_kernel":81-rank,
        "interpretation":"Three generic SU5 vectorlike 5+5bar pairs lifted; 3*(16+1) representation components remain massless before other couplings.",
        "CRITICAL_SCOPE":"No full gaugino-Higgsino spectrum, no SM Yukawa textures, and no proof that 51 kernel states are all protected physical particles."
    }

def verify():
    a=su5_adjoint_spectral();b=three_family_cubic();v=competing_SU5_F_flat_vacua()
    return {"status":"PASS_SU5_SPECTRALLY_STABLE_ADJOINT_AND_E6_3FAMILY_RANK",
            "effective_SU5":a,"three_family_E6_yukawa":b,
            "competing_susy_vacua":v,
            "invariant_scope":"The proposed cubic SU5 adjoint interaction is not itself an E6-invariant polynomial. Its existence after symmetry breaking does not prove UV completion."}
if __name__=="__main__":
    x=verify();OUT.parent.mkdir(parents=True,exist_ok=True)
    OUT.write_text(json.dumps(x,indent=2,sort_keys=True)+"\n",encoding="utf-8")
    print(x["status"],x["effective_SU5"]["F_term_linearization_rank"],x["three_family_E6_yukawa"]["mass_matrix_rank"])
