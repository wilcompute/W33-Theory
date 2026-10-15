"""Test the actual common stabilizer, rather than identify two C4's by size.

11983 owns the atlas connection,11987 its spin lifts;11663 owns the odd
Weil basis and Witting dictionary. The new test is their labelled action.
"""
import itertools
import json
from functools import lru_cache
from pathlib import Path
import numpy as np
import sympy as s
from w33_pass1081_1086_core import build_w33, symp, normalize
from w33_pass11663_odd_weil_normal_map import parity_bases, reduce_w, W
from w33_pass11980_heisenberg_fixed_holonomies import field_basis

ROOT=Path(__file__).resolve().parents[1]


def odd_encoding():
    even,odd=parity_bases()
    O=np.array(odd,float)/np.sqrt(2)
    E=np.array(even,float)@np.diag([1,*([1/np.sqrt(2)]*4)])
    assert np.max(abs(O.T@E))<1e-14
    return O,E


@lru_cache(None)
def displacement(v):
    X=s.zeros(3)
    for j in range(3):X[(j+1)%3,j]=1
    Z=s.diag(1,W,W**2)
    return s.kronecker_product(*[W**((2*v[j]*v[j+1])%3)*X**v[j]*Z**v[j+1] for j in (0,2)]).applyfunc(reduce_w)


def wedge2(a):
    pairs=list(itertools.combinations(range(4),2))
    return s.Matrix([[reduce_w(a[i,k]*a[j,l]-a[i,l]*a[j,k]) for k,l in pairs] for i,j in pairs])


def common_actions():
    pts,lookup,*_=build_w33();p=pts[0]
    opposite=[i for i,x in enumerate(pts) if i and symp(p,x)]
    a=s.Matrix([[int(i!=j and symp(pts[i],pts[j])==0) for j in opposite] for i in opposite])
    for i,x in enumerate(opposite):
        fiber={normalize((t*np.array(p)+b*np.array(pts[x]))%3) for t in range(3) for b in (1,2)}
        for j,y in enumerate(opposite):
            if i!=j and pts[y] in fiber:a[i,j]=1
    q=3*s.eye(27)-3*a+s.ones(27)
    columns=q.rref()[1];basis=q[:,list(columns)]
    left=(basis.T*basis).inv()*basis.T
    _,odd=parity_bases();rows=[]
    numeric_D=[np.array(displacement(v).subs(W,np.exp(2j*np.pi/3)),complex) for v in pts]
    numeric_L=[(np.eye(9)+d+d.conj().T)/3 for d in numeric_D]
    for v in pts:
        if symp(p,v):continue
        # U_v=omega I+(1-omega)L_v implements the inverse transvection.
        perm=[lookup[normalize((np.array(x)-symp(x,v)*np.array(v))%3)] for x in pts]
        T=s.zeros(27);oi={x:i for i,x in enumerate(opposite)}
        for j,x in enumerate(opposite):T[oi[perm[x]],j]=1
        r=left*T*basis
        assert T*basis==basis*r and r**3==s.eye(6)
        d=displacement(v);inv=displacement(tuple((-x)%3 for x in v))
        Lv=(s.eye(9)+d+inv)/3
        u=(W*s.eye(4)+(1-W)*(odd.T*Lv*odd)/2).applyfunc(reduce_w)
        ww=wedge2(u)
        full=(W*s.eye(9)+(1-W)*Lv).applyfunc(reduce_w)
        full_inverse=(W**2*s.eye(9)+(1-W**2)*Lv).applyfunc(reduce_w)
        assert (full*odd-odd*u).applyfunc(reduce_w)==s.zeros(9,4)
        for j in range(4):
            x=tuple(int(k==j) for k in range(4))
            y=tuple(int(t) for t in (np.array(x)-symp(x,v)*np.array(v))%3)
            assert (full*displacement(x)*full_inverse-displacement(y)).applyfunc(reduce_w)==s.zeros(9)
        un=np.exp(2j*np.pi/3)*np.eye(9)+(1-np.exp(2j*np.pi/3))*numeric_L[lookup[v]]
        err=max(np.max(abs(un@ell@un.conj().T-numeric_L[perm[j]])) for j,ell in enumerate(numeric_L))
        assert err<1e-12 and reduce_w(u.det())==1
        rows.append((v,r,u,ww,float(err)))
    return basis,rows


def tangent_repair(basis,actions):
    """Restrict scalars Q(omega)^3 -> Q^6 after dividing the ray phase."""
    constraints=[];tangents=[];coordinates=[0,2,3]
    for v,r,u,ww,err in actions:
        # For center label(0,0,0,1), the Witting ray is odd basis e_1.
        phase=u[1,1]
        assert all(u[i,1]==u[1,i]==0 for i in coordinates)
        t=(u.extract(coordinates,coordinates)*phase.subs(W,W**2)).applyfunc(reduce_w)
        A=t.applyfunc(lambda z:s.expand(z).coeff(W,0));B=t.applyfunc(lambda z:s.expand(z).coeff(W,1))
        real=A.row_join(-B).col_join(B.row_join(A-B))
        constraints.append(s.kronecker_product(s.eye(6),r)-s.kronecker_product(real.T,s.eye(6)))
        tangents.append(real)
    null=s.Matrix.vstack(*constraints).nullspace();assert len(null)==2
    S=s.Matrix(6,6,lambda i,j:null[0][i+6*j]);assert S.det()==9
    assert all(r*S==S*t for (_,r,_,_,_),t in zip(actions,tangents))
    omega6=s.zeros(3).row_join(-s.eye(3)).col_join(s.eye(3).row_join(-s.eye(3)))
    Jnumerator=2*S*omega6*S.inv()+s.eye(6);G=basis.T*basis
    assert Jnumerator**2==-3*s.eye(6)
    assert Jnumerator.T*G+G*Jnumerator==s.zeros(6)
    assert all(r*Jnumerator==Jnumerator*r for _,r,_,_,_ in actions)
    previous=json.loads((ROOT/'data/w33_pass11983_atlas_projector_descent.json').read_text())['compact_holonomy_closure']
    assert G==s.Matrix(previous['source_fiber_Gram'])
    loops=[]
    for row in previous['first_three_loop_matrices_Q_sqrt3']:
        loops.append(s.Matrix(row['rational'])+s.sqrt(3)*s.Matrix(row['sqrt3_coefficient']))
    defects=[]
    for name,h in [('H0',loops[0]),('H1',loops[1]),('H2',loops[2]),('H0 H1',loops[0]*loops[1])]:
        comm=h*Jnumerator-Jnumerator*h
        norm=s.simplify(s.trace(G.inv()*comm.T*G*comm)/3)
        assert norm>0
        defects.append(dict(loop=name,exact_metric_Frobenius_commutator_squared=str(norm)))
    return dict(Hom_dimension_over_Q=2,intertwiner_integer_matrix=S.tolist(),determinant=9,
        map='The atlas6 is exactly the scalar restriction of the projective tangent3 Hom(ray,ray_perp) at the odd-Weil Witting ray e1, for all13 labelled stabilizing transvections. Divide the transverse3 gate by its ray eigenphase BEFORE realifying.',
        tangent_Q_omega_coordinates=coordinates,complex_structure_numerator_Q=[[str(x) for x in row] for row in Jnumerator.tolist()],
        complex_structure='J=Jnumerator/sqrt3; J^2=-I and J.T G+GJ=0, with G the actual atlas source-fiber Gram.',
        finite_stabilizer_preserves_J=True,polar_holonomy_commutator_controls=defects,
        global_boundary='The11983 polar connection does not preserve thisJ, even on the displayed orientation-even loop. FullSO6 holonomy admits no parallel orthogonal complexstructure. A U3/family3-preserving connection or dynamical reduction is additional structure. This tangent intertwiner does NOT retract the different wedge2/spinor no-intertwiner above.',
        prior='analysis/PASS11664_11671_KERNEL_DYNAMICS.md already identifies odd transverse3 with the even mass-kernel3 on the Witting stabilizer. New here is the explicit integral map to11983 actual atlas6 and the holonomy/complex-structure compatibility test.')


def payload():
    basis,actions=common_actions();ranks={}
    for prime in (1009,1021):
        omega=next(t for t in range(2,prime) if (t*t+t+1)%prime==0)
        def residue(x):
            x=reduce_w(x);x=s.Poly(x,W)
            return int(sum(int(c.p)*pow(int(c.q),-1,prime)*pow(omega,int(e[0]),prime) for e,c in x.terms())%prime)
        constraints=[];progress=[]
        for v,r,u,ww,err in actions:
            a=np.array(r.applyfunc(residue),dtype=np.int64);b=np.array(ww.applyfunc(residue),dtype=np.int64)
            constraints.append(np.kron(np.eye(6,dtype=np.int64),a)-np.kron(b.T,np.eye(6,dtype=np.int64)))
            rank=field_basis(np.concatenate(constraints),prime).shape[1];progress.append(rank)
            if rank==36:break
        assert progress[-1]==36
        ranks[str(prime)]=dict(omega_residue=omega,progress=progress)
    row=next(row for row in actions if row[0]==(0,1,0,0))
    assert s.trace(row[1])==3 and reduce_w(s.trace(row[3]))==-3
    x=s.Symbol('x');rpoly=s.factor(row[1].charpoly(x).as_expr())
    wpoly=s.Poly(row[3].charpoly(x).as_expr(),x)
    wpoly=s.factor(sum(reduce_w(c)*x**i[0] for i,c in wpoly.terms()))
    assert rpoly==(x-1)**4*(x*x+x+1)
    assert wpoly==(x*x+x+1)**3
    O,E=odd_encoding()
    return dict(status='PASS',common_center_point=0,center_label=[0,0,0,1],
        stabilizing_transvections_checked=len(actions),atlas_fiber_basis=basis.tolist(),
        exact_trace_obstruction=dict(direction=list(row[0]),atlas_vector_trace=3,odd_Weil_exterior_square_trace=-3,
            atlas_characteristic_polynomial=str(rpoly),Weil_exterior_square_characteristic_polynomial=str(wpoly)),
        exact_Q_omega_canonical_Pauli_conjugations_checked=4*len(actions),
        common_label_equivariance_max=max(row[4] for row in actions),
        Hom_dimension_over_Q_omega=0,Hom_modular_full_rank_certificates=ranks,
        exact_projective_tangent_repair=tangent_repair(basis,actions),
        conclusion='No nonzero intertwiner between the specified six-dimensional atlas stabilizer action and wedge2 of the odd Weil action with the SAME Pauli-label action. Therefore no invertible equivariant identification of the associated spinor and odd-Weil carriers follows. In fact the vector eigenvalue multiplicities4+1+1 versus3+3 also exclude a scalar projective identification for the displayed element.',
        odd_encoding_real=O.tolist(),even_auxiliary_encoding_real=E.tolist(),
        available_repair='Declare the prior odd-Weil C4 as an encoding of the atlas gate matrices. This is a choice of Hilbert-space coordinates, not an intertwiner of their original finite symmetry actions.11990 gives explicit paths using four of the five even levels as auxiliaries.',
        actions=[dict(direction=list(v),atlas_trace=str(s.trace(r)),Weil_wedge_trace=str(reduce_w(s.trace(ww)))) for v,r,u,ww,err in actions],
        scope='A labelled representation obstruction and explicit two-qutrit encoding. Different group homomorphisms, outer twists or additional symmetry breaking are not excluded.',
        prior=['11983 native atlas six-spaces','11987 spinor gate library','analysis/PASS11663_ODD_WEIL_NORMAL_MAP.md owns the odd-Weil basis and Witting/Pauli labelled projectors','analysis/PASS11664_11671_KERNEL_DYNAMICS.md owns the transverse3/masskernel3 equality','analysis/2026-10-10_toe45_cusp_tomography_parallel_research_audit.md owns other labelledPauli incidence maps','W33_FOR_EVERYONE.tex historical Wittinggeometry, not an atlas-spinor identification'])


if __name__=='__main__':
    d=payload();(ROOT/'data/w33_pass11988_spinor_weil_intertwiner.json').write_text(json.dumps(d,indent=2,default=int)+'\n');print(d['status'],d['Hom_dimension_over_Q_omega'])
