"""Independent controls of five followups; no scope is inferred from PASS alone."""
from pathlib import Path
import sys,json
import numpy as np
import sympy as s
from scipy.integrate import solve_ivp
from scipy.linalg import expm
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'analysis'))
import w33_pass12016_12020_neutrino_vacuum_native_measure as p


def test_neutrino_and_existing_charged_branch():
    o,details=p.neutrino_observables();assert max(abs(o/p.NEUTRINO_TARGET-1))<1e-7
    assert max(abs(p.prior.rg_residual(p.prior.RG_FIT)))<1e-7
    masses=np.array(details['masses_eV']);assert abs(masses[2]**2-masses[0]**2-.002511)<1e-12


def test_C5_hadamard_factors_against_matrix_ODE():
    _,_,F1,F2=p.lepton_running();C=np.array([[1,.3j,.2],[.3j,.7,.4j],[.2,.4j,.5]],complex)
    def rhs(t,c):
        g,m=p.prior.unpack(p.prior.running().sol(t));ell=np.linalg.svd(m[2],compute_uv=False)[::-1]**2;H=np.diag(ell);T=sum(a*np.trace(z@z.conj().T).real for a,z in zip([3,3,1],m));P=H/p.LOOP
        Q=-1.5*P-(57*g[0]**2/16-33*g[1]**2/16-5*T/4)*P/p.LOOP+19*(P@P)/4;c=c.reshape(3,3)
        return (Q@c+c@Q.T+2*P@c@P.T).ravel()
    result=solve_ivp(rhs,[p.prior.RG_FIT[-1],0],C.ravel(),rtol=1e-11,atol=1e-13)
    assert np.max(abs(result.y[:,-1].reshape(3,3)-C*F2))<1e-10
    assert np.max(abs(F2-F1))>1e-9
    log=np.log(F1);assert np.max(abs(log-(np.diag(log)[:,None]+np.diag(log)[None,:])/2))<1e-14
    log=np.log(F2);assert np.max(abs(log-(np.diag(log)[:,None]+np.diag(log)[None,:])/2))>1e-15


def test_neutrino_rank_four_retains_one_shape_direction():
    h=1e-5;J=np.column_stack([(np.log(p.neutrino_observables(p.NU_FIT+h*v)[0])-np.log(p.neutrino_observables(p.NU_FIT-h*v)[0]))/(2*h) for v in np.eye(5)])
    assert np.linalg.matrix_rank(J,tol=1e-5)==4


def test_threshold_refits_are_actual_residual_controls():
    out=p.neutrino_thresholds();scales=[]
    for row in out['threshold_refits']:
        assert max(abs(p.threshold_residual(np.array(row['parameters']),row['universal_down_threshold'])))<1e-6
        scales.append(row['scale_GeV'])
    assert scales[0]>5e6 and scales[1]<3.5e6


def test_invariant_differential_and_CP_evenness():
    A,B=p.flavour_home();rng=np.random.default_rng(17);d=rng.normal(size=(3,3))+1j*rng.normal(size=(3,3));d=(d+d.conj().T)/2;h=1e-5
    fd=(p.invariants(A+h*d,B)-p.invariants(A-h*d,B))/(2*h)
    assert np.max(abs(fd-p.invariant_derivative(A,B,d,np.zeros((3,3)))))<1e-7
    assert np.max(abs(p.invariants(A,B)-p.invariants(A.conj(),B.conj())))<1e-12


def test_full_flavour_hessian_and_symmetry_tangents():
    out=p.flavour_potential();assert out['positive_normal_modes']==10 and out['symmetry_zero_modes']==8
    assert min(out['normal_Hessian_eigenvalues'])>1e-8 and out['orbit_annihilation_error']<1e-10
    A,B=p.flavour_home();target=p.invariants(A,B);w=np.array(out['weights']);rng=np.random.default_rng(171);dA=rng.normal(size=(3,3));dA=(dA+dA.T)/2;dB=rng.normal(size=(3,3));dB=(dB+dB.T)/2
    pred=2*np.linalg.norm(w*p.invariant_derivative(A,B,dA,dB))**2;h=1e-5
    V=lambda h:np.linalg.norm(w*(p.invariants(A+h*dA,B+h*dB)-target))**2
    assert abs((V(h)+V(-h))/h**2-pred)<1e-5*pred


def test_flavour_vacuum_second_basis():
    A,B=p.flavour_home();W=expm(1j*np.array([[.1,.2j,.3],[-.2j,-.1,.2],[.3,.2,0]]));assert np.max(abs(p.invariants(W@A@W.conj().T,W@B@W.conj().T)-p.invariants(A,B)))<1e-10


def test_mediation_boundary_and_positive_soft_spectrum():
    out=p.gauge_mediation();assert 1200<out['dc_soft_mass_GeV']<out['Q_soft_mass_GeV']<1700
    assert out['leading_log_Ad_GeV']<0 and out['colored_threshold']['minimum_soft_eigenvalue']>1e6
    assert abs(out['colored_threshold']['sum'])<1e-10
    assert 'cancellation noise' in out['one_sided_exact_result']


def test_one_sided_theorem_arbitrary_diagonal_LR():
    rng=np.random.default_rng(181);M=np.diag([.3,.8,1.7]);z=rng.normal(size=(3,3))+1j*rng.normal(size=(3,3));L=5*np.eye(3)+.2*(z+z.conj().T);R=np.diag([6.,7.,8.]);LR=np.diag([.13,-.07,.3]);S=np.block([[L,LR],[LR,R]])
    out=p.prior.colored_phase(M,S);assert abs(out['sum'])<1e-12
    for zz in [-1.,-3.,-10.]:
        block=np.linalg.inv(zz*np.eye(6)-S)[:3,3:];assert max(abs(np.diag(block).imag))<1e-14
    ev,V=np.linalg.eigh(S)
    for fun in [np.exp,lambda x:x**3,lambda x:np.sin(x)]:
        F=(V*fun(ev))@V.conj().T;assert max(abs(np.diag(F[:3,3:]).imag))<1e-10


def test_both_sided_misalignment_CP_control():
    out=p.one_sided_alignment();assert abs(out['both_sides']['sum'])>1e-7
    assert abs(out['both_sides']['sum']+out['CP_partner']['sum'])<1e-12


def test_exact_native_quadratic_and_quartic():
    b,v,M,k,lam=p.exact_native_dispersion();assert M==s.Rational(2,27) and lam[1]==lam[3]==0
    assert len(s.Poly(lam[4],*k).terms())==31
    assert s.expand(lam[2]).coeff(k[0],2)==5
    assert lam[4].subs(dict(zip(k,[1,0,0,0])))==-s.Rational(1,12)
    assert lam[4].subs(dict(zip(k,[0,0,1,0])))==-s.Rational(11,54)
    out=p.native_continuum();errors=[abs(z['quadratic_error']) for z in out['refinement']]
    assert all(3.9<errors[i]/errors[i+1]<4.1 for i in range(3))


def test_native_marking_change_preserves_operator():
    b,v,M,k,lam=p.exact_native_dispersion();bf=np.array(b,float);vf=np.array(v,float);T=np.array([[1,1,0,0],[0,1,0,0],[0,0,1,1],[0,0,0,1]]);q=np.array([.03,.02,-.01,.04])
    def matrix(voltage,momentum):
        B=bf.astype(complex).copy()
        for e in range(135):B[e,np.flatnonzero(bf[e]>0)[0]]*=np.exp(1j*(voltage[e]@momentum))
        return B.conj().T@B
    assert np.max(abs(matrix(vf@T,q)-matrix(vf,T@q)))<1e-13


def test_native_word_differential_and_local_gauge_action():
    rng=np.random.default_rng(20);edges,_,_,_,_,words=p.prior.native_paths();links=[p.prior.su3(rng) if hasattr(p.prior,'su3') else np.eye(3,dtype=complex) for _ in edges]
    # Generate genuinely noncommuting links independently.
    def group():
        z=rng.normal(size=(3,3))+1j*rng.normal(size=(3,3));z=(z-z.conj().T)/2;z-=np.trace(z)*np.eye(3)/3;return expm(.1*z)
    links=[group() for _ in edges];gs=[group() for _ in range(27)];e=words[0][0][0];A=np.array([[.2j,.1,0],[-.1,-.2j,.2],[0,-.2,0]]);h=1e-5
    plus=list(links);minus=list(links);plus[e]=expm(h*A)@links[e];minus[e]=expm(-h*A)@links[e]
    new=[gs[a]@L@gs[b].conj().T for (a,b),L in zip(edges,links)]
    for word in words:
        fd=(p.word_product(word,plus)-p.word_product(word,minus))/(2*h);assert np.linalg.norm(fd-p.word_derivative(word,links,e,A))<1e-8
        assert np.linalg.norm(p.word_product(word,new)-gs[0]@p.word_product(word,links)@gs[0].conj().T)<1e-10


def test_local_measure_curvature_and_internal_intertwiner():
    out=p.local_measure();assert out['projector_rank']==30 and out['minimum_reference_overlap']>.25
    assert abs(out['projector_Berry_curvature'])>.001
    assert abs(out['projector_Berry_curvature']-out['frame_connection_curvature'])<1e-7
    assert out['native_path_derivative_error']<1e-7 and out['internal_operator_intertwining_error']<1e-10


def test_frozen_scope_boundaries():
    out=json.loads((ROOT/'data/w33_pass12016_12020_neutrino_vacuum_native_measure.json').read_text())
    assert out['status']=='PASS' and 'NOT a complete two-loop' in out['pass12016']['scope']
    assert 'engineered target' in out['pass12017']['scope'] and 'SUSYbenchmark is NOT' in out['pass12018']['gauge_mediation']['scope']
    assert 'not curved homogenization' in out['pass12019']['scope'] and 'not a globally' in out['pass12020']['scope']
