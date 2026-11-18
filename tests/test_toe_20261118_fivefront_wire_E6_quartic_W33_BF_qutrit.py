"""Exact and numerical tests for W33/E6 five-front continuation."""
import math,sys,unittest
from pathlib import Path
import sympy as sp
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/"analysis"))
import toe_20261118_fivefront_wire_domain_E6_S3_analyticBF_anytime_loss as F
import toe_20261118_native_E6_quartic_two_step as E


class FiveFrontCheck(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.x=F.run()
        cls.y=E.run()

    def test_relative_all_holonomies_and_boundary_choices(self):
        self.assertEqual(self.x["boundary"]["cases"],4*sum(range(1,8)))
        for item in self.x["boundary"]["m3_sensitivity"]:
            self.assertEqual(item["b1"],item["r"])
            self.assertEqual(item["b2"],3-item["r"])
            self.assertEqual(item["index"],2*item["r"]-3)

    def test_boundary_index_changes_if_one_physical_defect_unseen(self):
        z=self.x["boundary"]["m3_sensitivity"]
        self.assertEqual([(i["r"],i["index"]) for i in z],[(1,-1),(2,1),(3,3)])

    def test_rank_two_charge_repair(self):
        g=self.x["gauge"]
        self.assertEqual(g["rank2_mass_matrix"],[[25,15],[15,25]])
        self.assertEqual(g["eigenvalues"],[10,40])
        self.assertEqual(g["determinant"],400)
        self.assertEqual(g["Dflat_minimal_algebraic_oppositely_charged_pair_set"],
                         [[-5,-3],[5,3],[0,4],[0,-4]])

    def test_repair_needs_new_fields_and_inflow(self):
        g=self.x["gauge"]
        self.assertFalse(g["existing_same_sheet_cubic_Yukawa_possible_with_27_or_27bar"])
        self.assertEqual(g["residual_anomaly_unaffected_by_vectorlike_pairs"]["gravity_Psi"],-144)

    def test_exact_native_quartic_two_step(self):
        self.assertEqual(self.y["native_E6_adj_dim"],78)
        self.assertEqual(self.y["localized_ten_dim"],10)
        self.assertEqual(self.y["first_action_rank"],10)
        self.assertEqual(self.y["second_action_rank"],5)
        self.assertEqual(self.y["nonzero_symmetric_pairs"],30)
        self.assertEqual(self.y["weak_doublet_rank"],2)
        self.assertEqual(self.y["weak_doublet_hypercharge_Q6Y"],-3)
        self.assertEqual(self.y["color_triplet_rank"],3)
        self.assertEqual(self.y["color_triplet_hypercharge_Q6Y"],2)
        self.assertTrue(self.y["adjoint_brackets_all_zero"])

    def test_native_cubic_singlet_path_and_weights(self):
        self.assertTrue(self.y["native_nu_adjoint_singlet_action_nonzero"])
        self.assertEqual(self.y["native_nu_image_charge_PsiChiY"],[1,-5,0])
        self.assertEqual(self.y["charge_balanced_78_27bar_27_singlet_VEVs"],
                         [[-5,-3],[5,-1],[0,4]])

    def test_native_D_F_flat_three_singlet_toy(self):
        self.assertTrue(self.y["compact_E6_weight_vector_D_flat"])
        self.assertTrue(self.y["toy_F_flat_all_components"])
        self.assertEqual(self.y["full_Abelian_Higgs_mass_matrix"],[[50,10],[10,26]])
        self.assertEqual(self.y["mass_matrix_determinant"],1200)
        self.assertEqual(self.y["scalar_Hessian_rank_in_three_singlet_subspace"],1)

    def test_chiral_anomaly_unresolved(self):
        self.assertIn("anomaly",self.y["unrepaired_anomalous_Psi"].lower())

    def test_w33_native_stabilizer_S3(self):
        g=self.x["W33"]
        self.assertEqual(g["group_order"],25920)
        self.assertEqual(g["flag_stabilizer_order"],162)
        self.assertEqual(g["W33_flags"],160)
        self.assertEqual(g["induced_permutation_group"],"S3")
        self.assertEqual(g["conjugacy_class_fixed_point_counts"],{"3":1,"1":3,"0":2})

    def test_w33_twofold_mass_degeneracy(self):
        self.assertEqual(self.x["W33"]["mass_eigenvalues"],{"a":2,"a+3b":1})

    def test_analytic_modular_area_stability(self):
        self.assertEqual(F.below_area(.5),0.)
        self.assertAlmostEqual(F.below_area(1.),1-3/math.pi)
        self.assertAlmostEqual(F.below_area(2.),1-3/(2*math.pi))

    def test_strict_BF_violation_band(self):
        for z in self.x["winding"]["samples"]:
            self.assertGreaterEqual(z["unsafe_fraction"],-1e-12)
            self.assertLessEqual(z["unsafe_fraction"],1+1e-12)
        a=next(z for z in self.x["winding"]["samples"]
               if z["r"]==2 and z["delta"]==1)
        self.assertAlmostEqual(a["unsafe_fraction"],.453122108370014,places=10)

    def test_optional_stopping_null_control_all_calibrations(self):
        for z in self.x["memory"]["exact_bounded_loss_sequential_results"]:
            self.assertLess(z["null_p"],z["alternative_p"])
            self.assertTrue(all(v<=.0100000001 for v in z["null_false_positive_by_n"].values()))

    def test_detection_power_falls_with_acceptance_bias(self):
        z=self.x["memory"]["exact_bounded_loss_sequential_results"]
        powers=[row["alternative_detection_by_n"]["600"] for row in z]
        self.assertTrue(all(a>b for a,b in zip(powers,powers[1:])))
        self.assertAlmostEqual(powers[0],.9987565333830355,places=10)
        self.assertAlmostEqual(powers[-1],.294715573185316,places=10)

    def test_expected_shots_increase_with_bias(self):
        z=self.x["memory"]["exact_bounded_loss_sequential_results"]
        costs=[row["alternative_expected_truncated_accepted"] for row in z]
        self.assertTrue(all(a<b for a,b in zip(costs,costs[1:])))
        self.assertLess(costs[0],125)
        self.assertGreater(costs[-1],760)


if __name__=="__main__":unittest.main()
