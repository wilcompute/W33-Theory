"""Regression tests for the five main and three outside-box W33 fronts."""
import json, math, sys
from pathlib import Path
import numpy as np
import pytest
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'analysis'))
import w33_20261031_eight_front_server_campaign as M

@pytest.fixture(scope='module')
def results():
    return M.build()['results']

def test_exact_polynomial_over_integers_without_roundoff():
    D,C=M.projector_exact()
    assert D.shape==(80,160)
    assert np.array_equal(C@C,320*C)
    assert np.array_equal(D@C,np.zeros((80,160),dtype=np.int64))
    assert np.trace(C)==81*320
    assert np.all(C.diagonal()==162)

def test_phase_survival_independent_of_logical_input(results):
    v=results['01_exact_optical_projector_phase_control']
    D,C=M.projector_exact();P=C/320
    from scipy.linalg import null_space
    Q=null_space(D.astype(float))
    rng=np.random.default_rng(567890)
    for _ in range(3):
        a=rng.normal(size=81)+1j*rng.normal(size=81);a/=np.linalg.norm(a)
        psi=Q@a
        sigma=.7
        phases=rng.normal(scale=sigma,size=(900,160))
        u=np.exp(1j*phases)*psi
        measured=np.einsum('bi,ij,bj->b',u.conj(),P,u,optimize=True).real.mean()
        exact=math.exp(-sigma*sigma)+(1-math.exp(-sigma*sigma))*81/160
        assert abs(measured-exact)<.012
    assert len(v['phase_samples'])==5

def test_160_port_encoder_has_reversible_givens_word(results):
    a=results['02_160_mode_adjacent_Givens_encoder']
    assert 1<=a['real_adjacent_two_mode_interferometers']<=a['worstcase_rectangular_elimination_bound']
    assert a['reconstruction_Frobenius_error']<1e-9
    assert len(a['gate_list_sha256'])==64

def test_herald_instrument_probabilities_sum_correctly(results):
    d=results['03_QND_asymmetric_readout_and_loss']
    for r in d['rows']:
        fn,fp=r['false_negative_probability'],r['false_positive_probability']
        prob=.5*(1-fn+fp)
        assert abs(r['reported_herald_probability']-prob)<1e-12
        assert abs(r['posterior_strange_fidelity']-(1-fn)/(1-fn+fp))<1e-12
        assert r['delivered_true_strange_per_attempt']<=r['delivered_herald_per_attempt']+1e-12
    assert d['rows'][-1]['Wigner_negative'] is True  # wrong-parity E is magic too
    assert d['rows'][-1]['posterior_strange_fidelity']<.5

def test_seven_noncommuting_7state_clock_finite_sizes(results):
    d=results['04_quantum_7clock_truncation_finite_scaling']
    assert {x['N'] for x in d['periodic_chain_results']}=={2,3,4,5}
    assert {x['h'] for x in d['periodic_chain_results']}=={.12,.5}
    assert all(x['finite_gap']>0 for x in d['periodic_chain_results'])
    assert all(x['Hilbert_dimension']==7**x['N'] for x in d['periodic_chain_results'])

def test_three_qutrit_erasure_code_exact_decoder(results):
    d=results['05_three_qutrit_erasure_edge_code']
    assert {r['erased_site'] for r in d['erased_site_exact_recovery']}=={0,1,2}
    assert max(r['decode_state_error'] for r in d['erased_site_exact_recovery'])<1e-12
    for r in d['erasure_curve']:
        p=r['per_carrier_erasure']
        assert abs(r['three_qutrit_encoded_recovery_probability']-(1-3*p*p+2*p**3))<1e-12

def test_floquet_erasure_compilation_tracks_actual_native_gate_exposure(results):
    d=results['06_encoded_Floquet_edge_erasure_transport']
    assert len(d['rows'])==3*6
    for r in d['rows']:
        assert len(r['three_consecutive_moving_edge_sources'])==3
        assert all(0<=k<=4 for k in r['carrier_swap_stage_counts'])
        assert 0<=r['encoded_known_erasure_recovery_probability']<=1
        assert all(0<=e<=1 for e in r['per_carrier_erasure_probability'])
        q=r['per_carrier_erasure_probability']
        target=np.prod([1-v for v in q])+sum(q[i]*np.prod([1-q[j] for j in range(3) if j!=i]) for i in range(3))
        assert abs(target-r['encoded_known_erasure_recovery_probability'])<1e-12

def test_curvature_plus_canonical_electric_gauge_Ward(results):
    d=results['07_lattice_gauge_curvature_Gauss']
    assert d['spatial_lattice']==[3,3,3]
    assert d['action_gauge_invariance_error']<1e-10
    assert d['canonical_local_Gauss_Ward_derivative']<1e-7

def test_noncompact_Lorentz_boost_has_no_positive_finite_metric(results):
    d=results['08_outsidebox_Lorentz_ghost_no_positive_norm']
    assert d['positive_definite_unitarity_possible'] is False
    assert abs(d['boost_eigenvalues'][0]-math.exp(-.7))<1e-12
    assert abs(d['boost_eigenvalues'][-1]-math.exp(.7))<1e-12
    assert d['indefinite_oscillator_negative_energy_sequence']==[-.5,-2.,-8.,-32.]

def test_reproducible_json_status_and_all_eight_modules(results):
    stored=json.loads(M.OUT.read_text())
    assert len(stored['results'])==8
    assert set(stored['results'])==set(results)
    assert all(x['status'].startswith('PASS') for x in results.values())
