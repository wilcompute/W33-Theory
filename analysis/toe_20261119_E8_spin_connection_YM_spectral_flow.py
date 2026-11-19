"""E8 spin-connection background on the specified H27 quotient.

Exact algebra supports the companion analytic sphere/quotient calculation.
The curved connection solves probe Yang-Mills and has charged Dirac zeros,
but has eleven globally descending negative Yang-Mills Hessian directions.
This is not an eleven-dimensional E8 Yang-Mills theory or a G2 vacuum.
"""
from collections import Counter
from itertools import combinations, product
from pathlib import Path
import json
import numpy as np
import sympy as s
from toe_20261118_E8_H27_wire_index_parity import e8_roots_twice

ROOT=Path(__file__).resolve().parents[1]


def orthogonal_branching():
    roots=e8_roots_twice()
    # Drop the eighth Cartan plane: its two real axes supply the odd
    # coordinates of R5 + R11. Coordinates below are twice the weights.
    actual=Counter(tuple(r[:7]) for r in roots)
    actual[(0,)*7]+=8
    def vector_weights(rank):
        ans=[(0,)*rank]
        for j in range(rank):
            for sign in (-2,2):
                v=[0]*rank;v[j]=sign;ans.append(tuple(v))
        return ans
    def B_adjoint(rank):
        ans=Counter({(0,)*rank:rank})
        for i,j in combinations(range(rank),2):
            for a,b in product((-2,2),repeat=2):
                v=[0]*rank;v[i]=a;v[j]=b;ans[tuple(v)]+=1
        for v in vector_weights(rank):
            if any(v):ans[v]+=1
        return ans
    target=Counter()
    for w,n in B_adjoint(2).items():target[w+(0,)*5]+=n
    for w,n in B_adjoint(5).items():target[(0,)*2+w]+=n
    for u,v in product(vector_weights(2),vector_weights(5)):target[u+v]+=1
    for signs in product((-1,1),repeat=7):target[signs]+=1
    assert actual==target and sum(actual.values())==248
    trace_E8=sum(s.Rational(w[0],2)**2*n for w,n in actual.items())
    trace_vector5=sum(s.Rational(w[0],2)**2 for w in vector_weights(2))
    assert trace_E8==60 and trace_vector5==2
    return {'roots_restriction_matches':240,'Cartan_zero_weights':8,
            'Spin5_times_Spin11_branch':'(10,1)+(1,55)+(5,11)+(4,32)',
            'block_dimensions':[10,55,55,128],
            'adjoint_E8_trace_H_squared':60,'Spin5_vector_trace_H_squared':2,
            'basic_embedding_index':1,
            'prior_art':'Round35 already gave this branching and vectorlike Spin11->Spin10 barrier; new use is the curved connection and spectral flow'}


def clifford_data():
    I=s.eye(2)
    X=s.Matrix([[0,1],[1,0]])
    Y=s.Matrix([[0,-s.I],[s.I,0]])
    Z=s.diag(1,-1)
    gamma=[s.kronecker_product(X,I),s.kronecker_product(Y,I),
           s.kronecker_product(Z,X),s.kronecker_product(Z,Y),s.kronecker_product(Z,Z)]
    for i,j in product(range(5),repeat=2):
        assert gamma[i]*gamma[j]+gamma[j]*gamma[i]==(2*s.eye(4) if i==j else s.zeros(4))
    return gamma


def parallel_spinor_and_flow():
    gamma=clifford_data();I=s.eye(4);psi=I.reshape(16,1)
    rotations=[gamma[a]*gamma[b]/2 for a,b in combinations(range(5),2)]
    total=[s.kronecker_product(T,I)-s.kronecker_product(I,T.T) for T in rotations]
    constraints=s.Matrix.vstack(*total)
    assert len(constraints.nullspace())==1
    assert all(T*psi==s.zeros(16,1) for T in total)
    self_dual=s.Matrix.vstack(*[s.kronecker_product(T,I)+s.kronecker_product(I,T) for T in rotations]).nullspace()
    assert len(self_dual)==1
    J=self_dual[0].reshape(4,4)
    assert J.T==-J and J.det()!=0 and J*J.conjugate()==-I
    curvature=s.zeros(16)
    for a,b in combinations(range(5),2):
        T=gamma[a]*gamma[b]/2
        curvature+=s.kronecker_product(-gamma[a]*gamma[b],-T.T)
    assert curvature*psi==-5*psi
    slopes=[]
    for sign in (1,-1):
        coset=[-sign*s.I*g.T/2 for g in gamma]  # dual Spin6 halfspin
        for a,b in combinations(range(5),2):
            gauge_ab=-(gamma[a]*gamma[b]/2).T
            assert coset[a]*coset[b]-coset[b]*coset[a]==-gauge_ab
        change=sum((s.kronecker_product(s.I*g,t) for g,t in zip(gamma,coset)),s.zeros(16))
        slope=sign*s.Rational(5,2)
        assert change*psi==slope*psi
        slopes.append(str(slope))
    return {'parallel_spinor_line_dimension':1,'Clifford_anticommutator_checks':25,
            'Spin5_spinor_self_duality_symplectic_matrix':[[str(t) for t in J.row(i)] for i in range(4)],
            'quaternionic_structure_square':-1,
            'spin_and_dual_spin_connection_cancel':True,
            'scalar_curvature_over4_at_R1':5,
            'gauge_curvature_term_on_parallel_line_at_R1':-5,
            'Spin10_16_and_16bar_homogeneous_D5_eigenvalues_R_units':['5*s/2','-5*s/2'],
            'verified_slopes':slopes,
            'scope':'Exact eigenbranches through the former zero modes, not the entire spectrum for intermediate s'}


def sphere_kernel_census():
    # Dolan/Parthasarathy on S5=Spin6/Spin5, long roots length2:
    # R^2 D_tau^2 = C_Spin6(pi)+5/2-C_Spin5(tau).
    fund=[s.Matrix([1,0,0]),s.Matrix([s.Rational(1,2),s.Rational(1,2),-s.Rational(1,2)]),
          s.Matrix([s.Rational(1,2),s.Rational(1,2),s.Rational(1,2)])]
    rho=s.Matrix([2,1,0])
    casimir=lambda w:(w.T*(w+2*rho))[0]
    fundamental=[casimir(w) for w in fund]
    assert fundamental==[5,s.Rational(15,4),s.Rational(15,4)]
    assert all((a.T*b)[0]>=0 for a,b in product(fund,repeat=2))
    assert min(casimir(w) for w in [fund[0],2*fund[1],2*fund[2],fund[1]+fund[2]])==5
    for a,b,c in product(range(5),repeat=3):
        if not(a or b or c):continue
        value=casimir(a*fund[0]+b*fund[1]+c*fund[2])
        assert value>=s.Rational(15,4)
        if (b+c)%2==0:assert value>=5
    blocks=[]
    for tau,mult,C in [(1,55,0),(5,11,4),(10,1,6),(4,32,s.Rational(5,2))]:
        zero=1 if tau==4 else 0
        lower=5 if tau==4 else s.Rational(15,4)+s.Rational(5,2)-C
        assert lower>0
        blocks.append({'Spin5_rep_dimension':tau,'Spin11_multiplicity':mult,
                       'Spin5_Casimir':str(C),'D5_kernel_per_copy':zero,
                       'positive_D5_squared_lower_bound_times_R2':str(lower)})
    assert sum(v['D5_kernel_per_copy']*v['Spin11_multiplicity'] for v in blocks)==32
    return {'formula':'RÂ² D_tauÂ²=C_Spin6(pi)+5/2-C_Spin5(tau)',
            'minimum_nontrivial_Spin6_Casimir':'15/4',
            'minimum_nontrivial_nonspinorial_Casimir':5,'blocks':blocks,
            'cover_D5_complex_kernel_dimension':32,
            'Y7_D7_complex_kernel_by_base_spin_structure':{'periodic_periodic':64,'antiperiodic_periodic':0,'periodic_antiperiodic':0,'antiperiodic_antiperiodic':0},
            'periodic_kernel_Spin11_rep':'two copies of spinor32',
            'Spin10_restriction':'two16 plus two16bar; zero representation-theoretic net chirality',
            'hypotheses':'natural vertical-spin gauge lift, no additional Spin11 Wilson twist, specified round-product quotient metric',
            'not_claimed':'64 physical four-dimensional Weyl particles or three generations'}


def matrix_generator(i,j):
    M=np.zeros((16,16),dtype=np.int64);M[i,j]=1;M[j,i]=-1
    return M


def YM_energy_and_Hessian():
    v=s.symbols('v0:11',real=True)
    u=sum(t*t for t in v)
    energy=(1-u)**2
    Hess=s.hessian(energy,v).subs(dict.fromkeys(v,0))
    assert Hess==-4*s.eye(11)
    bracket=lambda A,B:A@B-B@A
    F={(a,b):matrix_generator(a,b) for a,b in combinations(range(5),2)}
    for a,b in product(range(5),repeat=2):
        if a>=b:continue
        for I in range(5,16):
            assert np.array_equal(bracket(matrix_generator(a,I),matrix_generator(b,I)),-F[a,b])
    def f(a,b):
        return np.zeros((16,16),dtype=np.int64) if a==b else (F[a,b] if a<b else -F[b,a])
    for I,b in product(range(5,16),range(5)):
        tangent=matrix_generator(b,I)
        J=4*tangent+2*sum((bracket(f(a,b),matrix_generator(a,I)) for a in range(5)),np.zeros((16,16),dtype=np.int64))
        assert np.array_equal(J,-4*tangent)
    t=s.symbols('s',real=True)
    return {'global_connection':'A_v=omega_Spin5+sum_I v_I e^a T_aI/R, I=1..11',
            'curvature':'F_v=(1-|v|Â²) e^a wedge e^b T_ab/RÂ²',
            'normalized_energy':'YM(A_v)/YM(A_0)=(1-|v|Â²)^2',
            'YM0_with_basic_inner_product':'5*pi^3*R*Area(T2)/(27*gYM^2)',
            'radial_stationary_s':[-1,0,1],
            'radial_second_derivative_at0':int(s.diff((1-t*t)**2,t,2).subs(t,0)),
            'negative_Hessian_directions_descending_to_Y':11,
            'Jacobi_eigenvalue_times_R2':-4,'exact_Jacobi_matrix_checks':55,
            'source_free_YM_at0':'D_A^*F=0 because the product curvature is covariantly constant',
            'quotient_descent':'vielbein tensor gauge vector contraction is equivariant; these modes are not removed by H27',
            'scope':'Standalone internal YM Hessian; not a complete spacetime/AdS BF stability calculation'}


def flat_endpoint_and_class():
    w=s.exp(2*s.pi*s.I/3)
    # Genuine SU3 SchrÃ¶dinger holonomy, not the previous compensated
    # projective PSU3 embedding. It has invariant3=0 and invariant8=0.
    X=s.Matrix([[0,0,1],[1,0,0],[0,1,0]]);Z=s.diag(1,w,w**2)
    def canon(t):return s.simplify(s.expand_complex(t))
    traces=[canon(s.trace(w**c*(X**b)*(Z**a))) for a,b,c in product(range(3),repeat=3)]
    inv3=canon(sum(traces)/27)
    inv8=canon(sum(canon(t*s.conjugate(t))-1 for t in traces)/27)
    assert inv3==inv8==0
    invariants=78+inv8+27*(inv3+s.conjugate(inv3))
    assert invariants==78
    old=json.loads((ROOT/'data/toe_20261119_native_E8_Cfield_flat_gates.json').read_text())
    lam=old['Cfield_topology']['spin_lambda_p1_over2_mod9']
    assert lam==3
    return {'curved_point_unbroken_Lie_algebra':'so11 (dimension55)',
            'generic_0_abs_s_lt1_holonomy_Lie_algebra':'so6',
            'generic_unbroken_Lie_algebra':'so10 (dimension45)',
            'flat_endpoint_global_holonomy':'genuine SU3 H27; projective phase compensation is not used',
            'flat_endpoint_invariant_SU3_3':0,'flat_endpoint_invariant_SU3_8':0,
            'flat_endpoint_unbroken_Lie_algebra':'e6 (dimension78)',
            'flat_endpoint_D7_kernel':0,
            'E8_characteristic_class_a_mod9':lam,
            'normalization':'Choose basic a_E8 so its index-one Spin embedding pulls back to lambda=p1/2',
            'torsion_invariant_along_path':'a_E8=lambda(TY)=3 etaÂ²; connections change on one fixed bundle',
            'scope':'No C-field phase/quadratic refinement, heterotic vacuum, or physical bulk E8 gauge bosons derived'}


def Cfield_equivalence():
    # Basic E8 trace restricts to a multiple of vector trace on this Spin5.
    # All coefficients of Tr(F wedge F), without choosing a normalization.
    basis=list(combinations(range(5),2)); coefficients=Counter()
    for ab,cd in product(basis,repeat=2):
        indices=ab+cd
        if len(set(indices))<4:continue
        sign=(-1)**sum(indices[i]>indices[j] for i in range(4) for j in range(i+1,4))
        trace=int(np.trace(matrix_generator(*ab)@matrix_generator(*cd)))
        coefficients[tuple(sorted(indices))]+=sign*trace
    assert len(coefficients)==5 and all(v==0 for v in coefficients.values())
    # Transfer from S5 x T2 gives b3=0. Flat same-characteristic
    # differences are H3(R)/image H3(Z)=0, even though Tor H4=Z9.
    return {'Tr_F_wedge_F_coefficients':{str(k):v for k,v in coefficients.items()},
            'Tr_F_wedge_F_identically_zero_for_all_v':True,
            'Tr_R_wedge_R_identically_zero':True,
            'real_betti3':0,'flat_character_differences':'H3(Y;R/Z)=Z9',
            'flat_same_characteristic_difference_group':'0',
            'fixed_metric_little_c_zero_curvature_G':0,
            'same_shifted_Cfield_for_all_v':True,
            'reason':'same curvature and integral characteristic; b3(real)=0 removes same-characteristic flat ambiguity',
            'counterexample':'auxiliary charged D7 kernel64 at v=0, kernel0 at |v|=1, on the same Cfield',
            'physical_conclusion':'Neither auxiliary E8 Dirac kernel nor added probe YM energy is an invariant physical Cfield observable',
            'boundary_scope':'closed internal manifold; fixed gravitational differential background; no physical boundary E8 sector',
            'source':'Diaconescu-Freed-Moore hep-th/0312069 sections2 and3.1-3.3'}


def run():
    result={'status':'PASS','scope':'source-free probe YM with exact charged Dirac kernel and an explicit unstable direction, not a TOE',
            'branching':orthogonal_branching(),'Clifford':parallel_spinor_and_flow(),
            'Dirac_kernel':sphere_kernel_census(),'YM':YM_energy_and_Hessian(),
            'endpoint_and_topology':flat_endpoint_and_class(),'Cfield_equivalence':Cfield_equivalence(),
            'limitations':['round product metric remains incompatible with proposed G2 geometry',
              'E8 here is a probe bundle/auxiliary gauge construction; no physical 11D E8 YM action supplied',
              'kernel is not a physical chiral-family index',
              'negative probe YM Hessian is not a derived full supergravity tachyon',
              'no stabilized Higgs vacuum, observed masses, or gravitational equations']}
    out=ROOT/'data/toe_20261119_E8_spin_connection_YM_spectral_flow.json'
    out.write_text(json.dumps(result,indent=2)+'\n',encoding='utf8')
    print('PASS source-free YM; D7 kernel64/0/0/0; eleven negative modes; former zeros flow to flat E6 gap')
    return result


if __name__=='__main__':run()
