#!/usr/bin/env python3
"""Exact LOCAL line-variance action for W(3,q), and a mediator-selection ambiguity.

For each symplectic-isotropic line ell with q+1 projective points,
K_ell = diag(1_ell) - 1_ell 1_ell^T/(q+1) is a positive semidefinite
rank-q centering projector. Sum over lines recovers graph Laplacian
exactly up to q+1; line SUM instead kills the 15d dark sector at q=3.
The W33 incidence identities belong to Pass4956 and prior repo results.
"""
from pathlib import Path
import json,itertools,math,sys
import numpy as np
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'analysis'))
from toe_20261103_q_pascal_symplectic_scale_selector import projective_points,omega
def build(q):
    pts=projective_points(q)
    index={p:i for i,p in enumerate(pts)}
    lines=set()
    for i,a in enumerate(pts):
        for b in pts[i+1:]:
            if omega(a,b,q):continue
            line=[]
            for x,y in itertools.product(range(q),repeat=2):
                if x==y==0:continue
                v=tuple((x*a[t]+y*b[t])%q for t in range(4))
                pivot=next(k for k in v if k)
                inv=pow(pivot,-1,q)
                line.append(index[tuple((z*inv)%q for z in v)])
            line=tuple(sorted(set(line)))
            assert len(line)==q+1
            lines.add(line)
    lines=sorted(lines)
    assert len(lines)==len(pts)
    N=len(pts)
    Z=np.zeros((N,N),dtype=np.int64)
    for j,line in enumerate(lines):Z[list(line),j]=1
    A=Z@Z.T-(q+1)*np.eye(N,dtype=np.int64)
    assert set(A.ravel())<={0,1}
    assert np.array_equal(A,A.T)
    assert np.all(A.sum(1)==q*(q+1))
    return Z,A,lines
def case(q):
    Z,A,lines=build(q)
    n=len(A)
    I=np.eye(n,dtype=np.int64)
    L=q*(q+1)*I-A
    assert np.array_equal(Z@Z.T, (q+1)*I+A)
    # Centered variances aggregated, no independent "graph mass" assumption:
    # (q+1)∑ell K_ell = L, where K_ell=D_ell-1/(q+1) z_ell z_ell^T.
    diag_sum=np.diag(Z.sum(1))
    K_num=(q+1)*diag_sum-Z@Z.T
    assert np.array_equal(K_num,L)
    eigen=np.linalg.eigvalsh(L)
    near=lambda x:int(np.count_nonzero(abs(eigen-x)<1e-7))
    dim0,dimsmall,dimlarge=near(0),near(q*q+1),near((q+1)*(q+1))
    assert dim0==1 and dimsmall==q*(q+1)**2//2 and dimlarge==n-1-dimsmall
    # Gram ZZ.T eigenvalues: {(q+1)^2,2q,0}; rank=1+dimsmall
    gram=np.linalg.eigvalsh(Z@Z.T)
    null=int(np.count_nonzero(abs(gram)<1e-8))
    assert null==dimlarge
    assert max(abs(Z.sum(0)-(q+1)))==0
    # Exact line variance energy on nonconstant vector.
    trial=np.arange(n,dtype=float)
    lhs=float(trial@L@trial)
    rhs=0.
    for line in lines:
        y=trial[list(line)]
        rhs+=(q+1)*float(np.sum((y-y.mean())**2))
    assert abs(lhs-rhs)<1e-8*max(1,abs(lhs))
    return {'q':q,'points_and_lines':n,'line_size':q+1,
      'graph_eigen_laplacian':{'0':dim0,str(q*q+1):dimsmall,str((q+1)**2):dimlarge},
      'rank_point_to_line_incidence':n-null,
      'incidence_dark_kernel_dimension':null,
      'graph_Laplacian_equals_scaled_sum_of_local_centered_line_projectors':True,
      'local_variance_energy_identity_numerical_residual':lhs-rhs,
      'line_sum_and_line_variance_choose_different_zero_sectors':True}
def main():
    rows=[case(q) for q in (3,5)]
    assert rows[0]['incidence_dark_kernel_dimension']==15
    assert rows[0]['graph_eigen_laplacian']=={'0':1,'10':24,'16':15}
    out={'status':'PASS_W33_LINE_LOCAL_VARIANCE_ACTION_MEDIATOR_AMBIGUITY',
       'rows':rows,
       'exact_identity':'For W(3,q) point-line incidence Z, each line ell contains q+1 points, K_ell=Diag(1_ell)-(1/(q+1))1_ell 1_ell^T is PSD. The combinatorial point Laplacian L_W=q(q+1)I-A=(q+1)sum_ell K_ell. Independently ZZ.T=(q+1)I+A and therefore a naive sum-of-line-amplitudes quadratic action u.T ZZ.T u has a (q-dependent) dark nullspace: dimension 15 at q=3. The centered line-variance action has only constants in its kernel and masses both 24D and 15D sectors.',
       'physical_interpretation':'A microscopic local q+1-point line fluctuation action can generate exactly the W33 graph Laplacian. But the alternative local positive line-amplitude coupling gives a different massless sector. Incidence geometry alone does not select which action or how the active portal is normalized. The active kinetic interaction/quantum symmetry must be specified independently before predicting a mass gap.',
       'prior_owner':'W33 line incidence singular rank25 and its point-line +2/-4 intertwiners were already derived by repo analysis/w33_pass4956_point_line_24d_intertwiner.py and exploration/w33_point_line_spread_rank_one_bridge.py; the present contribution is the explicit local centered-line Dirichlet action and gate implications.',
       'caveats':'Euclidean positive quadratic forms, not a chiral gauge action, not spacetime derivation, no portal microscopics or quantum radiative corrections.',
       'sources':['https://mathworld.wolfram.com/GeneralizedQuadrangle.html']}
    (ROOT/'data/toe_20261103_W33_local_line_variance_action.json').write_text(json.dumps(out,indent=2)+'\n')
    print('W33_LINE_ACTION',json.dumps(rows),flush=True)
if __name__=='__main__':main()
