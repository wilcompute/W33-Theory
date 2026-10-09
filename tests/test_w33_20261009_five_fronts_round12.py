"""Round12 five research fronts: independently recompute certificates."""
import sys,shutil,json
from pathlib import Path
import pytest
from fractions import Fraction
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'analysis'))
def test_cycle_weighted_quantum_local_bound_where_old_bound_vanishes():
 import w33_20261009_weighted_cycle_local_quantum_bound as m
 d=m.certificate()
 assert len(d['eight_cycle_edges'])==8
 assert Fraction(d['exact_new_lower_rational'])>Fraction(33,100)
 assert d['exact_new_lower_decimal']<d['numerical_optimal_local_potential']
 assert d['exact_integer_left_null_weight_histogram']=={'0':4,'1':152,'2':4}
def test_H_worldsheet_actual_wsl_catalog_audit():
 if not shutil.which('wsl.exe'):
  pytest.skip('Live source audit requires authorized Windows WSL orbifolder exports')
 import w33_20261009_heterotic_wsl_catalog_F_audit as m
 d=m.certificate()
 assert d['total_finite_named_C_records']==221
 assert len(d['candidate_audit'])==16
 assert sum(x['sources_exact_named_full_monomial_matches'] for x in d['candidate_audit'])==40
 assert sorted(x['source_catalog_direct_colored_mask_rank'] for x in d['candidate_audit'])==[0]*12+[5]*4
 assert not d['triplet_n81_n17_n82_present_in_limited_exports']
def test_committed_original_orbifolder_coupling_source_fingerprints():
 d=json.loads((ROOT/'data/w33_20261009_heterotic_wsl_catalog_F_audit.json').read_text())
 assert d['total_finite_named_C_records']==221
 assert len(d['candidate_audit'])==16
 assert len(d['catalog_fingerprints']['.dbd']['sha256'])==64
 assert len(d['catalog_fingerprints']['.sp']['sha256'])==64

def test_full_quantum_connection_exact_modular_nonzero_curvature():
 import w33_20261009_quantum_curl_exact_modular as m
 d=m.certificate()
 assert d['dual_derivative_basis_verified_exactly']
 assert len(d['modular_certificates'])==2
 assert all(x['antisym_nonzero_residue']>0 for x in d['modular_certificates'])
def test_adversarial_shotwise_clipping_under_frame_randomization():
 import w33_20261009_shot_clipped_frame_optics as m
 d=m.certificate()
 assert d['seeded_runs']['no_optical_signal']['rejections']==0
 assert d['seeded_runs']['signal_proxy']['rejections']==36
 assert d['corrupted_shots_arbitrary']==40
def test_all_85320_coordinate_3D_Abelian_quotients():
 import w33_20261009_all_coordinate_3D_quotients as m
 d=m.certificate()
 assert d['total_coordinate_three_chord_quotients']==85320
 assert abs(d['minimal_anisotropy_coordinate_basis']['anisotropy_eigenvalue_ratio']-1.0375)<1e-8
 assert abs(d['maximal_anisotropy_coordinate_basis']['anisotropy_eigenvalue_ratio']-4)<1e-8
def test_prior_local_fullH_IMS_bound_preserved():
 import w33_20261009_local_coercivity_IMS_packet as m
 d=m.certificate()
 assert d['exact_energy_bound_at_radius_half']=='1/10'
