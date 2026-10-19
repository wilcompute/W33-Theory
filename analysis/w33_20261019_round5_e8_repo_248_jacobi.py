"""Front 4: explicit Pauli80-to-repository-248 coordinate injection,
and covariance / Jacobi rechecks with existing Pass11681 E8 bracket.
Does NOT derive a map to a chosen Chevalley root-vector normalization.
"""
from __future__ import annotations
import json
from pathlib import Path
import numpy as np
import w33_pass11681_e8_from_two_qutrits as E
from w33_pass11687_11691_two_qutrit_e8_dictionary import E8Data
from w33_20261019_nextfive_optics_su9 import BASIS,rep,GENERATORS
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/"data"/"w33_20261019_round5_e8_repo_248_jacobi.json"
Z9=np.zeros((9,9),complex);Z84=np.zeros(84,complex)
_,SL,SLP=E.e8_basis()
J=np.column_stack([SLP@X.ravel() for X in BASIS])
J248=np.zeros((248,80),complex);J248[:80,:]=J
def coord(X):
    A,x,y=X
    return np.concatenate([SLP@A.ravel(),x,y])
def entry(v):
    return (SL@v[:80],v[80:164],v[164:])  # first sector flattened
def elem(v):
    A,x,y=entry(v)
    return (A.reshape((9,9)),x,y)
def rnd(rng):
    A=rng.normal(size=(9,9))+1j*rng.normal(size=(9,9))
    A=A-np.trace(A)/9*np.eye(9)
    return (A,rng.normal(size=84)+1j*rng.normal(size=84),
              rng.normal(size=84)+1j*rng.normal(size=84))
def run():
    rng=np.random.default_rng(20261019)
    max_reconstruct=max(np.linalg.norm(SL@(SLP@x.ravel())-x.ravel()) for x in BASIS)
    rank=int(np.linalg.matrix_rank(J,tol=1e-9))
    errs=[]
    for name,U in GENERATORS.items():
        V=U*np.exp(-1j*np.angle(np.linalg.det(U))/9)
        A80,er=rep(V)
        vs=[]
        for x in BASIS:
            e=(x,Z84,Z84)
            c=coord(E8Data.act(V,e))
            vs.append(c)
        Jtest=np.array(vs).T
        embed_err=float(np.linalg.norm(Jtest-J248@A80))
        # Full 248-dimensional bracket automorphism on random mixed elements
        auto=0.;inv=0.
        for _ in range(10):
            a=rnd(rng);b=rnd(rng)
            left=E8Data.act(V,E.bracket(a,b))
            right=E.bracket(E8Data.act(V,a),E8Data.act(V,b))
            auto=max(auto,float(np.linalg.norm(coord(left)-coord(right))))
            # grade1 / grade2 separately are transformed via dual Ubar.
            inv=max(inv,float(np.linalg.norm(coord(E8Data.act(V,a)))))
        errs.append({"generator":name,"e8_248_embedding_equivariance":embed_err,
                     "repository_full_E8_bracket_automorphism_residual":auto,
                     "old_operator80_coordinates_residual":er})
    gamma,jacobi=E.jacobi_certificate(np.random.default_rng(11681))
    checks={"80_to_repository_248_rank":rank==80,
         "operator_basis_reconstructs":max_reconstruct<1e-10,
         "all_five_repository_248_intertwiners":max(q["e8_248_embedding_equivariance"] for q in errs)<1e-10,
         "full_repo_E8_bracket_automorphism":max(q["repository_full_E8_bracket_automorphism_residual"] for q in errs)<1e-9,
         "repository_mixed_Jacobi_27_cases":jacobi<1e-9 and abs(gamma+1)<1e-9}
    out={"schema":"w33.round5.e8_repo_basis_248_intertwiner.v1",
         "basis_origin":"Repository analysis/w33_pass11681_e8_from_two_qutrits.py e8_basis(), full bracket gamma=-1; analysis/w33_pass11687_11691_two_qutrit_e8_dictionary.py E8Data.act()",
         "explicit_embedding":"J248[:,j]=(Slp@vec(P_p0-P_p1 or P_p0-P_p2), zeros84, zeros84); injects 80D two-qutrit traceless contrasts into first 80 basis vectors of the repository 248 basis.",
         "J248_shape":[248,80],"J248_rank":rank,
         "per_generator":errs,"max_operator_reconstruction_residual":float(max_reconstruct),
         "jacobi_27_grade_case_max_residual":float(jacobi),
         "jacobi_coefficient_fit":[float(gamma.real),float(gamma.imag)],
         "physical_scope":"This IS an explicit 80->248 coordinate matrix in the repository's existing elementary sl9/exterior basis, and 5-generator bracket automorphism regression. It is NOT a new E8 construction; Pass11681 had the bracket and Jacobi certificate already. It is NOT an explicit normalized 248 Chevalley-root basis map, E8(-24) real form proof, or a physical matter Hamiltonian.",
         "checks":{k:bool(v) for k,v in checks.items()},
         "all_checks_pass":all(checks.values())}
    OUT.write_text(json.dumps(out,indent=2)+"\n")
    print(json.dumps({"checks":out["checks"],"max_jacobi":jacobi,
        "max_bracket_auto":max(q["repository_full_E8_bracket_automorphism_residual"] for q in errs)},indent=2))
    assert out["all_checks_pass"]
    return out
if __name__=="__main__":run()
