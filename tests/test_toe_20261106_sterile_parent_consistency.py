"""Independent derivatives, inherited controls and continuous-window falsifiers."""
import importlib.util
import json
import math
import pathlib
from fractions import Fraction

import mpmath as mp
import pytest

ROOT = pathlib.Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('sterile_parent',ROOT/'analysis/toe_20261106_sterile_parent_consistency.py')
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)


@pytest.fixture(scope='module')
def packet():
    return mod.build()


def test_freezein_integrated_collision_term():
    with mp.workdps(40):
        integral = mp.quad(lambda t: 6/mp.cosh(t)**3,[0,1,3,10,mp.inf])
        assert abs(integral-3*mp.pi/2) < mp.mpf('1e-35')
        # Two daughters, MB collision term / entropy / Hubble expansion.
        M,mS,y = mp.mpf('0.000016'),mp.mpf('3000'),mp.mpf('1e-8')
        Gamma = y*y*mS/(16*mp.pi)
        expected = 2*45/(4*mp.pi**4)*integral/(mp.mpf('1.66')*mp.mpf('106.75')**mp.mpf('1.5'))*mp.mpf('1.22e19')*Gamma/mS**2*mp.mpf('2.744e8')*M
        assert math.isclose(float(expected),mod.omega_per_y_squared(float(M),float(mS))*float(y)**2,rel_tol=1e-14)


def test_valley_hessian_and_null_direction_numerically():
    with mp.workdps(40):
        b,v0,lam,p = map(mp.mpf,['.2','3','.7','.6'])
        v = lambda q: v0*mp.exp(-b*q)
        V = lambda q,s: lam*(s*s-v(q)**2)**2/4
        ss = v(p)
        H = mp.matrix([[mp.diff(lambda q: V(q,ss),p,2),mp.diff(lambda q:mp.diff(lambda s:V(q,s),ss),p)],
                       [mp.diff(lambda s:mp.diff(lambda q:V(q,s),p),ss),mp.diff(lambda s:V(p,s),ss,2)]])
        assert mp.norm(H*mp.matrix([1,-b*ss])) < mp.mpf('1e-35')
        assert abs(mp.det(H)) < mp.mpf('1e-35')
        assert abs(H[0,0]+H[1,1]-2*lam*ss**2*(1+(b*ss)**2)) < mp.mpf('1e-35')


def test_majorana_curvature_and_scale_control():
    with mp.workdps(50):
        b,m = mp.mpf('.053'),mp.mpf('16000')
        for a in [mp.mpf(0),mp.mpf('-.25'),mp.mpf('.5')]:
            def V(x):
                z=m*m*mp.exp(-2*b*x)
                return -z*z*(mp.log(z/(m*m))-2*a-mp.mpf('1.5'))/(32*mp.pi**2)
            actual=mp.diff(V,0,2)
            expect=b*b*m**4/(4*mp.pi**2)*(1+4*a)
            assert abs(actual-expect)/m**4 < mp.mpf('1e-45')


def test_continuous_portal_boundary_and_fifteenth_power():
    for mass in [7.1,13.1,16,19.7,30]:
        row=mod.portal_boundary(mass)
        assert math.isclose(row['portal_floor'],row['portal_clock_cap'],rel_tol=2e-14)
        doubled=mod.portal_boundary(2*mass)
        assert math.isclose(doubled['m_S_GeV']/row['m_S_GeV'],2**6,rel_tol=2e-14)
        assert math.isclose(doubled['lambda_S']/row['lambda_S'],2**15,rel_tol=2e-14)


def test_declared_cuts_have_no_larger_mass_solution(packet):
    for cut in packet['supplied_perturbativity_cuts']:
        m=cut['maximum_M_keV']
        row=mod.portal_boundary(m)
        assert math.isclose(row['lambda_S'],cut['lambda_S_cut_input'],rel_tol=2e-14)
        assert mod.portal_boundary(m*1.001)['lambda_S'] > cut['lambda_S_cut_input']
        assert mod.parent_point(m*1.001,row['m_S_GeV'])['portal_open'] is False


def test_incoming_grid_and_reliability_scope(packet):
    rows=packet['incoming_open_points_under_parent_hypothesis']
    assert [(r['M_keV'],r['m_S_GeV']) for r in rows] == [(16,3000),(16,10000),(18,10000),(20,10000)]
    assert all(r['portal_open'] for r in rows)
    assert rows[0]['lambda_S'] > 9
    assert all(r['beta_lambda_over_lambda'] > 1 for r in rows)
    assert all(not r['one_loop_fractional_beta_below_one'] for r in rows)
    for r in rows:
        w=r['canonical_real_scalar_vev_GeV']
        assert math.isclose(r['y']*w,r['M_keV']*1e-6,rel_tol=1e-14)
        assert math.isclose(2*r['lambda_S']*w*w,r['m_S_GeV']**2,rel_tol=1e-14)


def test_majorana_half_of_prior_dirac_and_soft_is_mass_parameter(packet):
    for row in packet['Majorana_benchmarks']:
        m=row['M_keV']*1000
        assert math.isclose(row['physical_small_soft_partner_splitting_eV'],row['soft_mass_parameter_cap_eV']**2/(2*m),rel_tol=1e-14)
        assert row['Majorana_CW_curvature_over_H0_squared'] > 1e21
    # DOF halving is exact at fixed inputs; old fits themselves differ.
    old_dirac=4*mod.B**2*(16000)**4/(8*math.pi**2*mod.MPL**2*mod.H0**2)
    current=next(r for r in packet['Majorana_benchmarks'] if r['M_keV']==16)
    assert math.isclose(old_dirac,2*current['Majorana_CW_curvature_over_H0_squared'],rel_tol=1e-14)


def test_history_is_real_input_and_survives_three_today_subtractions(packet):
    rows=[r for r in packet['actual_line_history_subtracted_benchmarks'] if r['z']==.5]
    assert len(rows)==4
    assert all(r['residual_over_reference_rho_DE_by_mass_keV']['16'] > 1e15 for r in rows)
    assert len({r['log_mass_ratio'] for r in rows})==4
    assert packet['input_raw_sha256']


def test_actual_server_execution_against_pc(packet):
    server=json.loads((ROOT/'data/toe_20261106_sterile_parent_server.json').read_text())
    assert server['status'].startswith('PASS_SERVER_')
    for ours,theirs in zip(packet['incoming_open_points_under_parent_hypothesis'],server['incoming_points']):
        assert (ours['M_keV'],ours['m_S_GeV'])==(theirs['M_keV'],theirs['m_S_GeV'])
        assert math.isclose(ours['lambda_S'],theirs['lambda_S'],rel_tol=1e-12)
    for ours,theirs in zip(packet['supplied_perturbativity_cuts'],server['cut_maxima']):
        assert math.isclose(ours['maximum_M_keV'],theirs['maximum_M_keV'],rel_tol=1e-12)
    a,b=server['same_mean_ballistic_counterexample']
    assert math.isclose(a['mean_momentum'],b['mean_momentum'],rel_tol=1e-14)
    assert abs(a['ballistic_density_kernel_at_k_tau_pi'])<1e-14
    assert b['ballistic_density_kernel_at_k_tau_pi']>.88
    a,b=server['same_mean_and_rms_ballistic_counterexample']
    assert math.isclose(a['mean_momentum'],b['mean_momentum'],rel_tol=1e-14)
    assert math.isclose(a['mean_squared_momentum'],b['mean_squared_momentum'],rel_tol=1e-14)
    assert abs(a['ballistic_density_kernel_at_k_tau_pi']-b['ballistic_density_kernel_at_k_tau_pi'])>.12


def test_published_star_anomalies_by_independent_integer_enumeration():
    d=json.loads((ROOT/'data/toe_20261106_published_star_axion_server.json').read_text())
    fields=d['field_blocks_q4_equals_6Y']
    for i in range(4):
        assert sum(f['n']*f['q'][i] for f in fields)==0
        for j in range(4):
            for k in range(4):
                assert sum(f['n']*f['q'][i]*f['q'][j]*f['q'][k] for f in fields)==0
    assert sum(p[0] for p in d['table2_pairs'])==52
    assert sum(p[0]*p[1]**2 for p in d['table2_pairs'])==12
    assert all(all(v==0 for v in row['residual']) for row in d['allowed_spectator_mass_checks'])


def test_published_star_matrix_exact_rational_reconstruction():
    d=json.loads((ROOT/'data/toe_20261106_published_star_axion_server.json').read_text())
    B=[[Fraction(0) for _ in range(4)] for _ in range(4)]
    for f in d['field_blocks_q4_equals_6Y']:
        q=list(map(Fraction,f['q']));q[3]/=6
        for i in range(4):
            for j in range(4):
                B[i][j]+=Fraction(2,3)*f['n']*q[i]*q[j]
    for f in d['scalar_blocks_physical_Y']:
        q=[Fraction(str(x)) for x in f['q']]
        for i in range(4):
            for j in range(4):
                B[i][j]+=Fraction(1,3)*f['n']*q[i]*q[j]
    assert B[3][3]==Fraction(247,9)
    for i in range(4):
        for j in range(4):
            assert math.isclose(float(B[i][j]),d['B_full_at_common_threshold'][i][j],rel_tol=2e-14)


def test_published_star_kinetic_eigenvalues_and_boundary():
    import numpy as np
    d=json.loads((ROOT/'data/toe_20261106_published_star_axion_server.json').read_text())
    B=np.array(d['B_full_at_common_threshold'])
    t=math.log(2.435e18/1e12)/(8*math.pi**2)
    for r in d['illustrative_running']:
        K=np.diag([1/r['g_hidden_input']**2]*3+[1/.4**2])-t*B
        assert bool(np.linalg.eigvalsh(K).min()>0)==r['positive_kinetic']['positive']
    g=d['benchmark']['common_hidden_coupling_upper_positive_K']
    for scale in [.999,1.001]:
        K=np.diag([1/(g*scale)**2]*3+[1/.4**2])-t*B
        assert bool(np.linalg.eigvalsh(K).min()>0)==(scale<1)
