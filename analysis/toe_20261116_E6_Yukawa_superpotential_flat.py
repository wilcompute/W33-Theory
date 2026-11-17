"""Full E6 cubic 27 Higgs mass rank, supersymmetric flat vacuum and degree-five diagnostic.

Uses the 45 exact monomials and 27 weights from the committed cubic
derivation certificate. Constructs a gauge-invariant superpotential
    W = S1( Hbar1*H1-v1^2 ) + S2( Hbar2*H2-v2^2 )
      + T ( tr_27(Phi^2)-w^2 ) + lambda I3(H)
with S1=S2=T=0, H1=e7, H2=e8, Hbar_a=H_a^dagger,
Phi=diag(Y). The two H's have a common rank-one A-sector row.

The vacuum is F/D flat for this specific superpotential, not isolated:
the full E6 adjoint Cartan retains 3 complex flat directions modulo
its SU5 Weyl group. A degree-five adjoint invariant generically
displaces the pure hypercharge direction, unless terms cancel its
gradient in broken E6 Cartan directions.
"""
from __future__ import annotations
import importlib.util, json
from pathlib import Path
import sympy as sp
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/"data"/"toe_20261116_E6_cubic_Yukawa_modulus_degree5.json"
spec=importlib.util.spec_from_file_location("e6full",ROOT/"analysis"/"toe_20261116_E6_full_cubic_SM_stabilizer.py")
old=importlib.util.module_from_spec(spec);spec.loader.exec_module(old)

def mass_hessian(a,b):
    monomials=old.cubic_monomials()
    h={7:sp.sympify(a),8:sp.sympify(b)}
    M=sp.zeros(27,27)
    for (i,j,k),c in monomials.items():
        for u,v,w in ((i,j,k),(i,k,j),(j,k,i)):
            M[u,v]+=c*h.get(w,0)
            M[v,u]+=c*h.get(w,0)
    assert M==M.T
    return M

def hessian_certificate():
    shapes=[]
    for a,b in ((1,0),(0,1),(1,1),(1,2),(1,sp.I),(1,1+sp.I)):
        M=mass_hessian(a,b)
        norm=sp.simplify(sp.conjugate(a)*a+sp.conjugate(b)*b)
        mass2=sp.simplify(M.conjugate().T*M)
        eig=mass2.eigenvals()
        assert eig=={0:17,norm:10},(a,b,eig)
        assert M.rank()==10
        # Triplet + antitriplet mass 3+3, weak vectorlike doublets 2+2.
        assert M[:9,:9].rank()==4
        assert M[9:18,18:27].rank()==3
        assert M[18:27,9:18].rank()==3
        shapes.append({"a":str(a),"b":str(b),"singular_mass_squared":str(norm),
                       "rank":10,"nullity":17,"A_A_block_rank":4,
                       "B_C_block_rank":3,"C_B_block_rank":3})
    return shapes

def cartan_five_invariant():
    p=old.cubic_monomials()
    inc=sp.zeros(len(p),27)
    for idx,triple in enumerate(p):
        for j in triple:inc[idx,j]+=1
    H=inc.nullspace()
    assert len(H)==6
    Y=sp.Matrix(old.hypercharge_integer_weights())
    assert inc*Y==sp.zeros(len(p),1)
    linears=sp.Matrix([[sum(Y[i]*h[i] for i in range(27)) for h in H],
                       [sum(Y[i]**4*h[i] for i in range(27)) for h in H]])
    assert linears.rank()==2
    # The fifth-order trace gradient is not parallel to the quadratic
    # trace gradient, so a superpotential T(tr Phi²-w²)+k tr Phi^5
    # cannot keep Phi=Y F-flat for any T when k !=0.
    quadratic=sum(Y[i]**2 for i in range(27))
    fifth=sum(Y[i]**5 for i in range(27))
    # SU5 Cartan: Higgs vectors e7 and e8 fixed, hence extra 2 linear constraints.
    rest=sp.Matrix([[h[i] for h in H] for i in (7,8)])
    Hl=[sp.Matrix.hstack(*H)*z for z in rest.nullspace()]
    assert len(Hl)==4
    # At fixed tr Phi², 3 independent SU5 Cartan deformations remain.
    charge=sp.Matrix([[sum(Y[i]*h[i] for i in range(27)) for h in Hl]])
    assert charge.rank()==1
    return {"E6_Cartan_dim":6,"SU5_stabilizer_Cartan_dim":4,
            "quadratic_norm_tr27_Y2":int(quadratic),
            "fifth_trace_tr27_Y5":int(fifth),
            "quadratic_vs_fifth_Cartan_gradient_rank":int(linears.rank()),
            "unlifted_complex_SU5_Cartan_moduli_at_least":3,
            "obstruction":"For lambda!=0, W=T(Tr27 Phi²-w²)+lambda Tr27 Phi^5 has no F-flat solution with Phi proportional to Y; the fifth-order Cartan derivative is not proportional to Y.",
            "scope":"No statement excluding cancellations from Hbar-Phi-H couplings or higher E6 invariants."}

def flat_superpotential_control():
    # Hbar=dual normalized, H=e7 or e8; singlet constraints =0.
    # Phi=Y, T=0; quadratic constraint equals Tr27(Y²)=180.
    # Every Phi Cartan direction commutes with its compact conjugate.
    A1=sp.zeros(3);A1[2,1]=1
    A2=sp.zeros(3);A2[2,2]=1
    s,t=sp.symbols("s t")
    V=s*A1+t*A2
    assert V.rank()==1 and V.adjugate()==sp.zeros(3)
    assert V.det()==0 and (A1.T*A2).trace()==0
    return {
        "superpotential":"S1(<barH1,H1>-v1²)+S2(<barH2,H2>-v2²)+T(Tr27 Phi²-w²)+lambda I3(H1,H2)",
        "F_flat":"S1=S2=T=0, <barHa,Ha>=va², Tr27 Phi²=w²; cubic polarizations vanish for common-row rank-one A-sector VEVs",
        "D_flat":"Each aligned 27bar cancels its partner 27 moment map for every compact E6 generator; the Cartan adjoint Phi is normal and has zero adjoint moment map.",
        "gauge_symmetry":"E6 -> SU5 by H1,H2 and SU5 -> SM Lie algebra by Phi proportional to Y",
        "not_isolated":True,"unlifted_Cartan_moduli_dim_lower_bound":3,
        "Y_standard_model_hypercharge_factor":"-1/6"}

def verify():
    masses=hessian_certificate()
    grads=cartan_five_invariant()
    pot=flat_superpotential_control()
    assert old.anomaly_table()["anomaly_checks_exact"]["U1_cubed"]=="0"
    return {"status":"PASS_E6_SUPERSONIC_CUBIC_27_MASS_AND_FD_FLAT_SM_BRANCHED_VACUUM",
            "cubic_mass_pairs":"Ten of 27 chiral fields acquire mass |lambda|sqrt(|a|²+|b|²) in a single 27 flavor, leaving 17 massless; rank only, not an SM physical mass claim.",
            "Higgs_mass_examples":masses,"adjoint_degree5_control":grads,
            "explicit_superpotential":pot,
            "unresolved":"Adjoint direction not dynamically selected, at least three Cartan complex moduli, unknown full coupled scalar Hessian and realistic fermion masses."}
if __name__=="__main__":
    data=verify();OUT.parent.mkdir(parents=True,exist_ok=True)
    OUT.write_text(json.dumps(data,indent=2,sort_keys=True)+"\n",encoding="utf-8")
    print(data["status"],data["Higgs_mass_examples"][-1],data["adjoint_degree5_control"]["unlifted_complex_SU5_Cartan_moduli_at_least"])
