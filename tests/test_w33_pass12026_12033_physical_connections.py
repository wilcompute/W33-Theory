"""Independent controls of theta fibres, soft kernels, thresholds, heat and topology."""
from pathlib import Path
import json,sys,itertools
import numpy as np
from scipy.integrate import solve_ivp
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'analysis'))
import w33_pass12026_12033_theta_soft_threshold_connections as q
import w33_pass12029_native_heat_curvature as h
import w33_pass12030_native_determinant_torus as c

def certificate(name):return json.loads((ROOT/'data'/name).read_text())


def test_theta_orientation_fibre_changes_masses():
    out=q.theta_pullback();assert out['orientation_rank']==4 and out['local_unfixed_theta_directions']==6
    assert min(out['mixing_Jacobian_singular_values'])>1e-3
    for row in out['fixed_orientation_continuations']:
        x=np.r_[row['parameters'],q.MATCH[-1]];assert max(abs(q.mix_coordinates(x)-q.mix_coordinates(q.MATCH)))<1e-8
    assert max(abs(np.array(out['fixed_orientation_continuations'][-1]['mass_ratio_log_changes'])))>.01
    assert min(out['charged_residual_Jacobian_singular_values'])>1e-8


def test_cross_branch_parent_is_retargeted_explicitly():
    out=q.cross_branch_parent();assert out['new_branch_energy_in_old_parent']>1e-10
    V=q.orientation(q.MATCH);A=np.diag(q.prior.old.A_SPEC);B=V@np.diag(q.prior.old.B_SPEC)@V.conj().T;fields=[A,B,A@A,B@B];w=np.array(q.prior.old.flavour_potential()['weights'])
    assert np.linalg.norm(q.prior.parent_residual(fields,np.array(out['retargeted_coefficients']),w))<1e-12
    assert np.linalg.norm(q.prior.parent_residual(fields,np.array(out['old_target']),w))>1e-5


def test_linked_all_orders_trace_identity_for_independent_functions():
    mass,E=q.linked_parameters();M=np.diag(mass)
    for eps,eta in [(.2,.3),(-.1,.2),(.3,-.1)]:
        S=np.block([[5*np.eye(3)+eps*E,.3*M],[.3*M,7*np.eye(3)+eta*M@E@M]]);ev,V=np.linalg.eigh(S)
        for fun in [np.sin,np.log,lambda x:x**3]:
            F=(V*fun(ev))@V.conj().T
            assert abs(np.trace(np.linalg.solve(M,F[:3,3:])).imag)<1e-10
            assert abs(np.trace(M@F[:3,3:]).imag)<1e-10
        assert abs(q.p.colored_phase(M,S)['quark'])<1e-12


def test_first_surviving_cubic_gluino_and_conjugation():
    out=q.linked_soft_theorem();co=out['cubic_coefficient'];assert abs(co)>1e-7
    errors=[abs(z['theta_over_t3']-co) for z in out['finite_controls']]
    assert all(3.8<errors[i]/errors[i+1]<4.2 for i in range(2))
    mass,E=q.linked_parameters();assert abs(q.cubic_gluino(mass,E.conj())+co)<1e-14
    perm=[1,0,2];assert abs(q.cubic_gluino(mass[perm],E[np.ix_(perm,perm)])-co)<1e-14
    mass[1]=mass[0];assert q.cubic_gluino(mass,E)==0


def test_B1_equal_mass_and_matching_log():
    assert abs(q.B1(4.,4.,3.)+.5*np.log(4/9))<1e-13
    pref=2*(q.matching_inputs()[0][2]**2/(4*np.pi))/(3*np.pi);a=q.sqcd_delta(2.3,'d');b=q.sqcd_delta(2.3,'d',Q=4000.)
    assert abs(b['chirality']-a['chirality'])<1e-12
    assert abs((b['total']-a['total'])+pref*np.log(2))<1e-12
    # This is exactly the difference between the SM and MSSM QCD Yukawa betas.
    assert abs((-8+16/3)*q.matching_inputs()[0][2]**2/q.prior.old.LOOP+pref)<1e-14


def test_all_six_SQCD_masses_and_unit_invariance():
    out=q.finite_thresholds();assert len(out['all_six_quark_matching'])==6
    for row in out['all_six_quark_matching']:
        assert abs(row['matching_residual'])<1e-10 and row['wavefunction']>.001
        assert abs(row['bare_mass_GeV']*(1+q.sqcd_delta(row['bare_mass_GeV'],row['kind'])['total'])-row['SM_mass_GeV'])<1e-10
    assert max(abs(q.residual(q.MATCH)))<1e-7
    assert max(abs(q.residual(q.prior.MATCH)))>1e-5
    assert q.units_control()['dimensionless_threshold_error']<1e-10


def test_independent_inverse_full_SQCD_EFT_match():
    sol=q.improved_running();logMS=np.log(q.prior.MS/q.p.MZ);t=q.MATCH[-1]-logMS;g,target=q.p.unpack(sol.sol(t));high=list(q.p.theta_matrices(q.MATCH)[:3]);high[0]*=np.linalg.svd(target[0],compute_uv=False)[0]/np.linalg.svd(high[0],compute_uv=False)[0];scale=np.linalg.svd(target[1],compute_uv=False)[0]/np.linalg.svd(high[1],compute_uv=False)[0];high[1]*=scale;high[2]*=scale
    down=solve_ivp(q.prior.mssm_beta,[t,0],q.p.pack(g,high),rtol=1e-10,atol=1e-13);g,ms=q.p.unpack(down.y[:,-1]);g=g.copy();g[0]/=np.sqrt(5/3);cb=1/np.sqrt(101);sb=10*cb;low=[]
    for kind,m,fac in zip(['u','d'],ms[:2],[sb,cb]):
        U,y,V=np.linalg.svd(m);bare=y*fac*246.22/np.sqrt(2);new=[z*(1+q.sqcd_delta(z,kind)['total']) for z in bare];low.append((U*(np.array(new)*np.sqrt(2)/246.22))@V)
    low.append(ms[2]*cb);back=solve_ivp(q.p.beta,[logMS,0],q.p.pack(g,low),rtol=1e-10,atol=1e-13);obs=q.p.shape_observables(q.p.unpack(back.y[:,-1])[1]);target=q.p.shape_observables(q.p.unpack(q.p.running().sol(0))[1]);assert max(abs(obs/target-1))<1e-6


def test_neutrino_local_fibre_is_fitted_but_not_one_prediction():
    out=q.neutrino_fibre();assert len(out['continuation'])==10
    for row in out['continuation']:
        obs,detail=q.neutrino(np.array(row['parameters']));assert max(abs(obs/q.prior.old.NEUTRINO_TARGET-1))<1e-7
        masses=detail['masses_eV'];assert abs(masses[2]**2-masses[0]**2-.002511)<1e-12
    assert np.ptp([r['J'] for r in out['continuation']])>.01
    assert np.ptp([r['masses_eV'][0] for r in out['continuation']])>.0003
    assert np.ptp([r['m_beta_beta_eV'] for r in out['continuation']])>2e-5
    assert 'not an excludedmodelbranch' in out['failed_coordinate_chart']['interpretation']


def test_heat_Hessian_against_full_realspace_operator():
    N=3;t=.12;eps=1e-4;a=2*np.pi/N;second=uniform=0.
    for trans in itertools.product(range(N),repeat=3):
        momentum=a*np.array(trans);second+=(h.full_sector_heat(N,momentum,t,eps)-2*h.full_sector_heat(N,momentum,t,0)+h.full_sector_heat(N,momentum,t,-eps))/eps**2
        ks=a*np.c_[np.arange(N),np.tile(trans,(N,1))];ev=np.linalg.eigvalsh(h.symbol(ks)/(h.M*a*a));uniform+=np.sum((4*t*t*ev*ev-4*t*ev)*np.exp(-t*ev))
    direct=(4*np.pi*t)**2/(2*np.pi)**4*(second-.5*uniform)/t;analytic=h.response(N,[t],symmetry_reduction=False)[0][0]
    assert abs(direct-analytic)<2e-6


def test_heat_inversion_pairing_independent_sweep():
    for beta in [4,0]:
        a=h.response(4,[.12],beta,True)[0][0];b=h.response(4,[.12],beta,False)[0][0];assert abs(a-b)<1e-11


def test_native_heat_converges_to_independent_continuum():
    out=certificate('w33_pass12029_native_heat_curvature.json');rows=out['geometric_response'];errors=np.array([z['continuum_errors'] for z in rows]);assert np.all(errors>0) and np.all(np.diff(errors,axis=0)<0)
    assert max(errors[-1])<.012
    ext=certificate('w33_pass12029_native_heat_extended.json');assert ext['geometric_response'][0]['N']==32
    assert np.all(np.array(ext['geometric_response'][0]['continuum_errors'])<errors[-1])
    assert max(out['fixed_capacity_N16'])<-.9


def test_form_factor_series_and_density_sign():
    out=h.formfactor_certificate();assert out['rows'][0]['exact_dimensionless_series']=='x**4/72 - 17*x**3/140 + x**2/2 + x'
    assert abs(h.local_form_factor(.001)-float(h.H[0,0]))<.002
    assert abs(h.local_form_factor(.001,0)+3*float(h.H[0,0]))<.002
    for t in [.08,.12]:assert abs(h.local_form_factor(t)-h.conti(t))<1e-8


def test_native_magnetic_words_and_flux():
    ratios,error=c.native_compile(6);assert error<1e-11 and np.max(abs(abs(ratios)-1))<1e-12
    for charge in [1,6]:
        S=c.magnetic(6,charge);plaquette=S[0]@S[1]@S[0].conj().T@S[1].conj().T
        assert np.linalg.norm(plaquette-np.exp(2j*np.pi*charge/36)*np.eye(36))<1e-10


def test_resolved_multi_patch_Chern_and_cubic_anomaly():
    out=certificate('w33_pass12030_native_determinant_torus.json');assert out['anomaly_sum_q3']==0
    for row in out['meshes'][1:]:
        for z in row['sectors']:
            assert abs(z['Chern']+z['charge'])<1e-10 and z['continuous_gap_bound']>0 and z['min_overlap']>.9
        assert abs(row['physical_toron_Chern_total'])<1e-10
    assert abs(out['meshes'][0]['physical_toron_Chern_total'])>1


def test_underresolved_integer_is_not_a_topology_certificate():
    bad=c.chern(6,6,12,True);assert bad['gap']>.4 and bad['maxplaquette']<np.pi and abs(bad['Chern']+2)<1e-10
    good=c.chern(6,6,24,True);assert abs(good['Chern']+6)<1e-10 and good['continuous_gap_bound']>.1
    # Both mesh answers are integers. Only the refined family is consistent.
    assert abs(bad['Chern']-good['Chern'])>3.9


def test_frozen_scope_boundaries():
    out=certificate('w33_pass12026_12033_theta_soft_threshold_connections.json');assert out['status']=='PASS'
    assert 'not complete MSSM thresholds' in out['pass12028']['scope'] and 'not a dynamically selected' in out['pass12026']['scope']
    topo=certificate('w33_pass12030_native_determinant_torus.json');assert 'not sufficient' in topo['scope']
