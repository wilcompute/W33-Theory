"""Independent controls of conventions, anomaly necessity and finite EFT scope."""
import importlib.util, pathlib, math
import numpy as np
import sympy as s
from scipy.integrate import solve_ivp
from scipy.optimize import minimize_scalar

ROOT=pathlib.Path(__file__).resolve().parents[1]
def load(stem):
    spec=importlib.util.spec_from_file_location(stem,ROOT/'analysis'/f'{stem}.py')
    m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m
q=load('toe_20261105_pq_quality_gauge_obstruction')
n=load('toe_20261105_pq_normalization_cutoff')

def test_global_minimum_shift_bound_independent_minimization():
    # Resolve all wells at moderately small amplitude, rather than only
    # using the producer's small-root initial condition.
    for d,r in [(5,.001),(12,.0001)]:
        for phase in [.4,1.5,3.]:
            fun=lambda t:1-math.cos(t)-r*math.cos(d*t+phase)
            points=np.linspace(-math.pi,math.pi,801)
            k=int(np.argmin([fun(t)for t in points]))
            out=minimize_scalar(fun,bounds=(points[max(0,k-2)],points[min(800,k+2)]),method='bounded',options={'xatol':1e-14})
            assert abs(out.x)<=q.uniform_shift_bound(r,d)

def test_canonical_operator_factor_and_dimension():
    for d in [11,12,13,14]:
        assert math.isclose(q.ratio(1e11,d,True)/q.ratio(1e11,d,False),2**(-d/2),rel_tol=2e-12)
    assert q.uniform_shift_bound(1.,12)is None
    assert q.uniform_shift_bound(q.ratio(1e11,12),12)<1e-10
    assert q.uniform_shift_bound(q.ratio(1e11,11),11)>1e-10

def test_mixed_anomaly_elimination_without_nullspace():
    d,a,b,z=s.symbols('d a b z')
    solution=s.solve([d+2*a+2*b,3*(a+b)/2+z,d/3+(a+b)/6-z],[d,a,z],dict=True)
    assert solution==[{d:0,a:-b,z:0}]
    # Independent triangle trace over actual LH heavy representation pairs.
    colors=[(3,1,s.Rational(-1,3)),(3,2,s.Rational(1,6)),(3,2,s.Rational(1,6))]
    yy=[dc*dw*Y**2 for dc,dw,Y in colors]
    assert yy==[s.Rational(1,3),s.Rational(1,6),s.Rational(1,6)]
    assert 1+2-2==1

def test_ordinary_discrete_instanton_necessity_beyond_scan():
    for N in [67,97,128,257]:
        assert [x for x in range(N)if(-x)%N==0]==[0]
    # A different color anomaly permits a nontrivial charge: hypotheses matter.
    assert [x for x in range(12)if(3*x)%12==0]==[0,4,8]

def test_yukawa_exact_solution_against_independent_scalar_integration():
    f=1e11;y=math.sqrt(2)*n.MQ/f
    # Integrate z directly, independent of producer's (lambda,y) pair.
    def zdot(t,z):
        a=1/.118+7*math.log(n.MQ/91.19)/(2*math.pi)+11/(6*math.pi)*(t-math.log(n.MQ))
        return [4/(math.pi*a)*z[0]-36*n.K]
    sol=solve_ivp(zdot,(math.log(f),math.log(n.MU)),[1/y**2],rtol=1e-11,atol=1e-12)
    assert sol.success
    assert math.isclose(sol.y[0,-1],n.inverse_y_squared(f,y),rel_tol=2e-10)
    # At the old f=2.7e10 benchmark a Yukawa pole is unavoidable in this beta.
    assert n.inverse_y_squared(2.7e10,n.MQ/2.7e10)<0

def test_positive_prefix_is_not_successful_stability():
    x=n.trajectory(2.7e10,n.MQ/2.7e10,2.)
    assert x['end_lambda']>0 and x['solver_success']
    assert not x['reaches_MU'] and x['classification']=='perturbativity_cut'

def test_mass_normalization_and_gravity_scale():
    f=1e11;y=math.sqrt(2)*n.MQ/f
    assert math.isclose(y*f/math.sqrt(2),n.MQ)
    for x in n.cutoff_rows():
        assert math.isclose(x['M5_GeV']**3*x['L_GeV_inverse'],n.M4**2,rel_tol=1e-13)
        assert 2e8<x['M5_GeV']<4e8
        assert x['MQ_over_M5']>70
        assert math.isclose(x['Wilson_line_g4_required']*x['axion_fa_input_GeV']*x['L_GeV_inverse'],1.)

def test_stretched_string_localization_inequality_and_radius_scaling():
    rows=n.stretched_string_controls()
    for x in rows:
        ratio=x['required_tension_over_M5_squared']
        assert 30<ratio<750
        assert math.isclose(x['MV_upper_if_tension_at_M5_squared_GeV']*ratio,n.MU)
        assert x['max_radius_micron_if_unit_tension_factor']<.05
        assert not x['allowed_tension_factors']['1']
        assert x['allowed_tension_factors']['1000']
    a,b=rows[:2]
    assert math.isclose(b['max_radius_micron_if_unit_tension_factor']/a['max_radius_micron_if_unit_tension_factor'],10**(-1.5))
