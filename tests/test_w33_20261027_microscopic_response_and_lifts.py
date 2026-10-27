"""Independent covariance, response-limit and lattice-integrality controls."""
import json
from pathlib import Path
import sys
import numpy as np
import sympy as s
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'analysis'))
import w33_20261027_microscopic_response_and_lifts as m


def test_infinite_cover_lift_and_action_repair():
    r=m.reflection_lift()
    assert r['exact_edge_voltage_identity'] and r['exact_involution_on_infinite_cover']
    assert r['selected105_faces_with_image_outside_selected_set']==47
    for row in r['spectral_controls']:
        assert row['original_spectrum_error']>1e-3
        assert row['averaged_spectrum_error']<1e-10
    ac=r['acoustic_controls']
    errors=[max(abs(np.array(x['three_soft_eigenvalues_over_t2'])-x['target_speed_squared']))for x in ac]
    assert errors[-1]<errors[0]/5


def test_spectral_response_against_time_determinant():
    coarse=m.temporal_determinant_control(slices=24)
    fine=m.temporal_determinant_control(slices=48)
    assert max(coarse['gauge_covariance_logdet_error'],fine['gauge_covariance_logdet_error'])<1e-10
    for a,b in zip(coarse['probes'],fine['probes']):
        assert b['error']<a['error']/3 and b['error']<1e-6


def test_gapped_response_has_regular_positive_limit():
    B=m.polarization(0,0,.1)
    E=[(m.polarization(0,nu,.1)-B)/nu**2 for nu in (.02,.01,.005)]
    assert min(np.linalg.eigvalsh(B))>1
    assert all(min(np.linalg.eigvalsh(x))>6 for x in E)
    assert np.linalg.norm(E[-1]-E[-2])<np.linalg.norm(E[-2]-E[-3])/3
    # Equal response diagonals cannot match the prior target's unequal diagonals.
    assert abs(B[0,0]-B[1,1])<1e-10
    H=np.array(m.prior.inputs()[-2],float)[:2,:2]
    assert abs(H[0,0]-H[1,1])>.5


def test_thermal_zero_mode_is_not_maxwell_inertia():
    B=m.polarization(1,0)
    K1=m.polarization(1,.00002);K2=m.polarization(1,.00001)
    assert np.linalg.norm(K2-B)>1.9
    assert np.linalg.norm(K1-K2)<1e-5


def test_complete_integer_cycle_bases():
    for d in (3,6):
        C,B,_=m.lifted_patch(d)
        assert not (C@B).any()
        assert len(C)==B.shape[0]-B.shape[1]+1
        assert m.cycle_lattice_index(C,B)==1
    low=m.rotor(1,1,3); high=m.rotor(2,1,3)
    assert high['ground_energy']<low['ground_energy']
    assert high['residual_norm']<1e-8 and high['boundary_probability']<low['boundary_probability']


def test_joint_nonabelian_representation_and_anomalies():
    r=m.nonabelian_interface()
    assert r['exact_Cartan_cubic_anomaly_polynomial']=='0'
    assert r['native_edge_hopping_covariance_error']<1e-11
    assert r['SU2_restriction']==dict(doublets=6,singlets=15,half_integer_multiplicity_even=True)
    assert r['bare_Weyl_mass_forbidden_by_Qpsi']


def test_continuous_threshold_bound_against_frozen_grid():
    r=m.continuous_threshold_bound()
    assert s.Rational(r['exact_remainder_AY_minus_bound_A2'])<0
    assert s.Rational(r['universal_positive_A2_upper_bound_kY'])==s.Rational(2297,1617)
    assert s.Rational(2297,1617)<s.Rational(8,3)
    assert r['original53_grid_rows_max_error']<1e-10


def test_reading_coverage_is_partial_and_content_specific():
    r=json.loads((ROOT/'analysis/2026-10-27_research_intake_coverage.json').read_text())
    assert sum(x['full_text_model_read_this_continuation']for x in r['pdf_pages'])>=39
    read=[x for x in r['historical_week_commits']if x['full_patch_model_read']]
    assert len(read)>=6 and len(read)<len(r['historical_week_commits'])
    assert 'Five empty reservation' in r['reading_increment_20261027_microscopic']['patch_scope']
