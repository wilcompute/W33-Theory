"""22 regression checks for the five global TOE closure fronts.

The test suite verifies mathematics/conditional statistics, not hardware,
11D full KK mixing, physical localized matter, or a complete TOE.
"""
import sys,unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/"analysis"))
import toe_20261118_fivefront_global_physics_closure as C

class GlobalClosure(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.parts=C.run()["parts"]
    def test_FR_AdS4_bound(self):
        self.assertEqual(self.parts["AdS4"]["BF_AdS4"],"-9/4")
    def test_FR_radius(self):
        self.assertEqual(self.parts["AdS4"]["S7_over_AdS4_radius"],2)
    def test_FR_breathing_mass(self):
        self.assertEqual(self.parts["AdS4"]["breathing_canonical_m2L2"],18)
    def test_FR_scalar_zero_mode(self):
        self.assertEqual(self.parts["AdS4"]["test_scalar_m2L2_first10"][0],"0")
    def test_FR_scalar_l1(self):
        self.assertEqual(self.parts["AdS4"]["test_scalar_m2L2_first10"][1],"7/4")
    def test_E8_family_triple_anomaly(self):
        self.assertEqual(self.parts["E8_family"]["isolated_chiral_27_triplet_SU3_cubed_anomaly"],27)
    def test_E8_family_cancel_with_conjugate(self):
        self.assertEqual(self.parts["E8_family"]["complete_adj_conjugate_pair_SU3_cubed_anomaly"],0)
    def test_E8_H27_commutant(self):
        self.assertEqual(self.parts["E8_family"]["H27_traceless_SU3_commutant_dim"],0)
    def test_PW_harmonic(self):
        self.assertEqual(self.parts["PW_global"]["laplacian"],0)
    def test_PW_energy_leading(self):
        self.assertIn("R^9",self.parts["PW_global"]["energy_ball_R"])
    def test_PW_energy_tilt(self):
        self.assertIn("a^2*R^3",self.parts["PW_global"]["energy_ball_R"])
    def test_PW_infinite_global_energy(self):
        self.assertFalse(self.parts["PW_global"]["global_source_free_finite_energy_R3"])
    def test_PW_compact_closed_no_exact_nonconstant_harmonic(self):
        self.assertFalse(self.parts["PW_global"]["smooth_closed_compact_nonconstant_exact_harmonic_f_possible"])
    def test_E6_invariant_ring(self):
        self.assertEqual(self.parts["E6"]["singlet_invariant_ring"],"C[xyz]")
    def test_E6_no_renormalizable_singlet_Fflat(self):
        self.assertTrue(self.parts["E6"]["no_nonzero_all_threeVEV_Fflat_with_only_renormalizable_cubic"])
    def test_E6_Hessian_rank(self):
        self.assertEqual(self.parts["E6"]["general_analytic_fI_at_stationary_dI_nonzero_Hessian_rank_at_most"],1)
    def test_E6_moduli(self):
        self.assertEqual(self.parts["E6"]["smooth_one_invariant_moduli_complex_lower_bound"],65)
    def test_E6_conditional_k_constraints(self):
        self.assertEqual(self.parts["E6"]["separable_k_constraints_reduced_moduli_lower_bound"],"max(0,66-k)")
    def test_photon_power_450(self):
        self.assertAlmostEqual(self.parts["photon_power"]["rows"][1]["model_exact_rejection_power"],.66128121221282,places=8)
    def test_photon_power_600(self):
        self.assertGreater(self.parts["photon_power"]["rows"][2]["model_exact_rejection_power"],.9)
    def test_photon_900(self):
        self.assertGreater(self.parts["photon_power"]["rows"][3]["model_exact_rejection_power"],.99)
    def test_photon_not_actual_experiment(self):
        self.assertTrue(self.parts["photon_power"]["not_experimental_data"])
if __name__=="__main__":unittest.main()
