"""Regression certificate: E6 scalar moduli, BF cusp tower, W33 H27 projector,
G2 wire relative Morse limitation, and pairwise classical qutrit memory."""
import math,sys,unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/"analysis"))
import toe_20261118_E6_flatness_BF_cusp_tower_wire_index_gate as E
import toe_20261118_qutrit_genuine_multitime_block_lift as Q
import toe_20261118_W33_address_operator_central_projector_probability as H

class NewResearch(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.e=E.run()
        cls.q=Q.run()
        cls.h=H.run()

    def test_E6_full_132_chiral_dimension(self):
        x=self.e["E6_flat_vacuum"]
        self.assertEqual(x["full_chiral_complex_coordinates"],132)
        self.assertEqual(x["exact_full_Fflat_hessian_rank"],1)

    def test_E6_codimension_one_Fflat_locus(self):
        x=self.e["E6_flat_vacuum"]
        self.assertEqual(x["Fflat_smooth_complex_hypersurface_dimension"],131)
        self.assertEqual(x["verified_three_singlet_subspace_Hessian"],[[-1]*3]*3)

    def test_E6_moduli_lower_bound_if_SM_survives(self):
        x=self.e["E6_flat_vacuum"]
        self.assertEqual(x["maximal_broken_complex_E6_generators_with_SM_preserved"],66)
        self.assertEqual(x["local_F_and_D_flat_complex_moduli_lower_bound"],65)
        self.assertEqual(x["tree_level_uneaten_real_flat_directions_lower_bound"],130)

    def test_charge_index20_is_conditional_not_physical_assertion(self):
        x=self.e["E6_flat_vacuum"]
        self.assertEqual(x["Abelian_charge_Smith_diagonal"],[1,20])
        self.assertIn("covering torus",x["conclusion"])

    def test_BF_cusp_count_grows(self):
        cases=[z for z in self.e["BF_cusp_tower"]["cases"] if z["flux_ratio"]==1]
        self.assertEqual([z["oriented_BF_unsafe_horizontal_vectors"] for z in cases],
                         [22,70,224,712])
        self.assertEqual([z["oriented_robust_subband_vectors"] for z in cases],
                         [4,12,32,104])

    def test_BF_count_asymptotic_normalization(self):
        z=next(t for t in self.e["BF_cusp_tower"]["cases"]
               if t["flux_ratio"]==1 and t["height"]==100000)
        self.assertAlmostEqual(z["normalized_unsafe_count_over_sqrt_y"],
                               4/math.sqrt(math.pi),delta=.05)

    def test_BF_subband_robust_margin(self):
        for z in self.e["BF_cusp_tower"]["cases"]:
            self.assertGreater(z["conservative_BF_deficit_lower_bound"],2.16)
            self.assertGreaterEqual(z["oriented_robust_subband_vectors"],0)
            self.assertLessEqual(z["oriented_robust_subband_vectors"],
                                 z["oriented_BF_unsafe_horizontal_vectors"])

    def test_wire_relative_three_does_not_force_bulk_critical_point(self):
        z=self.e["wire_harmonic"]
        self.assertEqual(z["relative_betti_three"],[0,3,0,0])
        self.assertEqual(z["relative_Euler_characteristic"],-3)
        self.assertIn("no interior zero",z["smooth_nowhere_vanishing_closed_1form"])

    def test_Qutrit_CPTP_full_Choi_all_three_pairs(self):
        for z in self.q["three_time_qutrit_block_embeddings"]:
            self.assertTrue(z["qutrit_CPTP"])
            self.assertLess(max(z["qutrit_Choi_errors"]),1e-12)

    def test_Qutrit_genuine_memory_original_sector_preserved(self):
        for z in self.q["three_time_qutrit_block_embeddings"]:
            self.assertAlmostEqual(z["qutrit_embedded_three_time_W"],-z["gamma"])
            self.assertGreaterEqual(z["p"],z["pairwise_classical_threshold"])

    def test_qutrit_extension_not_intrinsically_3level(self):
        self.assertTrue(self.q["embedded_not_intrinsically_qutrit"])
        self.assertIn("two-level",self.q["qubit_channel_support"]+" two-level")

    def test_two_qutrit_cubic_resource_outside_quadratic_clifford(self):
        x=self.q["cubic_resource_compare"]
        self.assertEqual(x["cubic_mixed_finite_difference"],2)
        self.assertFalse(x["qutrit_two_body_cubic_gate_is_Clifford"])
        self.assertTrue(x["cubic_is_outside_native_27_quadratic_phase_subgroup"])

    def test_W33_three_center_projector_ranks(self):
        x=self.h["source_regular_character_sector_ranks"]
        self.assertEqual([x[k]["exact_projector_rank"] for k in ("0","1","2")],[9,9,9])

    def test_W33_computational_address_success_third(self):
        self.assertAlmostEqual(self.h["probability_for_each_of_27_address_basis_states"],1/3)
        self.assertAlmostEqual(self.h["probability_for_maximally_mixed_address"],1/3)
        self.assertEqual(self.h["worst_case_input_success_probability"],0)

    def test_W33_no_unitary_regular_operator_intertwiner(self):
        self.assertEqual(self.h["equivariant_linear_map_rank_upper_bound"],9)
        self.assertEqual(self.h["E6_operator_representation_dimension"],27)
        self.assertTrue(self.h["fourier_projectors_pairwise_orthogonal"])

if __name__=="__main__":unittest.main()
