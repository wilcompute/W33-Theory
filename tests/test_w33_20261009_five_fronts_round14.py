"""Round14 W33 five-front research plus intrinsic association algebra.

All tests call standalone source certificate(), verify exact integer,
rational symbolic, full 160-cycle, full 16-support, optical randomized
design and 86,400 selector group orbit energies. No physical theory
of everything or laboratory hardware result is presumed.
"""
import sys
from fractions import Fraction
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'analysis'))
def test_uniform_local_current_bound_on_160_tubes():
 import w33_20261009_round14_all160_uniform_tube_bound as m
 d=m.certificate()
 assert d['verified_channel_representatives']==160
 assert d['exact_t_min']=='20/39'
 assert d['rigorous_uniform_energy_lower_on_all_160_balls']=='6400/77571'
def test_all16_heterotic_necessary_cubic_uniqueness():
 import w33_20261009_round14_heterotic_n81_cubic_census as m
 d=m.certificate()
 assert d['exact_degree3_monomial_histogram']=={'1':16}
 assert d['known_cubic_n81_n17_n82_present_in_all']
 assert all(x['exact_cubic_necessary_monomials']==[['n_81','n_17','n_82']] or
            sorted(x['exact_cubic_necessary_monomials'][0])==sorted(['n_81','n_17','n_82'])
            for x in d['all_supports'])
def test_quantum_connection_exact_16_78_rational_rank():
 import w33_20261009_round14_exact_quantum_curvature_rank as m
 d=m.certificate()
 assert d['exact_magnetic_curvature_Q_rank']==16
 assert d['adapted_two_parameter_y_verified_all_78']
 assert d['adapted_exact_y_coefficients']==['50/196319','2299/15705520']
def test_paired_causal_optical_intervention_with_leakage():
 import w33_20261009_round14_paired_optical_intervention as m
 d=m.certificate()
 assert d['runs']['null']['rejections']==0
 assert d['runs']['optical']['rejections']==30
 assert d['runs']['electronics_only']['rejections']==0
def test_native_selector_gapped_incidence_motif_Hamiltonians():
 import w33_20261009_round14_intrinsic_selector_energies as m
 d=m.certificate()
 assert d['total_intrinsic_isotropic_selectors']==86400
 assert all(v['ground_degeneracy']==4320 and v['first_excitation_gap']==2 for v in d['integer_local_motif_energies'].values())
 assert [r['selector_one_flag_swap_degree'] for r in d['exact_PSp_orbits']]==[117]*5
def test_all_86400_five_orbits_exact_fullband_flux_isospectrality():
 import w33_20261009_round14_fullband_magnetic_isospectrality as m
 d=m.certificate()
 assert d['exact_magnetic_isospectrality_all_k']
 assert d['identical_restricted_moments_m0_to_m4']
 assert d['optimal_flag_triples']==86400
 assert all(x['max_full_80_band_difference']<1e-11 for x in d['numerical_full80band_probes'])

def test_commutative_cycle_flag_association_algebra():
 import w33_20261009_round14_cycle_relation_algebra as m
 d=m.certificate()
 assert d['full_five_relation_multiplication_closes'] and d['relation_algebra_commutative']
 assert d['plusone_graph_integer_spectrum']=={'-9':48,'1':81,'9':30,'81':1}
 assert d['exact_one_flag_swap_degree']==117
 assert d['optimal_triples_86400']==86400
