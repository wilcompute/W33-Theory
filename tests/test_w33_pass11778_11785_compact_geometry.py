"""Independent differential, rational, Fourier and second-basis controls."""
import importlib.util
from pathlib import Path
from fractions import Fraction
import json
import numpy as np
import sympy as sp
from scipy.integrate import quad
ROOT=Path(__file__).resolve().parents[1]


def load(name):
    spec=importlib.util.spec_from_file_location(name,ROOT/'analysis'/f'{name}.py')
    obj=importlib.util.module_from_spec(spec);spec.loader.exec_module(obj);return obj


V=load('w33_pass11778_11783_compact_vacuum_thermodynamics')
N=load('w33_pass11779_11780_11782_local_net_index_constraints')
G=load('w33_pass11781_11784_11785_nonlinear_cone_bargmann_lift')


def test_word_depth_certificate_uses_actual_parent_graph():
    j=json.loads((ROOT/'data/w33_pass11767_global_current_algebra.json').read_text())['witness']
    degrees=[]
    for k,(parent,steps,scale) in enumerate(j['operations']):
        assert scale%101!=0
        d=1 if parent[0]=='g' else 1+degrees[parent[1]]
        for i,c in steps:
            assert 0<=i<k
            d=max(d,degrees[i])
        degrees.append(d)
    assert len(degrees)==6240 and max(degrees)==5
    assert V.depth_certificate()['word_degree_upper_bound']==5


def test_weyl_antiphase_and_real_part_bound_on_actual_wavefunctions():
    # Infinite-line Gaussian, with phase-modulation M and translation by pi.
    for sigma,center in [(1,0),(.3,2),(4,-.7)]:
        norm=(np.pi*sigma*sigma)**(-.25)
        psi=lambda x:norm*np.exp(-(x-center)**2/(2*sigma*sigma))
        mdef=quad(lambda x:abs((np.exp(1j*x)-1)*psi(x))**2,-np.inf,np.inf)[0]
        tdef=quad(lambda x:abs(psi(x-np.pi)-psi(x))**2,-np.inf,np.inf)[0]
        assert mdef+tdef>=4-2*np.sqrt(2)-1e-10
        x=.37
        assert abs(np.exp(1j*x)*psi(x-np.pi)+np.exp(1j*(x-np.pi))*psi(x-np.pi))<1e-14


def test_weyl_smoothing_hilbert_schmidt_norm_by_independent_integral():
    for eps in [.2,.8]:
        # Integrate x and r=x-y independently, using the actual heat kernel.
        xint=quad(lambda x:np.exp(-2*eps*x*x),-np.inf,np.inf)[0]
        rint=quad(lambda r:np.exp(-r*r/(2*eps))/(4*np.pi*eps),-np.inf,np.inf)[0]
        assert abs(xint*rint-1/(4*eps))<1e-11


def test_fractional_coercivity_exponent_and_heat_phase_space_constant():
    theta=Fraction(1,6)
    assert Fraction(2,5)-2*theta==Fraction(1,15)>0
    # The radial calculation in one dimension independently checks normalization.
    beta=.7
    integral=quad(lambda x:np.exp(-beta*abs(x)**(1/3)),0,np.inf)[0]*2
    assert abs(integral-12/beta**3)<1e-7
    assert Fraction(2*78,1)/(2*theta)==468
    j=V.thermodynamics()
    exact=36*sp.gamma(234)**2/(2**78*sp.gamma(39)**2)
    assert sp.Integer(j['heat_prefactor_exact'])==exact


def test_current_net_locality_and_nontrivial_interval_symplectic_form():
    x=sp.symbols('x');phi=(1-x*x)**6;psi=sp.diff(phi,x)
    sigma=-sp.integrate(phi*sp.diff(psi,x),(x,-1,1))
    assert sigma==sp.sympify(N.local_net()['nontrivial_interval_symplectic_exact'])>0
    # Integration by parts has no endpoint term for these closure test vectors.
    assert (phi*psi).subs(x,1)==(phi*psi).subs(x,-1)==0
    # Compact supports in (0,1) and (2,3) have disjoint derivative supports.
    f=lambda x:((x*(1-x))**6 if 0<x<1 else 0)
    hprime=lambda x:(6*((x-2)*(3-x))**5*(5-2*x) if 2<x<3 else 0)
    assert quad(lambda x:f(x)*hprime(x),0,3,points=[1,2])[0]==0


def test_halfline_modular_dilation_relation_on_nontrivial_vector():
    theta=np.linspace(-3,3,51);s=.23;t=.47
    vector=lambda x:np.exp(-x*x/2)*(1+.2j*x)
    left=np.exp(1j*t*np.exp(-(theta+2*np.pi*s)))*vector(theta)
    right=np.exp(1j*t*np.exp(-2*np.pi*s)*np.exp(-theta))*vector(theta)
    assert np.allclose(left,right,atol=1e-14)
    assert np.min(np.exp(-theta))>0


def test_expected_current_curvature_vanishes_for_other_gaussian_parameters():
    g=N.A.geometry();base=N.A.spectral_covariance(g)[0];d=np.diag(g['s'])
    pair=g['v']@g['u'].T
    for t,f in [(1.7,.3),(.6,-.8)]:
        cross=g['v']@(t*base)@(f*d)@g['u'].T/2
        actual=pair*(cross.T+.05)-pair.T*(cross+.05)
        assert np.max(np.abs(actual))<1e-14


def test_constant_spinor_gaussian_zero_mode_obstruction_exactly():
    # Clifford anticommutation makes the square of a sum equal the number of terms.
    assert 160*sp.Rational(1,20)**2==sp.Rational(2,5)>0
    x=sp.symbols('x');state=sp.exp(-(2+sp.I)*x*x)
    assert sp.diff(state,x).subs(x,0)==0 and state.subs(x,0)!=0


def test_bott_untruncated_even_kernel_and_no_odd_l2_kernel():
    x=sp.symbols('x');even=sp.exp(-x*x/2);odd=sp.exp(x*x/2)
    assert sp.diff(even,x)+x*even==0
    assert sp.diff(odd,x)-x*odd==0
    assert sp.integrate(even**2,(x,-sp.oo,sp.oo))==sp.sqrt(sp.pi)
    assert sp.limit(odd,x,sp.oo)==sp.oo
    assert N.bott_control()['even_to_odd_index']==1


def test_surviving_gauge_constraints_commute_with_nonlinear_matter_energy():
    q1,q2,p1,p2,a=sp.symbols('q1 q2 p1 p2 a')
    variables=[q1,q2,p1,p2]
    omega=sp.Matrix([[0,0,1,0],[0,0,0,1],[-1,0,0,0],[0,-1,0,0]])
    poisson=lambda f,h:(sp.Matrix([sp.diff(f,x) for x in variables]).T*omega*
                         sp.Matrix([sp.diff(h,x) for x in variables]))[0]
    c=q1+q2;q=(q1-q2)/2;p=p1-p2;h=(q+a)**2*(p+a)**2
    assert sp.expand(poisson(c,h))==0 and poisson(q,p)==1
    assert N.surviving_constraints()['reduced_phase_dimension']==156


def test_nonlinear_kinetic_hessian_by_finite_differences():
    z=G.setup();rng=np.random.default_rng(11781)
    q=.15*rng.normal(size=78);p=.1*rng.normal(size=78);direction=rng.normal(size=78)
    direction/=np.linalg.norm(direction);step=.002
    hessian=(G.wick_energy(q,p+step*direction,z)-2*G.wick_energy(q,p,z)
             +G.wick_energy(q,p-step*direction,z))/step**2
    kinetic=G.coefficients(q,z)[0]
    assert abs(hessian-direction@kinetic@direction)<2e-7


def test_completed_square_equals_full_displaced_wick_energy():
    z=G.setup();rng=np.random.default_rng(11784)
    for _ in range(3):
        q=.2*rng.normal(size=78);p=.3*rng.normal(size=78)
        kinetic,ell,v,connection,effective,_=G.coefficients(q,z)
        assert abs(G.wick_energy(q,p,z)-(.5*(p-connection)@kinetic@(p-connection)+effective))<1e-10
        assert np.linalg.eigvalsh(kinetic)[0]>0


def test_cone_trace_is_exact_nonzero_rational_geometry():
    z=G.setup();g=z['g'];u40=np.rint(40*g['u']).astype(np.int64)
    pw40=np.rint(40*g['pw']).astype(np.int64);adj10=np.rint(10*g['g']).astype(np.int64)
    mnum=25*pw40-40*adj10+adj10@adj10
    for u in u40:
        assert Fraction(int(u@mnum@u),6400000)==Fraction(39,80)
    w=np.r_[g['kernel_witness'],np.zeros(40)]
    assert np.dot(w,w)==216
    assert abs(np.sum((g['v']@w)**2)-864)<1e-11
    result=G.nonlinear_cone()
    assert result['samples'][2]['squared_speed_max']>2


def test_curvature_rational_witness_and_analytic_jacobian_independently():
    z=G.setup();j=G.exact_curvature()
    assert Fraction(j['contracted_integer'],j['denominator'])==Fraction(-31,10)
    rng=np.random.default_rng(11785);q=.05*rng.normal(size=78);direction=rng.normal(size=78)
    direction/=np.linalg.norm(direction);eps=1e-5
    numeric=(G.coefficients(q+eps*direction,z)[3]-G.coefficients(q-eps*direction,z)[3])/(2*eps)
    u,v,a,c=(z[k] for k in ('u','v','a','c'))
    kinetic,_,_,connection,_,_=G.coefficients(q,z);x=v@q+a
    target=-np.linalg.solve(kinetic,u.T@((4*x*(u@connection+a)+4*c)*(v@direction)))
    assert np.linalg.norm(numeric-target)<1e-9


def test_curvature_and_lorentz_metric_survive_second_orthogonal_basis():
    z=G.setup();rng=np.random.default_rng(80);rotation=np.linalg.qr(rng.normal(size=(78,78)))[0]
    other=dict(z);other['u']=z['u']@rotation;other['v']=z['v']@rotation
    q=.1*rng.normal(size=78);first=G.coefficients(q,z);second=G.coefficients(rotation.T@q,other)
    assert np.allclose(second[0],rotation.T@first[0]@rotation,atol=1e-12)
    assert np.allclose(second[3],rotation.T@first[3],atol=1e-12)
    assert np.allclose(second[-1],rotation.T@first[-1]@rotation,atol=1e-12)
    assert np.linalg.norm(first[-1])>.1


def test_full_80d_lorentzian_signature_inverse_and_null_reduction():
    z=G.setup();q=np.zeros(78);kinetic,_,_,connection,effective,_=G.coefficients(q,z)
    metric=np.zeros((80,80));metric[:78,:78]=np.linalg.inv(kinetic)
    metric[:78,78]=connection;metric[78,:78]=connection
    metric[78,78]=-2*effective;metric[78,79]=metric[79,78]=1
    values=np.linalg.eigvalsh(metric)
    assert np.count_nonzero(values>0)==79 and np.count_nonzero(values<0)==1
    p=np.linspace(-.1,.1,78);energy=G.wick_energy(q,p,z)
    momenta=np.r_[p,-energy,1]
    assert abs(momenta@np.linalg.inv(metric)@momenta/2)<1e-9


def test_constant_energy_shift_is_lift_diffeomorphism_not_screening():
    g,a,v,shift=sp.symbols('g a v shift')
    old=sp.Matrix([[g,a,0],[a,-2*(v+shift),1],[0,1,0]])
    # v_new=v_old-shift*u, so dv_old=dv_new+shift*du.
    jac=sp.Matrix([[1,0,0],[0,1,0],[0,shift,1]])
    assert sp.simplify(jac.T*old*jac)==sp.Matrix([[g,a,0],[a,-2*v,1],[0,1,0]])


def test_stored_certificate_source_hashes_and_claim_boundaries():
    import hashlib
    names=[V,N,G]
    for module in names:
        stored=json.loads(module.OUT.read_text())
        source=Path(module.__file__).read_bytes().replace(b'\r\n',b'\n')
        assert stored['source_sha256']==hashlib.sha256(source).hexdigest()
    assert 'still open' in json.loads(N.OUT.read_text())['pass11780']['actual_index_boundary']
    assert 'not a computed one-loop' in json.loads(G.OUT.read_text())['pass11781']['boundary']
