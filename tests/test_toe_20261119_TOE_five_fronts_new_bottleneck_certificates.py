"""Regression certificates for TOE physical bottlenecks, independent of W33."""
import sys, unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'analysis'))
import toe_20261119_TOE_five_fronts_new_bottleneck_certificates as toe

class PhysicalFiveFronts(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.s=toe.singlet_holomorphic_vacuum()
        cls.t=toe.topology_chiral_tradeoff()
        cls.g=toe.adjoint_GUT_consistency()
        cls.e=toe.anisotropic_GR_relational_clock()
        cls.q=toe.single_photon_local_superselection()
        cls.y=toe.chiral_Yukawa_hierarchy_control()
        cls.a=toe.selective_topological_cubic_alignment()

    def test_complete_singlet_renormalizable_invariant_inventory(self):
        inv=self.s['gauge_invariants_degrees_1_2_3']
        self.assertEqual(len(inv['1']),0)
        self.assertEqual(set(map(tuple,inv['2'])),{
            ('S_12','S_12_conj'),('S_14','S_14_conj')})
        self.assertEqual(set(map(tuple,inv['3'])),{
            ('S_12','S_14_conj','S_24'),
            ('S_13','S_14_conj','S_34_1'),
            ('S_13','S_14_conj','S_34_2')})

    def test_singlet_Fterm_forces_S13_zero_at_Dflat(self):
        self.assertIn('F_{G_i}',self.s['generic_nonzero_CEG_obstruction'])
        self.assertTrue(self.s['third_family_one_spurion_diagonal_needs_S13'])
        ell=self.s['ell_functional_on_fields']
        self.assertEqual(ell['S_12'],0)
        self.assertEqual(ell['S_12_conj'],0)
        self.assertGreater(ell['S_13'],0)
        self.assertLess(ell['S_14_conj'],0)

    def test_two_bilinears_force_unique_singlet_origin(self):
        self.assertTrue(self.s['both_bilinears_nonzero_unique_SUSY_vacuum_origin'])
        self.assertIn('m !=0',self.s['two_bilinears_proof'])

    def test_topology_minimum_three_cycle_tradeoff(self):
        self.assertEqual(self.t['relative_cup_xyz'],1)
        self.assertEqual(self.t['b1_absolute'],3)
        self.assertEqual(self.t['b1_relative_to_one_sphere'],3)
        self.assertTrue(self.t['triple_cup_requires_b1_at_least_three'])

    def test_unbroken_flat_gauge_adjoint_exotics(self):
        self.assertEqual(self.t['unbroken_Spin10_Lie_algebra_dimension'],45)
        self.assertEqual(self.t['adjoint_chiral_multiplets_if_no_projection'],3)
        self.assertEqual(self.t['adjoint_chiral_zero_modes_if_trivial_flat_ad_bundle_and_no_boundary_projection'],135)

    def test_SU5_mass_Clebsch_relation(self):
        c=self.g['renormalizable_mass_Clebsch_coefficients']
        self.assertEqual(c['octet'],2)
        self.assertEqual(c['triplet'],-3)
        self.assertEqual(c['X_leptoquark'],-.5)
        self.assertAlmostEqual(2*c['X_leptoquark'],c['octet']+c['triplet'])

    def test_SU5_light_unwanted_leptoquark_and_RGE_shift(self):
        self.assertLess(self.g['inevitable_X_upper_mass_GeV_if_same_24'],1.2e7)
        self.assertGreater(self.g['new_inverse_alpha1_minus_alpha3_mismatch_magnitude_at_original_MU'],6)
        self.assertTrue(all(abs(v-10/3)<1e-12 for v in self.g['full_24_majorana_beta_shifts']))

    def test_anisotropic_Kasner_scalar_constraint(self):
        self.assertAlmostEqual(self.e['Kasner_sum_p'],1)
        self.assertAlmostEqual(self.e['Kasner_sum_p_squared'],7/18)
        self.assertTrue(all(z['constraint_error']<1e-12 for z in self.e['samples']))
        self.assertTrue(all(z['KG_error']<1e-12 for z in self.e['samples']))
        self.assertTrue(all(z['directional_error_max']<1e-12 for z in self.e['samples']))

    def test_relational_clock_needs_lapse_not_just_exchange_count(self):
        z=self.e['samples']
        self.assertEqual(len(z),6)
        self.assertAlmostEqual(z[2]['required_lapse_dt_dn'],1.)
        self.assertAlmostEqual(z[3]['required_lapse_dt_dn'],2.)
        self.assertIn('exp(p_i phi/sigma)',self.e['exact_relational_observables'])

    def test_single_photon_unrestricted_CHSH(self):
        from math import sqrt
        self.assertAlmostEqual(self.q['untwirled_CHSH_unrestricted'],2*sqrt(2),places=12)
        self.assertAlmostEqual(self.q['coherence_01_10_before'],.5)
        self.assertEqual(self.q['coherence_01_10_after'],0.)

    def test_single_photon_local_SSR_CHSH_bound(self):
        self.assertTrue(self.q['locally_number_twirl_is_mixed_separable'])
        self.assertEqual(self.q['number_conserving_CHSH_upper'],2)
        self.assertLessEqual(self.q['sampled_max_abs_CHSH'],2+1e-10)
        self.assertEqual(self.q['sampled_number_conserving_measurement_quartets'],1500)

    def test_hollow_complex_Yukawa_cannot_make_large_hierarchy(self):
        self.assertEqual(self.y['tested_random_complex_hollow_symmetric_matrices'],1000)
        self.assertLessEqual(self.y['max_s1_over_s2_seen'],2+1e-10)

    def test_selective_cohomology_alignment_avoids_singlet_cubic(self):
        self.assertEqual(self.a['physical_Yukawa_triple_cup'],1)
        self.assertEqual(self.a['singlet_loop_triple_cup'],0)
        self.assertEqual(self.a['single_entry_perturbation_triple_cup'],1)
        self.assertIn('codimension-one',self.a['non_generic_warning'])

if __name__=='__main__': unittest.main()
