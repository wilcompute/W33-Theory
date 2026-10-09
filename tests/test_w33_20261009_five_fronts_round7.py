"""Research regression controls for W33 TOE five frontier continuation."""
from pathlib import Path
import sys
from fractions import Fraction as F
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'analysis'))
def test_packet_obstructs_uniform_elliptic_operator_lower_bound():
 import w33_20261009_no_uniform_ellipticity_packet as m
 d=m.certificate()
 assert d['A']=='1599/5' and d['B']=='1681/10' and d['C']=='39/5'
 assert len(d['active_incidence_indices'])==4
 assert len(d['carrier_integral_vector'])==80
 assert d['controls'][-1]['ratio']<.016
def test_matched_parity_even_su4_D_flat_local_extensions():
 import w33_20261009_SU4_matched_Dflat_extensions as m
 d=m.certificate()
 assert d['charge_rank']==8
 assert len(d['allowed_single_matched_SU4_pairs'])==10
 assert len(d['allowed_two_matched_SU4_pairs'])==20
 for p in d['allowed_two_matched_SU4_pairs']:
  assert p['first'][1]!=p['second'][1]
  assert F(p['second_amplitude_square_over_first'])>0
def test_he246_rational_Wick_bounds_strictly_improve():
 import w33_20261009_he246_symmetry_exact_wick as m
 d=m.certificate()
 assert d['degrees']==[2,4,6]
 assert len(d['sectors']['24']['matrix_intervals'])==6
 assert len(d['sectors']['15_p']['matrix_intervals'])==3
 assert F(d['sectors']['24']['rigorous_sector_lowest_energy_upper_endpoint'])<F('142.435')
 assert F(d['sectors']['15_p']['rigorous_sector_lowest_energy_upper_endpoint'])<F('143.464')
def test_randomized_sham_common_slope_inverted_interval():
 import w33_20261009_randomized_sham_CI as m
 d=m.certificate()
 assert len(d['samples'])==3
 assert d['samples'][-1]['n']==1000000
 assert all(l['confidence_interval'][0]<.003<l['confidence_interval'][1] for l in d['samples'])
 assert d['samples'][-1]['width']<.01
 assert 'per-shot' in d['important_impossibility']
def test_exact_fortuin_kasteleyn_40_line_selector_on_grids():
 import w33_20261009_selector_potts_dimension_firewall as m
 d=m.certificate()
 assert d['q']==40
 assert 1.991<d['imposed_square_lattice_critical_betaJ']<1.992
 assert [x['edges'] for x in d['grids']]==[8,7,12]
 assert d['grids'][2]['data'][-1]['mean_equal_bond_probability']>.8
 assert 'SUPPLIED' in d['critical_boundary']
