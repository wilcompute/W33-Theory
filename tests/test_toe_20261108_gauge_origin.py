"""Independent gauge quotient, operator sum, eigenmass and proper-time checks."""
import sys
from pathlib import Path
import itertools
import json
import math
import numpy as np
import mpmath as mp
import pytest

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'analysis'))
import toe_20261108_gauge_ring_quality as ring
import toe_20261108_wilson_line_mass_probe as wl


def test_phase_quotient_metric_from_constrained_kinetic_energy():
    F=np.array([.12,.2,.3,.4,.5]);psi=.71;N=len(F)
    K=np.zeros((N+1,N+1));K[:N,:N]=np.diag(F*F);K[N,:N]=K[:N,N]=1.
    right=np.r_[np.zeros(N),psi];theta=np.linalg.solve(K,right)[:N]
    f=1/math.sqrt(sum(F**-2))
    assert sum(theta)==pytest.approx(psi)
    assert .5*sum(F*F*theta*theta)==pytest.approx(.5*f*f*psi*psi)
    uniform=.2*np.ones(N);feff=1/math.sqrt(sum(uniform**-2))
    assert math.sqrt(N)*.2==pytest.approx(N*feff)


def test_integer_gauge_kernel_and_first_breaking_degree():
    N=5;B=ring.incidence(N)
    invariant=[z for z in itertools.product([-1,0,1],repeat=N)if np.all(B@z==0)]
    assert invariant==[(-1,)*N,(0,)*N,(1,)*N]
    assert np.linalg.matrix_rank(B)==N-1


@pytest.mark.parametrize('N',[5,24,110])
def test_actual_gauge_covariant_ring_singular_modes(N):
    r=ring.matrix_control(N)
    assert r['singular_spectrum_residual']<1e-12
    assert r['gauge_covariance_residual']<1e-12


def test_physical_ring_branch_coupling_from_diagonal_matrix_element():
    N=24;eps=.053;theta=.37;h=1e-5
    k=3;v=np.exp(2j*np.pi*k*np.arange(N)/N)/math.sqrt(N)
    # phi/f_mass=theta; psi=Ntheta, so all link phases theta.
    mass=lambda x:float(np.real(v.conj()@ring.mass_matrix(np.ones(N)*x,eps)@v))
    beta=-(math.log(mass(theta+h))-math.log(mass(theta-h)))/(2*h)
    exact=eps*math.sin(theta+2*math.pi*k/N)/(1+eps*math.cos(theta+2*math.pi*k/N))
    assert beta==pytest.approx(exact,rel=2e-8)


def test_scalar_tower_bound_from_differentiated_generating_potential():
    N=5;r=.03;nu=1.;q=ring.quality(N,r,nu);u=mp.mpf(str(q['u']));v=u**(mp.mpf(N)/2)
    with mp.workdps(60):
        potential=lambda psi:-2*mp.re(v*mp.exp(1j*psi)/(1-v*mp.exp(1j*psi)))/(1-u)**N
        derivative=mp.diff(potential,0,2)
        assert derivative>0
        logQ=mp.log10(derivative)+4*mp.log10(mp.mpf(str(ring.MP))*q['cutoff_over_MP'])-2*mp.log10(mp.mpf(str(ring.MP))*q['f_loop_over_MP']*mp.mpf(str(ring.H0)))
        assert float(logQ)==pytest.approx(q['all_scalar_bound_log10'],abs=3e-12)


def test_species_and_radial_dressing_are_material():
    nominal=ring.quality(110,1,0);species=ring.quality(850,1,1);smaller=ring.quality(300,.15,9)
    assert nominal['all_scalar_bound_log10']<-3
    assert species['leading_log10_curvature_over_H0_squared']<-7
    assert species['all_scalar_bound_log10']>248
    assert smaller['all_scalar_bound_log10']<-14
    assert ring.quality(300,1,4)['all_scalar_bound_log10']is None


@pytest.mark.parametrize('N',[5,6,12])
def test_conservative_cyclic_fermion_loop_bound(N):
    with mp.workdps(65):
        eps=mp.mpf('.1');pi=mp.pi
        def potential(theta):
            masses=[1+eps*mp.cos(theta+2*pi*k/N)for k in range(N)]
            return -mp.fsum(m**4*(2*mp.log(m)-mp.mpf('1.5'))for m in masses)/(16*pi*pi)
        c=mp.mpf(24)/mp.fprod(range(N-4,N+1))
        bound=N**3*c*eps**N/(8*pi*pi*(1-eps))
        for theta in [mp.mpf(0),mp.mpf('.37'),mp.mpf('.8')]:
            assert abs(mp.diff(potential,theta,2))<bound


def test_complementary_mediators_admit_a_bilinear():
    B=ring.incidence(24);x=B[:,:12].sum(axis=1);y=B[:,12:].sum(axis=1)
    assert np.any(x!=0)and np.all(x+y==0)


@pytest.mark.parametrize('a',[.1,1.,12.])
def test_full_KK_curvature_against_polylogarithm_sum(a):
    with mp.workdps(65):
        R=mp.mpf(str(a))/wl.M;x=2*mp.pi*a;z=mp.exp(-x);f=mp.mpf('.01')*mp.mpf(str(wl.MP));H=mp.mpf(str(wl.H0))
        series=mp.polylog(3,z)+x*mp.polylog(2,z)+x*x/3*mp.polylog(1,z)
        exact=3/(16*mp.pi**6*R**4*f*f*H*H)*series
        assert wl.curvature_log10(a)==pytest.approx(float(mp.log10(exact)),abs=2e-12)


def test_KK_mass_is_a_physical_Dirac_singular_mass_and_coupling():
    b=wl.benchmark();x=b['branch']['initial_x'];R=b['R_eV_minus1'];f=b['f_eV']
    matrix=wl.M*np.eye(4)+1j*x/R*np.diag([1,1,-1,-1])
    assert np.linalg.svd(matrix,compute_uv=False)==pytest.approx(np.ones(4)*b['branch']['initial_mass_eV'])
    h=1e-5
    mass=lambda delta:math.sqrt(wl.M**2+((x+delta/(2*math.pi*.01))/R)**2)
    beta=-(math.log(mass(h))-math.log(mass(-h)))/(2*h)
    assert beta==pytest.approx(.053,rel=2e-8)
    assert wl.benchmark(bulk_fields=2)['log10_loop_curvature_over_H0_squared']-wl.benchmark(bulk_fields=1)['log10_loop_curvature_over_H0_squared']==pytest.approx(math.log10(2))
    with mp.workdps(50):
        aa=mp.mpf(12);xx=mp.mpf(str(x));C=1/(2*mp.pi*mp.mpf('.01'))
        physical=lambda d:mp.sqrt(1+(xx+C*d)**2/aa**2)
        induced=3*mp.mpf('.26')*mp.diff(physical,0,2)/physical(0)
        assert float(induced)==pytest.approx(b['fixed_population_density_curvature_control']['curvature_over_H0_squared'],rel=1e-14)


def test_large_gauge_relabeling_and_ground_band_limit():
    a=12.;theta=.37;R=a/wl.M
    mass=lambda n,t:math.sqrt(wl.M**2+(n+t/(2*math.pi))**2/R**2)
    for n in range(-5,6):assert mass(n,theta+2*math.pi)==pytest.approx(mass(n+1,theta))
    lo=min(mass(n,0)for n in range(-2,3));hi=min(mass(n,math.pi)for n in range(-2,3))
    assert math.log(hi/lo)==pytest.approx(.5*math.log1p(1/(4*a*a)))
    assert math.log(hi/lo)<.001
    assert wl.branch(12.)['fixed_branch_excursions'][-1]['beta']<0


def test_primary_worldline_integrals_and_independent_server():
    data=json.loads((ROOT/'data/toe_20261108_wilson_line_mass_probe.json').read_text())
    server=json.loads((ROOT/'data/toe_20261108_gauge_origin_server.json').read_text())
    for local,other in zip(data['proper_time_controls'],server['worldline']):
        assert abs(local['relative_integral_residual'])<1e-12
        assert other['positive_integral']==pytest.approx(local['closed_harmonic'],rel=2e-12)
    for q in server['ring']:
        own=ring.quality(q['N'],q['r'],q['nu'])
        assert q['all']==pytest.approx(own['all_scalar_bound_log10'],abs=1e-12)
    for q in server['generating']:assert q['truncated']==pytest.approx(q['closed'],rel=2e-14)


def test_conditional_window_and_charged_contamination():
    data=json.loads((ROOT/'data/toe_20261108_wilson_line_mass_probe.json').read_text())
    assert data['conditional_window']['window_exists']
    assert 10<data['conditional_window']['first_a_with_loop_envelope_below_target']<12
    assert data['benchmark']['log10_loop_curvature_over_H0_squared']<-5
    assert data['charged_contamination'][1]['log10_curvature_over_H0_squared']>21
