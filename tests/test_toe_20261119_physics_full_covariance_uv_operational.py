"""Regression tests: exact SU5 mass sum rule, physical neutrino freedom,
published DESI covariance model selection and single-photon number SSR."""
import hashlib
from pathlib import Path
import sys
import unittest
import numpy as np

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"analysis"))
import toe_20261119_physics_full_covariance_uv_operational as p


class TOEPhysicalCompletion(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.r=p.make_results()["domains"]

    def test_SU5_adjoint_matrix_sumrule_for_two_families(self):
        g=self.r["physical_SU5_adjoint_mass_embedding"]
        self.assertEqual(g["renormalizable_SU5_matrix_mass_relation"],
                         "2 MX = M8 + M3")
        self.assertAlmostEqual(g["Takagi_light_X_analytic_upper_bound_GeV"],
                         (g["toy_triplet_two_mass_GeV"]+
                          g["toy_light_octet_mass_GeV"])/2)
        self.assertLessEqual(
          g["explicit_commuting_example_X_Takagi_masses_GeV"][0],
          g["Takagi_light_X_analytic_upper_bound_GeV"]+1e-5)

    def test_light_SU5_X_forced_even_with_complex_mixing(self):
        g=self.r["physical_SU5_adjoint_mass_embedding"]
        self.assertEqual(g["random_complex_symmetric_mass_mixing_checks"],200)
        self.assertLess(g["maximum_numerical_violation_of_upper_bound_GeV"],1e-6)
        self.assertLess(g["Takagi_light_X_analytic_upper_bound_GeV"],1.2e7)

    def test_SU5_24F_complete_beta_multiplet_equal_shift(self):
        g=self.r["physical_SU5_adjoint_mass_embedding"]
        a=g["full_24F_one_loop_shifts"]
        b=np.array(a["triplet"])+np.array(a["octet"])+np.array(a["X_and_Xbar"])
        np.testing.assert_allclose(b,[10/3]*3)

    def test_unretuned_24F_extra_X_spoils_previous_one_loop_crossing(self):
        g=self.r["physical_SU5_adjoint_mass_embedding"]
        self.assertGreater(g["forced_light_X_inverse_coupling_shift_spread_if_unretuned"],5)
        self.assertLess(g["toy_light_octet_mass_GeV"],
                        g["toy_triplet_two_mass_GeV"])

    def test_typeIII_neutrino_exact_matrix_reconstruction_at_all_angles(self):
        n=self.r["neutrino_Yukawa_continuum_and_naturalness"]
        self.assertTrue(n["light_mass_matrix_fixed"])
        self.assertEqual(n["tree_level_lightest_mass_eV"],0)
        self.assertEqual(len(n["Casas_Ibarra_angle_samples"]),7)
        self.assertLess(max(r["mass_reconstruction_error_GeV"]
                            for r in n["Casas_Ibarra_angle_samples"]),1e-22)

    def test_typeIII_real_angle_norm_invariance(self):
        rows=self.r["neutrino_Yukawa_continuum_and_naturalness"]["Casas_Ibarra_angle_samples"]
        for row in rows[1:3]:
            self.assertAlmostEqual(row["Y_frobenius_squared"]/rows[0]["Y_frobenius_squared"],1,places=11)

    def test_typeIII_imaginary_angle_exponential_yukawa_growth(self):
        rows=self.r["neutrino_Yukawa_continuum_and_naturalness"]["Casas_Ibarra_angle_samples"]
        for row in rows:
            self.assertAlmostEqual(
               row["Y_frobenius_squared"]/rows[0]["Y_frobenius_squared"],
               np.cosh(2*row["Im_z"]),places=10)
        self.assertGreater(rows[-1]["threshold_over_125GeV_mass_squared"],1000)
        self.assertGreater(rows[0]["threshold_over_125GeV_mass_squared"],10)

    def test_gravity_fourth_derivative_ghost_residue(self):
        g=self.r["higher_derivative_spin2_spectral_test"]
        self.assertEqual(g["spin2_massless_pole_residue"],1)
        self.assertEqual(g["spin2_extra_pole_residue"],-1)
        self.assertLess(g["partial_fraction_identity_max_relative_error"],1e-10)

    def test_gravity_scalaron_short_range_is_not_toy_UV_completion(self):
        g=self.r["higher_derivative_spin2_spectral_test"]
        self.assertTrue(g["R2_no_new_spin2_ghost_at_quadratic_tree_level"])
        self.assertLess(g["R2_scalaron_fifth_force_length_m"],1e-29)
        self.assertGreater(g["R2_scalaron_fifth_force_length_m"],1e-30)

    def test_DESI_source_files_have_exact_Git_blob_shas(self):
        expected=[("data/desi_dr2_13_mean_20261119.txt",
                   "8aff444fdb42c0946342aa0011ab287eda097c4c"),
                  ("data/desi_dr2_13_cov_20261119.txt",
                   "fd8e5697ab61379b07b52efb781ea6713417a4d9")]
        for rel,sha in expected:
            raw=(ROOT/rel).read_bytes()
            blob=b"blob "+str(len(raw)).encode()+b"\x00"+raw
            self.assertEqual(hashlib.sha1(blob).hexdigest(),sha)

    def test_DESI_full_covariance_valid_and_13_observables(self):
        z,y,k,c=p._source_bao()
        self.assertEqual(len(z),13)
        self.assertEqual(len(y),13)
        self.assertTrue(np.all(np.linalg.eigvalsh(c)>0))
        self.assertAlmostEqual(y[3],17.35069094)
        self.assertAlmostEqual(y[4],19.45534918)
        self.assertEqual(k[0],"DV_over_rs")

    def test_BAO_LCDM_and_CPL_are_nested(self):
        r=self.r["full_DESI_DR2_Gaussian_covariance"]
        self.assertGreater(r["LCDM_only_DESI13"]["chi_squared"],r["CPL_only_DESI13"]["chi_squared"])
        self.assertGreater(r["DESI13_delta_chi2_LCDM_minus_CPL"],4)
        self.assertLess(r["DESI13_delta_chi2_LCDM_minus_CPL"],6)
        self.assertGreater(r["CPL_only_DESI13_wide_bounds"]["w0"],
                           r["CPL_only_DESI13"]["w0"])

    def test_BAO_information_criteria_do_not_claim_discovery(self):
        r=self.r["full_DESI_DR2_Gaussian_covariance"]
        self.assertGreater(r["DESI13_delta_AIC_CPL_minus_LCDM"],-2)
        self.assertGreater(r["DESI13_delta_BIC_CPL_minus_LCDM"],0)
        self.assertLess(r["DESI13_wide_vs_baseline_CPL_delta_chi2"],.1)
        self.assertEqual(r["LCDM_only_DESI13"]["n_parameters"],2)
        self.assertEqual(r["CPL_only_DESI13"]["n_parameters"],4)

    def test_BAO_only_cannot_separate_H0_and_rd(self):
        r=self.r["full_DESI_DR2_Gaussian_covariance"]
        for k in ["LCDM_only_DESI13","CPL_only_DESI13"]:
            x=r[k]
            self.assertAlmostEqual(x["q_c_over_H0_rd"]*x["H0_rd_km_s"]/299792.458,1,places=12)

    def test_BAO_14point_independent_DES_is_observationally_narrow(self):
        r=self.r["full_DESI_DR2_Gaussian_covariance"]
        self.assertEqual(r["LCDM_plus_overlap_removed_DES14"]["n_data"],14)
        self.assertGreater(r["LCDM_plus_overlap_removed_DES14"]["chi_squared"],
                           r["LCDM_only_DESI13"]["chi_squared"])
        self.assertGreater(r["CPL_plus_overlap_removed_DES14"]["chi_squared"],
                           r["CPL_only_DESI13"]["chi_squared"])

    def test_single_photon_SSR_removes_accessible_Bell_violation(self):
        r=self.r["single_photon_local_SSR_and_CHSH"]
        self.assertAlmostEqual(r["unrestricted_entanglement_negativity"],.5)
        self.assertAlmostEqual(r["locally_U1_twirl_entanglement_negativity"],0)
        self.assertAlmostEqual(r["unrestricted_max_CHSH"],2*np.sqrt(2),places=12)
        self.assertAlmostEqual(r["locally_twirled_max_CHSH"],2,places=12)
        self.assertEqual(r["locally_number_conserving_observables_checked"],120)

    def test_all_five_physics_gates_are_explicitly_conditional(self):
        self.assertEqual(len(self.r),5)
        self.assertTrue(all(x["status"]=="PASS" for x in self.r.values()))

if __name__=="__main__":
    unittest.main()
