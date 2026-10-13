"""Independent matching, canonical, chirality and soft-stationarity gates."""
from pathlib import Path
import json
import sys
import numpy as np
import mpmath as mp
from scipy.linalg import svdvals
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'analysis'))
import w33_pass11975_mediator_flavour_matching as flavour
import w33_pass11976_metric_lapse_bracket as metric
import w33_pass11977_native_overlap as overlap
import w33_pass11978_full_singlet_soft_vacuum as soft
from w33_pass11974_coupled_patch_matter import Patch


def cert(n):
    names={11975:'mediator_flavour_matching',11976:'metric_lapse_bracket',11977:'native_overlap',11978:'full_singlet_soft_vacuum',11979:'native_patch_decimation'}
    return json.loads((ROOT/'data'/f'w33_pass{n}_{names[n]}.json').read_text())


def test_mediator_elimination_and_rank_one_coefficient_relation():
    rng=np.random.default_rng(51975)
    for _ in range(10):
        M=rng.uniform(.5,2);g=rng.normal(size=2);current=rng.normal(size=2)+1j*rng.normal(size=2)
        source=g@current;chi=-source/M**2
        uv=M*M*abs(chi)**2+2*(chi.conjugate()*source).real
        assert abs(uv+abs(source)**2/M**2)<1e-12
        C=-np.outer(g,g)/M**2
        assert abs(np.linalg.det(C))<1e-12 and np.linalg.eigvalsh(C)[-1]<1e-12


def test_weyl_norm_identity_and_orientation_gradient_off_vacuum():
    rng=np.random.default_rng(61975);x=rng.normal(size=12)
    z=x[:3]+1j*x[3:6]
    assert abs(sum(abs(flavour.currents(z))**2)-np.linalg.norm(z)**4)<1e-10
    M=np.array([1,1.2,1.4,1.4]);gh=np.array([.3,.6,-.7,-.7]);gf=np.array([-.2,.4,.5,.5])
    _,gr=flavour.energy_gradient(x,M,gh,gf);direction=rng.normal(size=12)
    num=(flavour.energy_gradient(x+1e-5*direction,M,gh,gf)[0]-flavour.energy_gradient(x-1e-5*direction,M,gh,gf)[0])/2e-5
    assert abs(num-gr@direction)<1e-8


def test_full_mediator_orientation_results_and_unfitted_failure():
    d=cert(11975)
    assert sum(r['smallest_pair_gap_over_top']>1e-6 for r in d['finite_vacuum_checks'])==4
    for r in d['finite_vacuum_checks']:
        assert min(r['normal_Hessian'])>.05 and r['tangent_gradient']<1e-7
        assert abs(r['unfitted_weak_CP_trace'])<1e-15
        assert r['up_singular_values'][-1]/r['up_singular_values'][0]>.3
    # These samples are not a universal CP theorem for the mediator class.


def test_curved_metric_bracket_against_direct_canonical_derivatives():
    rng=np.random.default_rng(119760);n=5
    ds=[]
    for _ in range(3):
        d=rng.normal(size=(n,n));ds.append(d-d.T)
    a=rng.uniform(.8,2,n);N,M,q,p=rng.normal(size=(4,n))
    actual,target=metric.matrices(ds,a,N,M)
    KN=sum(d.T@np.diag(N*a)@d for d in ds);KM=sum(d.T@np.diag(M*a)@d for d in ds)
    lhs=(KN@q)@(M*p/a**3)-(N*p/a**3)@(KM@q)
    assert abs(lhs-p@actual@q)<1e-10 and np.linalg.norm(actual-target)>0


def test_native_exact_metric_obstruction_is_not_labeled_GR():
    import fractions
    d=cert(11976);w=d['exact_defect_witness']
    assert fractions.Fraction(w['coefficient'])==fractions.Fraction(-2452420000,366506427)
    assert d['max_curved_defect']>6
    assert 'Pi=0' in d['metric_potential_repair_gate'] and 'Not an all' in d['scope']


def test_native_overlap_GW_and_modified_chiral_projectors():
    D,Q,G5,ev,record=overlap.overlap([.012,-.015,.018],.013)
    assert record['GW_max']<1e-10
    hat=G5@(np.eye(320)-D)
    assert np.max(abs(hat@hat-np.eye(320)))<1e-10
    P=(np.eye(320)+hat)/2
    assert np.max(abs(P@P-P))<1e-10
    assert abs(-.5*sum(np.sign(ev))-record['index'])<1e-10


def test_origin_massless_spinors_and_static_pairing_with_new_phases():
    D,Q,G5,ev,r=overlap.overlap([0,0,0])
    assert sum(svdvals(D)<1e-9)==4
    phases=np.random.default_rng(21977).uniform(-.1,.1,160)
    _,Q,_,ev,r=overlap.overlap([.07,-.1,.12],phases=phases)
    gamma,g5=overlap.clifford();R=np.kron(1j*gamma[3]@g5,np.eye(80))
    assert np.max(abs(R@Q+Q@R))<1e-10 and r['index']==0


def test_domain_wall_sign_error_bound():
    rows=cert(11977)['finite_domain_wall']
    assert all(r['sign_error_max']<=r['gap_bound']+1e-14 for r in rows)
    assert all(rows[i+1]['GW_spectral_defect']<rows[i]['GW_spectral_defect'] for i in range(3))
    assert rows[-1]['sign_error_max']<6e-6


def test_full_soft_and_SUGRA_physical_modes_are_positive():
    d=cert(11978)
    assert d['total_positive_physical_real_modes']==26 and d['gauge_phase_zero_modes']==2
    assert min(d['core_masses_GeV'])>.58
    s=d['canonical_pinned_hidden_SUGRA']
    assert s['positive_physical_real_modes']==26 and s['gauge_zero_modes']==2
    assert min(s['masses_GeV'])>.58 and float(s['gradient_max'])<1e-85
    assert 1e9<abs(float(s['multiplier_VEV_GeV'][-1]))<1e10
    assert float(s['V_GeV_fourth'])>1e21 # observedCC has not been solved!
    assert float(s['auxiliary_phase_alignment_max'])<1e-80


def test_stored_full_SUGRA_root_stationary_in_independent_precision():
    mp.mp.dps=80;d=cert(11978);m=json.loads((ROOT/'data/w33_pass11973_mediation_transmission.json').read_text())
    mg=mp.mpf(str(m['gravity_scale_GeV']));Lambda=mp.mpf('1e16');g=mp.mpf('.1');rho=mp.mpf(1)/32
    dd=(2*rho+rho*rho)/12;f0=mp.sqrt((mp.sqrt(dd*dd+4)+dd)/2)*rho**12
    masses=[mp.mpf(str(x))**2/Lambda**2 for x in m['soft_masses_GeV']]
    matched=masses+[masses[4]]*3+[mp.mpf(0)]*2+[masses[4]]*2
    r=[mp.mpf(x) for x in d['canonical_pinned_hidden_SUGRA']['real_coordinates']]
    z=soft.sugra_home(r);point=tuple(mp.re(x) for x in z)+tuple(mp.im(x) for x in z)
    def V(*x):return soft.sugra_potential([x[i]+mp.j*x[i+14] for i in range(14)],matched,mg,Lambda,f0,g)
    for i in range(28):
        assert abs(mp.diff(V,point,tuple(int(k==i) for k in range(28))))<mp.mpf('1e-55')


def test_first_order_shielding_and_actual_Barr_soft_misalignment():
    d=cert(11978);s=d['canonical_pinned_hidden_SUGRA']
    assert mp.mpf(d['first_order_condensate_F_shielding_GeV_squared'])<mp.mpf('1e-65')
    assert mp.mpf(s['ST_auxiliary_ratio_spread_GeV'])<mp.mpf('1e-40')
    assert abs(mp.mpf(s['Barr_mixing_Im_B_A_dagger_GeV']))<mp.mpf('1e-42')
    # Independent algebra for the actual prior rational mixing row.
    r=np.array([1,2,1])/10;t=np.array([1,-1,2])/10;a,b=.17,.23
    B=r+1j*t;AB=a*r+1j*b*t
    assert abs(np.imag(B@AB.conj())-(a-b)/100)<1e-15


def test_native_theta_subdivision_and_exact_loop_Gram():
    c=Patch();bits=sum(1<<i for i in range(c.n) if c.background[i]);ext=np.zeros(c.n,int)
    C=np.array([c.flux(bits,l,ext) for l in ((1,0),(0,1))]);G=C@C.T
    small=np.array([[-1,1,0],[-1,0,1]])
    small[1]*=int(G[0,1]/4)
    assert np.array_equal(G,4*small@small.T)
    degrees=np.bincount(np.array(c.edges).ravel(),minlength=c.n)
    branch=np.flatnonzero(degrees==3)
    assert len(branch)==2 and c.background[branch[0]]==c.background[branch[1]]


def test_heavy_matter_decimation_controls():
    d=cert(11979);rows=d['heavy_matter_checks']
    assert d['path_lengths']==[4,4,4] and d['dimension']==11550
    assert abs(d['leading_virtual_hop_coefficient']-4.41)<1e-4
    assert all(rows[i+1]['error']<rows[i]['error']/1.9 for i in range(2))
    assert all(rows[i+1]['mean_internal_defects']<rows[i]['mean_internal_defects']/3 for i in range(2))
    assert all(r['residual']<1e-8 for r in rows)
