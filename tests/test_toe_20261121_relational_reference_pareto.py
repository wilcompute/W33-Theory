"""Regression tests for independent Witting relational-channel continuation."""
from __future__ import annotations
import json, math, sys, unittest
from pathlib import Path
import numpy as np
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"analysis"))
import toe_20261121_relational_reference_pareto as m

class RelationalWittingFronts(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.rays,cls.H,cls.A,cls.P=m.geometry()
        cls.cal=m.calibration(cls.H,cls.P[2])
        cls.priv=m.privacy(cls.H,cls.P[2])
        cls.rel=m.relational_bath(cls.P)
        cls.gate=m.chart_gate(cls.rays,cls.H)
        cls.petz=m.petz_dilation(cls.rays)
        cls.phase=m.phases(cls.rays)

    def test_exact_chart_ray_incidence(self):
        self.assertEqual(self.H.shape,(45,40))
        self.assertEqual(set(self.H.sum(axis=1)),{8})
        self.assertEqual(set(self.H.sum(axis=0)),{9})

    def test_complete_45D_projector_resolution(self):
        P1,P20,P24=self.P
        np.testing.assert_allclose(P1+P20+P24,np.eye(45),atol=1e-12)
        self.assertEqual([round(np.trace(z)) for z in self.P],[1,20,24])

    def test_unknown_efficiency_optimal_calibration_split(self):
        self.assertAlmostEqual(self.cal["Cramer_Rao_coefficient"],17.06666666667,places=9)
        self.assertAlmostEqual(self.cal["per_launch_Fisher_eigenvalue"],1.40625)

    def test_cost_asymmetric_optimal_budget_allocation(self):
        self.assertAlmostEqual(self.cal["reference_budget_fraction_if_reference_cost_4x"],2/3)
        self.assertAlmostEqual(self.cal["reference_launch_fraction_if_reference_cost_4x"],1/3)

    def test_new_detector_dominates_previous_under_ideal_noise(self):
        prior=self.priv["noise_sweep"][0]["old"]
        new=self.priv["noise_sweep"][0]["new"]
        self.assertLess(new[0],prior[0])
        self.assertLess(new[1],prior[1])
        self.assertAlmostEqual(new[0],1.412155394967,places=9)
        self.assertAlmostEqual(new[1],11.322222222222,places=8)

    def test_dominance_survives_five_and_fifteen_percent_mislabel(self):
        for v in self.priv["noise_sweep"][1:]:
            self.assertLess(v["new"][0],v["old"][0])
            self.assertLess(v["new"][1],v["old"][1])

    def test_privacy_only_minimum_does_not_minimize_fisher_error(self):
        v=self.priv["noise_sweep"][0]
        self.assertLess(v["minimum_leakage"][0],v["new"][0])
        self.assertGreater(v["minimum_leakage"][1],v["new"][1])

    def test_relational_interaction_populates_24D_sector(self):
        pops=self.rel["sector_populations"]
        self.assertAlmostEqual(pops[0]["sector_populations"][2],0,places=11)
        self.assertAlmostEqual(pops[1]["sector_populations"][2],96/2025,places=11)
        self.assertAlmostEqual(pops[-1]["sector_populations"][2],24/45,delta=1e-4)

    def test_open_system_vs_closed_system_caveat(self):
        self.assertTrue(self.rel["reference_interaction_offdiagonal_factor"]<1)
        self.assertIn("Open-system",self.rel["caution"])

    def test_non_circular_45gate_compiler(self):
        self.assertEqual(self.gate["charts"],45)
        self.assertLess(self.gate["max_matrix_residual"],1e-10)
        self.assertEqual(self.gate["canonical_CNOT_upper_bound"],14)

    def test_Petz_fidelity_reproduced(self):
        self.assertEqual(self.petz["best_seeded_subcode_index"],261)
        self.assertAlmostEqual(self.petz["entanglement_fidelity"],0.9034972067200646,places=9)

    def test_Petz_deterministic_ten_mode_dilation(self):
        self.assertEqual(self.petz["recovery_dilation_shape"],[10,9])
        self.assertEqual(self.petz["unitary_extension_shape"],[10,10])
        self.assertEqual(self.petz["recovery_Kraus_count"],5)
        self.assertLess(self.petz["isometry_error"],1e-10)

    def test_triangle_phase_loop_census(self):
        self.assertEqual(self.phase["triangle_count"],
                         {"zero":6640,"pi_over_6":2880,"pi_over_2":360})
        self.assertTrue(self.phase["conjugation_odd"])

    def test_certificate_if_generated(self):
        path=ROOT/"data/toe_20261121_relational_reference_pareto.json"
        if not path.exists():
            self.skipTest("Run analysis producer first; certificate is generated locally")
        record=json.loads(path.read_text(encoding="utf-8"))
        self.assertEqual(record["status"],"PASS")
        self.assertEqual(len([k for k in record if k.startswith("front")]),6)

if __name__=="__main__":unittest.main()
