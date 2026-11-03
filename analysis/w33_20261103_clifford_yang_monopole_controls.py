"""Native gamma-axis realization of the known Yang bundle, with controls.

Pass4153 owns the synthetic second-Chern construction in this repo. This
checks the actual native matrices, Wilson loops and enlarged-group boundary.
"""
import itertools
import json
import pathlib
import sys

import numpy as np
import sympy as s

ROOT=pathlib.Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'analysis'))
from w33_20261102_toroidal_knight_clifford_bridge import matrices


def wilson(gamma,plane,epsilon,steps):
    vertices=[(0.,0.),(epsilon,0.),(epsilon,epsilon),(0.,epsilon),(0.,0.)]
    coordinates=[]
    for a,b in zip(vertices,vertices[1:]):
        for u in np.linspace(0,1,steps,endpoint=False):coordinates.append((1-u)*np.array(a)+u*np.array(b))
    coordinates.append(np.zeros(2));frames=[]
    for x,y in coordinates:
        n=np.zeros(5);n[plane[0]]=x;n[plane[1]]=y;n[4]=np.sqrt(1-x*x-y*y)
        H=np.einsum('a,aij->ij',n,gamma);frames.append(np.linalg.eigh(H)[1][:,:2])
    hol=np.eye(2,dtype=complex)
    for a,b in zip(frames,frames[1:]):
        left,_,right=np.linalg.svd(a.conj().T@b);hol=hol@(left@right)
    assert np.max(abs(hol.conj().T@hol-np.eye(2)))<1e-12
    return hol


def build():
    gamma,blades,old,omega=matrices();product=s.eye(4)
    for g in gamma:product*=g
    sign=int(product[0,0]);assert product==sign*s.eye(4) and sign in [-1,1]
    P=(s.eye(4)-gamma[4])/2;density=0
    for p in itertools.permutations(range(4)):
        parity=sum(p[i]>p[j] for i in range(4) for j in range(i+1,4))%2
        term=P
        for j in p:term=term*(-gamma[j]/2)
        density+=(-1)**parity*s.trace(term)
    assert density==-3*sign
    metric=s.Matrix(4,4,lambda i,j:s.trace(gamma[i]*gamma[j])/8)
    assert metric==s.eye(4)/2
    numeric=np.array([np.array(g,dtype=complex) for g in gamma]);samples=[]
    for steps in [16,32,64]:
        A=wilson(numeric,(0,1),.25,steps);B=wilson(numeric,(0,2),.25,steps)
        comm=float(np.linalg.norm(A@B-B@A));assert comm>1e-4
        samples.append(dict(steps_per_edge=steps,loop_A_trace=float(np.trace(A).real),loop_B_trace=float(np.trace(B).real),commutator_Frobenius=comm,maximum_unitarity_error=max(float(np.max(abs(A.conj().T@A-np.eye(2)))),float(np.max(abs(B.conj().T@B-np.eye(2)))))))
    U=(s.eye(4)+s.I*blades[15])/s.sqrt(2);residuals=[]
    for g in gamma:
        transformed=s.simplify(U*g*U.conjugate().T)
        projection=s.zeros(4)
        for h in gamma:projection+=s.simplify(s.trace(h*transformed)/4)*h
        delta=s.simplify(transformed-projection);residuals.append(int(s.simplify(s.trace(delta.conjugate().T*delta))))
    assert sorted(residuals)==[0,4,4,4,4]
    return dict(status='PASS_NATIVE_YANG_BUNDLE_AND_NONABELIAN_CONTROLS',gamma_volume_sign=sign,
        rank2_projector='P(n)=(I-sum n_a gamma_a)/2 on the supplied unit S4.',
        north_pole_Tr_P_dP4_density=int(density),second_Chern_number=int(density/3),first_Chern_number=0,
        exact_density_proof='Clifford covariance gives density=-3*gamma_volume_sign times the unit S4 volume form. Vol(S4)=8*pi^2/3, so (8*pi^2)^-1 integral Tr P(dP)^4=-gamma_volume_sign.',
        tangent_Grassmann_metric='g_ij=(1/2)Tr(d_iP d_jP)=delta_ij/2 in north-pole tangent coordinates.',
        noncommuting_Wilson_loop_convergence=samples,added_gate_gamma_span_residual_squared=residuals,
        enlarged_group_boundary='The added Clifford gate takes four of the five Hermitian gamma axes outside their linear span. This S4 family is Spin5-covariant, not invariant under the full enlarged SU4 Clifford action. Its six-skew-form representation is a different carrier.',
        vacuum_boundary='The conditional vacuum orbit is S5, with H4(S5)=0. The Yang bundle lives on a separately supplied S4 control manifold; its Chern number is not a monopole charge forced on the vacuum orbit.',
        ownership='Pass4153/BT4153_BT4160 already establishes the standard second-Chern synthetic pump. This records the actual native gamma sign, noncommuting controlled loops and an explicit covariance obstruction.',
        reference='https://arxiv.org/abs/1610.06228',
        boundary='Exact synthetic bundle invariant and numerical Wilson-loop convergence. No physical parameter manifold, protected laboratory gate or spacetime dimension derived.')


if __name__=='__main__':
    d=build();(ROOT/'data/w33_20261103_clifford_yang_monopole_controls.json').write_text(json.dumps(d,indent=2)+'\n',encoding='utf-8')
    print(d['status'],d['second_Chern_number'],d['noncommuting_Wilson_loop_convergence'][-1],flush=True)
