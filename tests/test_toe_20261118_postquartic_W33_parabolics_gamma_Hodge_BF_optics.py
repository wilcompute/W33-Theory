"""Regression: five post-quartic fronts plus W33 dual radicals and full E6 gamma."""
import sys,math,unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/"analysis"))
import toe_20261118_post_quartic_fivefront_hodge_GS_selector_BF_optics as M
import toe_20261118_W33_dual_parabolic_radicals_27 as G
import toe_20261118_W33_ordered_flag_H27_kernel as O
import toe_20261118_E6_full_spinor_symmetric_gamma10 as Y

class AdvancedTOE(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.m=M.run()
        cls.g=G.run()
        cls.o=O.run()
        cls.y=Y.run()

    def test_wire_hodge_relative_modes_exact(self):
        z=self.m["boundary_hodge"]["cases"]
        for q in z:
            self.assertEqual(q["Hodge_D_kernel"],q["defects"])
            self.assertEqual(q["betti"],[0,q["relative_spheres"],
                                          q["defects"]-q["relative_spheres"],0])
            self.assertEqual(q["formal_chiral_excess"],
                             2*q["relative_spheres"]-q["defects"])

    def test_wire_hodge_spectral_gap_and_hermiticity(self):
        self.assertTrue(all(abs(q["spectral_gap"]-1)<1e-12
                            for q in self.m["boundary_hodge"]["cases"]))
        self.assertEqual([x["formal_chiral_excess"] for x in
                          self.m["boundary_hodge"]["cases"] if x["defects"]==3
                          and x["monodromy"]=="2"],[3,1,-1])

    def test_GS_anomaly_pure_chi_vanishes(self):
        z=self.m["anomaly_GS"]
        self.assertIn("b*(",z["U1_cubic_factorization"])
        self.assertEqual(z["U1_gravity_polynomial"],"-144*b")

    def test_GS_universal_SU5_mixed_coeffs(self):
        z=self.m["anomaly_GS"]
        self.assertEqual(set(z["GUT_normalized_mixed_anomalies"].values()),{-18.0})
        self.assertFalse(z["can_SM_singlets_alone_cancel_mixed_SU3_SU2_anomaly"])

    def test_stueckelberg_plus_higgs_rank(self):
        z=self.m["anomaly_GS"]
        self.assertEqual(z["mass_determinant"],"25*k^2*v^2 >0 when both nonzero")
        self.assertIn("UV anomaly inflow",z["residual_issue"])

    def test_W33_selector_all_160_flags_and_gap(self):
        z=self.m["W33_selector"]
        self.assertEqual((z["points"],z["lines"],z["flags"]),(40,40,160))
        self.assertAlmostEqual(z["invariant_selector_energy_min"],-2.6)
        self.assertLess(z["invariant_selector_energy_min"],z["uniform_energy"])

    def test_S3_six_non_degenerate_minima(self):
        z=self.m["W33_selector"]
        self.assertEqual(len(z["six_scalar_minima_at_A1"]),6)
        self.assertEqual(z["combined_degenerate_vacua"],960)
        self.assertAlmostEqual(z["Hessian_eigenvalues_at_A1"][0],4-2*math.sqrt(2))
        self.assertAlmostEqual(z["Hessian_eigenvalues_at_A1"][-1],4+2*math.sqrt(2))

    def test_point_radical_is_genuine_H27(self):
        z=self.g["point_parabolic"]
        self.assertEqual((z["parabolic_order"],z["Sylow3_order"],z["O3_order"]),(648,81,27))
        self.assertEqual(z["O3_center_order"],3)
        self.assertEqual(z["O3_derived_order"],3)
        self.assertEqual(z["O3_element_order_counts"],{"1":1,"3":26})

    def test_line_radical_is_Abelian_C3cubed(self):
        z=self.g["isotropic_line_parabolic"]
        self.assertEqual(z["O3_order"],27)
        self.assertEqual(z["O3_center_order"],27)
        self.assertEqual(z["O3_derived_order"],1)
        self.assertEqual(z["O3_element_order_counts"],{"1":1,"3":26})

    def test_point_H27_irreducible_qutrit(self):
        z=self.g["qutrit_Schrodinger"]
        self.assertEqual(z["qutrit_Pauli_group_order"],27)
        self.assertEqual(z["commutant_dimension"],1)
        self.assertTrue(z["is_irreducible"])
        self.assertIn("omega^2",z["qutrit_clock_shift_commutator"])

    def test_ordered_flag_stabilizer_distinct_from_H27(self):
        z=self.o
        self.assertEqual(z["ordered_flag_configurations"],960)
        self.assertEqual(z["pointwise_triplet_stabilizer_order"],27)
        self.assertEqual(z["pointwise_stabilizer_center_order"],27)
        self.assertIn("NOT nonabelian Heisenberg",z["group_classification"])

    def test_native_full_E6_symmetric_spinor_tensor(self):
        z=self.y
        self.assertEqual(z["spinor_dimension"],16)
        self.assertEqual(z["full_symmetric_pairs"],136)
        self.assertEqual(z["symmetric_square_image_rank"],10)

    def test_native_gamma_SU5_branch_selection(self):
        z=self.y["SU5_branch_pair_ranks"]
        self.assertEqual([z[k]["image_rank"] for k in
                          ("10x10","10x5bar","5barx1")],[5,5,5])
        self.assertEqual([z[k]["image_rank"] for k in
                          ("10x1","5barx5bar","1x1")],[0,0,0])

    def test_coupled_BF_kinetic_budget(self):
        vals=self.m["coupled_BF"]["robust_model_rows"]
        v=next(x for x in vals if x["r"]==2 and
               x["mass_shift_bound"]==.5 and x["kinetic_norm_bound"]==.125)
        self.assertAlmostEqual(v["effective_budget"],1)
        self.assertAlmostEqual(v["robustly_unstable_modular_fraction"],.4531221083700141)

    def test_offdiagonal_coupling_cannot_cure_trial_mode(self):
        z=self.m["coupled_BF"]
        self.assertEqual(z["guaranteed_unstable_triple_count"],200)
        self.assertLess(z["worst_random_min_generalized_mass_sq"],-4)

    def test_adaptive_herald_martingale_null(self):
        z=self.m["adaptive_photon"]
        self.assertEqual(z["predictable_four_cycle_kappa"],[1.,1.1,1.05,1.])
        self.assertTrue(z["all_600_per_step_null_multiplier_equal_one"])
        self.assertEqual(z["analytic_anytime_null_false_positive_max"],.01)

    def test_adaptive_alternative_power_and_error_bars(self):
        z=self.m["adaptive_photon"]
        self.assertEqual(z["MonteCarlo_paths"],50000)
        self.assertAlmostEqual(z["simulated_detection_by_n"]["600"],.99462,places=8)
        self.assertLess(z["approximate_95pct_power_interval"][0],.99462)
        self.assertGreater(z["approximate_95pct_power_interval"][1],.99462)
        self.assertTrue(155<z["simulated_mean_truncated_accepted"]<165)


if __name__=="__main__":
    unittest.main()
