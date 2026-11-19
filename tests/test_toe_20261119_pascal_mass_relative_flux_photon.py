"""Regression for source-aware Pascal/Sierpinski mass, U1-SSR decoherence,
3D relative flux, SU5 Higgs-adjoint covariance and causal KG mass artifact."""
import sys,unittest
from math import sqrt,comb
from pathlib import Path
import numpy as np
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"analysis"))
import toe_20261119_pascal_sierpinski_mass_spectrum as pa
import toe_20261119_TOE_relative_flux_SU5_mass_causet as tf

class FractalMassFivePhysics(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.p=pa.run();cls.x=tf.run()
    def test_pascal_dyadic_kronecker_all_levels_1_to_6(self):
        for row in self.p["levels"]:self.assertTrue(row["Kronecker_Lucas_exact"])
    def test_pascal_mass_multiplicities_binomial(self):
        for row in self.p["levels"]:
            L=row["level"];self.assertEqual([z["multiplicity"] for z in row["spectrum"]],
                [comb(L,j) for j in range(L+1)])
    def test_pascal_mass_singular_values_analytic(self):
        for row in self.p["levels"]:
            L=row["level"]
            for z in row["spectrum"]:
                self.assertAlmostEqual(z["mass_singular_value"],
                    pa.PHI**(2*z["j"]-L))
    def test_pascal_det_unimodular_all(self):
        for row in self.p["levels"]:
            self.assertEqual(row["det_unimodular"],1)
    def test_pascal_selfsimilar_max_mass_ratio(self):
        for row in self.p["levels"]:
            self.assertAlmostEqual(row["extreme_mass_ratio"],
                                   pa.PHI**(2*row["level"]))
    def test_pascal_three_family_corner_has_ratio_2_plus_sqrt3(self):
        self.assertAlmostEqual(self.p["three_family_raw_pascal"]["max_to_min_ratio"],
                               2+sqrt(3),places=12)
    def test_three_charged_leptons_not_predicted(self):
        d=self.p["three_family_raw_pascal"]
        self.assertGreater(d["charged_lepton_tau_e_ratio"],3000)
        self.assertLess(d["max_to_min_ratio"],4)
    def test_first_l_matching_tau_e_extremes_is_nine_512_modes(self):
        self.assertEqual(self.p["smallest_dyadic_level_with_large_enough_extreme_ratio"],9)
        self.assertEqual(self.p["corresponding_2power_family_dimension"],512)
    def test_one_hot_family_embedding_has_no_mass_splitting(self):
        m=self.p["flavor_kinetic_metric_nonidentifiability"]
        self.assertEqual(m["one_hot_three_family_pascal_submatrix"],np.eye(3,dtype=int).tolist())
        self.assertTrue(m["one_hot_mass_eigenvalues_identical"])
    def test_arbitrary_masses_possible_only_with_fitted_kinetic_metric(self):
        m=self.p["flavor_kinetic_metric_nonidentifiability"]
        self.assertTrue(m["any_positive_target_spectrum_admits_a_fitted_positive_KR"])
        self.assertGreater(m["kinetic_metric_condition_number"],1e5)
    def test_weighted_sierpinski_partition_exact(self):
        self.assertEqual(len(self.p["weighted_partition_examples"]),15)
        for row in self.p["weighted_partition_examples"]:
            if row["alpha"]==row["beta"]==0:
                self.assertEqual(row["Z"],3**row["L"])
    def test_massive_Gram_determinant_analytic(self):
        self.assertEqual(len(self.p["massive_logdet_checks"]),16)
        self.assertTrue(all(np.isfinite(r["logdet_Gram_plus_m2"])
                            for r in self.p["massive_logdet_checks"]))
    def test_massive_SSR_CSHS_baseline(self):
        vals=self.p["mass_dependent_two_copy_SSR"]["table"]
        self.assertAlmostEqual(vals[0]["optimal_CHSH_under_strict_SSR"],1+sqrt(2))
    def test_dephasing_SSR_local_classical_limit(self):
        vals=self.p["mass_dependent_two_copy_SSR"]["table"]
        self.assertLess(abs(vals[-1]["optimal_CHSH_under_strict_SSR"]-2),1e-6)
    def test_differential_phase_not_common_mass_phase(self):
        self.assertIn("common",self.p["mass_dependent_two_copy_SSR"]["important_common_mode"].lower())
        self.assertIn("no established nonzero rest mass",self.p["mass_dependent_two_copy_SSR"]["mass_caution"])
    def test_finite_pascal_is_not_Sierpinski_Laplacian(self):
        self.assertIn("separately specified adjacency",self.p["not_the_same_as"])
    def test_relative_flux_perfect_pairing_rank_three(self):
        self.assertEqual(self.x["relative_flux"]["pairing_rank"],3)
        self.assertEqual(self.x["relative_flux"]["H2_rel_twisted_dual_dimension"],3)
    def test_relative_flux_absolute_H2_still_vanishes(self):
        self.assertEqual(self.x["relative_flux"]["H2_abs_twisted_dimension"],0)
        self.assertIn("not an ordinary 1+1+1",self.x["relative_flux"]["important"])
    def test_relative_flux_breaks_S3_twofold_degeneracy(self):
        self.assertEqual(self.x["relative_flux"]["background_relative_flux_toy_masses"],[1,2,3])
        self.assertEqual(self.x["relative_flux"]["example_S3_breaking_eigenvalue_split_first_order"],
                         "2*epsilon/sqrt(3)")
    def test_SU5_octet_full_spurion_covariance(self):
        self.assertTrue(self.x["SU5_covariant_octet_spurion"]["full_SU5_Higgs_spurion_covariance_verified"])
        self.assertEqual(self.x["SU5_covariant_octet_spurion"]["random_SU5_transformations"],40)
    def test_SU5_Higgs_frozen_non_covariance(self):
        self.assertGreater(self.x["SU5_covariant_octet_spurion"]["max_SU5_non_covariance_residual_with_H_frozen"],.1)
    def test_octet_requires_nonminimal_mass_operator(self):
        self.assertIn("24H",self.x["SU5_covariant_octet_spurion"]["operator_hierarchy"])
    def test_causet_KG_mass_does_not_reduce_variance(self):
        for z in self.x["causal_mass_counterterm"]["test_cases"]:
            self.assertAlmostEqual(z["stochastic_variance_B"],
                                   z["variance_with_m_squared_plus2"],places=8)
    def test_causet_fake_mass_counterterm_sign_flips(self):
        a=self.x["causal_mass_counterterm"]["test_cases"]
        self.assertLess(a[0]["counterterm_mass_squared_to_force_zero_mean"],0)
        self.assertGreater(a[1]["counterterm_mass_squared_to_force_zero_mean"],0)
    def test_source_qualifications_clear(self):
        self.assertIn("parity alone predicts no mass",self.p["flavor_kinetic_metric_nonidentifiability"]["physics_caution"])
        self.assertIn("no quantum state",self.x["causal_mass_counterterm"]["scope"])
if __name__=="__main__":unittest.main()
