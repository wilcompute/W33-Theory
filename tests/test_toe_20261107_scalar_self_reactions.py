"""Independent tree enumeration, Lorentz symmetry and reaction normalization."""
import importlib.util
import itertools
import json
import math
from pathlib import Path
import numpy as np
from scipy.special import kv

R=Path(__file__).resolve().parents[1]
s=importlib.util.spec_from_file_location('self_collision',R/'analysis/toe_20261107_scalar_self_reactions.py')
p=importlib.util.module_from_spec(s);s.loader.exec_module(p)


def recursive_amplitude(legs,g3,g4):
    # Root the tree at external leg4; enumerate unordered partitions of the
    # other labels, not pairs of propagators as in the production code.
    def partitions(labels,k):
        out=[]
        for assignment in itertools.product(range(k),repeat=len(labels)):
            if set(assignment)!=set(range(k)):continue
            blocks=tuple(tuple(labels[i] for i,a in enumerate(assignment) if a==b) for b in range(k))
            if list(blocks)==sorted(blocks):out.append(blocks)
        return out
    cache={}
    def numerator(labels):
        return sum(g*math.prod(current(block) for block in blocks)
                   for k,g in [(2,g3),(3,g4)] for blocks in partitions(labels,k))
    def current(labels):
        if len(labels)==1:return 1.
        if labels not in cache:
            cache[labels]=numerator(labels)/(p.minkowski(legs[list(labels)].sum(axis=0))-1)
        return cache[labels]
    return numerator((0,1,2,3))


def test_all25_diagrams_and_generic_threshold_against_published_formula():
    assert len(p.PAIRS)==10 and len(p.DOUBLE_PAIRS)==15
    legs,beta=p.kinematics(np.zeros((1,3)),np.tile([0.,0.,1.],(1,3,1)),np.array([[0.,0.,1.]]))
    for g3,g4 in [(1.3,.7),(2.,3.),(.5,.02)]:
        expected=-5*g3*(3*g4-g3*g3)/8
        assert math.isclose(p.amplitude(legs,g3,g4)[0],expected,rel_tol=1e-13)
        # All-identical initial/final symmetry factors reproduce2212.09759(2.5).
        rate=beta[0]*expected**2/(math.factorial(2)*math.factorial(3)*64*math.pi)
        published=25*math.sqrt(5)*g3*g3*(3*g4-g3*g3)**2/(math.factorial(2)*math.factorial(3)*12288*math.pi)
        assert math.isclose(rate,published,rel_tol=1e-13)


def test_recursive_rooted_tree_matches_pair_enumeration():
    legs,_=p.sample(1.,5,17)
    for event in legs[:8]:
        assert math.isclose(p.amplitude(event,1.3,.7),recursive_amplitude(event,1.3,.7),rel_tol=1e-11,abs_tol=1e-12)


def test_kinematics_energy_shells_and_lorentz_invariance():
    legs,_=p.sample(.7,6,11)
    assert np.max(abs(legs.sum(axis=1)))<2e-12
    assert np.max(abs(p.minkowski(legs)-1))<2e-11
    velocity=np.broadcast_to([.2,-.1,.3],legs.shape[:-1]+(3,))
    boosted=p.boost(legs,velocity)
    assert np.allclose(p.amplitude(boosted,1.1,.4),p.amplitude(legs,1.1,.4),rtol=1e-10,atol=1e-11)
    assert np.allclose(p.amplitude(legs[:,[4,1,3,0,2]],1.1,.4),p.amplitude(legs,1.1,.4),rtol=1e-12,atol=1e-12)


def test_broken_Z2_threshold_zero_but_finite_momentum_nonzero():
    fixed=np.tile([0.,0.,1.],(1,3,1));final=np.array([[1.,0.,0.]])
    a0,_=p.kinematics(np.zeros((1,3)),fixed,final)
    assert abs(p.amplitude(a0,math.sqrt(18*.1),.6)[0])<1e-14
    momenta=np.array([[.2,.3,.4]])
    legs,_=p.kinematics(momenta,fixed,final)
    assert abs(p.amplitude(legs,math.sqrt(18*.1),.6)[0])>1e-5


def test_pointwise_detailed_balance_and_fugacity_direction():
    legs,beta=p.sample(1.,9,31)
    for z in [.1,1.,2.]:
        f,b=p.collision_average(legs,beta,1.,.1,lambda q:np.full_like(q,z))
        assert math.isclose(f/b,z,rel_tol=1e-14)
        assert (b-f)*(1-z)>=0
    assert np.max(abs(legs[:,:3,0].sum(axis=1)+legs[:,3:,0].sum(axis=1)))<1e-12


def test_scalar_rate_homogeneity_at_fixed_distribution():
    legs,beta=p.sample(2.,8,41);ratio=lambda q:np.exp(-.1*q)
    f1,b1=p.collision_average(legs,beta,2.,.03,ratio)
    f2,b2=p.collision_average(legs,beta,2.,.09,ratio)
    assert math.isclose(f2/f1,27,rel_tol=1e-12)
    assert math.isclose(b2/b1,27,rel_tol=1e-12)


def test_MB_inverse_CDF_normalization_and_energy_moment():
    # Stratified one-dimensional samples avoid testing a stochastic coincidence.
    u=(np.arange(100000)+.5)/100000
    for r in [.3,1.,6.]:
        q=p.proposal(r,u)
        expected=3+r*kv(1,r)/kv(2,r)
        assert math.isclose(np.hypot(q,r).mean(),expected,rel_tol=2e-5)


def test_elastic_Htheorem_equilibrium_and_nonequilibrium():
    legs,beta=p.elastic_sample(1.,10,53)
    assert np.max(abs(legs.sum(axis=1)))<1e-12
    assert np.max(abs(p.minkowski(legs)-1))<1e-10
    for z in [.1,1.,2.]:
        _,entropy=p.elastic_average(legs,beta,1.,.1,lambda q:np.full_like(q,z))
        assert abs(entropy)<1e-25
    # Any temperature and chemical potential give an elastic equilibrium.
    _,thermal=p.elastic_average(legs,beta,1.,.1,lambda q:.2*np.exp(-.3*np.hypot(q,1.)))
    assert thermal<1e-25
    # A curved energy dependence is not a kinetic equilibrium.
    events,entropy=p.elastic_average(legs,beta,1.,.1,lambda q:.2*np.exp(-.07*q*q))
    assert events>0 and entropy>0


def test_frozen_server_integration_and_minimal_potential_consistency():
    pc=json.loads((R/'data/toe_20261107_scalar_self_reactions.json').read_text())
    server=json.loads((R/'data/toe_20261107_scalar_self_server.json').read_text())
    for row in server['rows']:
        ours=next(x for x in pc['rows'] if x['M_keV']==row['M_keV'] and x['r']==1.)
        for field in ['gamma32_over_nS_H','gamma23_over_nS_H']:
            assert math.isclose(ours[field],row[field],rel_tol=.03)
    r1={x['M_keV']:x for x in pc['rows'] if x['r']==1.}
    assert r1[16.]['net_number_gain_over_nS_H']>1e6
    assert r1[30.]['net_number_gain_over_nS_H']>1e3
    assert r1[100.]['gamma23_over_nS_H']<.1
    assert r1[100.]['elastic_entropy_production_over_nS_H']>10
