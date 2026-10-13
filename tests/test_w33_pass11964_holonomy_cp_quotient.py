from pathlib import Path
import json
import sys
import numpy as np
import pytest

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'analysis'))
import w33_pass11964_holonomy_cp_quotient as model


@pytest.fixture(scope='module')
def geometry():
    return model.setup()


def test_negative_control_nonzero_real_sign_flux_preserves_conjugation(geometry):
    edges,volts,_=geometry
    for bits in ([1,0,0],[1,1,1]):
        phi=np.pi*np.array(bits)
        assert np.linalg.norm(phi)>0
        # Direct link matrix is already real, independently of the loop diagnostic.
        assert max(abs(np.exp(1j*volts@phi).imag))<1e-14
        assert model.cp_loop_residual(volts@phi,edges)[0]<1e-14


def test_closed_loop_obstruction_survives_arbitrary_vertex_gauge(geometry):
    edges,volts,_=geometry
    phi=np.array([.3,-.7,.9]);phases=volts@phi
    chi=np.random.default_rng(7).normal(size=80)
    shifted=phases+np.array([chi[b]-chi[a] for a,b in edges])
    r0,w0=model.cp_loop_residual(phases,edges)
    r1,w1=model.cp_loop_residual(shifted,edges)
    assert r0>.7 and r1>.7
    assert np.max(abs(np.exp(1j*w0)-np.exp(1j*w1)))<1e-13


def test_analytic_stiffness_matches_energy_response(geometry):
    edges,volts,_=geometry
    phi=np.full(3,np.pi)
    grad,hess=model.local_derivatives(phi,edges,volts)
    assert max(abs(grad))<1e-12
    assert min(np.linalg.eigvalsh(hess))>.09
    direction=np.array([1.,-2.,3.]);direction/=np.linalg.norm(direction)
    step=.003
    F=lambda x:model.free_energy(x,edges,volts)
    curvature=(F(phi+step*direction)+F(phi-step*direction)-2*F(phi))/step**2
    assert abs(curvature-direction@hess@direction)<1e-6


def test_published_search_retains_global_and_physical_scope():
    d=json.loads((ROOT/'data/w33_pass11964_holonomy_cp_quotient.json').read_text())
    assert d['best_conjugation_fixed_corner']['pi_bits']==[1,1,1]
    assert d['best_conjugation_fixed_corner']['energy']<d['zero_energy']-.8
    assert abs(d['energy_difference_best_vs_corner'])<1e-10
    assert len(d['numerical_multistart'])==32
    assert any(not x['success'] for x in d['numerical_multistart'])
    assert 'not a certified global minimum' in d['scope']
