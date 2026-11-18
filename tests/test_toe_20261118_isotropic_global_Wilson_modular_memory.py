"""Regression suite: native W33 isotropy versus symmetry, E6 Wilson and defects,
modular winding measure, and operational quantum-memory robustness."""
import math,sys,unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/"analysis"))
import toe_20261118_isotropic_Levi_symmetry_no_go as W
import toe_20261118_fivefront_global_Wilson_modular_photonic as P


class TOEFrontTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.w=W.run()
        cls.p=P.run()

    def test_exhaustive_voltage_census(self):
        x=self.w["optimization"]
        self.assertEqual(x["total_triplets"],85320)
        self.assertEqual(x["min_triplet_count"],10152)
        self.assertEqual(x["min_score"],12)
        self.assertEqual(x["indices"],[0,4,8])
        self.assertEqual(x["selected"],[(1,45),(2,50),(3,55)])

    def test_diffusion_tensor_near_isotropic(self):
        x=self.w["optimization"]
        self.assertEqual(x["D_eigen_numerators_12800"],[80,80,83])
        self.assertAlmostEqual(x["anisotropy_condition_ratio"],83/80)
        self.assertEqual(x["off_diagonal_Gram320_counts"],
                         {"-54":162,"-6":1134,"2":1620,"18":324})

    def test_bloch_error_and_full_flag_transitivity(self):
        self.assertLess(self.w["optimization"]["bloch_checks"][-1]["relative_error"],.001)
        z=self.w["symmetry"]
        self.assertEqual(z["checked_symplectic_transvections"],40)
        self.assertEqual(z["flag_orbit_size"],160)
        self.assertEqual(z["projective_symplectic_order"],25920)
        self.assertEqual(z["GL3_F3_order"],11232)
        self.assertEqual(z["rational_H1_full_group_invariants"],0)

    def test_general_relative_index_all_boundary_patterns(self):
        z=self.p["general_defect_index"]
        self.assertEqual(z["ranges_checked"],sum(k-1 for k in range(3,13)))
        self.assertEqual(z["target_three_family_examples"][0]["total_boundary_spheres"],5)
        self.assertEqual(z["target_three_family_examples"][0]["negative_boundaries"],4)
        self.assertEqual(z["target_three_family_examples"][0]["trivial_b1_b2"],[3,0])
        self.assertEqual(z["target_three_family_examples"][0]["nontrivial_flat_char_b1_b2"],[4,1])

    def test_extra_vectorlike_modes_in_nontrivial_character(self):
        z=self.p["general_defect_index"]
        for t in z["target_three_family_examples"]:
            self.assertGreaterEqual(t["nontrivial_flat_char_b1_b2"][1],1)
        self.assertIn("b2>=1",z["vectorlike_obstruction"])

    def test_cyclic_wilson_first_leptoquark_free_order(self):
        z=self.p["order_seven_Wilson"]
        self.assertEqual(z["smallest_cyclic_order_to_kill_SO10_ten_generators"],7)
        self.assertEqual(z["minimal_order7_candidate"]["SO10_centralizer"],13)
        self.assertEqual(z["minimal_order7_candidate"]["E6_min_centralizer"],14)
        self.assertEqual([(x["a"],x["b"],x["SO10_centralizer"])
                          for x in z["C4_cases"]],[(0,2,21),(2,1,19),(2,3,19)])

    def test_extended_E6_phase_search(self):
        z=self.p["order_seven_Wilson"]
        self.assertEqual(len(z["rank7_phase_options"]),7)
        self.assertEqual(z["rank7_phase_options"][5]["spinor_invariants"],0)
        self.assertEqual(z["rank7_phase_options"][5]["E6_centralizer"],14)
        self.assertEqual(sum(z["order7_spinor_charge_multiset"].values()),16)

    def test_E6_anomalies(self):
        z=self.p["E6_anomalies"]
        self.assertAlmostEqual(z["SM_TrY"],0)
        self.assertAlmostEqual(z["SM_TrY3"],0)
        self.assertEqual(z["Psi_gravitational"],-144)
        self.assertEqual(z["Psi_cubic"],-1296)
        self.assertAlmostEqual(z["Psi_SU3_squared"],-18)
        self.assertAlmostEqual(z["Psi_SU2_squared"],-18)
        self.assertAlmostEqual(z["Psi_Y_squared"],-30)

    def test_modular_ratio_boundary(self):
        z=self.p["modular_winding"]
        self.assertAlmostEqual(z["critical_ratio"],2*math.sqrt(3)/math.pi)
        self.assertEqual(z["numerical_cross_checks"][0]["analytic_modular_stable_fraction"],0)
        self.assertAlmostEqual(z["numerical_cross_checks"][5]["analytic_modular_stable_fraction"],
                               1-6/math.pi**2)
        for row in z["numerical_cross_checks"]:
            self.assertLess(abs(row["quadrature_fraction"]-
                                row["analytic_modular_stable_fraction"]),2e-7)

    def test_no_IID_needed_if_per_history_conditional_guarantees(self):
        z=self.p["quantum_memory"]
        self.assertIn("conditional success",z["IID_not_necessary_for_type1"])
        self.assertAlmostEqual(z["distinguishability_requires_kappa_less_than"],
                               math.sqrt(7/4))

    def test_quantum_witness_loss_budget(self):
        z=self.p["quantum_memory"]
        t=z["ratio_table"]
        self.assertEqual([(i["accepted_events"],i["threshold"]) for i in t],
                         [(292,117),(428,171),(664,265),(2382,949),(7044,2805)])
        for i in t:
            self.assertLessEqual(i["alpha"],.01)
            self.assertLessEqual(i["beta"],.01)
        self.assertIn("multitime",z["literature_warning"])


if __name__=="__main__":
    unittest.main()
