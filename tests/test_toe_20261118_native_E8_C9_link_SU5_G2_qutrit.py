"""Independent regression gates for E8 C9 linked holonomy, E6 Higgs,
pure-electric AdS4 G2, and intrinsic qutrit witness.

Only conditional math statements are asserted. No experiment or
physical chiral zero-mode theorem is claimed.
"""
import math,sys,unittest
from pathlib import Path
import numpy as np
import sympy as s
from scipy.stats import binom
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/"analysis"))
import toe_20261118_native_E8_C9_link_SU5_G2_qutrit as C

class NativeE8C9LinkTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.d=C.run()
        cls.b=cls.d["native_E8_link_holonomy"]
        cls.e=cls.d["E6_Higgs_and_moduli"]
        cls.g=cls.d["Freund_Rubin_G2"]
        cls.q=cls.d["intrinsic_qutrit_memory"]
        cls.z=cls.d["geometric_Z3_selection"]

    def test_C9_is_SU3_element(self):
        self.assertAlmostEqual(abs(np.linalg.det(C.C9)),1,places=12)
        self.assertLess(abs(np.linalg.det(C.C9)-1),1e-12)
    def test_C9_cube_has_nontrivial_shared_center(self):
        self.assertLess(np.max(abs(np.linalg.matrix_power(C.C9,3)-
                                   C.w*np.eye(3))),1e-12)
    def test_C9_has_exact_order_nine(self):
        self.assertLess(np.max(abs(np.linalg.matrix_power(C.C9,9)-
                                  np.eye(3))),1e-12)
        self.assertGreater(np.max(abs(np.linalg.matrix_power(C.C9,3)-
                                     np.eye(3))),1)
    def test_C9_is_projective_order3_qutrit_Clifford_gate(self):
        w=C.w
        Z=np.diag([1,w,w*w])
        self.assertLess(np.max(abs(C.C9@C.X@C.C9.conj().T-C.X@Z@Z)),1e-12)
        self.assertLess(np.max(abs(C.C9@Z@C.C9.conj().T-Z)),1e-12)
        self.assertEqual(self.b["qutrit_projective_gate_order"],3)
        self.assertEqual(self.b["qutrit_SU3_lift_order"],9)
    def test_torus_link_relation(self):
        self.assertLess(self.b["linked_relation_full_SU5xSU3_residual"],1e-11)
    def test_SU3_image_order_81(self):
        self.assertEqual(self.b["exact_finite_image"]["orders"]["SU3_full_group"],81)
    def test_H27_subgroup_order_27(self):
        self.assertEqual(self.b["exact_finite_image"]["orders"]["H27_normal_subgroup"],27)
    def test_C9_H27_quotient_order_three(self):
        self.assertEqual(self.b["exact_finite_image"]["orders"]["SU3_order9_extension_over_H27"],3)
    def test_full_image_order_567(self):
        self.assertEqual(self.b["exact_finite_image"]["orders"]["SU5_W7_times_SU3_family"],567)
    def test_matter_E6_weight_census(self):
        self.assertEqual(len(self.b["matter_E6_27_weight_exponents"]),27)
        self.assertEqual(self.b["matter_E6_27_weight_exponents"].count(0),2)
    def test_matter_base_acyclic(self):
        a=C.coh(C.X,C.C9)
        self.assertEqual(a["absolute_betti"],[0,0,0])
        self.assertEqual(a["relative_one_sphere_betti"],[0,3,0])
    def test_conjugate_base_acyclic(self):
        a=C.coh(C.X.conj(),C.C9.conj())
        self.assertEqual(a["absolute_betti"],[0,0,0])
        self.assertEqual(a["relative_one_sphere_betti"],[0,3,0])
    def test_full_27_relative(self):
        self.assertEqual(self.b["matter_27x3_relative_betti"],[0,81,0])
    def test_full_27bar_relative(self):
        self.assertEqual(self.b["conjugate_27barx3bar_relative_betti"],[0,81,0])
    def test_symmetric_boundary_does_not_remove_conjugate(self):
        self.assertTrue(self.b["same_relative_boundary_does_not_project_conjugate_matter"])
    def test_family_adjoint_absolute_four_four(self):
        self.assertEqual(self.b["SU3_family_adjoint8_absolute_betti"],[0,4,4])
    def test_family_adjoint_relative_twelve_four(self):
        self.assertEqual(self.b["SU3_family_adjoint8_relative_betti"],[0,12,4])
    def test_no_parallel_family_fundamental(self):
        self.assertTrue(self.b["family_charged_E8_27x3_no_parallel_invariant"])
    def test_27x1_not_global_E8_rep(self):
        self.assertFalse(self.b["gauge_Higgs_27x1_global_E8_representation_exists"])
    def test_SU5_residual_gauge_dim_twelve(self):
        self.assertEqual(self.b["SU5_centered_root_generator_count"],12)
    def test_E6_pair_mass_Hessian_rank_four(self):
        self.assertEqual(self.e["full_model_Hessian_rank_at_most"],4)
        self.assertEqual(self.e["singlet_6x6_holomorphic_Hessian_eigenvalues"],
           ["-sqrt(2)","-sqrt(2)","0","0","sqrt(2)","sqrt(2)"])
    def test_E6_full_higgs_fields_110(self):
        self.assertEqual(self.e["chiral_fields"],110)
    def test_E6_smooth_Fflat_dim_106(self):
        self.assertEqual(self.e["F_flat_local_complex_dimension"],106)
    def test_E6_moduli_lower_bound_52(self):
        self.assertEqual(self.e["local_complex_moduli_lower_bound"],52)
    def test_E6_SU5_stabilizer_at_least_24(self):
        self.assertEqual(self.e["unbroken_at_least_SU5_dim"],24)
        self.assertTrue(self.e["unbroken_nonabelian_SU5_needs_further_W7_or_other_representation"])
    def test_FR_internal_positive_Ricci_for_flux(self):
        self.assertEqual(self.g["R_internal_tensor_coefficient"],"+f²/6")
    def test_FR_torsionfree_G2_forces_zero_flux(self):
        self.assertTrue(self.g["if_torsionfree_G2_then_f_zero"])
    def test_FR_fluxless_external_not_AdS(self):
        self.assertTrue(self.g["f_zero_implies_Minkowski_not_AdS4"])
    def test_qutrit_intrinsic_dim3_fidelity(self):
        self.assertAlmostEqual(self.q["exact_fidelity"],7/9,places=12)
        self.assertGreater(self.q["exact_fidelity"],2/3)
    def test_qutrit_rank3_noise_threshold(self):
        self.assertEqual(self.q["rank3_certification_visibility_threshold"],5/8)
    def test_qutrit_exact_fixed_n(self):
        v=self.q["exact_fixed_stopping_binomial"]
        self.assertEqual(v["accepted_Bell_projection_trials"],214)
        self.assertEqual(v["observed_Bell_successes_to_reject"],159)
        self.assertLessEqual(v["exact_one_sided_typeI"],.01)
        self.assertGreaterEqual(v["design_point_power"],.90)
    def test_qutrit_no_genuine_three_time_claim(self):
        self.assertIn("NOT by itself",self.q["limitation"])
    def test_Z3_rotational_invariance_requires_divisible3(self):
        for z in self.z["table"]:
            self.assertEqual(z["invariant_under_w_to_omega_w"],
                             z["holomorphic_degree"]%3==0)
    def test_Z3_geometric_rotation_excludes_quartic_not_physics(self):
        self.assertTrue(self.z["n3_quartic_not_invariant"])
        self.assertIn("Conditional",self.z["scope"])

if __name__=="__main__":unittest.main()
