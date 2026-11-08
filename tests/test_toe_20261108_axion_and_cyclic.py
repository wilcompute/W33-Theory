"""Independent derivative, canonical-basis and finite-group controls."""
import sys
from pathlib import Path
import json
import math
import numpy as np
import mpmath as mp
import pytest

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'analysis'))
import toe_20261108_axion_eigenmode_audit as ax
import toe_20261108_cyclic_partner_control as cy
import toe_20261108_native_cyclic_orders as gr


def test_rank_one_in_rotated_canonical_basis():
    f,F=.23,2.7
    R=np.array([[F,-f],[f,F]])/math.hypot(f,F)
    H=np.outer([1/f,1/F],[1/f,1/F])
    assert R.T@R==pytest.approx(np.eye(2),abs=1e-15)
    assert R.T@H@R==pytest.approx(np.diag([1/f**2+1/F**2,0]),abs=1e-13)
    assert ax.symbolic()['determinant']=='0'


@pytest.mark.parametrize('kappa',[1e-4,.1,1.,100.])
def test_relaxed_heavy_slope_against_finite_difference(kappa):
    u=.6;du=1e-5
    row=ax.pinning_row(kappa,u)
    hi=ax.pinning_row(kappa,u+du);lo=ax.pinning_row(kappa,u-du)
    derivative=(math.log(hi['heavy_mass_squared'])-math.log(lo['heavy_mass_squared']))/(2*du*row['F_over_MP'])
    canonical=derivative/math.sqrt(row['canonical_light_metric'])
    assert -.5*canonical==pytest.approx(row['beta_physical_along_canonical_trough'],rel=3e-4,abs=2e-11)
    assert abs(row['gradient_residual'])<1e-12


def test_pinning_changes_the_light_curvature():
    weak=ax.pinning_row(1e-6);strong=ax.pinning_row(1e6)
    assert weak['beta_physical_along_canonical_trough']<1e-11
    assert strong['beta_physical_along_canonical_trough']<1e-7
    assert strong['relaxed_light_curvature']>1e5*weak['relaxed_light_curvature']


def test_hellmann_feynman_and_positive_branch_bound():
    A=np.array([2.,3.,5.]);Q=np.array([[2.,0.],[0.,.7],[2.,-2.1]]);x=np.array([.1,.13])
    r=ax.spectrum_and_slope(A,Q,x);u=np.array(r['light_eigenvector']);h=1e-5
    eigen=lambda z:np.linalg.eigvalsh(ax.hessian_cosines(A,Q,z))[-1]
    slope=-(math.log(eigen(x+h*u))-math.log(eigen(x-h*u)))/(4*h)
    assert slope==pytest.approx(r['beta_along_light_eigenvector'],rel=1e-7)
    assert abs(slope)<=r['convex_cosine_bound']
    assert ax.convex_scan(128)['max_bound_ratio']<=1


def test_light_translation_does_not_change_heavy_dynamics():
    r=ax.single_cosine_dynamics()
    assert r['max_heavy_history_difference']<1e-10
    assert r['max_relative_energy_drift']<2e-9


def test_phenomenological_Fi_zero_is_discontinuous_control():
    r=ax.running_eft_control()
    assert r['positive_Fi_rows'][-1]['mass_ratio']==pytest.approx(r['continuous_Fi_zero_mass_ratio'],abs=1e-14)
    assert abs(r['continuous_Fi_zero_mass_ratio']-r['separately_switched_exponential_mass_ratio'])>1e-3
    assert r['positive_Fi_rows'][-1]['beta']==pytest.approx(r['continuous_Fi_zero_beta'],abs=1e-14)


@pytest.mark.parametrize('N',[3,9,18,21,27])
def test_high_precision_cw_against_differentiated_potential(N):
    eps=mp.mpf('.05314971931113116');theta=mp.mpf('.37')
    exact=cy.cw_second(N,eps,theta)
    derivative=mp.diff(lambda x:cy.cw_potential(N,eps,x),theta,2)
    assert abs(exact-derivative)<mp.mpf('1e-85')
    # Root-of-unity permutation invariance of the complete spectrum.
    assert abs(cy.cw_potential(N,eps,theta+2*mp.pi/N)-cy.cw_potential(N,eps,theta))<mp.mpf('1e-90')


def test_full_native_orders_and_projective_quotients():
    G,J=gr.enumerate_symplectic();sp=gr.orders(G)
    assert sum(sp.values())==51840 and max(map(int,sp))==18
    extension=gr.three_qutrit_order24(G,J)
    M=np.array(extension['matrix']);K=np.array(extension['symplectic_form'])
    assert np.all((M.T@K@M-K)%3==0)
    P=np.eye(6,dtype=int)
    for exponent in range(1,25):
        P=P@M%3
        assert np.array_equal(P,np.eye(6,dtype=int))==(exponent==24)
        if exponent<24:assert not np.array_equal(P,2*np.eye(6,dtype=int))
    for name,matrices in [('PSp43',G),('PGSp43',np.concatenate([G,(np.diag([1,1,2,2])@G)%3]))]:
        count=gr.orders(matrices,True)
        assert all(v%2==0 for v in count.values())
        assert max(map(int,count))==12
        saved=json.loads((ROOT/'data/toe_20261108_native_cyclic_orders.json').read_text())[name]
        assert saved=={k:v//2 for k,v in count.items()}


def test_independent_server_population_and_pinning_controls():
    server=json.loads((ROOT/'data/toe_20261108_axion_server_control.json').read_text())
    local=json.loads((ROOT/'data/toe_20261108_cyclic_partner_control.json').read_text())
    assert server['first_N']==local['first_N_leading_envelope_below_H0_squared']==21
    for row in server['pinning']:
        own=ax.pinning_row(row['kappa'],row['u'])
        assert row['high']==pytest.approx(own['heavy_mass_squared'],rel=2e-14)
        assert row['beta']==pytest.approx(own['beta_physical_along_canonical_trough'],rel=1e-5,abs=1e-16)
    for row,own in zip(server['populations'],local['populations']):
        assert (row['N'],row['T'])==(own['N'],own['Td_over_M'])
        assert row['rms']==pytest.approx(own['biased_fractional_rms'],rel=1e-12)
        assert row['maxBeta']==pytest.approx(own['max_abs_collective_beta_f_equals_MP'],rel=1e-12)
        assert sum(own['frozen_weights'])==pytest.approx(1.)
        assert own['biased_fractional_rms']>1e10*own['uniform_fractional_rms']
