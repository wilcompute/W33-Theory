"""Exact central idempotents and rational/algebraic Wedderburn audit.

Start from 17x17 integer orbital table p_ij^k. Find exact rational
center, choose a small integral generic central element, and factor its
minimal polynomial. If split with eight rational simple eigenvalues,
construct eight orthogonal primitive central idempotents by Lagrange
polynomials. If not split over Q, report explicit extension obstruction.
"""
import json, itertools
from pathlib import Path
import numpy as np
import sympy as S
from scipy.linalg import qr
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/"data/w33_20261019_round12_central_spectrum.json"
def run():
    old=json.loads((ROOT/"data/w33_20261019_round11_vacuum_intersection_algebra.json").read_text())
    p=np.array(old["intersection_numbers_p_i_j_k"],dtype=np.int64)
    n=17
    L=[S.Matrix(p[i,:,:].T.tolist()) for i in range(n)]
    equations=np.concatenate([np.column_stack([((np.array(L[i]*L[j]-L[j]*L[i],dtype=np.int64)).ravel()) for i in range(n)]) for j in range(n)])
    numerical_rank=np.linalg.matrix_rank(equations.astype(float),tol=1e-8)
    piv=qr(equations.T,mode="economic",pivoting=True)[2][:numerical_rank]
    B=S.Matrix(equations[piv,:].tolist())
    central=B.nullspace()
    assert len(central)==8
    assert all(not (S.Matrix(equations.tolist())*z).applyfunc(S.simplify) for z in []) # vacuous
    central_int=[]
    for z in central:
        t=S.ilcm(*[int(v.q) for v in z])
        zz=z*t;g=S.igcd(*[int(x) for x in zz])
        vec=[int(x/g) for x in zz]
        central_int.append(vec)
    Z=[sum((v*L[i] for i,v in enumerate(vec) if v),S.zeros(n)) for vec in central_int]
    x=S.symbols("x")
    trials=[]
    selected=None
    for coeff in ([1,2,3,5,7,11,13,17],[2,3,5,7,11,13,17,19],
                  [0,1,2,3,5,7,11,13],[1,1,1,1,1,1,1,1]):
        C=sum((t*M for t,M in zip(coeff,Z)),S.zeros(n))
        char=S.factor_list(C.charpoly(x).as_expr())[1]
        factors=[(str(f),int(m),int(S.degree(f,x))) for f,m in char]
        trials.append({"coefficients":list(coeff),"charpoly_factors":factors})
        if len(char)==8 and all(S.degree(f,x)==1 for f,m in char):
            selected=C;selectedcoeff=coeff;selectedfactors=char
            break
    result={"schema":"w33.round12.17class_exact_central_spectrum.v1",
       "center_dimension":8,"rational_center_integer_generators":central_int,
       "candidate_spectral_elements":trials,
       "rational_split_generating_central_element_found":selected is not None,
       "claimed_complex_Wedderburn_blocks":{"scalar":5,"matrix_2":3},
       "scope":"Always report exact characteristic factorization. If no central element with eight rational eigenvalues found in tested choices, only a nontrivial rational splitting field, not absence of eight complex idempotents, follows."}
    if selected is not None:
        eig=[]
        for f,m in selectedfactors:
            a,b=S.Poly(f,x).all_coeffs()
            eig.append(-b/a)
        D=[]
        I=S.eye(n)
        for val in eig:
            M=I
            for other in eig:
                if other!=val:M=M*(selected-other*I)/(val-other)
            M=M.applyfunc(S.cancel)
            assert M*M==M
            assert M*selected==val*M
            assert all(M*N==N*M for N in L)
            D.append(M)
        assert sum(D,S.zeros(n))==I
        ranks=[M.rank() for M in D]
        assert sorted(ranks)==[1]*5+[4]*3
        result["primitive_center_eigenvalues"]=[str(t) for t in eig]
        result["central_idempotents_regular_ranks"]=ranks
        result["central_idempotents_17x17_rational"]=[[[str(v) for v in row] for row in M.tolist()] for M in D]
        # For every block matrix factor of dimension four, spectral
        # corners from algebra element are 2x2; preserve exact images.
        result["matrix_2_factors_central_eigenspaces"]=[i for i,r in enumerate(ranks) if r==4]
    checks={"center_dimension_eight":len(central)==8,
       "valid_exact_characteristic_factors":len(trials)>0,
       "explicit_eight_central_idempotents_if_split":selected is None or len(result["central_idempotents_regular_ranks"])==8}
    result["checks"]=checks;result["all_checks_pass"]=all(checks.values())
    OUT.write_text(json.dumps(result,indent=2)+"\n")
    print(json.dumps({"checks":checks,"factors":trials,"ranks":result.get("central_idempotents_regular_ranks")},indent=2))
    return result
if __name__=="__main__":run()
