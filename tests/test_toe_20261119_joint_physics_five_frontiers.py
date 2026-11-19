"""Independent numerical regression gates for physics-only TOE benchmark."""
import pathlib
import sys
import unittest
import numpy as np

ROOT=pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"analysis"))
import toe_20261119_joint_physics_five_frontiers as f

class FiveFrontiers(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.out=f.run_all()
        cls.r=cls.out["frontiers"]

    def test_two_majorana_triplets_and_one_octet_anomaly_safe(self):
        g=self.r["gauge_and_chiral_content"]
        self.assertEqual([x["SM_rep"] for x in g["field_content"]],
                         ["(1,3,0)","(8,1,0)"])
        self.assertEqual([x["count"] for x in g["field_content"]],[2,1])
        self.assertAlmostEqual(g["one_loop_beta_above_thresholds"][1],
                               -19/6+8/3)
        self.assertAlmostEqual(g["one_loop_beta_above_thresholds"][2],-5)

    def test_thresholds_inside_stated_interval_and_unification(self):
        g=self.r["gauge_and_chiral_content"]
        mu=g["chosen_unification_scale_GeV"]
        self.assertLess(g["admissible_MU_interval_GeV"][0],mu)
        self.assertGreater(g["admissible_MU_interval_GeV"][1],mu)
        self.assertTrue(all(f.MZ<x["Mass_GeV"]<mu
             for x in g["field_content"]))
        self.assertLess(g["one_loop_closure_error"],1e-10)
        self.assertTrue(.02<g["unified_alpha"]<.04)

    def test_thresholds_are_not_unique_prediction(self):
        a=f.gauge_bridge(1e16)
        b=f.gauge_bridge(3e16)
        self.assertNotAlmostEqual(
          a["field_content"][0]["Mass_GeV"]/b["field_content"][0]["Mass_GeV"],1)
        self.assertLess(a["one_loop_closure_error"],1e-10)
        self.assertLess(b["one_loop_closure_error"],1e-10)

    def test_neutrino_rank_two_and_PMNS_reconstruction(self):
        n=self.r["neutrino_typeIII"]
        self.assertTrue(n["one_exactly_massless_neutrino"])
        self.assertEqual(n["light_masses_eV"][0],0)
        self.assertLess(n["Takagi_reconstruction_error_GeV"],1e-20)
        self.assertTrue(5e-2<n["light_mass_sum_eV"]<6e-2)
        self.assertLess(n["maximum_yukawa_abs"],.001)
        self.assertGreater(n["maximum_yukawa_abs"],1e-5)

    def test_neutrino_phase_envelope_min_max(self):
        n=self.r["neutrino_typeIII"]
        self.assertLess(n["mbb_phase_range_eV"][0],
                        n["mbb_phase_range_eV"][1])
        self.assertGreater(n["mbb_phase_range_eV"][0],.001)
        self.assertLess(n["mbb_phase_range_eV"][1],.004)

    def test_R2_scalaron_short_range(self):
        g=self.r["gravity_R2_and_dark_energy_naturalness"]
        self.assertGreater(g["scalaron_Compton_length_m"],1e-30)
        self.assertLess(g["scalaron_Compton_length_m"],1e-29)
        self.assertEqual(g["Yukawa_factor_at_1nanometer"],0)

    def test_R2_vacuum_hierarchy_is_only_naturalness_diagnostic(self):
        g=self.r["gravity_R2_and_dark_energy_naturalness"]
        self.assertGreater(g["naive_M4_over_64pi2_to_rhoLambda_ratio"],1e97)
        self.assertLess(g["inferred_present_dark_energy_scale_meV"],2.5)

    def test_real_BAO_fixed_parameter_comparison(self):
        b=self.r["real_data_BAO_two_point_audit"]
        self.assertEqual(len(b["LambdaCDM"]["samples"]),2)
        self.assertEqual(len(b["DES_Y6_DESI_DR2_best_fit_CPL"]["samples"]),2)
        self.assertGreater(b["delta_chi2_LCDM_minus_CPL_fixed_inputs"],0)
        self.assertTrue(1<b["DES_Y6_DESI_DR2_best_fit_CPL"]["diagonal_only_chi2"]<4)
        self.assertTrue(4<b["LambdaCDM"]["diagonal_only_chi2"]<7)

    def test_BAO_surveys_and_units(self):
        b=self.r["real_data_BAO_two_point_audit"]
        self.assertEqual([x["observable"] for x in b["LambdaCDM"]["samples"]],
                         ["DM_over_rd","DH_over_rd"])
        self.assertEqual([x["z"] for x in b["LambdaCDM"]["samples"]],[.851,.706])

    def test_CHSH_dual_certificate_PSD_and_saturation(self):
        q=self.r["quantum_Tsirelson_PSD_certificate"]
        self.assertGreater(min(q["PSD_dual_certificate_eigenvalues"]),-1e-12)
        self.assertAlmostEqual(q["dual_objective"],2*np.sqrt(2),places=12)
        self.assertAlmostEqual(q["primal_objective"],q["dual_objective"],places=12)

    def test_PR_is_not_Born_rule_quantum(self):
        q=self.r["quantum_Tsirelson_PSD_certificate"]
        self.assertGreater(q["PR_no_signaling_algebraic_CHSH"],q["dual_objective"])
        self.assertTrue(q["no_signaling_does_not_imply_quantum"])

    def test_joint_five_fronts_no_TOE_claim(self):
        self.assertFalse(self.out["W33_used_as_foundation"])
        self.assertEqual(len(self.r),5)
        self.assertTrue(all(v["status"]=="PASS" for v in self.r.values()))
        self.assertIn("no unified theory",self.out["status"])

if __name__=="__main__":
    unittest.main()
