"""Regression tests for five physical TOE gates, independent of W33 geometry."""
import sys,unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"analysis"))
import toe_20261119_five_physical_gates_beyond_W33 as toe

class FivePhysicalGates(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.chiral=toe.independent_chirality_gate()
        cls.parent=toe.asymptotically_free_parent()
        cls.covariant=toe.covariance_test()
        cls.quantum=toe.quantum_resource_gate()
        cls.running=toe.gauge_running_gate()

    def test_local_Morse_index_minus_three(self):
        self.assertEqual(len(self.chiral["f1_local_critical_points"]),3)
        self.assertEqual(self.chiral["local_gradient_index_sum"],-3)
        self.assertTrue(all(t["local_gradient_index"]==-1 for t in self.chiral["f1_local_critical_points"]))

    def test_compact_closed_odd_dimensional_index_zero(self):
        self.assertEqual(self.chiral["S3_boundary_simplex_euler"],0)
        self.assertEqual(self.chiral["T3_euler"],0)
        self.assertIn("compensating",self.chiral["compactness_obstruction"])

    def test_mirror_yukawa_rank_no_go(self):
        self.assertEqual(self.chiral["net_16_chirality_index"],3)
        self.assertEqual(self.chiral["bare_six_family_star_Yukawa_rank_upper_bound"],2)
        self.assertEqual(self.chiral["projected_three_light_family_Yukawa_ranks"],[2])
        self.assertEqual(self.chiral["random_full_rank_three_mirror_mixings_checked"],64)

    def test_no_surviving_unmixed_ab_anomaly_free_U1(self):
        self.assertEqual(self.chiral["primitive_common_mixed_anomaly_kernel"],[14,-7,-9])
        self.assertEqual(self.chiral["local_source_primitive_kernel_pure_cubic"],49032)

    def test_asymptotic_freedom_of_parent(self):
        self.assertEqual(self.parent["SU4_perturbative_one_loop_b0"],2)
        self.assertEqual(self.parent["intermediate_SU3_b0_if_nine_light_flavors"],0)
        self.assertEqual(self.parent["UV_vectorlike_cubic_gauge_anomaly"],0)
        self.assertLess(self.parent["full_Dflat_moment_max_abs"],1e-12)

    def test_parent_embeds_SIC_without_F_flat_selection_claim(self):
        self.assertEqual(len(self.parent["lifted_SIC_frame_eigenvalues"]),3)
        self.assertGreater(self.parent["SU4_baryon_three_SIC_plus_Higgsing_flavor_abs"],0)
        self.assertIn("f-flat",self.parent["critical_missing_step"].lower())

    def test_worldsheet_constraint_bracket_refinement(self):
        rows=self.covariant["numeric_bracket_test"]
        self.assertEqual([p["N"] for p in rows],[32,64,128,256])
        self.assertTrue(all(p["spectral_bracket_defect"]<1e-11 for p in rows))
        self.assertGreater(self.covariant["high_frequency_alias_defect"],.1)

    def test_single_photon_capacity_scaling(self):
        self.assertEqual(self.quantum["max_qubits_in_40_single_photon_modes"],5)
        entries=self.quantum["examples"]
        self.assertEqual(entries[0]["minimum_single_photon_orthogonal_modes"],16)
        self.assertEqual(entries[-1]["minimum_single_photon_orthogonal_modes"],2**60)
        self.assertGreater(entries[-1]["nonoverlap_1ns_time_bin_duration_seconds"],1e9)

    def test_memory_and_unencoded_T9(self):
        self.assertEqual(self.quantum["qutrit_memory_min_environment_Schmidt_rank"],3)
        self.assertGreater(self.quantum["required_detection_efficiency_to_beat_entanglement_breaking_1over3"],.4)
        self.assertLess(self.quantum["T9_injection_worst_statevector_error"],1e-12)
        self.assertEqual(self.quantum["T9_one_qudit_injection_outcomes_tested"],48)

    def test_measured_SM_one_loop_no_exact_unification(self):
        self.assertAlmostEqual(self.running["inputs"]["alpha_s_MSbar_MZ"],.1177)
        self.assertGreater(self.running["SM_inverse_alpha3_mismatch"],-6)
        self.assertLess(self.running["SM_inverse_alpha3_mismatch"],-5)
        self.assertGreater(self.running["SM_one_loop_pairwise_crossing_GeV"]["23"],1e16)

    def test_MSSM_is_comparator_not_TOE_prediction(self):
        self.assertAlmostEqual(self.running["beta_idealized_MSSM"][0],6.6)
        self.assertLess(abs(self.running["SM_to_1TeV_then_MSSM_inverse_alpha3_mismatch"]),1)
        self.assertGreater(abs(self.running["SM_to_1TeV_then_MSSM_inverse_alpha3_mismatch"]),.4)

if __name__=="__main__":
    unittest.main()
