#!/usr/bin/env python3
"""Exact joint obstruction to 24D Euclidean eiconal cubic:
any invariant cubic a*sum x_i^3+b*sum_s(Z_s.x)^3 fails
|grad C|^2=constant*|x|^4 on V24, certified by 4 integer vectors.

Theory: Tkachev (2010) classifies eiconal cubic solutions; no Cartan
cubic in dimension 24. This independent integer determinant test is stronger
as a reproducible self-contained certificate for THIS invariant pencil.
"""
from pathlib import Path
import sys,json
import numpy as np
import sympy as sp
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'analysis'))
from w33_20261102_route_216_cubic_tomography import geometry
from w33_20261102_five_deeper_fronts import route_frame

def main():
    pts,lines,N,idx,norm,omega=geometry()
    A=N@N.T-4*np.eye(40,dtype=np.int64)
    P=5*A+20*np.eye(40,dtype=np.int64)-2*np.ones((40,40),dtype=np.int64)
    assert np.array_equal(P@P,30*P)
    assert np.array_equal(A@P,2*P)
    Z,_=route_frame()
    assert Z.shape==(216,40)
    # This is the canonical G-invariant inner product, unique up to
    # positive scalar since V24 is a real-type absolutely irreducible.
    PP=P.astype(object);ZZ=Z.astype(object)
    rng=np.random.default_rng(20261105)
    data=[]
    for t in range(9):
        w=rng.integers(-2,3,size=40,dtype=np.int64)
        x=PP@w.astype(object)
        assert np.array_equal(A.astype(object)@x,2*x)
        U=ZZ@x
        g1=PP@(x*x)
        g2=PP@(ZZ.T@(U*U))
        # g1, g2 are 10 times the projected gradients of C_point,C_route
        # due to gradient factor 3 and P/30 orthogonal projection.
        k11=int(g1@g1);k12=int(2*(g1@g2));k22=int(g2@g2)
        quart=int((x@x)**2)
        data.append({'seed':t,'w':list(map(int,w)),
            'norm_squared':int(x@x),
            'grad_quartic_coefficients':[k11,k12,k22],
            'norm_quartic':quart})
    witness=None
    M=sp.Matrix([[*r['grad_quartic_coefficients'],-r['norm_quartic']] for r in data])
    assert M.rank()==4
    from itertools import combinations
    for inds in combinations(range(len(data)),4):
        det=int(M[list(inds),:].det())
        if det:
            witness={'row_indices':list(inds),'integer_determinant':str(det)}
            break
    assert witness
    # All two cubics are harmonic: point cubic Laplacian project:
    # 6 sum_i P e_i norm² <P e_i,x>=6 const sum_i x_i=0.
    # Route cubic: 6 sum_s ||P Z_s||² (Z_s.x),
    # all route row norms equal, and sum_s Z_s = 0.
    norms=[int(z@z) for z in ZZ]
    assert len(set(norms))==1, set(norms)
    assert not any(sum(int(ZZ[s,j]) for s in range(216)) for j in range(40))
    assert np.array_equal(P@np.ones(40,dtype=int),np.zeros(40,dtype=int))
    out={
     'status':'PASS_EXACT_RANK4_EICONAL_CUBIC_PENCIL_NO_GO',
     'G':'PSp4(3)','carrier_dimension':24,
     'invariant_cubic_pencil':'a*Cpoint+b*Croute',
     'integer_samples':data,
     'rank_of_linearized_eiconal_constraints':4,
     'four_row_determinant_certificate':witness,
     'eiconal_constraint':'For all x in V24, |grad(a*Cpoint+b*Croute)|^2 = lambda*|x|^4. Its coefficients [a^2,ab,b^2,lambda] must lie in the kernel of the exact 4-column matrix. Our rank-4 witness excludes all nonzero a,b and all lambda.',
     'both_cubics_harmonic':True,
     'route_row_norm_squared':norms[0],
     'Tkachev_classification_corroboration':'Homogeneous real cubic eiconal solutions are reducible x_n^3-3x_n|x_perp|^2 or exceptional Cartan in dimensions 5,8,14,26. All PSp4(3)-invariant cubics here are harmonic and 24D, excluding both cases.',
     'scope':'No invariant cubic on irreducible Euclidean W33 24D satisfies the Cartan eiconal equation. This does NOT prohibit an Albert cubic N on a larger 27D algebra, since its restriction to a 24D submodule need not satisfy that eiconal equation; a different nonlinear metric or symmetry-breaking embedding not tested.'}
    target=ROOT/'data/w33_20261102_exact_eiconal_cubic_pencil_obstruction.json'
    target.write_text(json.dumps(out,indent=2)+'\n',encoding='utf-8')
    print('EICONAL_EXACT',json.dumps({'rank':M.rank(),'witness':witness,'rows':len(data),'route_row_norm_squared':norms[0]})[:2800],flush=True)
    return out
if __name__=='__main__':main()
