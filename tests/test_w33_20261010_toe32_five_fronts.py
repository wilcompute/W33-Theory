"""Round32 focused regressions for five independent theory/engineering fronts."""
import sys,json,math
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'analysis'))
import w33_20261010_toe32_phenom_temporal_decoder as temporal
import w33_20261010_toe32_voltage_opt_search as voltage
import w33_20261010_toe32_e8_extension_monotonicity as e8
import w33_20261010_toe32_cover_causal_growth as causal
import w33_20261010_toe32_C8_platform_gap_screen as hardware
def frozen(name,res):
 data=json.loads((ROOT/'data'/f'w33_20261010_toe32_{name}.json').read_text())
 assert data==res
def test_approx_temporal_decoder_reduces_both_check_and_logical_failure():
 r=temporal.run(180);frozen('phenom_temporal_decoder',r)
 assert len(r['runs'])==3
 assert all(z['logical_recovery_failures_temporal']<z['logical_recovery_failures_raw'] for z in r['runs'])
 assert r['runs'][1]['logical_recovery_failures_temporal']==35
def test_compact_cover_search_negative_results_do_not_fake_nogo():
 # Search is ~80 sec and seeded: replay separately when desired. This
 # audit verifies all recorded attempted degrees and exact evidence
 # status, but does not assert their mathematical impossibility.
 r=json.loads((ROOT/'data/w33_20261010_toe32_voltage_opt_search.json').read_text())
 assert [v['p'] for v in r['attempts']]==[4,5,7,8,11,13]
 assert not r['successful_degrees']
 assert r['attempts'][-1]['best_violations']==8
 assert 'UNKNOWN' in r['scope']
def test_E8_fixed_embedding_centralizer_cannot_grow_on_extension():
 r=e8.run();frozen('e8_extension_monotonicity',r)
 assert r['dimension']==11 and r['algebraic_centre_dimension']==0
 assert r['parallel_certificate_filename']=='data/w33_pass11843_e8_tits_lorentz_commutant.json'
def test_17_cover_graph_balls_and_quantum_tails():
 r=causal.run();frozen('cover_causal_growth',r)
 assert r['sampled_native_ball_counts_r0_to4']==[1,5,17,53,161]
 assert r['cubic_Z3_spatial_ball_counts_r0_to4']==[1,7,25,63,129]
 assert all(v['radius_0_to_8_balls'][:5]==[1,5,17,53,161] for v in r['sampled_root_ball_growth'])
def test_C8_platform_real_world_refs_and_hardcore_nogo():
 r=hardware.run();frozen('C8_platform_gap_screen',r)
 assert len(r['competing_research_platforms'])==4
 assert sum(x['categorical_rejection'] for x in r['competing_research_platforms'])==1
 assert r['lifetime_threshold_for_50percent_survival']['ramsey_60us_T1_min_us']>173
 assert r['lifetime_threshold_for_50percent_survival']['direct_20us_T1_min_us']<58
