"""Focused physics-first TOE followthrough regression, no W33 assumptions."""
import sys, unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"analysis"))
import toe_20261119_TOE_five_fronts_new_physics_crosschecks as theory

class TOEFivePhysicalFronts(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.cup=theory.compact_topology_cup()
        cls.yuk=theory.charged_family_texture()
        cls.sing=theory.e8_singlet_cone()
        cls.grav=theory.einstein_scalar_constraint()
        cls.mem=theory.memory_capacity_gate()
        cls.gut=theory.two_split_gut_gate()

    def test_punctured_torus_relative_triple_cup_nonzero(self):
        self.assertAlmostEqual(self.cup["cup_product_integral"],1.0,places=12)
        self.assertTrue(self.cup["relative_triple_cup_is_nonzero"])

    def test_relative_representatives_vanish_on_boundary(self):
        self.assertTrue(self.cup["vanish_near_boundary"])
        self.assertEqual(self.cup["relative_H1_rank"],3)

    def test_hollow_complex_symmetric_takagi_hierarchy_no_go(self):
        self.assertEqual(self.yuk["random_complex_matrices_checked"],6000)
        self.assertLess(self.yuk["max_numeric_inequality_violation"],1e-11)
        self.assertIn("s1<=s2+s3",self.yuk["exact_takagi_inequality"])

    def test_physical_hierarchy_requires_order_one_texture_correction(self):
        self.assertGreater(self.yuk["spectral_norm_minimum_nonhollow_correction"],.32)
        self.assertLess(self.yuk["spectral_norm_minimum_nonhollow_correction"],.34)

    def test_actual_e8_charged_singlet_Dflat_triangle(self):
        self.assertEqual(self.sing["charged_singlet_multiplets"],8)
        self.assertEqual(self.sing["Dflat_triangle_charge_sum"],[0,0,0])
        self.assertEqual(self.sing["combined_Dflat_pair_and_triangle"],[0,0,0])
        self.assertTrue(self.sing["Dflat_nonzero_Spin10_singlet_condensate_exists_at_zero_FI"])

    def test_diagonal_yukawa_one_singlet_selections(self):
        c=self.sing["one_singlet_spurion_diagonal_selection"]
        self.assertIn({"Higgs":"10_34","spurion":"S_12_conj"},c["16_1^2"])
        self.assertIn({"Higgs":"10_34","spurion":"S_12"},c["16_2^2"])
        self.assertIn({"Higgs":"10_24","spurion":"S_13"},c["16_3^2"])

    def test_Fflatness_is_not_implied_by_Dflatness(self):
        self.assertIn("nonzero F-terms",self.sing["Fflat_warning"])

    def test_FRW_Einstein_constraint_preserved(self):
        self.assertLess(self.grav["max_constraint_drift_consistent"],1e-10)
        self.assertGreater(self.grav["max_constraint_drift_gamma_1p05"],.001)
        self.assertAlmostEqual(self.grav["midpoint_Cdot_prediction"],
                               self.grav["midpoint_Cdot_finite_difference"],places=6)

    def test_quantum_Bell_witness_with_zero_unassisted_capacity(self):
        self.assertGreater(self.mem["unconditional_Bell_witness_probability"],1/3)
        self.assertAlmostEqual(self.mem["unconditional_Bell_witness_probability"],.37)
        self.assertEqual(self.mem["unassisted_Q_of_pure_qutrit_erasure"],0.)

    def test_memory_event_ready_binomial_power(self):
        rows=self.mem["sample_size_power_rows"]
        self.assertEqual(len(rows),3)
        self.assertGreater(rows[0]["exact_binomial_power_at_n"],.9)
        self.assertGreater(rows[0]["n_approx_90pct_power_at_0p1pct_typeI"],3000)

    def test_two_split_GUT_escapes_one_pair_mass_ordering(self):
        self.assertTrue(self.gut["single_pair_no_go"])
        self.assertTrue(self.gut["two_pairs_satisfy_mass_ordering_with_example"])
        self.assertLess(self.gut["one_loop_unification_spread"],1e-10)
        self.assertLess(self.gut["two_pairs_mD_GeV"],self.gut["formal_unification_MU_GeV"])

    def test_gut_scale_is_still_low_and_proton_risky(self):
        self.assertLess(self.gut["formal_unification_MU_GeV"],1e14)
        self.assertLess(self.gut["relative_dimension_six_proton_lifetime_to_MX_1e16_same_couplings"],1e-8)

if __name__=="__main__":unittest.main()
