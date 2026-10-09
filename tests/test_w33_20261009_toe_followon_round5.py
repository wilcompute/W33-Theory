"""Recompute all five W33 2026-10-09 follow-up research certificates."""
import sys
from pathlib import Path
from fractions import Fraction as F
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'analysis'))
def test_local_Hormander_bracket_rank():
  import w33_20261009_local_hormander_depth as m
  c=m.certificate()
  assert c['actual_hormander_bracket_step_upper']==4
  assert [x['vector_field_evaluation_rank_lower'] for x in c['stage_rank_lower_certificates']]==[4,16,52,78]
def test_global_bracket_graph_Hormander():
  import w33_20261009_global_hormander_graph as m
  c=m.certificate()
  assert (c['graph_vertices'],c['graph_edges'],c['graph_degree'],c['graph_diameter'])==(160,480,6,4)
  assert c['global_pointwise_bracket_step_upper']==5
  assert c['sample_ranks'][1]['depth_to_78']==4
def test_Z6II_H_momentum_conditional_no_oscillator():
  import w33_20261009_conditional_H_momentum_bilinears as m
  c=m.certificate()
  assert c['count']==6
  assert all(not x['satisfies_no_oscillator_R'] for x in c['records'])
  assert {tuple(x['twist_sectors']) for x in c['records']}=={(2,4),(3,3)}
  assert 'assumption' in c['result'].lower()
def test_24_and_15_exact_Wick_interval():
  import w33_20261009_symmetry_he2_rational_intervals as m
  c=m.certify()
  for name,target in [('24_lower_ritz_interval',142.7193362242),
                      ('24_upper_ritz_interval',145.1724550873),
                      ('15_point_ritz_interval',143.6110807403),
                      ('15_line_ritz_interval',143.6110807403)]:
    low,high=map(F,c[name]);assert low<=high
    assert abs(float(low)-target)<1e-9
    assert high-low<F(1,10**20)
def test_160_minima_connected_tunneling():
  import w33_20261009_tunneling_160_triples as m
  c=m.certificate()
  assert c['one_replacement_components']==40
  assert c['one_replacement_degree']==3 and c['two_replacement_degree']==27
  assert c['full_graph_connected']
  assert c['line_graph_spectrum']=={'12':1,'2':24,'-4':15}
  assert abs(c['numeric_samples'][1]['numeric_first_gap']-.2241627049784)<1e-7
def test_paired_sham_controls():
  import w33_20261009_sham_reference_homodyne as m
  c=m.certificate()
  assert c['arms']['uncorrelated_reference_null']['rejections']<=8
  assert c['arms']['genuine_gate']['rejections']>=45
  assert c['arms']['mismatched_reference_null']['rejections']>=45
