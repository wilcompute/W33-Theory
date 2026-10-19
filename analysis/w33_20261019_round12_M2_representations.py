"""Explicit rational 2x2 representations of the three simple M2 blocks
in the 17-dimensional Clifford-vacuum orbital adjacency algebra.

Central idempotents E_i from Round12 provide 4D regular ideals;
find 2D minimal left ideals by diagonalizing a right-regular element.
"""
import json,itertools
from pathlib import Path
import sympy as S
import numpy as np
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/"data/w33_20261019_round12_M2_representations.json"
def coordinate_rep(A,V):
    # exact restricted linear map on columns of V
    n=V.cols
    # pick n independent rows by rank of transposed basis
    _,piv=V.T.rref()
    ids=list(piv[:n])
    R=V[ids,:]
    assert R.det()!=0
    T=R.inv()* (A*V)[ids,:]
    assert A*V==V*T
    return T
def run():
    p=np.array(json.loads((ROOT/"data/w33_20261019_round11_vacuum_intersection_algebra.json").read_text())["intersection_numbers_p_i_j_k"],dtype=int)
    d=json.loads((ROOT/"data/w33_20261019_round12_central_spectrum.json").read_text())
    L=[S.Matrix(p[i,:,:].T.tolist()) for i in range(17)]
    R=[S.Matrix(p[:,i,:].T.tolist()) for i in range(17)]
    blocks=[]
    for id,Erows in enumerate(d["central_idempotents_17x17_rational"]):
        if d["central_idempotents_regular_ranks"][id]!=4:continue
        E=S.Matrix([[S.Rational(v) for v in row] for row in Erows])
        V=S.Matrix.hstack(*E.columnspace())
        assert V.cols==4
        first=None
        for i in range(1,17):
            r4=coordinate_rep(R[i],V)
            eigs=r4.eigenvects()
            for lam,mul,vecs in eigs:
                if len(vecs)==2 and lam.is_Rational:
                    W=V*S.Matrix.hstack(*vecs)
                    assert W.cols==2 and W.rank()==2
                    mats=[coordinate_rep(A,W) for A in L]
                    assert all(m*n==coordinate_rep(L[i]*L[j],W) for i,m in enumerate(mats) for j,n in enumerate(mats))
                    first={"right_generator_orbit":i,"right_eigenvalue":str(lam),
                           "matrices_17_of_2x2":[[[str(v) for v in row] for row in m.tolist()] for m in mats]}
                    break
            if first is not None:break
        if first is None:
            # Algebraic right eigenvalues can be accepted, but report as
            # unconstructed rather than misleadingly claiming matrices.
            blocks.append({"id":id,"found_rational_2D_simple_rep":False})
        else:
            blocks.append({"id":id,"found_rational_2D_simple_rep":True,**first})
    good=sum(q["found_rational_2D_simple_rep"] for q in blocks)
    checks={"three_4dim_regular_blocks":len(blocks)==3,
        "all_three_rational_2x2_representations":good==3}
    out={"schema":"w33.round12.explicit_rational_three_M2_representations.v1",
        "theorem":"Starting from eight exact central idempotents, identify the three rank-four left-regular ideals. In each ideal find an eigenspace of dimension two for a rational right-regular operator, invariant under all left multiplications. Restrict the 17 orbital generators to these invariant 2D subspaces, giving exact rational 2x2 matrices satisfying all 17x17 orbital multiplication structure constants. The other five blocks are 1D, reconstructed from central idempotents separately.",
        "rank_four_factors":blocks,"rational_2x2_blocks_found":good,
        "checks":checks,"all_checks_pass":all(checks.values())}
    OUT.write_text(json.dumps(out,indent=2)+"\n")
    print(json.dumps({"pass":out["all_checks_pass"],"blocks":[(b["id"],b.get("right_generator_orbit"),b.get("right_eigenvalue")) for b in blocks]},indent=2))
    assert out["all_checks_pass"]
    return out
if __name__=="__main__":run()
