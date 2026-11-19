"""Focused regression tests of full E8 relative topology, Psi Wilson,
conjugate sector, weak-G2 and four-local-MUB qutrit memory witness."""
import sys,unittest
from pathlib import Path
import numpy as np
import sympy as s
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/"analysis"))
import toe_20261118_E8_248_relative_Psi_G2_MUB as T

class E8Full248MUB(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.d=T.run()
        cls.w=cls.d["full_E8_census"]
        cls.c0=cls.w["entire_E8_relative_cohomology_cases"][0]
        cls.c3=cls.w["entire_E8_relative_cohomology_cases"][3]
        cls.g=cls.d["nearly_parallel_G2"]
        cls.q=cls.d["local_qutrit_MUB"]
        cls.dual=cls.d["conjugation_obstruction"]
    def test_78_branching_count(self):
        self.assertEqual(len(T.weights_E6(0)[0]),78)
    def test_27_branching_count(self):
        self.assertEqual(len(T.weights_E6(3)[1]),27)
    def test_SU5_adj_fixed12(self):
        self.assertEqual(T.weights_E6(0)[2]["SU5_adjoint_24_fixed"],12)
    def test_c0_unbroken_E6_16(self):
        self.assertEqual(self.c0["E8_unbroken_gauge_generators"],16)
    def test_c3_unbroken_E6_14(self):
        self.assertEqual(self.c3["E8_unbroken_gauge_generators"],14)
    def test_E6_45_fixed13(self):
        self.assertEqual(T.weights_E6(3)[2]["SO10_45_fixed"],13)
    def test_c3_16_charged_root_fixed_zero(self):
        self.assertEqual(T.weights_E6(3)[2]["E6_16minus3_fixed"],0)
        self.assertEqual(T.weights_E6(3)[2]["E6_16barplus3_fixed"],0)
    def test_all_7_Psi_phases_exhaustive(self):
        self.assertEqual(self.w["fixed_E6_center_dimensions_by_Psi_phase"],[16,18,26,14,20,16,20])
    def test_unique_psi3(self):
        self.assertEqual(self.w["unique_minimal_Psi_phase_c"],3)
    def test_E8_dimensions_total248(self):
        self.assertEqual(sum(a["dim"] for a in self.c3["E8_sector_betti"].values()),248)
    def test_E6_adjoint_cohom_c0(self):
        self.assertEqual(self.c0["E8_sector_betti"]["E6_adjoint_78"]["relative_S2_betti"],[0,94,16])
    def test_E6_adjoint_cohom_c3(self):
        self.assertEqual(self.c3["E8_sector_betti"]["E6_adjoint_78"]["relative_S2_betti"],[0,92,14])
    def test_family_adjoint_cohom(self):
        self.assertEqual(self.c3["E8_sector_betti"]["SU3_adjoint_8"]["relative_S2_betti"],[0,12,4])
    def test_matter_eightyone_threefamilies_input(self):
        self.assertEqual(self.c3["E8_sector_betti"]["E6_27_family_3"]["relative_S2_betti"],[0,81,0])
    def test_conjugate_matter_same(self):
        self.assertEqual(self.c3["E8_sector_betti"]["E6_27bar_family_3bar"]["relative_S2_betti"],[0,81,0])
    def test_full_c0_relative268_20(self):
        self.assertEqual(self.c0["E8_relative_S2_betti"],[0,268,20])
    def test_full_c3_relative266_18(self):
        self.assertEqual(self.c3["E8_relative_S2_betti"],[0,266,18])
    def test_net_index_is_coefficient_rank(self):
        for case in self.w["entire_E8_relative_cohomology_cases"]:
            self.assertEqual(case["E8_relative_S2_betti"][1]-case["E8_relative_S2_betti"][2],248)
    def test_relative_overcount_correction(self):
        self.assertEqual(self.c3["historical_overcount_if_ignore_fixed_vectors"],280)
        self.assertEqual(self.c3["missing_subtraction"],14)
    def test_trivial_local_system_has_relative_two_not_three(self):
        A=np.eye(1,dtype=complex);C=np.eye(1,dtype=complex)
        h=T.absolute_cell(A,C)
        self.assertEqual(h["absolute_betti"],[1,2,1])
        self.assertEqual(h["relative_S2_betti"],[0,2,1])
    def test_rank3_acyclic_rel3_is_assumed_dimension(self):
        self.assertEqual(self.dual["test_qutrit_3"]["absolute_betti"],[0,0,0])
        self.assertEqual(self.dual["test_qutrit_3"]["relative_S2_betti"],[0,3,0])
    def test_flat_conjugation_H1_H2_equal(self):
        self.assertIn("same real",self.dual["theorem"])
        a=T.absolute_cell(T.X,T.C9)
        b=T.absolute_cell(T.X.conj(),T.C9.conj())
        self.assertEqual(a["relative_S2_betti"],b["relative_S2_betti"])
    def test_G2_weak_Ricci_flux_matching(self):
        self.assertEqual(self.g["curvature_consistency_condition"],"abs(tau0)=2 abs(f)/3")
    def test_G2_nearly_parallel_torsion_scale(self):
        self.assertEqual(self.g["at_f3_overL_tau0"],"2/L")
    def test_G2_Killing_spinor_not_zero_mode(self):
        self.assertEqual(self.g["untwisted_real_Killing_spinor_Dirac_abs_eigenvalue_L"],"7/4")
        self.assertTrue(self.g["no_untwisted_geometric_Dirac_zero_modes"])
    def test_MUB_four_settings(self):
        self.assertEqual(self.q["number_of_local_settings"],4)
        self.assertEqual(self.q["native_qutrit_Clifford_MUBs"],["Z","X","XZ","XZ^2"])
    def test_MUB_three_nonZ_bases_one_C9_clifford_orbit(self):
        self.assertLess(self.q["C9_clifford_MUB_cycle_max_residual"],2e-12)
        self.assertTrue(self.q["fourth_Z_basis_is_fixed_by_C9"])
        self.assertEqual(self.q["C9_clifford_cycle_of_three_nonZ_MUBs"],"X -> XZ^2 -> XZ -> X")
    def test_MUB_2design_identity(self):
        self.assertLess(self.q["identity_max_residual"],2e-12)
    def test_MUB_bound_p0(self):
        self.assertEqual(self.q["Schmidt_number_at_most2_match_bound"],.75)
    def test_MUB_model_fidelity(self):
        self.assertAlmostEqual(self.q["model_entanglement_fidelity"],7/9,places=12)
        self.assertAlmostEqual(self.q["model_match_probability"],5/6,places=12)
    def test_MUB_optimum_n317_k256(self):
        v=self.q["fixed_sample_noiseless_90pct_power"]
        self.assertEqual((v["n"],v["match_count_at_least"]),(317,256))
        self.assertLessEqual(v["exact_alpha"],.01)
        self.assertGreaterEqual(v["power"],.90)
    def test_MUB_conservative_noisy_budgets(self):
        rows=self.q["readout_assignment_budgets"]
        self.assertEqual([r["conservative_uncalibrated_null_p0_075"]["n"] for r in rows],[317,472,790])
    def test_MUB_calibrated_noisy_budgets(self):
        rows=self.q["readout_assignment_budgets"]
        self.assertEqual([r["known_calibrated_confusion_null"]["n"] for r in rows],[317,348,389])
    def test_no_claim_genuine_three_time(self):
        self.assertIn("NOT genuine three-time",self.q["limitations"])

if __name__=="__main__":unittest.main()
