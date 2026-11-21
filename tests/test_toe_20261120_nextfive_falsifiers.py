"""Five experimental-design/finite-geometry gates with explicit prior-art boundaries."""
import sys,unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/"analysis"))
import toe_20261120_nextfive_falsifiers as F

class NextFive(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.r=F.run(write=False)
        cls.a=cls.r["selection"];cls.b=cls.r["exceptional"]
        cls.c=cls.r["tomography"];cls.d=cls.r["reference"];cls.e=cls.r["continuum"]
    def test_01_status(self):self.assertEqual(self.r["status"],"PASS_FIVE_FOLLOWTHROUGH_GATES")
    def test_02_chart_count(self):self.assertEqual(self.a["charts"],45)
    def test_03_chart_kernel_rank(self):self.assertEqual(self.a["M_rank"],25)
    def test_04_chart_kernel_eigenspaces(self):self.assertEqual(self.a["K_spectrum"],{72:1,12:24,0:20})
    def test_05_disjoint_chart_graph(self):self.assertEqual(self.a["disjoint_graph_srg"],[45,12,3,3])
    def test_06_noncmt_pairs(self):self.assertEqual(self.a["all_noncmt_pairs"],540)
    def test_07_selecting_pairs_per_chart(self):self.assertEqual(self.a["unique_pairs_per_chart"],12)
    def test_08_energy_source_noncommuting(self):self.assertEqual(self.a["source_spectra"]["noncommuting"],[1,16,28])
    def test_09_energy_source_commuting(self):self.assertEqual(self.a["source_spectra"]["commuting"],[3,12,30])
    def test_10_beta10_ground_probability(self):self.assertGreater(self.a["source_ground_probability_beta10"],.90)
    def test_11_positive_toy_masses(self):self.assertEqual(self.a["vacuum_amplitude_quadratic_fluctuation_coefficients"],{"6J":32,"8J":12})
    def test_12_fortyfive_degenerate_vacua(self):self.assertEqual(self.a["invariant_action_global_vacua"],45)
    def test_13_all_projection_centers(self):self.assertEqual(self.b["centers_tested"],1093)
    def test_14_isotropic_projection_undefined(self):self.assertEqual(self.b["isotropic_centers_undefined"],364)
    def test_15_projection_norm_one(self):self.assertEqual((self.b["norm1_centers"],self.b["norm1_distinct_images"]),(351,238))
    def test_16_projection_norm_two(self):self.assertEqual((self.b["norm2_centers"],self.b["norm2_distinct_images"]),(378,247))
    def test_17_projection_fiber_histograms(self):self.assertEqual(self.b["norm1_fibers"],{"single":112,"double":126})
    def test_18_classical_garbling_POVM(self):self.assertEqual(self.c["classical_parity_garbling_rates"],{"even":.4,"odd":.25})
    def test_19_parity_operator_identity(self):self.assertLess(self.c["projector_sum_error"],1e-10)
    def test_20_local_displaced_parity(self):self.assertTrue(self.c["physical_parity_is_local_tensor_product"])
    def test_21_exact_variance_penalty(self):self.assertAlmostEqual(self.c["maxmixed_variance_ratio_randomized_to_direct"],40,places=8)
    def test_22_ideal_1pct_shots(self):
        self.assertEqual((self.c["randomized_Hoeffding_shots_both_errors_below_1pct"],
                          self.c["randomized_binomial_deterministic_shots_size_1pct_power_99pct"],
                          self.c["randomized_binomial_randomized_boundary_shots_size_1pct_power_99pct"],
                          self.c["direct_parity_shots_size_1pct_power_100pct_for_pure_odd"]),
                         (1638,791,785,7))
        self.assertLess(self.c["randomized_binomial_deterministic_actual_false_positive"],.01)
        self.assertGreater(self.c["randomized_binomial_deterministic_actual_power"],.99)
    def test_23_E8_scalar_phases_same_density(self):self.assertLess(self.d["global_phase_projector_error"],1e-10)
    def test_24_coherent_phase_copy_budget(self):self.assertEqual(self.d["first_hypothetical_copy_count_above_99pct"],14)
    def test_25_one_copy_phase_information(self):self.assertAlmostEqual(self.d["hypothetical_coherently_referenced_one_copy_PGM_success"],1/3)
    def test_26_naive_graph_diameter(self):self.assertEqual(self.e["point_graph_diameters"],{"W(3,q)":2,"H(q)":3})
    def test_27_GH_collapse(self):self.assertAlmostEqual(self.e["GH_distance_lower_bound_to_any_unit_diameter_compact_space_limit"],.5)
    def test_28_running_dimension_not_dimension_four(self):
        h=self.e["computed_heat_spectral_dimension_peaks"]
        self.assertLess(h["W33"]["peak"],4)
        self.assertGreater(h["H3"]["peak"],4)

if __name__=="__main__":unittest.main()
