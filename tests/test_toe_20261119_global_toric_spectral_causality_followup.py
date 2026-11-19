"""Focused independent regressions for six physics-first TOE follow-ups."""
import sys, unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"analysis"))
import toe_20261119_global_toric_spectral_causality_followup as q

class FollowupSixFronts(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.v=q.e8_five_driver_full_singlet_vacuum()
        cls.g=q.three_adjoint_radiative_sensitivity()
        cls.s=q.spin_c_global_family_gate()
        cls.c=q.causal_link_valency_diagnostic()
        cls.p=q.pure_quantum_state_nonuniqueness()
        cls.o=q.phase_noisy_two_copy_photons()

    def test_all_eight_charged_singlets_are_nonzero(self):
        self.assertEqual(len(self.v["singlet_vev_magnitudes"]),8)
        self.assertTrue(all(x>0 for x in self.v["singlet_vev_magnitudes"]))
        self.assertEqual(self.v["three_D_term_residual"],[0,0,0])

    def test_five_toric_invariants_have_independent_exponents(self):
        self.assertEqual(self.v["invariant_exponent_rank"],5)
        self.assertEqual(self.v["gauge_rank"],3)
        self.assertEqual(self.v["generic_complex_moduli_before_drivers"],5)

    def test_all_fterms_vanish(self):
        self.assertTrue(all(abs(x)<1e-12 for x in self.v["F_driving_residual"]))
        self.assertTrue(all(abs(x)<1e-12 for x in self.v["F_charged_residual"]))

    def test_13_field_hessian_has_only_gauge_null_directions(self):
        self.assertEqual(self.v["W_hessian_rank"],10)
        self.assertEqual(self.v["Hessian_kernel_gauge_dimension"],3)
        self.assertLess(self.v["linearized_gauge_orbit_coupling_norm"],1e-11)
        self.assertEqual(self.v["local_complex_moduli_after_five_drivers"],0)

    def test_gravitational_R_anomaly_parity(self):
        self.assertEqual(self.v["Z4R_gravitational_coefficient_after_five_R2_neutral_drivers"],-16)
        self.assertEqual(self.v["Z4R_gravitational_mod2"],0)

    def test_three_adjoint_running_is_conditional(self):
        self.assertLess(self.g["original_three_adjoint_one_loop_spread"],1e-9)
        self.assertGreater(self.g["original_low_octet_GeV"],1e4)
        self.assertIn("no",self.g["conclusion"].lower())

    def test_adjoint_mass_cancellation_is_ultrafragile(self):
        self.assertLess(self.g["ten_percent_octet_shift_relative_to_MU"],3e-13)
        self.assertGreater(self.g["SU5_invariant_mass_shifts"][-1]["inverse_coupling_spread"],4)

    def test_spin_c_CP2_only_odd_flux_is_valid(self):
        vals=self.s["flux_index_table"]
        self.assertTrue(all(row["Spin_c_admissible"]==(row["c1_coefficient"]%2==1)
                            for row in vals))
        self.assertTrue(all(float(row["formal_index"]).is_integer() for row in vals
                            if row["Spin_c_admissible"]))

    def test_CP2_three_family_index_is_input_not_prediction(self):
        self.assertEqual(self.s["k_plus5_index"],3)
        self.assertTrue(self.s["CP2_observed_families_NOT_derived"])
        self.assertTrue(self.s["CP2_not_spin"])

    def test_flat_spin_gauge_twist_depends_on_charge_parity(self):
        z=self.s["charge_specific_torus_holonomy_cancellation"]
        self.assertEqual([a["zero_momentum_possible"] for a in z],[False,True,False,True])

    def test_expected_causal_links_grow(self):
        rows=self.c["sampled"]
        self.assertEqual(len(rows),6)
        self.assertTrue(all(rows[j+1]["E_links_3plus1_truncated_cone"]>
                            rows[j]["E_links_3plus1_truncated_cone"]
                            for j in range(5)))

    def test_4D_causal_link_asymptotic(self):
        from math import pi,sqrt
        self.assertAlmostEqual(self.c["E4_asymptotic_coefficient"],pi*sqrt(6),places=10)
        self.assertLess(abs(self.c["sampled"][-1]["E4_over_sqrt_rho"]-pi*sqrt(6)),.25)

    def test_two_event_pure_squeezed_quantum_states_have_same_commutator(self):
        self.assertEqual(len(self.p["state_samples"]),4)
        self.assertTrue(all(z["commutator_error"]<1e-12 for z in self.p["state_samples"]))
        self.assertTrue(all(abs(z["symmetrized_variance_det"]-.25)<1e-12
                            for z in self.p["state_samples"]))

    def test_purity_does_not_fix_quantum_state(self):
        rows=self.p["state_samples"]
        self.assertGreater(rows[-1]["position_variance"],rows[0]["position_variance"])
        self.assertGreater(rows[-1]["momentum_variance"],0.)
        self.assertTrue(all(min(z["positive_W_eigenvalues"])>-1e-12 for z in rows))

    def test_phase_noise_CHSH_exact_horodecki(self):
        from math import sqrt
        rows=self.o["samples"]
        self.assertAlmostEqual(rows[0]["ideal_conditional_CHSH_max"],2*sqrt(2),places=11)
        self.assertAlmostEqual(rows[0]["CHSH_max_with_white_weight_0p82"],
                               1.64*sqrt(2),places=11)

    def test_phase_reference_is_required_with_white_noise(self):
        rows=self.o["samples"]
        self.assertGreater(rows[0]["CHSH_max_with_white_weight_0p82"],2)
        self.assertLess(rows[-1]["CHSH_max_with_white_weight_0p82"],2)
        self.assertAlmostEqual(self.o["transmission_eta_0p8_ideal_QND_herald_probability"],
                               .32,places=12)

if __name__=="__main__":unittest.main()
