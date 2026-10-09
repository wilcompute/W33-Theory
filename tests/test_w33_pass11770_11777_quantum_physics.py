"""Independent checks for the eight11770-11777 investigations."""
import importlib.util
from pathlib import Path
from functools import lru_cache
import numpy as np
import sympy as sp
ROOT=Path(__file__).resolve().parents[1]


def module(name):
    spec=importlib.util.spec_from_file_location(name,ROOT/'analysis'/f'{name}.py')
    m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m


A=module('w33_pass11769_quantized_current_vacuum')
V=module('w33_pass11770_11774_11776_vacuum_constraints_modular')
C=module('w33_pass11771_11773_11777_cones_fermions_propagation')
R=module('w33_pass11775_symmetric_non_gaussian_vacuum')


def test_current_unitary_flow_composition_and_volume():
    g=A.geometry();u,v=g['u'][17],g['v'][17];a=1/np.sqrt(20)
    q=np.random.default_rng(11770).normal(size=80);q=g['pw']@q
    def flow(t,q):return q-t*(v@q+a)*u
    assert np.allclose(flow(.3,flow(-.7,q)),flow(-.4,q))
    assert abs(np.linalg.det(np.eye(80)-.7*np.outer(u,v))-1)<1e-12
    assert abs(v@flow(.3,q)-v@q)<1e-13
    # Thus both the pullback volume and the real phase modulus are preserved.
    assert abs(abs(np.exp(-.3j*a*(v@q+a)))-1)<1e-15


def test_constraint_conversion_rank_and_symplectic_reduction():
    omega=sp.kronecker_product(sp.eye(3),sp.Matrix([[0,0,1,0],[0,0,0,1],[-1,0,0,0],[0,-1,0,0]]))
    constraints=sp.kronecker_product(sp.eye(3),sp.Matrix([[1,1,0,0],[0,0,1,-1]]))
    assert constraints*omega*constraints.T==sp.zeros(6)
    assert 12-2*constraints.rank()==0
    assert V.central_conversion()['reduced_phase_dimension']==0


def test_modular_spectrum_is_independent_of_local_phase_and_scale():
    result=V.modular_spectrum(t=2.7,f=.31)
    assert np.allclose(result['symplectic_eigenvalues'][:15],.5)
    assert np.allclose(result['symplectic_eigenvalues'][15:],2/np.sqrt(10))
    assert abs(result['thermal_modular_energy']-np.log((4+np.sqrt(10))/(4-np.sqrt(10))))<1e-13


def test_rapidity_mass_shell_and_boost_equations_exactly():
    theta,m=sp.symbols('theta m',real=True,positive=True)
    h=(sp.exp(theta)+m*m*sp.exp(-theta))/2
    p=(sp.exp(theta)-m*m*sp.exp(-theta))/2
    assert sp.simplify(h*h-p*p-m*m)==0
    assert sp.simplify(sp.diff(h,theta)-p)==0
    assert sp.simplify(sp.diff(p,theta)-h)==0


def test_actual_displacement_hessian_by_independent_finite_difference():
    g=A.geometry();tr=A.exact_trial();m,t,f=[tr[k] for k in ('m','t','f')]
    vx,vy,c=t*m,m/t+f*f*t*m,f*t*m;b=.05
    rng=np.random.default_rng(11771);dq=g['pw']@rng.normal(size=80);dp=g['pw']@rng.normal(size=80)
    dq/=np.linalg.norm(dq);dp/=np.linalg.norm(dp)
    def energy(h):
        x=np.sqrt(b)+h*(g['v']@dq);y=np.sqrt(b)+h*(g['u']@dp)
        return np.sum(vx*vy+2*c*c+vx*y*y+vy*x*x+4*c*x*y+x*x*y*y)
    step=1e-3
    second=(energy(step)-2*energy(0)+energy(-step))/(step*step)
    q=2*(vy+b)*(g['v'].T@g['v']);p=2*(vx+b)*(g['u'].T@g['u'])
    r=4*(c+b)*(g['v'].T@g['u'])
    target=dq@q@dq+2*dq@r@dp+dp@p@dp
    assert abs(second-target)<1e-6


def test_kinetic_inverse_is_local_polynomial_on_actual_carrier():
    g=A.geometry();adj=np.block([[np.zeros((40,40)),g['n']],[g['n'].T,np.zeros((40,40))]])
    polynomial=np.eye(80)/4-adj/10+adj@adj/40
    inverse=g['pw']/4-g['g']/10+g['g']@g['g']/40
    assert np.allclose(g['pw']@polynomial@g['pw'],inverse,atol=1e-14)
    reachable=(np.eye(80)+adj+adj@adj)>0
    assert np.max(np.abs(polynomial[~reachable]))==0


def test_common_cone_flow_and_real_small_oscillation_frequencies():
    result=C.oscillator_response()
    assert max(x['error'] for x in result['matched_checks'])<2e-11
    assert result['frequency_squared_48']>0
    assert abs(result['frequency_squared_30']/result['frequency_squared_48']-1.6)<1e-13
    # Independent long-wavelength limit of the supplied lattice dispersion.
    k=np.array([.2,-.4,.6]);ell=1e-3
    lattice=4*np.sum(np.sin(k*ell/2)**2)/ell**2
    assert abs(lattice-k@k)<2e-8


def test_actual_current_curvature_support():
    edges=A.actual_edges();count=0
    for i,e in enumerate(edges):
        ue=np.zeros(80);ve=np.zeros(80);ue[list(e)]=1;ve[e[0]]=1;ve[e[1]]=-1
        for f in edges[i+1:]:
            uf=np.zeros(80);vf=np.zeros(80);uf[list(f)]=1;vf[f[0]]=1;vf[f[1]]=-1
            bracket=np.outer(ue,vf)*(ve@uf)-np.outer(uf,ve)*(vf@ue)
            nonzero=np.any(bracket)
            assert nonzero==(not set(e).isdisjoint(f))
            count+=bool(nonzero)
    assert count==480


def test_fermionic_clifford_and_chirality_controls():
    r=C.clifford_extension()
    assert r['square_check_error']<1e-13
    corners=r['lattice_control']['zeros']
    signs=[int(round(np.prod(np.cos(np.pi*np.array(x['corner_pi_units']))))) for x in corners]
    assert signs.count(1)==signs.count(-1)==4
    assert sum(x['wilson_mass']==0 for x in corners)==1


def test_regulator_fourth_moment_via_independent_wick_recursion():
    tr=A.exact_trial();m,t,f=[tr[k] for k in ('m','t','f')]
    covariance=((t*m,f*t*m),(f*t*m,m/t+f*f*t*m));a=np.sqrt(.05)
    @lru_cache(None)
    def wick(indices):
        if not indices:return 1.
        if len(indices)%2:return 0.
        head,*rest=indices
        return sum(covariance[head][r]*wick(tuple(rest[:j]+rest[j+1:])) for j,r in enumerate(rest))
    from math import comb
    fourth=160*sum(comb(4,i)*comb(4,j)*a**(8-i-j)*wick((0,)*i+(1,)*j) for i in range(5) for j in range(5))
    r=C.bounded_propagation()
    assert abs(r['gaussian_fourth_current_moment_sum']-fourth)<1e-9
    assert all(0<x['error']<x['fourth_moment_error_bound'] for x in r['trial_records'])


def test_symmetry_restored_non_gaussian_state_and_exact_gram_norm():
    r=R.payload()
    assert 127.61950<r['energy']<127.61952
    norm=40*(sp.Integer(1)+12*sp.Rational(1,3)**4+27*sp.Rational(1,9)**4)
    assert norm==sp.Rational(11200,243)
    coeff=np.array([complex(*z) for z in r['coefficients']])
    assert abs(np.vdot(coeff,coeff)-1)<1e-12
    kp,kl=complex(*r['point_coupling']),complex(*r['line_coupling'])
    mat=np.array([[A.exact_trial()['energy'],kp.conjugate(),kl.conjugate()],
                  [kp,r['diagonal'],0],[kl,0,r['diagonal']]])
    assert np.linalg.norm(mat@coeff-r['energy']*coeff)<1e-10
    # The correction entangles the two kernel factors but has only Schmidt rank2.
    kernel=np.array([[coeff[0],coeff[2]],[coeff[1],0]])
    assert np.linalg.matrix_rank(kernel,tol=1e-12)==2


def test_optimized_gaussian_is_fixed_by_parallel_dressed_antiunitary():
    # Independent Wigner-covariance test, rather than the precision-inverse
    # calculation used by the producer. T(q,p)=(D*p,D*q).
    g=A.geometry();tr=A.exact_trial();c,ci=A.spectral_covariance(g)
    c=c*tr['t'];ci=ci/tr['t'];d=np.diag(g['s']);f=tr['f']*d
    sigma=np.block([[c,c@f],[f@c,ci+f@c@f]])/2
    exchange=np.block([[np.zeros((80,80)),d],[d,np.zeros((80,80))]])
    assert np.allclose(exchange@sigma@exchange.T,sigma,atol=3e-13)
    # The exact family action is an involution for arbitrary positive t, real f.
    t,f=sp.symbols('t f',real=True,positive=True)
    tp=(1+f*f*t*t)/t;fp=f*t*t/(1+f*f*t*t)
    assert sp.factor((1+fp*fp*tp*tp)/tp-t)==0
    assert sp.factor(fp*tp*tp/(1+fp*fp*tp*tp)-f)==0


def test_rank_changing_principal_symbol_exact_star_gram():
    g=A.geometry();edges=A.actual_edges();star=[i for i,e in enumerate(edges) if e[0]==0]
    scaled=sp.Matrix(np.rint(40*g['u'][star]).astype(int).tolist())
    gram=scaled*scaled.T/sp.Integer(1600)
    assert gram.det()==sp.Rational(24,5)
    assert sorted(gram.eigenvals().values())==[1,3]
    result=V.principal_symbol()
    assert result['principal_rank_at_star']==4 and result['principal_rank_at_origin']==78
