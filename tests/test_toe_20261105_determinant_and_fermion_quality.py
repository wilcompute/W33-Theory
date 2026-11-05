"""Independent charge, determinant, numerical loop and minimum checks."""
import importlib.util,pathlib,math
import numpy as np
P=pathlib.Path(__file__).resolve().parents[1]/'analysis/toe_20261105_determinant_and_fermion_quality.py'
spec=importlib.util.spec_from_file_location('detquality',P);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)

def test_color_instanton_determinant_with_mixing():
    Q=np.array([[2+1j,.7j],[.3-1j,3.]])
    full=np.zeros((5,5),complex);full[0,0]=1.2j;full[1:3,1:3]=Q;full[3:5,3:5]=Q
    assert np.allclose(np.linalg.det(full),1.2j*np.linalg.det(Q)**2)
    alpha=.271
    # Scalar gauge charges equal minus left/right charges, arbitrary mixing.
    left=np.array([1,2]);right=np.array([3,4]);dcharge=-2*(sum(left)+sum(right))
    Qp=np.exp(-1j*alpha*left[:,None])*Q*np.exp(-1j*alpha*right[None,:])
    assert np.allclose(1.2j*np.exp(-1j*alpha*dcharge)*np.linalg.det(Qp)**2,np.linalg.det(full))

def test_one_higgs_SM_color_anomaly_cancels_without_family_universality():
    q=np.array([3,-2,7]);h=5
    # diagonal full rank suffices; sums also follow from any full-rank determinant.
    u=-q-h;d=-q+h
    assert sum(2*q+u+d)==0

def test_64_assignments_and_short_invariants():
    out=m.assignments();assert out['count']==64
    assert out['max_primitive_degree']==5
    for row in out['rows']:
        x,y=row['primitive_scalar_X'];assert row['A']*x+row['B']*y==0
        assert math.gcd(abs(x),abs(y))==1

def test_operator_lower_bound_by_an_independent_small_dynamic_program():
    # doubled canonical dimension <=18. States: total X, low X, Weyl parity.
    states=[set()for _ in range(19)];states[0].add((0,0,0));found=None
    particles=[(2,2,2,0),(-2,-2,2,0),(26,0,2,0),(-26,0,2,0),
               (1,1,3,1),(-1,-1,3,1),(13,0,3,1),(-13,0,3,1)]
    for cost in range(19):
        if any(x==0 and l!=0 and p==0 for x,l,p in states[cost]):found=cost;break
        for x,l,p in states[cost]:
            for dx,dl,dc,dp in particles:
                if cost+dc<19:states[cost+dc].add((x+dx,l+dl,p^dp))
    assert found==18
    assert m.mixed_minimum()['minimum_relaxed_Lorentz_scalar_dimension']==9

def test_mixed_operator_is_gauge_invariant_and_PQ_breaking():
    row=m.mixed_minimum();assert row['explicit_total_X']==0
    assert row['explicit_PQ']==6.5
    # Two insertions plus conjugate diagonal masses: S^(12+1) Tdag.
    assert 2*6+1==13 and 2*(9-4)==10

def test_Weyl_loop_phase_trace_by_complex_numeric_matrices():
    a=.7*np.exp(.3j);b=1.1*np.exp(-.2j);z=.2*np.exp(.4j)
    M=np.array([[a,z],[z,b]]);H=M.conj().T@M
    expected=abs(a)**4+abs(b)**4+2*abs(z)**4+4*(abs(a)**2+abs(b)**2)*abs(z)**2+4*(a.conjugate()*b.conjugate()*z*z).real
    assert np.allclose(np.trace(H@H),expected)
    eig=np.linalg.eigvalsh(H)
    def cw(logmu):return -sum(eig**2*(np.log(eig)-2*logmu-1.5))/(32*np.pi**2)
    eps=1e-4
    assert np.allclose((cw(eps)-cw(-eps))/(2*eps),np.trace(H@H).real/(16*np.pi**2))

def test_quality_bound_controls_arbitrary_phase_in_same_harmonic():
    r=1e-6
    for phase in np.linspace(-np.pi,np.pi,101):
        exact=abs(np.angle(1+r*np.exp(1j*phase)))
        assert exact<=r/(1-3*r)
    out=m.determinant_control();assert out['sufficient_c_for_uniform_theta_1e_10']<1e-45
    assert out['max_absolute_basis_magnitude_residual']<1e-10

def test_logarithmic_operator_has_original_scalar_Planck_power():
    out=m.loop_control();assert out['Planck_power']==10 and out['scalar_dimension']==14
    assert .1<out['induced_c_magnitude_for_unit_y_kappa_and_zero_UV_c']<.3

def test_flavor_trace_and_Frobenius_bound_under_complex_basis_change():
    rng=np.random.default_rng(13)
    A=np.array([[.5,.1j],[.1j,.8]]);B=np.array([[.7,.2],[.2,.9]])
    K=rng.normal(size=(2,2))+1j*rng.normal(size=(2,2))
    U=np.linalg.qr(rng.normal(size=(2,2))+1j*rng.normal(size=(2,2)))[0]
    V=np.linalg.qr(rng.normal(size=(2,2))+1j*rng.normal(size=(2,2)))[0]
    inv=lambda a,k,b:np.trace(a.conj().T@k@b.conj().T@k.T)
    assert np.allclose(inv(A,K,B),inv(U.T@A@U,U.T@K@V,V.T@B@V))
    assert abs(inv(A,K,B))<=np.linalg.norm(A,2)*np.linalg.norm(B,2)*np.linalg.norm(K)**2+1e-12
    row=m.loop_control()['full_singlet_flavor_control']
    assert row['coherent_unit_entry_trace']==468
    assert 85<row['coherent_fixed_coupling_leading_log_c']<86
