from __future__ import annotations
import json,math
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def load(n):return json.loads((ROOT/'data'/n).read_text())
def test_5725_center_pairing():
 d=load('PART_W33_PASS5725_TORSION_CENTER_PAIRING.json');assert d['GL23_invariant_covectors']==[[0,0]];assert d['detecting_nonzero_covectors_per_nonzero_torsion_class']==6
def test_5726_exact_jacobi_rank_and_canonical_complement():
 d=load('PART_W33_PASS5726_EXACT_FIREWALL_JACOBIATOR_RANK.json');assert d['rank_over_Q']==d['output_support_size']==d['minimal_2term_repair']['minimal_dim_Y']==234;assert d['nonzero_jacobiator_triples']==32400;assert d['untouched_complement_dimension']==14
 s=d['untouched_complement_structure'];assert s['root_subsystem_type']=='A2';assert s['root_subsystem_rank']==2 and s['root_subsystem_size']==6;assert s['internal_firewall_deleted_pairs']==0 and s['closed_under_filtered_bracket'];assert s['reductive_type'].startswith('A2 + T6')
 a=load('PART_W33_PASS5726_FAMILY_A2_COMPLEMENT_IDENTIFICATION.json');assert a['canonical_A2_match'];assert a['image_root_decomposition']=={'E6_grade0_roots':72,'g1_matter_roots':81,'g2_conjugate_matter_roots':81};assert a['complement_decomposition']=={'Cartan_coordinates':8,'canonical_A2_roots':6}
def test_5727_heisenberg_intertwiner():
 d=load('PART_W33_PASS5727_TORSION_E8_FAMILY_HEISENBERG_INTERTWINER.json');assert d['correction_to_pass5708']['generated_group_order']==27;assert d['correction_to_pass5708']['commutant_dimension']==1
def test_5728_switching_selector():
 d=load('PART_W33_PASS5728_RAMANUJAN_SWITCHING_INVARIANT_SELECTOR.json');assert len(d['known_levels'])==4;assert all(x['gap_to_second']>1e-6 and x['min_is_ramanujan'] for x in d['known_levels'])
def test_5729_breaking_lattice():
 d=load('PART_W33_PASS5729_FAMILY_SYMMETRY_BREAKING_LATTICE.json');assert d['Hermitian_commutant_real_dimensions']=={'trivial':9,'center_Z3_scalar':9,'cyclic_X':3,'cyclic_Z':3,'C2_swap':5,'S3_permutation':2,'Heisenberg_H3_XZ':1};assert abs(d['fourier_overlap_abs']-1/math.sqrt(3))<1e-12
def test_5730_extended_clifford():
 d=load('PART_W33_PASS5730_HEISENBERG_QUTRIT_GL23_EXTENDED_CLIFFORD.json');assert d['Heisenberg_group']['order']==27 and d['Heisenberg_group']['center_order']==3;assert d['GL23_extension']['antiunitary']
def test_5731_mixed_extension_nogo():
 d=load('PART_W33_PASS5731_Z3_Z2_MIXED_EXTENSION_TOPOLOGY.json');assert d['central_extension_cohomology']['H2_C3_with_C2_trivial']==0 and d['central_extension_cohomology']['H2_C2_with_C3_trivial']==0;assert 'S3' in d['noncentral_escape']['semidirect_group']
def test_5732_det_hinge():
 d=load('PART_W33_PASS5732_P2_P3_DETERMINANT_ARITHMETIC_BRIDGE.json');assert d['exact_cross_prime_hinge']['fiber_sizes']=={'1':24,'2':24};assert d['primary_no_go']['Hom_C2_C3']==0 and d['primary_no_go']['Hom_C3_C2']==0
