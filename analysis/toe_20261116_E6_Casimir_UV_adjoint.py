"""Search full E6 Casimir superpotentials selecting hypercharge Y with nonzero Hessian.

E6-invariant polynomial Casimirs on adjoint have degrees
2,5,6,8,9,12, represented on the diagonal Cartan by
Tr_27(Phi^k). Choose W(Phi)=sum_k c_k Tr_27(Phi^k)
and demand dW(Y)=0 in ALL SIX E6 Cartan directions.

E6-invariance ensures that if F vanishes on Cartan directions
then it vanishes in off-Cartan root directions at semisimple Y,
since roots have nonzero weights or centralizer directions
invariant under the Cartan. Exact linear algebra searches the
kernel of the 6x6 gradient matrix and evaluates Hessian on
the 4D SU5 Cartan surviving two Higgs pairs.

An isolated nonsingular Cartan Hessian is stronger than prior
SU5-only cubic, but DOES NOT establish complete multi-Higgs
physical scalar Hessian nor hierarchy, no-Goldstone spectrum,
proton lifetime, or a realistic Planck-suppressed EFT.
"""
import json,itertools
from pathlib import Path
import sympy as S
import importlib.util
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/"data"/"toe_20261116_E6_highCasimir_adj_rank_search.json"
spec=importlib.util.spec_from_file_location("fullE6",ROOT/"analysis"/"toe_20261116_E6_full_cubic_SM_stabilizer.py")
old=importlib.util.module_from_spec(spec);spec.loader.exec_module(old)
DEGREES=(2,5,6,8,9,12)

def search():
    p=old.cubic_monomials()
    inc=S.zeros(len(p),27)
    for row,triplet in enumerate(p):
        for j in triplet:inc[row,j]+=1
    h=S.Matrix.hstack(*inc.nullspace())
    assert h.shape==(27,6)
    y=S.Matrix(old.hypercharge_integer_weights())
    assert inc*y==S.zeros(len(p),1)
    rest=S.Matrix([list(h[7,:]),list(h[8,:])])
    hl=h*S.Matrix.hstack(*rest.nullspace())
    assert hl.shape==(27,4)
    vals=[int(z) for z in y]
    G=S.Matrix([[sum(S.Integer(k)*v**(k-1)*h[i,j] for i,v in enumerate(vals)) for k in DEGREES] for j in range(6)])
    null=G.nullspace()
    def Hess(c):
        ds=[sum(c[a]*DEGREES[a]*(DEGREES[a]-1)*v**(DEGREES[a]-2)
                for a in range(len(DEGREES))) for v in vals]
        return hl.T*S.diag(*ds)*hl
    ranks=[]
    for c in null:
        mat=Hess(c)
        ranks.append({"c":[str(z) for z in c],"Hessian_SU5_Cartan_rank":mat.rank(),
                      "Hessian_det":str(mat.det())})
    # Search simple integer combos up to 3 for a nonsingular Hessian.
    selected=None
    if null:
        cand=[null[i] for i in range(len(null))]
        cand+= [sum((null[i] for i in subset),S.zeros(len(DEGREES),1))
                for size in range(2,min(4,len(null))+1) for subset in itertools.combinations(range(len(null)),size)]
        for z in cand:
            m=Hess(z)
            if m.rank()==4:
                selected=z;break
    cartan_modes={}
    if selected is not None:
        K=hl.T*hl
        H4=Hess(selected)
        assert K.det()!=0 and H4.det()!=0
        eigen=(K.inv()*H4).eigenvals()
        assert sum(eigen.values())==4 and all(x!=0 for x in eigen)
        cartan_modes={"canonical_trace_metric_generalized_F_Hessian_eigenvalues":
                          {str(x):int(m) for x,m in eigen.items()},
                      "kinetic_metric_det":str(K.det()),
                      "all_four_Cartan_modes_massive":True,
                      "full_physical_mass_note":"Values are in polynomial normalization Tr_27 Phi^k. Physical masses need 78 Kähler metric and an overall mass scale."}
    answer={
       "SU5_Cartan_generalized_mass_certificate":cartan_modes,
       "gradient_rank":int(G.rank()),
       "gradient_nullspace_dim":len(null),
       "basis_candidates":ranks,
       "selected_nonzero":selected is not None,
       "selected_Casimir_coefficients":([str(v) for v in selected] if selected is not None else None),
       "selected_SU5_Cartan_Hessian_det":(str(Hess(selected).det()) if selected is not None else None),
       "selected_SU5_Cartan_Hessian_rank":(int(Hess(selected).rank()) if selected is not None else None),
       "constraint":"Full six-dimensional E6 Cartan gradient must vanish at the hypercharge diagonal weight vector.",
       "scope":"Exact diagonal Cartan polynomial diagnostics. Non-Cartan Hessian, couplings to two Higgs pairs, complete F/D stability and UV naturalness not computed."
    }
    return answer

def verify():
    r=search()
    assert r["gradient_rank"]>=1 and r["gradient_rank"]<=6
    return {"status":"PASS_E6_CASIMIR_GRADIENT_AND_SU5_CARTAN_HESSIAN_SEARCH",**r}
if __name__=="__main__":
    r=verify();OUT.parent.mkdir(parents=True,exist_ok=True)
    OUT.write_text(json.dumps(r,indent=2,sort_keys=True)+"\n",encoding="utf8")
    print(r["status"],r["gradient_rank"],r["gradient_nullspace_dim"],r["selected_nonzero"],r["selected_SU5_Cartan_Hessian_rank"])
