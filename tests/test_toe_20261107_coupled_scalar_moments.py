"""Independent thermodynamics, detailed balance and energy-transfer controls."""
import importlib.util
import math
import json
from pathlib import Path
import numpy as np
from scipy.special import kve

R=Path(__file__).resolve().parents[1]
s=importlib.util.spec_from_file_location('coupled',R/'analysis/toe_20261107_coupled_scalar_moments.py')
m=importlib.util.module_from_spec(s);s.loader.exec_module(m)


def test_thermodynamic_inverse_and_heat_capacity():
    rates=m.ThermalRates()
    for t in np.geomspace(1e-4,1000,50):
        assert math.isclose(rates.temperature(m.thermal_energy(t)),t,rel_tol=3e-6)
        eps=t*1e-4
        numeric=(m.thermal_energy(t+eps)-m.thermal_energy(t-eps))/(2*eps)
        assert math.isclose(m.heat_capacity(t),numeric,rel_tol=2e-5)
    assert math.isclose(m.heat_capacity(1e-5),1.5,rel_tol=3e-5)
    assert math.isclose(m.heat_capacity(1000),3,rel_tol=1e-6)


def test_annihilation_bound_and_nonrelativistic_limits():
    rates=m.ThermalRates()
    for t in np.geomspace(.0001,1000,30):
        contact=(kve(1,1/t)/kve(2,1/t))**2/(32*math.pi)
        assert 1-1e-5<rates.a22(t)/contact<4+1e-4
        assert rates.epair(t)>2
    assert math.isclose(rates.a22(1e-5),1/(8*math.pi),rel_tol=1e-4)
    assert math.isclose(rates.epair(1e-5),2,rel_tol=3e-5)
    # Independent n^2/2 <sigma*v>: sigma0=4.5lambdaS^2/(pi*m^2),
    # mean relative speed=4sqrt(Tdark/(pi*m)).
    assert math.isclose(rates.self_elastic(1e-5),9/math.pi**1.5*math.sqrt(1e-5),rel_tol=2e-4)


def test_full_elastic_number_conservation_and_detailed_balance():
    q,w=m.p.quadrature(64,50.)
    for r in [.1,1.,10.]:
        L=m.elastic_generator(q,w,r,.2,True,32)
        measure=w*q*q;eq=np.exp(-np.hypot(q,r))
        assert np.max(abs(measure@L))<1e-10
        assert np.max(abs(L@eq))<1e-13
        off=L-np.diag(np.diag(L));assert off.min()>-1e-13
        base=m.p.Kernel(q,w,.2,0.,0.).components(r)[3]
        assert np.allclose(m.elastic_generator(q,w,r,.2,False),base,rtol=1e-13,atol=1e-13)


def test_heavy_bath_scattering_self_exchange_factor_four():
    # At soft momentum transfer, 1+3/(t/m^2-1) -> -2.
    q,w=m.p.quadrature(64,40.);r=1e5
    full=m.elastic_generator(q,w,r,.3,True,48)
    contact=m.elastic_generator(q,w,r,.3,False)
    assert math.isclose(full[0,1]/contact[0,1],4,rel_tol=1e-5)


def test_scalar_sterile_decay_energy_and_chemical_energy_conservation():
    rates=m.ThermalRates();a=m.p.inverse_decay_branch(30.)
    a.update(A=0.,lambda_portal=0.,DH=0.)
    model=m.Moments(a,rates,nq=32)
    r=2.;I=.1;t=.4;R=r*I*m.thermal_energy(t)
    derivative=model.rhs(math.log(r),[I,R,0.,0.,0.])
    J=model.closure(r,I,R)[3]
    assert math.isclose(derivative[1]+derivative[3],r*r*J,rel_tol=1e-12)
    none=m.Moments(a,rates,nq=32,chemical_scale=0.)
    control=none.rhs(math.log(r),[I,R,0.,0.,0.])
    assert derivative[1]==control[1] and derivative[0]!=control[0]
    assert derivative[2]>0 and derivative[4]>0


def test_all_collision_terms_equilibrate_at_same_temperature():
    rates=m.ThermalRates();a=m.p.inverse_decay_branch(30.);a['DN']=0.
    model=m.Moments(a,rates,nq=64,nangle=32)
    for r in [.3,1.,3.]:
        I=r*r*m.kv(2,r);R=r*I*m.thermal_energy(1/r)
        d=model.pieces(r,I,R)
        for key in ['number_decay','energy_decay','chemical','number_ann','energy_ann','energy_elastic']:
            assert abs(d[key])<1e-6,key


def test_actual_server_rate_coefficients():
    rates=m.ThermalRates()
    server=json.loads((R/'data/toe_20261107_coupled_scalar_rate_server.json').read_text())
    for row in server['rows']:
        predicted=rates.k32(1/row['inverse_dark_temperature'])
        assert math.isclose(predicted,row['gamma32_over_n_eq_cubed_per_lambdaS_cubed'],rel_tol=.025)


def test_frozen_moment_number_budget_and_closure_limits():
    d=json.loads((R/'data/toe_20261107_coupled_scalar_moments.json').read_text())
    for row in d['rows']:
        assert abs(row['integrated_number_budget']['relative_balance_error'])<1e-5
        assert abs(row['closure_diagnostics']['daughter_number_integral_relative_error'])<1e-5
        assert row['closure_diagnostics']['rate_table_clipped_samples']==0
        assert row['minimum_sampled_scalar_I']>0
    first=d['rows'][0]['closure_diagnostics']
    assert first['max_classical_Hartree_restoration_ratio']>1
    assert first['fraction_N_produced_with_MB_occupation_above_point1']>.1
