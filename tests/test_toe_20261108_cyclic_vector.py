"""Action-map, independent spin trace, thermal integral and energy controls."""
import sys
from pathlib import Path
import json
import math
import numpy as np
import mpmath as mp
import pytest
from scipy.integrate import quad

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'analysis'))
import toe_20261108_cyclic_action_quality as aq
import toe_20261108_cyclic_conversion_moments as cv


def test_regular24_orbit_and_scalar_operator_inventory():
    o=aq.orbit24();assert len({tuple(x)for x in o['orbit']})==24
    d=aq.scalar_monomials()
    assert d['first_degree']==24
    assert {(r['degree'],r['charge_difference'])for r in d['phase_breaking']}=={(24,24),(24,-24),(26,24),(26,-24),(28,24),(28,-24)}
    assert aq.field_inventory()['anomalies']['sum_q']==0
    assert aq.field_inventory()['anomalies']['sum_q_cubed']==0
    assert aq.field_inventory()['anomalies']['classical_shift_U1D_squared_coefficient_LH_convention']==24


def test_action_cyclic_mass_covariance_and_extra_flavor_rule():
    N=24;w=np.exp(2j*np.pi/N);phi=.37+.14j;y=.1;M=2.
    c=np.array([M+y*w**k*phi for k in range(N)])
    transformed=np.array([M+y*w**k*(w*phi)for k in range(N)])
    assert np.roll(transformed,1)==pytest.approx(c,abs=2e-15)
    # Cyclic symmetry permits an off-diagonal circulant mass: its absence is
    # an additional U1_k assumption, not a claimed Z24 selection rule.
    shift=np.roll(np.eye(N),1,axis=0)
    assert shift.T@shift@shift==pytest.approx(shift)


def test_finite_affine_flavor_extension_and_its_extra_operators():
    d=aq.finite_flavor_extension();q=np.array(aq.orbit24()['orbit'])
    assert d['order']==17496 and d['representation_dimension']==24
    assert d['distinct_abelian_character_signatures']==729
    assert d['generator_covariance_max_residual']<1e-12
    assert d['offdiagonal_Dirac_bilinears_allowed_by_additive_subgroup']==[]
    assert d['Majorana_bilinears_allowed_by_additive_subgroup']==[]
    w=d['four_fermion_rearrangement_witness'];a,b=w['incoming'];c,e=w['outgoing']
    assert len({a,b,c,e})==4
    assert np.all((q[a]+q[b]-q[c]-q[e])%3==0)


def test_quality_derivative_and_excursion_necessary_condition():
    q=aq.quality_and_excursion();r=q['necessary_f_over_MP_on_small_eps_branch']
    assert q['rows'][2]['available_max_log_mass_ratio']==pytest.approx(.053*.3)
    assert aq.quality_log10(24,r)>101
    assert abs(aq.quality_log10(24,q['maximum_f_over_MP_for_unit_coefficient_degree24_quality']))<1e-10
    assert aq.quality_log10(129,r)>0 and aq.quality_log10(130,r)<0
    # Arbitrary precision direct differentiation of the declared operator.
    with mp.workdps(60):
        N=24;rr=mp.mpf('.15')
        amp=2*(rr/mp.sqrt(2))**N
        potential=lambda x:amp*mp.cos(N*x/rr)
        curvature=abs(mp.diff(potential,0,2))
        ratio=curvature*(mp.mpf(str(aq.MP))/mp.mpf(str(aq.H0)))**2
        assert float(mp.log10(ratio))==pytest.approx(aq.quality_log10(N,float(rr)),abs=2e-13)


@pytest.mark.parametrize('z',[.3,3.,100.,1e5,1e10])
def test_scaled_bessel_against_arbitrary_precision(z):
    with mp.workdps(40):
        for n in [1,2]:
            exact=mp.exp(mp.mpf(str(z)))*mp.besselk(n,mp.mpf(str(z)))
            assert float(cv.kve(n,np.array(z)))==pytest.approx(float(exact),rel=2e-13)


def test_heat_capacity_and_speed_from_independent_integrals():
    m=np.array([.97,1.03]);T=.07;h=T*1e-4
    E,C=cv.energies_and_capacity(m,T)
    plus=cv.energies_and_capacity(m,T+h)[0];minus=cv.energies_and_capacity(m,T-h)[0]
    assert (plus-minus)/(2*h)==pytest.approx(C,rel=2e-8)
    for mass,speed in zip(m,cv.mean_speed(m,T)):
        den=quad(lambda p:p*p*math.exp(-(math.hypot(p,mass)-mass)/T),0,5)[0]
        num=quad(lambda p:p**3/math.hypot(p,mass)*math.exp(-(math.hypot(p,mass)-mass)/T),0,5)[0]
        assert speed==pytest.approx(num/den,rel=1e-9)


def test_spin_averaged_vector_cross_section_from_dirac_traces():
    I=np.eye(2);O=np.zeros((2,2));sig=[np.array([[0,1],[1,0]]),np.array([[0,-1j],[1j,0]]),np.diag([1,-1])]
    gamma=[np.block([[I,O],[O,-I]])]+[np.block([[O,s],[-s,O]])for s in sig]
    metric=[1,-1,-1,-1];I4=np.eye(4)
    def slash(p):return sum(metric[a]*p[a]*gamma[a]for a in range(4))
    mi,mj,root=1.03,.97,2.5;s=root*root
    pi=math.sqrt(s/4-mi*mi);pf=math.sqrt(s/4-mj*mj)
    p1=np.array([root/2,0,0,pi]);p2=np.array([root/2,0,0,-pi])
    def msq(c):
        k1=np.array([root/2,pf*math.sqrt(1-c*c),0,pf*c]);k2=np.array([root/2,-k1[1],0,-k1[3]])
        total=0j
        for a in range(4):
            for b in range(4):
                L=np.trace((slash(p2)-mi*I4)@gamma[a]@(slash(p1)+mi*I4)@gamma[b])
                R=np.trace((slash(k1)+mj*I4)@(metric[a]*gamma[a])@(slash(k2)-mj*I4)@(metric[b]*gamma[b]))
                total+=L*R/4
        assert abs(total.imag)<1e-10
        return total.real
    integrated=quad(msq,-1,1)[0]*pf/pi/(32*math.pi*s)
    assert integrated==pytest.approx(cv.cross_section_contact(s,mi,mj),rel=1e-12)


@pytest.mark.parametrize('T',[.1,.03,.003])
def test_independent_server_simpson_thermal_integrals(T):
    server=json.loads((ROOT/'data/toe_20261108_cyclic_conversion_server.json').read_text())
    for r in server['rates']:
        if r['T']!=T:continue
        own=cv.downward_rates(np.array([r['mh']]),np.array([r['ml']]),T,192)[0]
        assert own==pytest.approx(r['refined_rate'],rel=8e-5)
        assert r['rate']==pytest.approx(r['refined_rate'],rel=1e-8)


@pytest.fixture(scope='module')
def rates():
    m=np.sqrt(1+cv.EPS**2+2*cv.EPS*np.cos(.37+2*np.pi*np.arange(24)/24))
    return cv.Rates(m,order=64,points=120)


def test_detailed_balance_number_conservation_and_entropy(rates):
    T=.033;m=rates.m;eq=cv.equilibrium(m,T)
    assert max(abs(rates.derivative(eq,T,1.)))<1e-8
    eta=np.random.default_rng(2408).uniform(.01,1,24);eta/=sum(eta)
    derivative=rates.derivative(eta,T,1.)
    assert abs(sum(derivative))<1e-16
    assert derivative@np.log(eta/eq)<0
    empty=np.zeros(24);empty[0]=1.
    d=rates.derivative(empty,T,1.)
    assert min(d[1:])>=0 and d[0]<=0


def test_zero_temperature_exothermic_rate_limit():
    mh,ml=1.03,.97;T=1e-8
    limit=(2*mh*mh+ml*ml)/(2*math.pi)*math.sqrt(1-ml*ml/(mh*mh))
    assert cv.downward_rates(np.array([mh]),np.array([ml]),T,128)[0]==pytest.approx(limit,rel=2e-6)


def test_closed_energy_and_heating_omission_control():
    data=json.loads((ROOT/'data/toe_20261108_cyclic_conversion_moments.json').read_text())
    for row in data['rows']:
        assert row['min_population']>-1e-10
        assert row['maximum_number_fraction_error']<1e-10
        assert row['minimum_heat_capacity']>1.49
        if row['heating']:assert row['maximum_first_law_absolute_residual']<1e-7
    on=next(r for r in data['rows']if r['strength']==100 and r['heating'])
    off=data['rows'][-1]
    assert off['maximum_first_law_absolute_residual']>.03
    assert on['final_temperature_over_M']>1000*off['final_temperature_over_M']
    assert on['final_response']['max_abs_beta_f_equals_MP']>.03


def test_independent_server_quality_and_orbit():
    d=json.loads((ROOT/'data/toe_20261108_cyclic_conversion_server.json').read_text());q=aq.quality_and_excursion()
    assert d['quality']['r_min']==pytest.approx(q['necessary_f_over_MP_on_small_eps_branch'])
    assert d['quality']['first_degree']==130
    assert d['quality']['log10_Q24']==pytest.approx(aq.quality_log10(24,d['quality']['r_min']))
    assert d['orbit']['orbit_length']==24
