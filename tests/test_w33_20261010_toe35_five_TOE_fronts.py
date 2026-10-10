"""Round35 five independent exact/numeric reproducibility tests."""
import json,sys,math
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'analysis'))
import w33_20261010_toe35_spinorial_e8_so11_centralizer as central
import w33_20261010_toe35_so11_chirality_ledger as chirality
import w33_20261010_toe35_Zdeck_dimensional_nogo as oned
import w33_20261010_toe35_three_deck_kinematic_construction as threed
import w33_20261010_toe35_alpha_CODATA_holdout as alpha
def frozen(name,res):
 expected=json.loads((ROOT/'data'/f'w33_20261010_toe35_{name}.json').read_text(encoding='utf-8'))
 assert expected==res
def test_spinorial_SL29_centralizer_SO11_not_just_SU5():
 rec=central.run();frozen('spinorial_e8_so11_centralizer',rec)
 assert rec['exact_invariant_vector6_dimension']==1
 assert rec['exact_invariant_bivector15_dimension']==0
 assert rec['total_fixed_Lie_algebra_dimension']==55
 assert rec['identified_fixed_Lie_algebra'].startswith('so(11)')
def test_SO11_to_SO10_chiral_and_antichiral_cancel():
 rec=chirality.run();frozen('spinorial_so11_spin10_chirality',rec)
 assert rec['su5_complex_rep_net_chirality_by_Lorentz_spin_dim']=={'10_vs_10bar':0,'5bar_vs_5':0}
 assert sum(x['dim'] for x in rec['SO10xSpin5_E8_decomposition'])==248
def test_fixed_rank1_Z_deck_has_1D_not_3D_diffusion():
 rec=oned.run();frozen('Zdeck_dimensional_nogo',rec)
 assert rec['winding_cycle_flux_gcd']==1
 assert rec['coefficient_D_of_k_squared_band']>0
 assert len(rec['spectral_dimension_tower'])==5
 assert rec['spectral_dimension_tower'][-1]['longest_running_dimension_near1']['span_ratio']>9
def test_three_generator_cover_genuine_infinite_diffusion_rank3():
 rec=threed.run();frozen('three_deck_kinematic_construction',rec)
 assert len(rec['three_selected_fundamental_chord_edge_indices'])==3
 assert min(rec['diffusion_tensor_eigenvalues'])>0
 assert [x['degree_per_axis'] for x in rec['tested_finite_quotients']]==[3,5,7,9]
def test_alpha_W33_exact_fraction_rejected_by_CODATA_2022():
 from decimal import Decimal
 rec=alpha.run();frozen('alpha_CODATA_2022_holdout',rec)
 assert rec['correction_exact_fraction']=='40/1111'
 assert Decimal(rec['discrepancy_in_CODATA_standard_uncertainties'])>200
