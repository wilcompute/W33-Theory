from pathlib import Path
import sys,json
import numpy as np
import pytest
from scipy.linalg import expm
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'analysis'))
import w33_pass12034_12038_joint_mechanisms as m

@pytest.fixture(scope='module')
def cert():return json.loads((ROOT/'data/w33_pass12034_12038_joint_mechanisms.json').read_text())

def test_supermultiplet_susy_cancellation():
    x=m.old.MATCH[:10]
    for Q in [.4,1.,3.]:assert abs(m.cw(x,soft=0,Q=Q))<1e-16

def test_exact_supertrace_scale_derivative():
    x=m.old.MATCH[:10];h=1e-4
    fd=(m.cw(x,Q=np.exp(h))-m.cw(x,Q=np.exp(-h)))/(2*h)
    assert fd==pytest.approx(m.cw_scale_derivative(x),abs=2e-11)

def test_fibre_counterterm_is_not_a_selected_vacuum(cert):
    d=cert['pass12034'];assert d['scale_identity_error']<1e-8
    assert min(z['norm'] for z in d['projected_gradients'])>1e-3
    assert d['unremovable_force_norm']>1e-6
    N=m.flat_basis();assert np.linalg.norm(N.T@N-np.eye(6))<1e-10

def test_trilinear_one_family_matches_primary_equations():
    g=np.array([.4,.6,1.]);mg=np.array([.5,.8,1.2]);yt,yb,ye=.8,.3,.2;at,ab,ae=.4,-.2,.1
    Y=[np.diag([0,0,q]) for q in [yt,yb,ye]];T=[np.diag([0,0,q]) for q in [at,ab,ae]]
    out=m.trilinear_beta(g,Y,T,mg);g1,g2,g3=g;M1,M2,M3=mg
    expected=[at*(18*yt**2+yb**2-16/3*g3**2-3*g2**2-13/15*g1**2)+2*ab*yb*yt+yt*(32/3*g3**2*M3+6*g2**2*M2+26/15*g1**2*M1),
    ab*(18*yb**2+yt**2+ye**2-16/3*g3**2-3*g2**2-7/15*g1**2)+2*at*yt*yb+2*ae*ye*yb+yb*(32/3*g3**2*M3+6*g2**2*M2+14/15*g1**2*M1),
    ae*(12*ye**2+3*yb**2-3*g2**2-9/5*g1**2)+6*ab*yb*ye+ye*(6*g2**2*M2+18/5*g1**2*M1)]
    assert np.allclose([q[2,2] for q in out],expected,atol=1e-13)

def test_trilinear_flavour_covariance():
    rng=np.random.default_rng(12035)
    def mat():return rng.normal(size=(3,3))+1j*rng.normal(size=(3,3))
    U=np.linalg.qr(mat())[0];V=[np.linalg.qr(mat())[0] for _ in range(3)];Y=[mat() for _ in range(3)];T=[mat() for _ in range(3)];g=np.array([.4,.6,.9]);mg=np.array([1.,2.,3.])
    base=m.trilinear_beta(g,Y,T,mg);rotate=lambda a:[U@q@v.conj().T for q,v in zip(a,V)]
    actual=m.trilinear_beta(g,rotate(Y),rotate(T),mg)
    assert max(np.linalg.norm(a-b) for a,b in zip(actual,rotate(base)))<2e-12

def test_zero_A_is_first_order_aligned_but_second_order_not(cert):
    d=cert['pass12035'];exact=np.array(d['analytic_log_squared_misalignment_GeV'])
    rows=d['A_zero_coupled_running'];assert min(exact)>0
    errors=[np.linalg.norm(np.array(r['misalignment_over_log_squared'])-exact) for r in rows[:3]]
    assert errors[2]<errors[1]<errors[0]
    assert np.allclose(rows[2]['misalignment_over_log_squared'],exact,rtol=.001)
    assert min(d['first_derivative_alignment_residual_GeV'])>0

def test_electroweak_inputs_close_tree_equations(cert):
    d=cert['pass12036'];assert max(abs(z) for z in d['stationary_residuals_GeV2'])<1e-8
    assert min(d['neutralino_tree_masses_GeV'])>0
    assert min(d['chargino_tree_masses_GeV'])>0
    assert 0<d['CP_even_tree_masses_GeV'][0]<d['running_Z_mass_GeV']
    assert d['leading_stop_delta_lambda']>0

def test_component_scheme_casimirs(cert):
    d=cert['pass12036'];g=np.array(d['declared_g_DR_for_isolated_scheme_map']);C_Q=np.array([1/60,3/4,4/3]);C_U=np.array([4/15,0,4/3]);C_D=np.array([1/15,0,4/3]);C_H=np.array([3/20,3/4,0]);C_L=C_H;C_E=np.array([3/5,0,0])
    expected=[np.dot(g*g,C_Q+C_U-2*C_H)/(32*np.pi**2),np.dot(g*g,C_Q+C_D-2*C_H)/(32*np.pi**2),np.dot(g*g,C_L+C_E-2*C_H)/(32*np.pi**2)]
    assert np.allclose(expected,d['Higgs_scalar_Yukawa_MS_over_DR_minus_one'],atol=1e-15)
    assert d['g_MS_from_DR'][0]==g[0]
    assert d['g_MS_from_DR'][2]<g[2]

def test_TT_formfactor_gaussian_series(cert):
    d=cert['pass12037'];assert d['series_coefficients']==['-1/12','1/120','-1/1680','1/30240','-1/665280']
    for z in d['samples']:
        x=z['x'];poly=-x/12+x*x/120-x**3/1680+x**4/30240-x**5/665280
        assert abs(z['normalized_heat_hessian']-poly)<=x**6/17297280+1e-15
    assert m.tensor_formfactor(0)==pytest.approx(0,abs=1e-15)

def test_TT_independent_finite_amplitude_operator(cert):
    rows=cert['pass12037']['independent_continuum_spectral_check']
    assert abs(rows[-1]['error'])<1e-8
    assert abs(rows[-1]['error'])<abs(rows[0]['error'])
    # A fresh, different longitudinal cutoff/quadrature/amplitude.
    h=.003;f=lambda z:m.tensor_spectral_heat(z,cutoff=28,quadrature_order=6)
    fd=(f(h)-2*f(0)+f(-h))/h**2
    assert fd==pytest.approx(m.tensor_formfactor(1),abs=5e-8)

def test_actual_native_TT_metrics_and_capacity(cert):
    d=cert['pass12037'];assert d['exact_metric_rank']==10
    for z in d['native_TT_metric_lifts']:
        assert z['min_weight']>.1;assert z['metric_error']<1e-12
        assert z['relative_capacity']==pytest.approx(1,abs=1e-12)

def test_nonabelian_atlas_cocycles_and_connection(cert):
    for z in cert['pass12038']['overlap_checks']:
        assert z['reference_overlap_min']>.5
        assert z['frame_cocycle_error']<1e-11
        assert z['transition_unitarity_error']<1e-11
        assert abs(z['connection_transition_identity_error'])<1e-8

def test_atlas_independent_rephasing_control():
    patch=m.prior.NativeChiralPatch();P=patch.evaluate(.07,-.04)[0];E=patch.evaluate(-.1,.15)[1];F,_=m.frame_from(P,E)
    rng=np.random.default_rng(12038);a=rng.normal(size=(30,30))+1j*rng.normal(size=(30,30));U=expm(.03*(a-a.conj().T));G,_=m.frame_from(P,E@U)
    assert np.linalg.norm(G-F@U)<1e-11
    assert abs(np.linalg.det(F.conj().T@G)-np.linalg.det(U))<1e-11

def test_scope_does_not_assert_remaining_physics_closed(cert):
    assert 'no selected theta vacuum' in cert['pass12034']['scope']
    assert 'not integrated' in cert['pass12035']['scope']
    assert 'not a pole-mass prediction' in cert['pass12036']['scope']
    assert 'not a native TT heat convergence theorem' in cert['pass12037']['scope']
    assert 'No all-configuration covering' in cert['pass12038']['scope']

def test_bino_commutator_symbolic_word():
    import sympy as s
    H,D=s.symbols('H D',commutative=False);cu,cd=s.symbols('cu cd',commutative=True)
    comm=lambda a,b:a*b-b*a
    Ru=3*cu*H+cd*D;Rd=3*cd*D+cu*H
    assert s.expand(4*comm(H,Ru)+2*comm(D,Ru)+2*comm(Rd,D)-4*(cd-cu)*comm(H,D))==0

def test_bino_commutator_independent_full_RG_and_control(cert):
    d=cert['pass12035']['bino_commutator'];on,off=d['controls']
    assert on['analytic_coefficient_norm']>1e-8
    err=[z['analytic_error'] for z in on['samples']]
    assert err[2]<err[1]<err[0]
    assert err[2]/on['analytic_coefficient_norm']<.02
    assert off['analytic_coefficient_norm']==0
    null=[z['antiHermitian_over_log_cubed_norm'] for z in off['samples']]
    assert null[2]<null[1]<null[0]
    assert null[2]<.005*on['analytic_coefficient_norm']

def test_scalar_misalignment_is_distinguished_from_offdiagonal_LR(cert):
    d=cert['pass12035'];coeff=d['analytic_log_squared_offdiagonal_GeV']
    assert coeff[0]>0 and coeff[1]>0 and coeff[2]<1e-12
    rows=d['A_zero_coupled_running']
    for r in rows[:3]:
        t=r['log_interval'];actual=np.array(r['offdiagonal_mass_basis_GeV'])/t**2
        assert np.allclose(actual[:2],coeff[:2],rtol=.01,atol=1e-10)
