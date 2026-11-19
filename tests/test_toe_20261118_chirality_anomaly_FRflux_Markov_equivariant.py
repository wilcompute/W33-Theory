"""Regression suite for 5 research fronts: domain-wall chiral index,
gauged E8 family anomalies, M2 flux, quantum Markov counterexample,
and compensated C3 equivariance. No physical TOE claim."""
import unittest,sys,math
from pathlib import Path
import numpy as np
import sympy as s
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/"analysis"))
import toe_20261118_chirality_anomaly_FRflux_Markov_equivariant as T

class TOEInterfaces(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.r=T.run()
        cls.k=cls.r["localized_chirality"]
        cls.a=cls.r["E8_anomaly"]
        cls.f=cls.r["FR_flux_quantization"]
        cls.m=cls.r["Markov_qutrit_counterexample"]
        cls.e=cls.r["equivariant_family_selection"]

    def test_domainwall_plus_index(self):
        self.assertEqual(self.k["positive_mass_profile_Fredholm_index"],1)
    def test_domainwall_reverse_index(self):
        self.assertEqual(self.k["negative_mass_profile_Fredholm_index"],-1)
    def test_domainwall_three_channels_not_prediction(self):
        self.assertEqual(self.k["three_independent_positive_wall_channels_index"],3)
        self.assertIn("toy",self.k["scope"])
    def test_domainwall_norm_mu1(self):
        self.assertEqual(self.k["rows"][0]["L2_norm_squared"],"2")
    def test_domainwall_norm_mu2(self):
        self.assertEqual(self.k["rows"][1]["L2_norm_squared"],"4/3")
    def test_domainwall_conjugate_total(self):
        self.assertEqual(self.k["formal_direct_sum_of_both_charges_total_index"],0)
    def test_E6_27_psi_trace(self):
        self.assertEqual(self.a["psi_trace_in_one_complete_27"],0)
    def test_E6_27_psi_cubed_trace(self):
        self.assertEqual(self.a["psi_cubic_trace_in_one_complete_27"],0)
    def test_E6_27_SU5_cubic(self):
        self.assertEqual(self.a["single_27_SU5_cubic_anomaly"],0)
    def test_family_triplet_anomaly27(self):
        self.assertEqual(self.a["one_chiral_27x3_family_SU3_cubic_anomaly"],27)
    def test_conjugate_triplet_anomaly_minus27(self):
        self.assertEqual(self.a["one_chiral_27barx3bar_family_SU3_cubic_anomaly"],-27)
    def test_family_anomaly_pair_cancels(self):
        self.assertEqual(self.a["complete_E8_adjoint_pair_family_anomaly"],0)
    def test_no_local_gauged_SU3_only_triplet(self):
        self.assertFalse(self.a["only_27x3_with_gauged_SU3_family_consistent_without_inflow_or_extra_matter"])
    def test_FR_exact_S7_N(self):
        self.assertEqual(self.f["exact_N"],"2*L^6/(pi^2*lp^6)")
    def test_FR_flux_integer_cannot_select_81(self):
        self.assertIn("independent quantized input",self.f["caveat"])
    def test_FR_round_S7_radius(self):
        self.assertEqual(self.f["exact_R7_to_lp"],"(32*pi^2*N)^(1/6)")
    def test_FR_tau_scaling(self):
        self.assertEqual(self.f["nearparallel_tau0_lp"],"2/(pi^2*N/2)^(1/6)")
    def test_FR_sample_N_81_and240(self):
        r={v["integer_flux_N"]:v for v in self.f["examples"]}
        self.assertTrue(5<r[81]["sphere_R_in_Planck_lengths"]<6)
        self.assertTrue(6<r[240]["sphere_R_in_Planck_lengths"]<7)
    def test_FR_large_N_radius_grows(self):
        r=self.f["examples"]
        self.assertLess(r[0]["sphere_R_in_Planck_lengths"],r[-1]["sphere_R_in_Planck_lengths"])
    def test_markov_one_step_SN3(self):
        self.assertGreater(s.Rational(self.m["one_step_entanglement_fidelity"]),s.Rational(2,3))
    def test_markov_two_steps_SN3(self):
        self.assertGreater(s.Rational(self.m["two_steps_entanglement_fidelity"]),s.Rational(2,3))
    def test_markov_MUB_witness_both(self):
        self.assertGreater(s.Rational(self.m["one_step_fourMUB_match_probability"]),s.Rational(3,4))
        self.assertGreater(s.Rational(self.m["two_steps_fourMUB_match_probability"]),s.Rational(3,4))
    def test_markov_counterexample_composition(self):
        self.assertLess(self.m["direct_matrix_composition_max_error"],1e-12)
        self.assertFalse(self.m["process_tensor_genuinely_multitime_quantum_memory"])
    def test_markov_env_independent(self):
        self.assertIn("fresh",self.m["Markov_reason"])
    def test_equivariant_quartic_q2(self):
        self.assertEqual(self.e["quartic_n3_requires_character_q"],2)
    def test_equivariant_two_sectors(self):
        self.assertEqual(self.e["E8_H27_family_triplet_center_character_q"],1)
        self.assertEqual(self.e["E8_H27_antitriplet_center_character_q"],2)
    def test_equivariance_does_not_select_n3(self):
        a=[v["Morse_family_count_parameter_n"] for v in self.e["census"]
           if v["compensation_center_character_q"]==2]
        self.assertEqual(a,[3,6,9,12])
    def test_equivariance_requires_geometric_assumption(self):
        self.assertIn("only if",self.e["limitation"])
    def test_results_are_not_TOE(self):
        self.assertFalse(self.r["physical_TOE"])

if __name__=="__main__":unittest.main()
