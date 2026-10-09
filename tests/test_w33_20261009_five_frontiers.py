"""Reproducibility regressions for five independent October 9 science fronts."""
from pathlib import Path
import sys
import numpy as np
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'analysis'))
import w33_20261009_9state_ritz as Ritz
import w33_20261009_curvature_perturbation as T
import w33_20261009_optical_eighth_moment_power as Opt
import w33_20261009_spatial_product_spectral_dimension as Geo
import w33_20261009_heterotic_benchmark_full_roots as Het
import w33_20261009_wilson_generator_phase_orbit as Orbit

def test_nine_state_ritz_two_degree_exact_rules():
    a,b=Ritz.ritz(11),Ritz.ritz(12)
    assert np.max(np.abs(a-b))<2e-9
    eig=np.linalg.eigvalsh(a)
    assert abs(eig[0]-127.595518296517)<2e-8
    assert eig[0]<np.linalg.eigvalsh(a[:7,:7])[0]-.02
    assert eig[1]>eig[0] # only the RITZ spectrum, not a certified full-system gap

def test_T_odd_form_stability_and_no_kramers():
    cert=T.certificate()
    assert cert['relative_form_bound']==1
    assert '-1 < eps < 1'==cert['compact_resolvent_for']

def test_optical_eighth_moment_and_tail_uncertainty():
    out=Opt.certificate()
    a=out['cases']['vacuum_ideal']
    assert abs(a['excess_kurtosis']-.3883520461881722)<1e-12
    assert a['relative_error_variance_ratio']>20
    assert a['alternative_asymptotic_N5']>80000
    squeezed=out['cases']['squeezed_eta_1/4']
    assert squeezed['alternative_asymptotic_N5']>2e7

def test_supplied_dimensions_not_selected():
    out=Geo.certificate()
    assert len(out['samples'])==5*6
    for d in range(5):
        val=Geo.product(d,500)['total_spectral_dimension']
        assert abs(val-d)<.003*max(d,1)
def test_full_gauge_root_screen_from_frozen_files():
    result=Het.analyze()
    assert result['candidate_models']==15
    assert result['benchmark_root_counts']=={'model1':(8,14),'model2':(8,26)}
    assert result['necessary_root_count_matches']['model1']==[
        'Z6II_34__SM_20260917_1558',
        'Z6II_34__SM_20260917_2068',
        'Z6II_34__SM_20260917_292']
    assert result['necessary_root_count_matches']['model2']==[]
def test_joint_phase_generator_redefinitions():
    import w33_20261009_joint_root_phase_sieve as Joint
    bench={b:tuple(tuple(sorted(k.items())) for k in Joint.joint(
        [Het.vector(Het.BENCH_V),Het.vector(x['W2']),Het.vector(x['W3'])]))
        for b,x in Het.BENCH.items()}
    matches={b:[] for b in bench}
    for name in Het.analyze()['candidate_model_results']:
        rows=Het.source_model(Het.SCAN/(name+'.model'))
        all_signatures=Orbit.orbit([rows[0],rows[7],rows[4]])
        for b,finger in bench.items():
            if finger in all_signatures:matches[b].append(name)
    assert matches=={'model1':['Z6II_34__SM_20260917_1558'],'model2':[]}
