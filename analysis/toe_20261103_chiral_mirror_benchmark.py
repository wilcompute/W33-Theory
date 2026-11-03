"""Published3450 mirror-gapping mechanism with explicit locality/relevance controls.

Wang-Wen1307.7480 and Thorngren-Preskill-Fidkowski2601.04304 own the
constructive chiral framework. This is a1+1D benchmark, not a4D SM regulator.
"""
import itertools,json,math,pathlib
import sympy as s
ROOT=pathlib.Path(__file__).resolve().parents[1]

def build():
    K=s.diag(1,1,-1,-1);q=s.Matrix([3,4,5,0]);L=s.Matrix([[1,-2,-1,2],[2,1,2,1]])
    assert (q.T*K*q)[0]==0 and s.trace(K)==0
    assert L*K*L.T==s.zeros(2) and L*K*q==s.zeros(2,1)
    minors=[int(L[:,cols].det())for cols in itertools.combinations(range(4),2)]
    assert math.gcd(*minors)==1 and L*L.T==10*s.eye(2)
    P=L.T*L/10;Q=s.eye(4)-P;V=3*P+Q/3
    assert P*P==P and K*P*K==Q and V*K*V==K
    assert V.eigenvals()=={s.Rational(1,3):2,s.Integer(3):2}
    dimensions=[s.simplify((row*V.inv()*row.T)[0]/2)for row in [L[i,:]for i in range(2)]]
    assert dimensions==[s.Rational(5,3)]*2
    k,mu=s.symbols('k mu',positive=True);M=mu**2*L.T*L
    generator=K*(k*V+M/k)
    assert s.simplify(generator**2-(k*k+10*mu*mu/3)*s.eye(4))==s.zeros(4)
    # Carry the free-fermion reference metric through a nonorthogonal integral
    # basis change. A bare Euclidean condition number would be a coordinate artifact.
    U=s.eye(4);U[0,1]=1;U[2,3]=2;assert U.det()==1
    KK=U.T*K*U;VV=U.T*V*U;Vfree=U.T*U;LL=L*U;qq=U.T*q
    assert LL*KK.inv()*LL.T==s.zeros(2) and LL*KK.inv()*qq==s.zeros(2,1)
    assert (Vfree.inv()*VV).eigenvals()==V.eigenvals()
    assert LL*VV.inv()*LL.T==s.Rational(10,3)*s.eye(2)
    assert (KK.inv()*VV)**2==s.eye(4)
    # All local gauge-neutral integer null vectors in a bounded box are controls,
    # not a claim of a globally minimal fermion interaction degree.
    short=[]
    for ell in itertools.product(range(-3,4),repeat=4):
        if not any(ell):continue
        v=s.Matrix(ell)
        if sum(ell[i]*K[i,i]*q[i]for i in range(4))==0 and sum(K[i,i]*ell[i]**2 for i in range(4))==0:
            short.append(list(ell))
    return dict(status='PASS_LOCAL_ANOMALY_FREE_3450_MIRROR_BENCHMARK',spacetime_dimension='1+1',
        K=list(map(list,K.tolist())),charges=list(q),gapping_rows=L.tolist(),gauge_anomaly=0,gravitational_anomaly=0,
        null_pairing=L*K*L.T,charge_pairing=L*K*q,primitive_minors=minors,primitive_minor_gcd=1,
        velocity_matrix=[[str(x)for x in row]for row in V.tolist()],velocity_positive_eigenvalues=['1/3','1/3','3','3'],
        characteristic_speed_eigenvalues=['-1','-1','1','1'],scaling_dimensions_free=['5','5'],scaling_dimensions_tuned=list(map(str,dimensions)),
        relevance='Delta_l=(1/2) l^T V^(-1) l for the displayed Gaussian theory with V K V=K. Both cosines have Delta=5/3<2; they are irrelevant at the free-fermion point Delta=5.',
        conditioning_lower_bound='Relative to the declared free-fermion metric Vfree=I, positive V with V K V=K has reciprocal generalized eigenvalues. If either norm-sqrt10 gapping row has Delta<2 then lambda_min(V^-1)<2/5, hence generalized condition_number(V,Vfree)>25/4. The family V=aP+a^-1(I-P) attains the infimum as a decreases to5/2 from above. This is not a claim about bare Euclidean matrix norms after arbitrary coordinate changes.',
        nonorthogonal_integer_basis_control=U.tolist(),reference_metric_carried_under_basis_change=True,
        displayed_condition_number=9,commuting_interactions='cos(l1 dot phi) and cos(l2 dot phi) have zero mutual equal-time null pairing. Primitivity rules out a spurious discrete degeneracy from a nonprimitive interaction lattice in the standard compact-boson gapping criterion.',
        harmonic_strong_pinning_dispersion='omega^2=k^2+(10/3)*mu^2 for all four canonical branches of the declared quadratic pinning Hamiltonian. mu is supplied; this is not an exact sine-Gordon mass prediction from a bare cosine.',
        bounded_null_vector_controls=short,
        source_classic='https://arxiv.org/abs/1307.7480',source_recent='https://arxiv.org/abs/2601.04304',
        ownership='3450 charges and mirror-decoupling mechanisms are published prior art. The explicit positive velocity matrix, reciprocal-spectrum conditioning control and harmonic spectrum are audited here; no priority claim.',
        boundary='Local continuum chiral benchmark and an interacting mirror-gapping criterion. No4D non-Abelian SM lattice action, finite-dimensional rotor truncation theorem, emergent spacetime or selected generation number.')

def serial(x):
    if isinstance(x,s.MatrixBase):return x.tolist()
    if isinstance(x,s.Integer):return int(x)
    return str(x)

if __name__=='__main__':
    d=build();(ROOT/'data/toe_20261103_chiral_mirror_benchmark.json').write_text(json.dumps(d,indent=2,default=serial)+'\n',encoding='utf-8');print(d['status'],d['scaling_dimensions_tuned'],flush=True)
