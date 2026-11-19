"""Independent TOE observational benchmark: exact invariants plus numerical falsifiers."""
import pathlib
import sys
import unittest

import numpy as np
from scipy.integrate import quad

ROOT=pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"analysis"))
import toe_20261119_physics_first_frontiers_v2 as f


class PhysicsFirstFiveFrontiers(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.all=f.certify()
        cls.r=cls.all["sections"]

    def test_two_loop_gauge_unification_is_not_exact(self):
        r=self.r["two_loop_GUT_and_complete_multiplet"]
        self.assertGreater(r["SM_one_loop"]["inverse_U1_minus_SU3_mismatch"],5)
        self.assertGreater(abs(r["SM_two_loop_topYukawa_at_one_loop"]["inverse_U1_minus_SU3_mismatch"]),1)
        for label in ("SM_one_loop","SM_two_loop_topYukawa_at_one_loop"):
            s=r[label]
            self.assertAlmostEqual(s["inverse_couplings_at_crossing"][0],
                 s["inverse_couplings_at_crossing"][1],places=8)

    def test_complete_SU5_multiplet_cannot_repair_one_loop_splitting(self):
        r=self.r["two_loop_GUT_and_complete_multiplet"]
        np.testing.assert_allclose(r["vectorlike_Dirac_SU5_5_5bar_beta_shift"],
                                   np.array([2/3]*3))
        np.testing.assert_allclose(
            np.array(r["split_5_fermion_D_shift"])
           +np.array(r["split_5_fermion_L_shift"]),[2/3]*3)

    def test_single_split_5_pair_insufficient_for_exact_one_loop_unification(self):
        r=self.r["two_loop_GUT_and_complete_multiplet"]
        x=r["one_split_Dirac_5_pair_formal_one_loop_full_unification"]
        self.assertFalse(x["feasible_with_MZ_le_mD_mL_le_MU"])
        self.assertGreater(abs(x["required_ln_mL_over_mD"]),x["ln_MU_over_MZ"])
        self.assertLess(x["required_mL_over_mD"],1e-15)
        self.assertGreater(x["scale_GeV"],1e13)

    def test_Majorana_phase_envelope_is_triangle_inequality(self):
        r=self.r["Majorana_phase_envelopes"]
        for ordering, rows in r["envelopes"].items():
            for row in rows:
                lengths=row["amplitudes_eV"]
                self.assertAlmostEqual(row["mbb_max_eV"],sum(lengths))
                self.assertAlmostEqual(row["mbb_min_eV"],
                    max(0,2*max(lengths)-sum(lengths)))
                self.assertLessEqual(row["mbb_min_eV"],row["mbb_max_eV"])

    def test_neutrino_IO_floor_and_NO_cancellation(self):
        r=self.r["Majorana_phase_envelopes"]
        self.assertGreater(r["IO_zero_lightest_mass_mbb_floor_eV"],.015)
        self.assertTrue(r["NO_has_exact_phase_cancellation_for_some_nonzero_lightest_mass"])
        self.assertLess(r["PMNS_unitarity_error"],1e-12)
        self.assertLess(r["Majorana_Takagi_reconstruction_error"],1e-12)

    def test_starobinsky_slowroll_efolds_and_tensor_suppression(self):
        r=self.r["healthy_R2_inflationary_EFT"]
        for row in r["results"]:
            y=row["exp_sqrt_2over3_phi"]
            e=4/(3*(y-1)**2)
            self.assertAlmostEqual(e,row["epsilon"],places=12)
            self.assertAlmostEqual(row["tensor_ratio_r"],16*e,places=12)
            self.assertAlmostEqual(row["scalar_tilt_ns"],
                1-6*e+2*row["eta"],places=12)
        self.assertGreater(r["results"][0]["tensor_ratio_r"],
                           r["results"][2]["tensor_ratio_r"])

    def test_starobinsky_As_reconstruction(self):
        r=self.r["healthy_R2_inflationary_EFT"]
        for row in r["results"]:
            y=row["exp_sqrt_2over3_phi"]
            M=row["M_over_reduced_Mplanck"]
            As=M**2*(1-1/y)**2/(32*np.pi**2*row["epsilon"])
            self.assertAlmostEqual(As/r["slowroll_scalar_amplitude_assumed"],1,places=12)

    def test_cosmological_distance_and_growth_normalization(self):
        r=self.r["CPL_distances_and_linear_growth"]
        for model in ("LCDM","CPL"):
            rows=r[model]
            self.assertTrue(all(row["H_km_s_Mpc"]>0 for row in rows))
            self.assertTrue(all(a["comoving_distance_Mpc"]<
                        b["comoving_distance_Mpc"] for a,b in zip(rows,rows[1:])))
            self.assertTrue(all(0<row["growth_D_over_D_today"]<1 for row in rows))
            self.assertTrue(all(0<row["growth_f"]<1.1 for row in rows))

    def test_CPL_and_LCDM_are_observationally_distinct_not_fitted(self):
        r=self.r["CPL_distances_and_linear_growth"]
        ds=r["CPL_fractional_shifts"]
        self.assertGreater(abs(ds[1]["H_CPL_over_LCDM_minus1"]),.015)
        self.assertLess(abs(ds[4]["H_CPL_over_LCDM_minus1"]),.005)
        self.assertAlmostEqual(r["phantom_crossing_redshift"],.4324324324324325)

    def test_PR_is_no_signaling_not_quantum_not_local(self):
        r=self.r["Bell_local_polytope_and_nosignaling"]
        self.assertEqual(r["PR_nosignaling_CHSH"],4)
        self.assertTrue(r["PR_nosignaling"])
        self.assertAlmostEqual(r["quantum_CHSH"],2*np.sqrt(2),places=12)
        self.assertTrue(r["LP_local_at_visibility_0p70"])
        self.assertTrue(r["LP_nonlocal_at_visibility_0p72"])

    def test_quantum_critical_visibility_exact(self):
        r=self.r["Bell_local_polytope_and_nosignaling"]
        self.assertAlmostEqual(r["critical_isotropic_visibility"],1/np.sqrt(2),places=12)
        self.assertAlmostEqual(r["critical_isotropic_white_noise_fraction"],
                               1-1/np.sqrt(2),places=12)

    def test_all_five_distinct_non_W33_reports(self):
        self.assertEqual(len(self.r),5)
        self.assertTrue(all("PASS"==rec["status"] for rec in self.r.values()))
        self.assertIn("W33",self.all["assumptions"])
        self.assertIn("NOT solved TOE",self.all["claim_level"])

if __name__=="__main__":
    unittest.main()
