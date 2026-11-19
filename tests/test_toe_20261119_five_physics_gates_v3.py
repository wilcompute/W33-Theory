"""Regression tests for independent Nov-19 2026 five-front physics gates."""
import importlib.util
import math
import unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
SOURCE=ROOT/'analysis'/'toe_20261119_five_physics_gates_v3.py'
spec=importlib.util.spec_from_file_location('toe_20261119_five_physics_gates_v3',SOURCE)
mod=importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

class TestFivePhysicsGatesV3(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.result=mod.run()
    def test_a01_memory_gamma_036_threshold(self):
        self.assertAlmostEqual(self.result['native_qutrit_noise']['noise_critical_table'][1]['critical_output_depolarizing_fraction'],.010263207615968257,places=11)
    def test_a02_memory_just_below_threshold(self):
        self.assertLess(self.result['native_qutrit_noise']['noise_critical_table'][1]['witness_at_one_pct'],0)
    def test_a03_memory_tiny_gamma_noise_fragility(self):
        self.assertLess(self.result['native_qutrit_noise']['noise_critical_table'][0]['critical_output_depolarizing_fraction'],.001)
    def test_a04_memory_pairwise_all_three_classical(self):
        self.assertTrue(self.result['native_qutrit_noise']['all_three_pairs_remain_classically_decomposable'])
    def test_a05_memory_choi_residual_and_tp(self):
        r=self.result['native_qutrit_noise'];self.assertLess(r['pairwise_kraus_choi_error_max'],1e-12);self.assertLess(r['kraus_tp_error_max'],1e-12)
    def test_a06_multi_dimension_noise_thresholds(self):
        row=self.result['all_dimension_MUB_noise_scaling']['critical_noise_table']
        self.assertEqual([x['dimension'] for x in row],[2,3,4,5,6,9,12])
        self.assertTrue(all(a['critical_depolarizing_fraction']>b['critical_depolarizing_fraction'] for a,b in zip(row,row[1:])))
    def test_a07_multi_dimension_qutrit_consistency(self):
        self.assertAlmostEqual(self.result['all_dimension_MUB_noise_scaling']['critical_noise_table'][1]['critical_depolarizing_fraction'],.010263207615968257,places=11)
    def test_b01_baryon_exact_full_rank(self):
        self.assertEqual(self.result['SIC_H27_baryon_coordinate_orbits']['full_jacobian_rank'],19)
    def test_b02_baryon_orbit_partition(self):
        self.assertEqual(self.result['SIC_H27_baryon_coordinate_orbits']['translation_triple_orbit_sizes'],[3]*4+[9]*8)
    def test_b03_baryon_min_closed_rank_size(self):
        self.assertEqual(self.result['SIC_H27_baryon_coordinate_orbits']['full_rank_minimum_closed_baryon_count'],27)
    def test_b04_baryon_all_subsets_tested(self):
        self.assertEqual(self.result['SIC_H27_baryon_coordinate_orbits']['translation_closed_subsets_examined'],4096)
    def test_b05_baryon_rank_census_24_all_fail(self):
        self.assertEqual(self.result['SIC_H27_baryon_coordinate_orbits']['rank_census_through_27']['24'],{'17':96,'18':72})
    def test_b06_baryon_27_full_rank_count(self):
        self.assertEqual(self.result['SIC_H27_baryon_coordinate_orbits']['minimum_27_subset_full_rank_count'],72)
    def test_c01_twirl_nine_exact_for_general_detector(self):
        self.assertLess(self.result['SU3_detector_Weyl_twirl']['max_complex_trace_error_9_setting_48_trials'],1e-12)
    def test_c02_twirl_three_only_diagonal(self):
        r=self.result['SU3_detector_Weyl_twirl']['example_errors'];self.assertLess(r[0]['three_shift_error'],1e-12);self.assertGreater(r[1]['three_shift_error'],1e-4)
    def test_c03_twirl_accepted_shot_budget(self):
        self.assertEqual(self.result['SU3_detector_Weyl_twirl']['accepted_detections_per_phase_sufficient_Hoeffding'],8426)
    def test_d01_g2_exact_stabilizer(self):
        self.assertEqual(self.result['real_G2_Albert_multiplets']['G2_generator_count'],14)
    def test_d02_g2_exact_schur_commutant(self):
        self.assertEqual(self.result['real_G2_Albert_multiplets']['real_7d_commutant_dimension'],1)
    def test_d03_albert_mass_7fold(self):
        self.assertTrue(self.result['real_G2_Albert_multiplets']['example_7fold_mass_multiplicity_exact'])
        self.assertEqual(self.result['real_G2_Albert_multiplets']['real_symmetric_G2_equivariant_mass_parameter_count'],27)
    def test_e01_causal_63_classes(self):
        self.assertEqual(self.result['causal_oriented_invariant']['five_event_isomorphism_classes'],63)
    def test_e02_causal_24_dual_pairs(self):
        self.assertEqual(self.result['causal_oriented_invariant']['distinct_nonselfdual_pairs'],24)
    def test_e03_causal_odd_statistic_blind_pair(self):
        r=self.result['causal_oriented_invariant'];self.assertEqual(r['nonself_dual_pairs_detected'],23);self.assertEqual(r['nonself_dual_pairs_blind'],1)
    def test_f01_certificate_persisted(self):
        self.assertTrue(mod.OUT.exists())

if __name__=='__main__':unittest.main()
