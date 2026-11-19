"""Regression tests for W33-independent, model-independent TOE physical sieve.

These test *necessary consistency relations*, not claims of a discovered TOE.
"""
import itertools
import pathlib
import sys
import unittest
import numpy as np
import sympy as sp

ROOT=pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"analysis"))
import toe_20261119_model_independent_consistency as t


class TOEConstraints(unittest.TestCase):

    def test_anomaly_polynomials_exact_zero_all_hypercharge_mixings(self):
        r=t.anomaly_ambiguity()
        self.assertEqual(r["anomaly_polynomials"],{
           "SU3_squared_U1":"0","SU2_squared_U1":"0",
           "gravity_squared_U1":"0","U1_cubed":"0"})
        self.assertEqual(r["Yukawa_charge_residuals"],["0"]*4)

    def test_B_minus_L_requires_neutrino_for_anomaly_freedom(self):
        r=t.anomaly_ambiguity()
        x=sp.symbols("t")
        self.assertEqual(sp.sympify(r["without_nuR_gravity_B_minus_L_mixing_anomaly"]),-x)
        self.assertNotEqual(sp.sympify(r["without_nuR_U1_cubed_mixed_anomaly"]),0)
        self.assertEqual(r["SU2_Witten_number_doublets_per_generation"],4)
        self.assertEqual(r["bare_nuR_Majorana_mass_U1_charge"],"2*t")
        self.assertEqual(r["Weinberg_LH_squared_U1_charge"],"-2*t")
        self.assertEqual(r["Majorana_mass_or_unspurioned_Weinberg_operator_forces_mixing_t"],0)

    def test_one_loop_gauge_pair_crossings_are_not_a_triple_crossing(self):
        r=t.gauge_unification()
        self.assertGreater(r["U1_SU3_inverse_mismatch_at_crossing"],5)
        g=r["inverse_couplings_at_U1_SU2_crossing"]
        self.assertAlmostEqual(g[0],g[1],places=10)
        self.assertAlmostEqual(g[0]-g[2],5.580376890281443,places=8)
        self.assertGreater(r["U1_SU2_crossing_GeV"],1e13)

    def test_simple_sharp_MSSM_threshold_is_inconsistent_below_MZ(self):
        r=t.gauge_unification()
        fit=r["simple_sharp_SM_MSSM_extrapolation"]
        self.assertTrue(fit["invalid_with_threshold_below_MZ"])
        self.assertLess(fit["best_equal_meeting_threshold_GeV"],r["input"]["MZ_GeV"])
        self.assertGreater(fit["unification_GeV"],1e16)
        self.assertLess(r["MSSM_sharp_threshold_1TeV"]["predicted_alpha_s_MZ"],.118)

    def test_neutrino_lower_sums_and_mass_scale(self):
        r=t.neutrino_spectrum()
        self.assertAlmostEqual(r["minimum_sum_NO_eV"],.05873293681861549,places=10)
        self.assertAlmostEqual(r["minimum_sum_IO_eV"],.09961657665582832,places=10)
        self.assertGreater(r["minimum_sum_IO_eV"],r["minimum_sum_NO_eV"])
        v=r["v_EW_GeV"];mass=r["reference_neutrino_mass_eV"]*1e-9
        self.assertAlmostEqual(r["Lambda_over_kappa_GeV"]*2*mass/v**2,1)

    def test_neutrino_sum_monotone_with_lightest_mass(self):
        delta21=7.465e-5;delta31=2.5093e-3
        f=lambda m: m+np.sqrt(m*m+delta21)+np.sqrt(m*m+delta31)
        self.assertGreater(f(.001),f(0))
        self.assertGreater(f(.05),f(.01))

    def test_CPL_density_analytic_continuity_and_phantom_crossing(self):
        r=t.dark_energy()
        zc=r["crosses_phantom_divide_at_z"]
        w=lambda z:r["w0"]+r["wa"]*z/(1+z)
        self.assertAlmostEqual(w(zc),-1,places=12)
        self.assertLess(w(1),-1)
        samples=r["samples"]
        self.assertAlmostEqual(samples[0]["dark_energy_density_relative_today"],1)
        z=.65;h=1e-5
        density=lambda z: (1+z)**(3*(1+r["w0"]+r["wa"]))*np.exp(
                           -3*r["wa"]*z/(1+z))
        derivative=(np.log(density(z+h))-np.log(density(z-h)))/(2*h)
        self.assertAlmostEqual(derivative,3*(1+w(z))/(1+z),places=8)

    def test_ghost_residue_sign_and_bh_thermodynamic_scaling(self):
        r=t.quantum_gravity_filters()
        prop=r["fourth_order_scalar_toy"]
        self.assertEqual((prop["massless_pole_residue"],
                          prop["massive_pole_residue"]),("1","-1"))
        bh=r["black_hole_one_solar_mass"]
        self.assertGreater(bh["Bekenstein_Hawking_entropy_over_k"],1e77)
        self.assertAlmostEqual(bh["Schwarzschild_radius_m"],2953.3,delta=1)
        self.assertAlmostEqual(bh["Hawking_temperature_K"],6.17e-8,delta=1e-10)

    def test_CHSH_classical_and_quantum_bounds(self):
        r=t.bell_quantum()
        classical_values=[]
        for a,ap,b,bp in itertools.product((-1,1),repeat=4):
            classical_values.append(a*b+a*bp+ap*b-ap*bp)
        self.assertEqual(max(map(abs,classical_values)),2)
        self.assertAlmostEqual(r["observed_toy_state_CHSH"],2*np.sqrt(2),places=12)
        self.assertGreater(r["no_signaling_PR_box_algebraic_max"],r["quantum_Tsirelson_abs_max"])

    def test_all_six_independent_constraints(self):
        report=t.certify()
        self.assertEqual(report["all_certificates"],"PASS")
        self.assertEqual(len(report["frontiers"]),6)
        self.assertTrue(all(f["status"].startswith("PASS") for f in report["frontiers"].values()))


if __name__=="__main__":
    unittest.main()
