"""2026-10-08 deep pi1/F20/H27 gauge and physical five-front followthrough."""
import sys,json,math
from pathlib import Path
import numpy as np
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"analysis"))
import w33_20261008_twenty_apartment_pi1_presentation as pi
import w33_20261008_apartment_torus_symmetry as sym
import w33_20261008_torus_H27_flat_flux as flux
import w33_20261008_photon_robust_decision_guards as phot
import w33_20261008_tetraquadric_exact_singular_sieve as smooth
from w33_pass607_johnson_clique_pi1 import tietze_eliminate, free_reduce
def frozen(name):
 return json.loads((ROOT/"data"/name).read_text())

def test_pi1_spanning_tree_presentation_reduces_to_torus_commutator():
 r=pi.build()
 assert r["CW_V_E_F"]==[40,60,20]
 assert r["spanning_tree_edge_count"]==39
 assert r["generators_before_Tietze"]==21
 assert r["face_relators_before_Tietze"]==20
 assert r["Tietze_eliminations"]==19
 assert r["generators_after_Tietze"]==2
 assert r["relators_after_Tietze"]==1
 assert r["remaining_relators_as_signed_word_lists"]==[[-13,19,13,-19]]
 assert r["final_relator_is_commutator"]
 assert r["pi1_equals_Z2_proved"]
 assert r["CW_simple_homotopy_to_standard_torus_via_19_Tietze_generator_relator_pairs"]

def test_pi1_exact_tietze_transcript_integrity():
 r=frozen("w33_20261008_twenty_apartment_fundamental_group.json")
 import hashlib
 h=hashlib.sha256()
 items=r["Tietze_transcript_complete"]
 assert len(items)==19
 for e in items:
  assert abs(e["eliminate"]) in [abs(x) for x in e["relation"]]
  assert sum(abs(x)==e["eliminate"] for x in e["relation"])==1
  assert e["eliminate"] not in [abs(x) for x in e["replacement"]]
  h.update(repr((e["eliminate"],tuple(e["relation"]),tuple(e["replacement"]))).encode())
 assert h.hexdigest()==r["Tietze_transcript_digest"]

def test_reconstruct_pi1_ab_homology_from_existing_chain_certificate():
 z=frozen("w33_20261008_twenty_apartment_cell_homology.json")
 assert z["integral_H0_H1_H2"]==["Z","Z^2","Z"]
 assert z["smith_d1_nonzero_diagonal_histogram"]=={"1":39}
 assert z["smith_d2_nonzero_diagonal_histogram"]=={"1":19}
 assert z["octagon_edge_face_multiplicity_histogram"]=={"2":40,"4":20}

def test_symplectic_normalizer_is_exact_F20_not_order_coincidence():
 r=frozen("w33_20261008_apartment_torus_symmetry.json")
 assert r["projective_symplectic_group_order"]==25920
 assert r["support_stabilizer_element_order_distribution"]=={"1":1,"2":5,"4":10,"5":4}
 assert r["support_stabilizer_derived_subgroup_order"]==5
 assert r["support_stabilizer_is_normalizer_of_its_Sylow5_in_PSp4_3"]
 assert r["full_PSp4_3_normalizer_order"]==20
 assert r["constructed_45_cycle_setwise_stabilizer"]==1
 assert r["constructed_20_cycle_relation_support_setwise_stabilizer"]==20
 assert r["orbit_size_of_20_cycle_support"]==1296
 assert r["support_stabilizer_abelianization"]=="C4"
 assert r["no_Z3_character_of_support_stabilizer"]
 assert not r["tetraquadric_Klein_four_is_subgroup_of_support_stabilizer"]

def test_H27_magnetic_cocycle_flat_and_flux_census():
 r=flux.compute()
 assert r["all_ordered_H27_holonomy_pairs"]==729
 assert r["ordered_holonomy_pair_center_commutator_flux_histogram"]=={0:297,1:216,2:216}
 assert r["flat_H27_holonomy_conjugacy_classes"]==105
 assert r["flat_conjugacy_orbit_length_histogram"]=={3:96,1:9}
 assert r["Z3_flat_line_bundle_characters"]==9
 assert r["nontrivial_Z3_flat_characters"]==8
 assert not r["physical_flux_quantization_or_SM_gauge_derived"]

def test_H27_commutator_formula_independently_for_all_729_pairs():
 from w33_20261008_h27_h13_five_frontiers import um,mm
 import itertools
 import numpy as np
 from w33_20261008_h27_h13_five_frontiers import canon
 for a,b,c,d,e,f in itertools.product(range(3),repeat=6):
  x=um(a,b,c);y=um(d,e,f)
  diff=(x@y-y@x)%3
  zero=not np.any(diff)
  assert zero==((a*e-b*d)%3==0)

def test_permutation_invariant_robust_photon_budget():
 r=phot.build()
 x=r["optimal_among_three_tested_depths"]
 assert x["dark0_sys0"]=={"best_stages":72,"min_expected_launches":2217}
 assert x["dark0.05_sys0.01"]=={"best_stages":72,"min_expected_launches":2982}
 assert x["dark0.1_sys0.02"]=={"best_stages":72,"min_expected_launches":4223}
 assert x["dark0.2_sys0.05"]=={"best_stages":72,"min_expected_launches":16972}
 assert not r["hardware_realized"]
 assert len(r["guarded_rows"])==75
 assert all(z["provable_observed_cross_class_margin_lower_bound"]>=0 for z in r["guarded_rows"])

def test_tetraquadric_bounded_rational_singular_sieve_is_inconclusive():
 r=smooth.build()
 assert r["sampled_ambient_points"]==20736
 assert r["hypersurface_rational_points_encountered"]==246
 assert r["exact_char0_singular_witnesses"]==[]
 assert not r["smooth_over_C_certified"]
 assert not r["singular_over_C_certified"]

def test_string_yukawa_missing_numerical_inputs_previous_repo():
 r=frozen("w33_20261008_tetraquadric_exact_singular_sieve.json")
 assert r["smooth_over_C_certified"] is False
 z=frozen("w33_20261008_h27_h13_five_frontiers.json")
 assert z["flavor_polynomial_candidate"]["Ricci_flat_HYM_kinetic_metrics_computed"] is False

def test_mod3_Heisenberg_slice_matches_earlier_H27_not_canonical_gluing():
 r=frozen("w33_20261008_h27_h13_five_frontiers.json")["h27_h13"]
 assert r["unipotent_H27_order"]==27
 assert r["H13_mod3_extraspecial_order"]==1594323
 assert r["chosen_H27_subgroup_order"]==27
 assert r["isomorphism_checked_multiplications"]==729
