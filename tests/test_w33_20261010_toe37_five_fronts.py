"""TOE Round37: five independent reproducibility tests."""
from pathlib import Path
import json,sys
import numpy as np
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'analysis'))
import w33_20261010_toe37_native_chiral_index as chir
import w33_20261010_toe37_finite_translation_form_obstruction as trans
import w33_20261010_toe37_quantum_graph_rank_selector as rank
import w33_20261010_toe37_flat_band_locality_tradeoff as flat
import w33_20261010_toe37_maxwell_normalization_audit as gauge
def frozen(name,r):
 x=json.loads((ROOT/'data'/f'w33_20261010_toe37_{name}.json').read_text(encoding='utf8'))
 def compare(a,b):
  if isinstance(a,dict):
   assert set(a)==set(b)
   for k in a:compare(a[k],b[k])
  elif isinstance(a,list):
   assert len(a)==len(b)
   for x,y in zip(a,b):compare(x,y)
  elif isinstance(a,(float,np.floating)) or isinstance(b,(float,np.floating)):
   assert np.isclose(a,b,rtol=1e-8,atol=1e-10),(a,b)
  else:assert a==b
 compare(r,x)
def test_native_W33_point_line_index_balanced_not_three_generations():
 r=chir.run(False);frozen('native_chiral_index',r)
 assert r['incidence_singular_values_multiplicity']=={'four':1,'sqrt_six':24,'zero':15}
 assert r['native_point_line_chiral_Fredholm_index']==0
 assert r['levi_0_1_cochain_kernel_dimensions']=={'H0':1,'H1':81}
def test_complete_abstract_spinorial_poincare_presentation_and_no_Heisenberg():
 r=trans.run(False);frozen('finite_translation_form_obstruction',r)
 assert r['alternating_constraint_rank']==6
 assert r['alternating_invariant_dimension']==0
 assert r['invariant_functional_dimension_on_S']==0
 assert r['abstract_spinorial_finite_Poincare_group_order']==174960
 assert r['order_after_quotient_by_central_constant']==58320
def test_quantum_graph_rank_mixing_does_not_select_3_without_external_input():
 r=rank.run(False);frozen('quantum_graph_rank_selector',r)
 assert r['total_vertices_by_rank']=={'1':240,'2':720,'3':2160}
 baseline=next(c for c in r['tested_ground_superpositions'] if c['mass']==.5 and c['rank_penalty']==0 and c['transition_amplitude']==.03)
 assert baseline['most_probable_rank']==2
 pos=next(c for c in r['tested_ground_superpositions'] if c['rank_penalty']==.05)
 neg=next(c for c in r['tested_ground_superpositions'] if c['rank_penalty']==-.05)
 assert pos['most_probable_rank']==1 and neg['most_probable_rank']==3
def test_flat_band_tradeoff_locality_vs_linear_wave():
 r=flat.run(False);frozen('flat_band_locality_tradeoff',r)
 ratios=r['dispersion_halving_ratios']
 assert 1.9<ratios['intrinsic_E_at_k_over_E_at_half_k']<2.1
 assert 3.8<ratios['local_mass_E_at_k_over_E_at_half_k']<4.2
 assert r['samples'][0]['fraction_nonzero_offdiagonal_entries_in_required_edge_projector']>.9
 assert r['flat_modes_before']==80
def test_Gaussian_Maxwell_coupling_remains_free_but_shell_ratio_fixed():
 r=gauge.run(False);frozen('maxwell_normalization_audit',r)
 assert r['resistance_adjacent']=='13/80'
 assert r['resistance_nonadjacent']=='7/40'
 assert r['resistance_adjacent_over_nonadjacent']=='13/14'
 assert r['MP_pseudoinverse_residual']<1e-12
 a,b=r['sample_pair_energies'][:2]
 assert np.isclose(a['neutral_adjacent_pair_action']/b['neutral_adjacent_pair_action'],10)
