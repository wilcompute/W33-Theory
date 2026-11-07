"""Independent conservation, scattering and analytic-decay checks."""
import importlib.util
import json
import math
from pathlib import Path

import numpy as np
import pytest
from scipy.integrate import quad,solve_ivp
from scipy.special import k1,kve

ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('phase_space',ROOT/'analysis/toe_20261107_sterile_phase_space.py')
p=importlib.util.module_from_spec(spec);spec.loader.exec_module(p)


def test_contact_phase_integral_and_MB_Bessel_identity():
    for r in [.1,1.,4.]:
        actual=quad(lambda q:q*q/math.hypot(q,r)*math.exp(-math.hypot(q,r)),0,np.inf,epsabs=1e-12)[0]
        assert math.isclose(actual,r*k1(r),rel_tol=1e-10)
    # Lorentz-invariant thermal cross-section integral independently yields
    # <sigma*vM>=nh*lambda^2/(64*pi*m^2)*(K1/K2)^2.
    for T in [.5,1.,2.]:
        integral=quad(lambda z:2*z*math.sqrt(max(0,z*z-4))*k1(z/T),2,np.inf,epsabs=1e-11)[0]
        assert math.isclose(integral,4*T*k1(1/T)**2,rel_tol=2e-9)


def test_collision_detailed_balance_and_elastic_number():
    q,w=p.quadrature(96);ker=p.Kernel(q,w,.3,0.,.2)
    for r in [.2,1.,5.,15.]:
        E,eq,jw,L=ker.components(r)
        assert np.max(abs(ker.rhs(r,eq)))<2e-8
        assert np.max(abs(ker.number_weights@L))<1e-11
        assert np.max(abs(L@eq))<1e-13
        off=L-np.diag(np.diag(L));assert off.min()>-1e-14


def test_elastic_reversible_generator_spectrum():
    q,w=p.quadrature(48);ker=p.Kernel(q,w,.4,0.,0.)
    E,eq,jw,L=ker.components(2.)
    # Similarity with equilibrium and quadrature measure makes L symmetric.
    D=np.sqrt(ker.number_weights/eq)
    S=D[:,None]*L/D[None,:]
    assert np.max(abs(S-S.T))<1e-12
    eig=np.linalg.eigvalsh(S)
    assert eig.max()<1e-12
    assert abs(eig[-1])<1e-12
    assert eig[-2]<0


def test_elastic_normalization_matches_nonrelativistic_n_sigma_v():
    # A heavy parent at rest scatters on four massless MB bath states.
    # sigma(sh->sh)=lambda_p^2/(16pi*mS^2), n_h=4*T^3/pi^2.
    # Thus Gamma/H=8*A/r. This independently checks the absolute elastic factor.
    q,w=p.quadrature(144);r=1e5;qi=1e-7;A=.23
    Ei=math.hypot(qi,r);Ej=np.hypot(q,r)
    angular=np.exp(-abs(qi-q)/2)*(-np.expm1(-np.minimum(qi,q)))
    loss=2*A/(Ei*qi)*np.sum(w*q/Ej*angular*np.exp((Ei-Ej)/2))
    assert math.isclose(r*loss,8*A/r,rel_tol=2e-4)


def test_full_nonlinear_jacobian():
    q,w=p.quadrature(24);ker=p.Kernel(q,w,.7,.03,.2)
    f=.3*np.exp(-np.hypot(q,1.3));v=np.random.default_rng(712).normal(size=len(q))*.001
    eps=1e-5
    actual=(ker.rhs(1.3,f+eps*v)-ker.rhs(1.3,f-eps*v))/(2*eps)
    assert np.max(abs(actual-ker.jac(1.3,f)@v))<1e-9


def test_exact_collisionless_decay_and_two_daughters():
    q,w=p.quadrature(64);r0=.01;rend=18.;dn=.2
    f0=p.initial(q,r0,'thermal_MB');ker=p.Kernel(q,w,0.,dn,0.)
    sol=solve_ivp(ker.rhs,(r0,rend),f0,method='DOP853',rtol=1e-11,atol=1e-13,dense_output=True)
    primitive=lambda r:.5*(r*np.hypot(q,r)-q*q*np.arcsinh(r/q))
    expect=f0*np.exp(-dn*(primitive(rend)-primitive(r0)))
    assert np.max(abs(sol.y[:,-1]-expect))<1e-11
    rr=np.geomspace(r0,rend,2001);bins=np.linspace(0,70,401)
    h,m=p.decay_postprocess(q,w,rr,sol.sol(rr),dn,bins)
    lost=float(ker.number_weights@(f0-expect))
    assert math.isclose(m[0],2*lost,rel_tol=2e-8)
    assert math.isclose(h.sum(),m[0],rel_tol=1e-12)


def test_thermal_reservoir_limit_recovers_existing_freezein_yield():
    pars=dict(A=0.,DN=.002,DH=3000.,M_keV=16.,m_S_GeV=3000.)
    d=p.solve_case(pars,'zero',nq=64,nr=1001)
    analytic_Y=2*p.YCOEFF*pars['DN']*3*math.pi/2
    assert math.isclose(d['Y_N'],analytic_Y,rel_tol=2e-3)


def test_daughter_bin_partition_and_angular_moments():
    q=np.array([2.]);w=np.array([1.]);rr=np.array([1.,1.00001,1.00002]);ff=np.ones((1,3))
    bins=np.linspace(0,4,501)
    h,m=p.decay_postprocess(q,w,rr,ff,.5,bins)
    # Tiny r interval approximates a single isotropic parent decay.
    E=math.hypot(2.,1.00001)
    assert math.isclose(m[1]/m[0],E/2,rel_tol=1e-9)
    assert math.isclose(m[2]/m[0],E*E/4+4/12,rel_tol=1e-9)
    assert np.all(h>=0)


def test_integrated_source_identities():
    I=quad(lambda r:r**3*k1(r),0,np.inf,epsabs=1e-11)[0]
    J=quad(lambda r:(r*k1(r))**2,0,np.inf,epsabs=1e-11)[0]
    assert math.isclose(I,3*math.pi/2,rel_tol=1e-11)
    assert math.isclose(J,3*math.pi**2/32,rel_tol=1e-10)


def test_inverse_decay_family_is_not_thermal_floor_limited():
    for mass in [16.,30.,100.]:
        par=p.inverse_decay_branch(mass)
        assert math.isclose(par['DH']/par['DN'],par['analytic_width_ratio'],rel_tol=1e-14)
        predicted=2.744e8*mass*1e-6*2*p.YCOEFF*3*math.pi/2*par['DN']*par['DH']/(par['DN']+par['DH'])
        assert math.isclose(predicted,.12,rel_tol=1e-14)
        assert par['lambda_portal']<par['old_annihilation_only_portal_floor']
        assert par['minimal_Z2_parent_quartic_if_imposed']<1
    # Numerical A=0 transport must recover the analytic family, even without
    # imposing thermal parents, and with elastic kernel switched off.
    par=p.inverse_decay_branch(100.)
    par['A']=0.
    out=p.solve_case(par,'zero',nq=64,nr=1601,elastic=False)
    assert math.isclose(out['omega_h2'],.12,rel_tol=3e-5)
    assert abs(out['integrated_number_sumrule_relative_error'])<3e-5


def test_full_collision_number_sumrule_and_upper_bound():
    par=p.inverse_decay_branch(16.)
    out=p.solve_case(par,'zero',nq=64,nr=1201)
    assert abs(out['integrated_number_sumrule_relative_error'])<2e-5
    assert out['omega_h2']<=out['infinite_interval_dropping_annihilation_loss_upper_omega']*(1+1e-6)
    assert abs(out['scalar_integrated_number_balance_relative_error'])<2e-5


def test_actual_server_kinetic_replay_against_frozen_PC_packet():
    pc=json.loads((ROOT/'data/toe_20261107_sterile_phase_space.json').read_text())
    server=json.loads((ROOT/'data/toe_20261107_sterile_phase_space_server.json').read_text())
    for row in server['rows']:
        ours=next(x for x in pc['rows'] if x['parameters']['M_keV']==row['M_keV']
                  and x['parameters']['m_S_GeV']==row['m_S_GeV'] and x['initial_scalar']==row['initial_scalar']
                  and x['parameters']['inherited_portal_fraction']==.5)
        assert math.isclose(ours['omega_h2'],row['omega_h2'],rel_tol=3e-4)
        assert math.isclose(ours['mean_q'],row['mean_q'],rel_tol=3e-4)
    for row in server['reopened']:
        ours=next(x for x in pc['reopened_inverse_decay_examples']if x['parameters']['M_keV']==row['M_keV'])
        assert math.isclose(ours['omega_h2'],row['omega_h2'],rel_tol=3e-4)
        assert math.isclose(ours['rms_q'],row['rms_q'],rel_tol=3e-4)


def test_frozen_packet_conservation_and_histogram_normalization():
    pc=json.loads((ROOT/'data/toe_20261107_sterile_phase_space.json').read_text())
    for row in pc['rows']+pc['reopened_inverse_decay_examples']:
        assert abs(row['integrated_number_sumrule_relative_error'])<2e-5
        assert abs(row['scalar_integrated_number_balance_relative_error'])<2e-5
        assert math.isclose(sum(row['comoving_daughter_Y_per_bin']),row['Y_N'],rel_tol=1e-10)
        assert row['omega_h2']<=row['infinite_interval_dropping_annihilation_loss_upper_omega']*(1+1e-6)
