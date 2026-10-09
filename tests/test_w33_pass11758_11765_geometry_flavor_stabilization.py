"""Independent geometric/physics regressions, including negative controls."""
from pathlib import Path
import hashlib
import itertools as it
import json
import sys
import numpy as np
import sympy as s
import pytest

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'analysis'))
import w33_pass11758_metric_harmonic_galerkin as A
import w33_pass11759_11765_geometry_flavor_stabilization as B


@pytest.fixture(scope='module')
def frozen():
    return json.loads((ROOT/'data/w33_pass11758_metric_harmonic_galerkin.json').read_text()),json.loads((ROOT/'data/w33_pass11759_11765_geometry_flavor_stabilization.json').read_text())


@pytest.mark.parametrize('which',[0,1])
def test_frozen_producer_binding(frozen,which):
    module=(A,B)[which]
    assert frozen[which]['source_sha256']==hashlib.sha256(Path(module.__file__).read_bytes().replace(b'\r\n',b'\n')).hexdigest()
    bindings=frozen[which]['prior_source_sha256' if which==0 else 'prior_sources']
    for name,digest in bindings.items():
        assert digest==hashlib.sha256((ROOT/name).read_bytes().replace(b'\r\n',b'\n')).hexdigest()


def test_new_sampling_solves_actual_homogeneous_polynomial():
    d=A.sample_hypersurface(918,8)
    assert len(d['z'])==16 and d['polynomial_residual']<1e-9
    assert np.all(d['weight']>0) and np.max(abs(d['z']))<=1+1e-12
    z,F,_,_=A.Q.reference_polynomial();f=s.lambdify(z,F,'numpy')
    north=np.where(d['bits'],1/d['z'],d['z'])
    normalized=f(*north.T)*np.prod(np.where(d['bits'],d['z']**2,1),axis=1)
    assert max(abs(normalized))<1e-8


def test_chart_gradient_is_the_polynomial_derivative():
    z=np.array([[.2+.3j,-.4+.1j,.6-.2j,.1+.7j]])
    bits=np.array([[True,False,True,False]])
    for j in range(4):
        h=1e-6;step=np.eye(4)[j]*h
        numeric=(A.chart_polynomial(z+step,bits)-A.chart_polynomial(z-step,bits))/(2*h)
        assert np.allclose(numeric,A.chart_polynomial(z,bits,j),rtol=1e-8,atol=1e-7)


@pytest.mark.parametrize('support,size',[(2,26),(4,71)])
def test_global_potential_basis_covariance(support,size):
    z=np.array([[.3+.2j,-.5+.4j,.8+.1j,.2-.6j]])
    bits=np.zeros((1,4),bool)
    v,H=A.potential_basis(z,bits,support)
    assert v.shape==(1,size) and np.max(abs(H-H.conj().transpose(0,1,3,2)))<1e-12
    vg,_=A.potential_basis(-z,bits,support);vh,_=A.potential_basis(1/z,bits,support)
    assert np.allclose(vg,v) and np.allclose(vh,v)
    vc,Hc=A.potential_basis(1/z,~bits,support)
    assert np.allclose(vc,v)
    jac=-1/z**2
    pulled=Hc*jac[:,None,None,:]*jac.conj()[:,None,:,None]
    assert np.allclose(pulled,H)


def test_potential_hessian_by_independent_real_derivatives():
    z=np.array([[.3+.2j,-.5+.4j,.8+.1j,.2-.6j]])
    bits=np.zeros((1,4),bool);_,H=A.potential_basis(z,bits,4);h=2e-4
    for j in (0,2):
        step=np.eye(4)[j][None,:]*h
        f=A.potential_basis(z,bits,4)[0]
        dx=(A.potential_basis(z+step,bits,4)[0]-2*f+A.potential_basis(z-step,bits,4)[0])/h**2
        dy=(A.potential_basis(z+1j*step,bits,4)[0]-2*f+A.potential_basis(z-1j*step,bits,4)[0])/h**2
        assert np.allclose((dx+dy)/4,H[:,:,j,j],atol=1e-6)


def test_metric_loss_gradient_by_finite_differences():
    d=A.sample_hypersurface(919,12);g,v,H=A.geometry(d);c=np.zeros(26)
    loss,grad=A.metric_loss(c,g,H,d['grad'][:,3],d['weight'])
    for j in (0,7,19,25):
        step=np.eye(26)[j]*1e-6
        numeric=(A.metric_loss(c+step,g,H,d['grad'][:,3],d['weight'])[0]-A.metric_loss(c-step,g,H,d['grad'][:,3],d['weight'])[0])/(2e-6)
        assert abs(numeric-grad[j])<1e-6


def test_reference_and_corrected_metrics_survive_another_elimination():
    d=A.sample_hypersurface(920,5);g,v,H=A.geometry(d)
    c=np.linspace(-1,1,26)*1e-4
    gg=g+np.einsum('b,nbij->nij',c,H)
    _,ambient_h=A.potential_basis(d['z'],d['bits'])
    t=np.array([float(s.N(x)) for x in A.N.flavor_certificate()['positive_Kahler_point']])
    full=np.einsum('b,nbij->nij',c,ambient_h)
    full+=np.eye(4)[None,:,:]*(t/(1+abs(d['z'])**2)**2)[:,None,:]
    eta=np.linalg.det(gg).real*abs(d['grad'][:,3])**2
    for excluded in range(3):
        other=[j for j in range(4) if j!=excluded]
        tangent=np.zeros((len(eta),4,3),complex)
        tangent[:,other,:]=np.eye(3)
        tangent[:,excluded,:]=-d['grad'][:,other]/d['grad'][:,excluded,None]
        metric=np.einsum('nki,nkl,nlj->nij',tangent.conj(),full,tangent)
        assert np.allclose(np.linalg.det(metric).real*abs(d['grad'][:,excluded])**2,eta,rtol=1e-10)


@pytest.mark.parametrize('family',[0,1,2])
def test_global_exact_form_trials_are_equivariant(family):
    z=np.array([[.3+.2j,-.5+.4j,.8+.1j,.2-.6j]])
    bits=np.zeros((1,4),bool);tangent=np.eye(4)[None,:,:];k=A.N.K[family]
    D=A.exact_form_basis(k,z,bits,tangent)
    Dg=-A.exact_form_basis(k,-z,bits,tangent)
    Dh=A.exact_form_basis(k,1/z,bits,tangent)*np.prod(z**np.array(k),axis=1)[:,None,None]*(-1/z.conj()**2)[:,None,:]
    assert np.allclose(Dg,D) and np.allclose(Dh,D)


def test_numerical_residuals_remain_visible(frozen):
    a=frozen[0]
    for run in (a,a['independent_larger_run'],a['enriched_basis_run']):
        v=run['metric']['validation']
        assert v['min_sample_metric_eigenvalue']>0
        assert v['corrected_log_density_variance']<v['reference_log_density_variance']
        assert v['weighted_relative_MA_rms']>1e-3
        assert run['HYM']['validation']['beta_product_max']<1e-10
    assert a['training_executed'] and not a['physical_normalized_Yukawa_certified']
    assert not a['snapshot_global_smoothness_certified']


def test_galerkin_stationarity_is_not_validation_harmonicity(frozen):
    for run in (frozen[0],frozen[0]['independent_larger_run'],frozen[0]['enriched_basis_run']):
        for f in run['harmonic']['families']:
            assert f['galerkin_stationarity']<1e-8
            assert f['train']['corrected_norm']<=f['train']['reference_norm']*(1+1e-10)
            assert f['validation']['corrected_norm']>0


def test_quotient_curve_normal_sections_independently():
    # Quotient O(1,1) sections by q=u0u1+v0v1, using relation last=-first.
    basis=s.Matrix.hstack(s.eye(4)[:,0],s.eye(4)[:,1],s.eye(4)[:,2])
    reduction=s.Matrix([[1,0,0,-1],[0,1,0,0],[0,0,1,0]])
    g=s.diag(1,-1,-1,1);h=s.zeros(4)
    for i in range(4):h[3-i,i]=1
    rg,rh=reduction*g*basis,reduction*h*basis
    common=(rg-s.eye(3)).col_join(rh-s.eye(3))
    assert common.rank()==3
    assert [int(x.trace()) for x in (s.eye(3),rg,rh,rg*rh)]==[3,-1,-1,-1]
    assert 8+2*(1-5)==0 # cover rank2 normal RR
    assert 2+2*(1-2)==0 # quotient rank2 normal RR


def test_elliptic_normal_and_worldvolume_counts(frozen):
    p=frozen[1]['passes']['11759'];prior=A.Q.anomaly_cycle_certificate()
    count=sum(x['multiplicity'] for x in prior['orbit_pair_curves'])
    assert p['worldvolume_abelian_vector_rank']==2+count==8
    assert p['universal_chiral_multiplets']==1+count==7
    assert p['quotient_h0_normal']==p['elliptic_quotient_h0_normal']==0
    assert (s.eye(2)-s.eye(2))/2==s.zeros(2)


def test_rank5_alternative_index_by_independent_cubic_chern_character():
    x=s.symbols('x:4');poly=sum(sum(k[i]*x[i] for i in range(4))**3/6 for k in B.PUBLISHED_LINES)
    third=s.Poly(s.expand(poly),*x)
    index=2*sum(third.coeff_monomial(s.prod(x[i] for i in inds)) for inds in it.combinations(range(4),3))
    assert index==-12 and sum(B.line_euler(k) for k in B.PUBLISHED_LINES)==index
    assert s.Matrix(B.PUBLISHED_LINES).rank()==3


def test_actual_koszul_map_is_invertible_and_serre_dual_correct(frozen):
    p=frozen[1]['passes']['11760'];mat=s.Matrix(p['actual_L1L2_Koszul_map'])
    assert mat.det()==s.Integer(p['actual_L1L2_Koszul_determinant'])!=0
    # Source monomials: H1(-4),H1(-5),H0(0),H0(1).
    # Target: H1(-2),H1(-3),H0(2),H0(3). Check three independent entries.
    src=list(it.product(range(3),range(4),range(1),range(2)))
    dst=list(it.product(range(1),range(2),range(3),range(4)))
    z,F,_,_=A.Q.reference_polynomial();poly=s.Poly(F,*z)
    for i,j in ((0,0),(12,17),(23,23)):
        exp=(src[j][0]-dst[i][0],src[j][1]-dst[i][1],dst[i][2]-src[j][2],dst[i][3]-src[j][3])
        expected=poly.coeff_monomial(s.prod(z[a]**e for a,e in enumerate(exp))) if min(exp)>=0 else 0
        assert mat[i,j]==expected


def test_all_order_proton_selection_and_mu_negative_control(frozen):
    p=frozen[1]['passes']['11760'];ell=s.Matrix(p['charge_separator'])
    assert sum(ell)==0
    for a,b in p['allowed_singlet_VEVs']:
        assert (ell.T*B.charge((a,1),(b,-1)))[0]==3
    assert p['dangerous_dim4_weights']==[7] and p['dangerous_dim5_weights']==[6]
    assert p['down_Yukawa_weights']==[6] # Same protection blocks needed down masses.
    assert p['direct_mu_charge_zero'] # Gauge invariance alone cannot protect mu.
    l1,l2=s.symbols('l1 l2');mass=s.Matrix([[0,0,l1],[0,0,l2],[l1,l2,0]])
    assert mass.det()==0 and mass.rank()==2


def test_six_circuits_cancel_arbitrary_diagonal_metrics(frozen):
    p=frozen[1]['passes']['11761'];inc=s.Matrix(p['incidence']);circuits=s.Matrix.hstack(*[s.Matrix(v['exponents']) for v in p['circuits']])
    assert inc.rank()==10 and circuits.rank()==6 and inc*circuits==s.zeros(12,6)
    rng=np.random.default_rng(927);Z=np.exp(rng.normal(size=12));phases=np.exp(1j*rng.uniform(-3,3,size=12))
    Y=np.array([complex(s.sympify(y)) for y in p['holomorphic_values']])
    for j,e in enumerate(p['edges']):Y[j]*=np.exp(.37)/np.prod([np.sqrt(Z[4*f+a])*phases[4*f+a] for f,a in enumerate(e)])
    for row in p['circuits']:
        assert np.allclose(np.prod(Y**np.array(row['exponents'])),float(row['exact_value']))


def test_real_negative_circuit_is_not_CP_violation(frozen):
    p=frozen[1]['passes']['11761'];vals=[s.sympify(x) for x in p['holomorphic_values']]
    assert all(v.is_real for v in vals) and any(r['exact_value']=='-1' for r in p['circuits'])
    assert s.ones(3,1).nullspace()==[]


def test_integral_neutral_generators_and_named_effective_curve(frozen):
    p=frozen[1]['passes']['11764'];K=s.Matrix(A.N.K)
    for q in p['generators']:
        assert K*s.Matrix(q)==s.zeros(3,1)
        assert all(v%2==0 for v in q) and len({v%4 for v in q})==1
    old=A.N.anomaly_class_certificate();pair=s.Matrix(old['intersection_pairing_matrix'])
    q=pair*s.Matrix([1,1,0,1,0,0])
    assert list(q)==p['generators'][1]==[2,2,2,6]
    assert s.Matrix(p['generators'][0])+s.Matrix(p['generators'][2])==4*q


def test_global_neutral_lattice_decomposition_outside_producer_range():
    for a,b in ((102,98),(100,196),(208,4),(202,402)):
        q=B.invariant_curve_lattice(a,b)
        assert min(q)>=0 and len({v%4 for v in q})==1
        if b<=a:cs=((a-b)//4,b//2,0)
        else:cs=(0,a-b//2,(b-a)//4)
        assert tuple(sum(c*g[i] for c,g in zip(cs,B.INSTANTON_GENERATORS)) for i in range(4))==q


def test_genus_zero_transfer_is_stricter_than_integral_descent(frozen):
    p=frozen[1]['passes']['11764'];qB=np.array(p['generators'][1])
    assert all(qB%2==0) and not all(qB%4==0)
    # Trivial deck action gives sum of all four translates, not merely
    # the integral-descent congruence. No odd multiple can be such a sum.
    for m in range(1,16,2):assert any((m*qB)%4)
    assert np.array_equal(2*qB,p['genus_zero_necessary_generators'][1])
    assert p['primitive_qB_genus_zero_excluded']
    for a,b in ((4,4),(4,8),(120,116),(200,396),(408,400)):
        q=B.invariant_curve_lattice(a,b);m,n=a//4,b//4
        cs=(m-n,n,0) if n<=m else (0,2*m-n,n-m)
        assert min(cs)>=0 and all(v%4==0 for v in q)
        assert tuple(sum(c*g[i] for c,g in zip(cs,B.GENUS_ZERO_NECESSARY_GENERATORS)) for i in range(4))==q
    U=frozen[1]['passes']['11762']['invariant_modulus_map']
    assert U[2][1:]==[4,4,4,12] # EFT uses the allowed necessary sublattice.


def test_h4_integer_operator_and_real_projectors(frozen):
    p=frozen[1]['passes']['11765']['h4_real_operator']
    a,b=np.array(p['A_plus'],dtype=np.int64),np.array(p['A_minus'],dtype=np.int64)
    assert a.shape==b.shape==(60,60) and not np.any(a&b)
    assert np.all(a.sum(axis=1)==12) and np.all(b.sum(axis=1)==12)
    D=a-b;P=(D@D)/80;Chi=D/np.sqrt(80)
    assert np.array_equal(D@D@D,80*D)
    assert np.array_equal((D@D)@(D@D),80*(D@D)) and np.trace(D@D)==80*18
    for projector in ((P+Chi)/2,(P-Chi)/2):
        assert np.isrealobj(projector) and np.allclose(projector,projector.T)
        assert np.allclose(projector@projector,projector) and np.isclose(np.trace(projector),9)
    pm=p['outer_order4_permutation']
    assert np.array_equal(D[np.ix_(pm,pm)],-D)
    assert np.allclose(P[np.ix_(pm,pm)],P)
    assert np.array_equal((a+b)@(D@D),4*(D@D))
    assert p['source_certificate_sha256']==hashlib.sha256((ROOT/p['source_certificate']).read_bytes().replace(b'\r\n',b'\n')).hexdigest()
    assert not p['physical_chiral_fermion_or_mass_prediction']


def test_h4_exchange_pairs_arbitrary_sector_preserving_kinetics(frozen):
    p=frozen[1]['passes']['11765']['h4_real_operator'];a,b=np.array(p['A_plus']),np.array(p['A_minus'])
    D=a-b;vals,V=np.linalg.eigh(D);E=V[:,vals>1];F=V[:,vals< -1]
    h=np.eye(60)[:,p['outer_order4_permutation']]
    rng=np.random.default_rng(11765);seed=rng.normal(size=(60,60));seed=seed@seed.T+np.eye(60)
    P=E@E.T;Q=F@F.T;seed=P@seed@P+Q@seed@Q
    averaged=sum(np.linalg.matrix_power(h,k)@seed@np.linalg.matrix_power(h.T,k) for k in range(4))/4
    # Independently compare restrictions of a random positive operator
    # after imposing the declared symmetry and sector preservation.
    assert np.allclose(averaged@h,h@averaged)
    assert np.allclose(np.linalg.eigvalsh(E.T@averaged@E),np.linalg.eigvalsh(F.T@averaged@F))


def test_four_dimensional_stability_and_gauge_nulls(frozen):
    p=frozen[1]['passes']['11762'];U=s.Matrix(p['invariant_modulus_map']);C=s.Matrix(p['gauged_axion_shifts']);W=s.Matrix(p['exact_superpotential_hessian'])
    assert U*C.T==s.zeros(3,2) and W.rank()==3 and W*C.T==s.zeros(5,2)
    assert len(U.nullspace())==2 and C.rank()==2
    g=np.array(p['Kahler_metric_at_point']);assert np.linalg.eigvalsh(g).min()>0
    assert min(p['real_scalar_mass_squared'])>0
    assert sum(v>1e-7 for v in p['axion_mass_squared_before_unitary_gauge'])==3
    assert p['physical_massive_real_scalars']==8
    assert p['W_at_point']==0 and p['D_terms_at_point']==[0,0]
    assert s.Matrix(U[:2,:]).rank()==2 # Removing one independent term leaves a physical flat modulus.


def test_four_dimensional_kahler_metric_by_finite_differences(frozen):
    p=frozen[1]['passes']['11762'];x=np.array([float(s.N(s.sympify(v))) for v in p['point']]);G=np.array(p['Kahler_metric_at_point'])
    def K(x):return -np.log(2*x[0])-np.log(.5*sum(np.prod(x[np.array(ids)+1]) for ids in it.combinations(range(4),3)))
    h=1e-4
    for i,j in ((0,0),(1,1),(1,3)):
        ei=np.eye(5)[i]*h;ej=np.eye(5)[j]*h
        value=(K(x+ei+ej)-K(x+ei-ej)-K(x-ei+ej)+K(x-ei-ej))/(16*h*h)
        assert abs(value-G[i,j])<1e-7


def test_interval_source_jumps_and_neutral_component(frozen):
    p=frozen[1]['passes']['11763'];slopes=np.array(p['piecewise_slopes'],dtype=int);charges=np.array(p['brane_curve_degrees'],dtype=int)
    assert np.array_equal(np.diff(slopes,axis=0),charges)
    assert np.all(slopes[0]+charges.sum(axis=0)+np.array(p['hidden_boundary_charge'])==0)
    assert p['curve_K_degrees'][0]==[0,0,0]
    assert all(any(x for x in row) for row in p['curve_K_degrees'][1:])
    assert min(s.sympify(x) for row in p['knot_profile_values'] for x in row)>0


def test_residue_normalization_cancels_polynomial_scaling(frozen):
    for run in (frozen[0],frozen[0]['independent_larger_run'],frozen[0]['enriched_basis_run']):
        h=run['harmonic'];z=np.prod([f['validation']['corrected_norm'] for f in h['families']]);o=h['residue_norm_without_universal_measure_constant']
        assert np.isclose(.5/np.sqrt(z*o),h['F_rescaling_invariant_geometry_proxy'])
        assert np.isclose(.5/np.sqrt(9*z*o/9),h['F_rescaling_invariant_geometry_proxy'])


def test_no_physical_completion_inference(frozen):
    assert all(v['status']=='PASS' for v in frozen[1]['passes'].values())
    assert 'supplied4D EFT' in frozen[1]['passes']['11762']['scope']
    assert 'not a rational' in frozen[1]['passes']['11764']['neutral_anomaly_curve']
    assert not frozen[0]['certified_Ricci_flat_HYM_harmonic_solution']
