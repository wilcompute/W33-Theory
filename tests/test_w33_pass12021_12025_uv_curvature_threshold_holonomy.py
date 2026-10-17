"""Independent operator, vacuum, continuum, matching and loop controls."""
from pathlib import Path
import json,sys
import numpy as np
from scipy.integrate import solve_ivp
from scipy.linalg import expm
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'analysis'))
import w33_pass12021_12025_uv_curvature_threshold_holonomy as q


def test_mixed_resolvent_against_independent_inverse():
    m,a,l,r,E,F=q.mixed_data();S=np.block([[np.diag(l),np.diag(a)],[np.diag(a),np.diag(r)]]);EE=np.zeros((6,6),complex);FF=EE.copy();EE[:3,:3]=E;FF[3:,3:]=F
    for z in [-1.,-3.]:
        R=np.linalg.inv(z*np.eye(6)-S);actual=np.diag((R@EE@R@FF@R+R@FF@R@EE@R)[:3,3:]).imag;D=(z-l)*(z-r)-a*a
        expected=np.array([sum(a[j]*(E[i,j]*F[j,i]).imag/D[i]/D[j] for j in range(3)) for i in range(3)])
        assert np.max(abs(actual-expected))<1e-14


def test_loop_kernel_and_negative_CP_control():
    out=q.mixed_soft();assert abs(out['total_mixed_coefficient'])>1e-5;errors=[abs(x['error']) for x in out['finite_difference_controls']]
    assert all(3.8<errors[i]/errors[i+1]<4.2 for i in range(3))
    m,a,l,r,E,F=q.mixed_data();left=q.mixed_loop_response(.49,a,l,r,E,F);right=q.mixed_loop_response(.49,a,l,r,E.conj(),F.conj());assert max(abs(left+right))<1e-14
    assert out['linked_spurion_imaginary_pair_max']<1e-14


def test_renormalizable_parent_differential():
    A,B=q.old.flavour_home();home=[A,B,A@A,B@B];weights=np.array(q.old.flavour_potential()['weights']);target=q.old.invariants(A,B);rng=np.random.default_rng(22);ds=[]
    for _ in range(4):
        z=rng.normal(size=(3,3))+1j*rng.normal(size=(3,3));ds.append((z+z.conj().T)/2)
    h=1e-5;fd=(q.parent_residual([a+h*b for a,b in zip(home,ds)],target,weights)-q.parent_residual([a-h*b for a,b in zip(home,ds)],target,weights))/(2*h)
    assert max(abs(fd-q.parent_differential(home,ds,weights)))<1e-8


def test_parent_full_hessian_and_relaxation():
    out=q.parent_vacuum();assert out['real_fields']==36 and out['constraint_rank']==28 and out['symmetry_zero_modes']==8
    assert min(out['normal_Hessian_eigenvalues'])>1e-10 and out['heavy_Hessian_min']>0
    ev=np.array(out['relaxed_light_Hessian_eigenvalues']);assert (ev>1e-10).sum()==10 and max(abs(ev[:8]))<1e-11


def test_vacuum_two_orientations_and_second_basis():
    A,B=q.old.flavour_home();_,U=np.linalg.eigh(A);_,V=np.linalg.eigh(B);Bsq=abs(U.conj().T@V)**2
    plus=q.unitary_from_moduli(Bsq);minus=q.unitary_from_moduli(Bsq,-1);assert np.linalg.norm(plus-minus.conj())<1e-10
    assert np.max(abs(abs(plus)**2-Bsq))<1e-10 and np.linalg.norm(plus@plus.conj().T-np.eye(3))<1e-10
    out=q.parent_vacuum();assert out['CP_partner_J'][0]*out['CP_partner_J'][1]<0
    W=expm(.2j*np.array([[1,.2j,.3],[-.2j,0,.1],[.3,.1,-1]]));fields=[A,B,A@A,B@B]
    assert np.max(abs(q.parent_invariants([W@z@W.conj().T for z in fields])-q.parent_invariants(fields)))<1e-10


def test_curved_recovery_second_order_and_density_control():
    out=q.curved_native();r=out['refinement'];errors=[abs(z['rayleigh_error']) for z in r];c=[abs(z['curvature_error']) for z in r]
    assert all(3.9<errors[i]/errors[i+1]<4.1 for i in range(4));assert all(3.9<c[i]/c[i+1]<4.1 for i in range(4))
    assert abs(out['fixed_capacity_rayleigh']-out['continuum_rayleigh'])>.01 and out['cell_relabelling_error']<1e-11


def test_three_mass_integral_exact_degeneracy_and_scaling():
    assert abs(q.three_mass_I(4.,4.,4.)-1/8)<1e-12
    a,b,c=6.25,4.84,4.;closed=(a*b*np.log(a/b)+b*c*np.log(b/c)+c*a*np.log(c/a))/((a-b)*(b-c)*(a-c))
    assert abs(q.three_mass_I(a,b,c)-closed)<1e-12
    assert abs(7*q.three_mass_I(7*a,7*b,7*c)-closed)<1e-12
    assert q.sqcd_threshold()>0 and abs(q.sqcd_threshold()+q.sqcd_threshold(-q.MU))<1e-14


def test_MSSM_third_family_beta_matches_known_limit():
    g=np.array([.46,.65,1.1]);yt,yb,ye=.8,.2,.1;mats=[np.diag([0.,0.,z]) for z in [yt,yb,ye]];dg,dm=q.p.unpack(q.mssm_beta(0,q.p.pack(g,mats)));g1,g2,g3=g
    target=[yt*(6*yt**2+yb**2-13*g1**2/15-3*g2**2-16*g3**2/3),yb*(6*yb**2+yt**2+ye**2-7*g1**2/15-3*g2**2-16*g3**2/3),ye*(4*ye**2+3*yb**2-9*g1**2/5-3*g2**2)]
    assert np.max(abs(np.array([m[2,2] for m in dm])*q.old.LOOP-target))<1e-14


def test_MSSM_gauge_running_and_threshold_refits():
    sol=q.matched_running();g0=q.p.unpack(sol.sol(0))[0];g1=q.p.unpack(sol.sol(3.))[0]
    assert np.max(abs(1/g1**2-(1/g0**2-2*np.array([33/5,1,-3])*3/q.old.LOOP)))<1e-9
    out=q.spectrum_matching();scales=[]
    for row in out['threshold_refits']:
        assert max(abs(q.matched_residual(np.array(row['parameters']),row['mu_GeV'])))<1e-6;scales.append(row['scale_GeV'])
    assert scales[0]>scales[1]>scales[2] and scales[0]/scales[2]>20


def test_independent_downward_MSSM_SM_match():
    high=list(q.p.theta_matrices(q.MATCH)[:3]);target=q.p.unpack(q.matched_running().sol(q.MATCH[-1]-np.log(q.MS/q.p.MZ)))[1]
    high[0]*=np.linalg.svd(target[0],compute_uv=False)[0]/np.linalg.svd(high[0],compute_uv=False)[0];common=np.linalg.svd(target[1],compute_uv=False)[0]/np.linalg.svd(high[1],compute_uv=False)[0];high[1]*=common;high[2]*=common
    up=q.matched_running();g=q.p.unpack(up.sol(q.MATCH[-1]-np.log(q.MS/q.p.MZ)))[0];back=solve_ivp(q.mssm_beta,[q.MATCH[-1]-np.log(q.MS/q.p.MZ),0],q.p.pack(g,high),rtol=1e-10,atol=1e-13)
    g,m=q.p.unpack(back.y[:,-1]);g=g.copy();g[0]/=np.sqrt(5/3);cb=1/np.sqrt(1+q.TANB**2);sb=q.TANB*cb;m=[m[0]*sb,m[1]*cb*(1+q.sqcd_threshold()),m[2]*cb]
    low=solve_ivp(q.p.beta,[np.log(q.MS/q.p.MZ),0],q.p.pack(g,m),rtol=1e-10,atol=1e-13)
    obs=q.p.shape_observables(q.p.unpack(low.y[:,-1])[1]);target=q.p.shape_observables(q.p.unpack(q.p.running().sol(0))[1]);assert max(abs(obs/target-1))<1e-6


def test_neutrinos_rematched_on_changed_inventory():
    out=q.spectrum_matching();obs=q.matched_neutrino(np.array(out['neutrino_parameters']));assert max(abs(obs/q.old.NEUTRINO_TARGET-1))<1e-7
    assert max(abs(q.matched_neutrino(q.old.NU_FIT)/q.old.NEUTRINO_TARGET-1))>.01


def test_native_projector_Frechet_derivative():
    patch=q.NativeChiralPatch();P,F,L,gap,overlap,dP=patch.evaluate(.02,-.03,.4,-.2);h=1e-5;fd=(patch.evaluate(.02+.4*h,-.03-.2*h)[0]-patch.evaluate(.02-.4*h,-.03+.2*h)[0])/(2*h)
    assert np.linalg.norm(fd-dP)<1e-8 and np.linalg.norm(P@dP@P)<1e-12
    assert gap>.5 and overlap>.2 and np.linalg.norm(F.conj().T@F-np.eye(30))<1e-11


def test_wedge_derivative_and_current_against_frame():
    patch=q.NativeChiralPatch();c=expm(.2*patch.A);dc=patch.B@c;h=1e-5
    fd=(q.p.wedge2(expm(h*patch.B)@c)-q.p.wedge2(expm(-h*patch.B)@c))/(2*h);assert np.linalg.norm(fd-patch.wedge_derivative(c,dc))<1e-9
    _,F,L,*_=patch.evaluate(.02,-.03,.4,-.2);dF=(patch.evaluate(.02+.4*h,-.03-.2*h)[1]-patch.evaluate(.02-.4*h,-.03+.2*h)[1])/(2*h)
    assert abs((1j*np.trace(F.conj().T@dF)).real-L)<1e-8


def test_closed_loop_holonomy_and_reversal():
    out=q.closed_measure();errors=[abs(z['phase_error']) for z in out['transport']];assert abs(out['connection_integral'])>1e-5
    assert all(3.8<errors[i]/errors[i+1]<4.2 for i in range(2));assert abs(out['reverse_phase']+out['transport'][1]['phase'])<1e-11
    assert max(z['unitarity_error'] for z in out['transport'])<1e-11 and max(z['projector_intertwining_error'] for z in out['transport'])<1e-11


def test_patch_frame_equivariance_and_scope():
    out=q.closed_measure();assert out['frame_gauge_equivariance_error']<1e-11 and abs(complex(*out['reference_representation_determinant_real_imag'])-1)<1e-11
    assert 'contractible' in out['scope'] and 'global native chiral measure remains open' in out['scope']
    frozen=json.loads((ROOT/'data/w33_pass12021_12025_uv_curvature_threshold_holonomy.json').read_text());assert frozen['status']=='PASS' and 'not a derivation' in frozen['pass12022']['scope'] and 'Omitted finite' in frozen['pass12024']['scope']
