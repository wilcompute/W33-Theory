#!/usr/bin/env python3
"""Cross-track regression tests: 5 physical gates + G2/E6 external-paper checks."""
import sys
import unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"analysis"))
import toe_20261119_five_orthogonal_vacuum_causal_memory_SU3_anomaly as gates
import toe_20261119_G2_E6_Fano27_45_tritangent_crosscheck as ex

class IndependentPhysicsGates(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.x=gates.run()["tracks"]
        cls.y=ex.run()
    def test_causal_4_event_enumeration(self):
        a=self.x["causal_order"]["censuses"][0]
        self.assertEqual((a["graph_presentations"],a["distinct_causal_orders_with_fixed_label_order"]),(64,40))
        self.assertEqual(a["orders_with_multiple_edge_presentations"],14)
    def test_causal_5_event_enumeration(self):
        a=self.x["causal_order"]["censuses"][1]
        self.assertEqual((a["graph_presentations"],a["distinct_causal_orders_with_fixed_label_order"]),(1024,357))
        self.assertEqual(a["orders_with_multiple_edge_presentations"],199)
        self.assertGreater(a["maximum_response_spread_within_one_order"],3)
    def test_canonical_Hasse_repair(self):
        for a in self.x["causal_order"]["censuses"]:
            self.assertEqual(a["Hasse_canonical_response_spread_within_one_order"],0.)
    def test_exact_SIC_hessian_lift(self):
        a=self.x["H27_SIC_MUB_mass_repair"]
        self.assertEqual(a["SIC_Hessian_determinant"],"162*l**2")
        self.assertGreater(a["all_27_SIC_stationary_vectors_min_singular_Hessian"],.1)
        self.assertLess(a["exact_SIC_F_residual"],1e-12)
    def test_SIC_MUB_projective_stability(self):
        a=self.x["H27_SIC_MUB_mass_repair"]
        for key in ("SIC_projective_Gram_residual","support3_F_residual",
                    "support3_MUB_within_basis_residual","support3_MUB_between_basis_residual"):
            self.assertLess(a[key],1e-12)
    def test_full_H27_invariant_Hessian_Higgs_caveat(self):
        a=self.x["H27_SIC_MUB_mass_repair"]
        self.assertLess(a["nine_triplet_frame_moment_map_traceless_residual"],1e-12)
        self.assertIn("not full continuous SU3",a["limitations"])
    def test_spin10_16_anomaly_census(self):
        a=self.x["SM_SO10_anomalies"]
        self.assertEqual(a["one_16_with_nuR"],["0"]*5+[0])
    def test_15_no_sterile_neutrino_anomaly_no_go(self):
        a=self.x["SM_SO10_anomalies"]
        self.assertEqual(a["one_15_without_nuR"],a["one_16_with_nuR"])
        self.assertNotEqual(a["without_charged_eR"],a["one_16_with_nuR"])
    def test_SU3_two_phase_readout(self):
        a=self.x["SU3_phased_Wilson"]
        self.assertLess(a["reconstructed_trace_error"],1e-12)
        self.assertGreater(a["W_vs_Wdag_pi_over2_intensity_difference"],2)
        self.assertLess(a["W_vs_Wdag_zero_phase_spectrum_error"],1e-12)
    def test_SU3_characters_and_gauge_frames(self):
        a=self.x["SU3_phased_Wilson"]
        self.assertLess(a["SU3_characteristic_polynomial_residual"],1e-12)
        self.assertLess(a["24_random_frame_max_trace_error"],1e-12)
    def test_temporal_conditional_entanglement(self):
        a=self.x["temporal_qutrit_heralding"]
        for row in a["dephasing_scan"]:
            self.assertAlmostEqual(row["GHZ_coherence"],row["conditional_BC_negativity"],places=12)
    def test_white_noise_threshold(self):
        a=self.x["temporal_qutrit_heralding"]
        self.assertEqual(a["heralded_BC_entanglement_visibility_threshold"],"v>1/4")
        self.assertAlmostEqual(a["white_noise_scan"][2]["conditional_negativity"],0,places=12)
        self.assertGreater(a["white_noise_scan"][3]["conditional_negativity"],0)
    def test_Fano_cubic_line_point_samples(self):
        a=self.y["G2_27_cubic_pencil"]
        self.assertEqual(a["random_unit_line_basepoints"],32)
        self.assertLess(a["max_trace_cubic_error_from_210"],1e-10)
        self.assertLess(a["max_phi_cubic_error_from_84"],1e-10)
    def test_critical_E6_pencil_polynomial(self):
        a=self.y["G2_27_cubic_pencil"]
        self.assertEqual(a["critical_lambda_quadratic"],"8*lambda^2-2*lambda+1")
        self.assertEqual(len(a["critical_lambda"]),2)
    def test_27_45_tritangent_incidence(self):
        a=self.y["E6_cubic_surface_lines"]
        self.assertEqual((a["lines"],a["tritangent_planes"]),(27,45))
        self.assertEqual((a["mixed_E_L_Q_tritangents"],a["three_pair_L_tritangents"]),(30,15))
        self.assertEqual(a["tritangents_incident_to_each_line"],5)
    def test_E6_intersection_graph_spectrum(self):
        a=self.y["E6_cubic_surface_lines"]
        self.assertEqual(a["intersection_graph_strongly_regular_parameters"],[27,10,1,5])
        self.assertEqual(a["intersection_graph_eigenvalues"],{"-5":6,"1":20,"10":1})

if __name__=="__main__": unittest.main()
