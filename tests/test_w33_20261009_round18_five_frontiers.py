"""Regression tests for Round18's five-frontier audit (source-native inputs)."""
import sys,json,math
from pathlib import Path
import numpy as np
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"analysis"))
import w33_20261009_round18_fixedU_resolvent_certificate as F
import w33_20261009_round18_chirality_plaquette_audit as C
import w33_20261009_round18_heterotic_cubic_information_bound as Y
import w33_20261009_round18_classical_star_squeezed_trial as S
import w33_20261009_round18_optical_chirality_identifiability as O
import w33_pass11769_quantized_current_vacuum as H
from w33_20261008_5state_ritz import geometry

def certificate(name):
    return json.loads((ROOT/"data"/name).read_text())

def test_fixedU_toy_and_native_exact_modular_witness():
    assert F.toy_check()
    edges,*_=geometry()
    reps=certificate("w33_20261009_PSp_orbits_isotropic_triplets.json")['orbits']
    F.prior.MOD=1000003
    G=[F.projected_returns(F.prior.phased_adj(edges,x['representative']),1000003) for x in reps]
    for U in (2,8,20):
        a=[F.interaction_deltas(x,U,1000003) for x in G]
        assert len({x['19'] for x in a})==5
        expected=certificate("w33_20261009_round18_fixedU_resolvent_certificate.json")['fixed_U']['1000003'][str(U)]['interacting_minus_free_trace']
        assert a==expected

def test_flux_reversal_gauge_currents_and_native_cycles():
    edges,*_=geometry()
    c=certificate("w33_20261009_round18_chirality_plaquette_audit.json")
    assert len(edges)==160 and c['unique_8cycles']==1620
    assert len(C.cycles_touching(edges,0))==81
    assert len(C.cycles_touching(edges,52))==81
    reps=certificate("w33_20261009_PSp_orbits_isotropic_triplets.json")['orbits']
    currents=[C.deriv_trace(edges,r['representative'],1,8,0) for r in reps]
    assert currents==[440117]*5
    assert all((currents[i]+C.deriv_trace(edges,r['representative'],-1,8,0))%C.P==0 for i,r in enumerate(reps))

def test_heterotic_necessary_not_sufficient_filter():
    data=certificate("w33_20261009_round18_heterotic_cubic_information_bound.json")
    assert data['screening']['gauge_neutral_with_repetition']==424
    assert data['screening']['necessary_R_and_nonR_pass']==90
    assert data['screening']['necessary_R_and_nonR_fail']==334
    assert data['examples'][0]['necessary_R_and_nonR']
    assert not data['examples'][1]['necessary_R_and_nonR']
    assert all(x not in data['present_field_schema'] for x in data['required_amplitude_inputs_missing_from_field_schema'])

def test_star_squeezed_gaussian_quantum_upper_bound():
    data=certificate("w33_20261009_round18_classical_star_squeezed_trial.json")
    samples=data['sampled_stars']
    assert len(samples)==6
    assert max(s['minimum_low_rank_real_gaussian'] for s in samples)-min(s['minimum_low_rank_real_gaussian'] for s in samples)<1e-5
    for s in samples:
        assert 229.06<s['minimum_low_rank_real_gaussian']<229.07
        assert abs(s['isotropic_star_gaussian_optimum']-(1521/10+math.sqrt(40053)/2))<1e-7
        assert s['minimum_low_rank_real_gaussian']<s['isotropic_star_gaussian_optimum']
    g=H.geometry()
    U=np.rint(40*g['u']).astype(np.int64);V=np.rint(40*g['v']).astype(np.int64)
    q,p=S.anchor(0,U,V)
    assert np.max(np.abs((V/40@q+1/math.sqrt(20))*(U/40@p+1/math.sqrt(20))))<1e-9


def test_optical_chirality_command_wire_nonidentifiability():
    a=O.experiment(seed=8807,n=1024,current=.08,leak=0.)
    b=O.experiment(seed=8807,n=1024,current=0.,leak=.08)
    assert np.array_equal(a['signal'],b['signal'])
    assert a['design_rank']==4 and a['distinct_parameters']==5
    assert a['regression_total_flux']==b['regression_total_flux']
