"""Regress exact Witting same-label Schmidt witness and W33 dynamic Gauss ring."""
from __future__ import annotations
import sys,unittest,math
from pathlib import Path
import numpy as np
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"analysis"))
import toe_20261122_2design_entanglement_capacity as ent
import toe_20261122_dynamic_W33_gauss_ring as gauge
import toe_20261122_witting_dual_frame_tomography as dual
import toe_20261122_generic_ququart_2design_control as mub

class WittingEntanglementAndGauge(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.ent=ent.run()
        cls.gauge=gauge.run()
        cls.dual=dual.run()
        cls.mub=mub.run()

    def test_40_ray_design_exact(self):
        self.assertEqual(self.ent["rays"],40)
        self.assertLess(self.ent["max_identity_error"],1e-10)

    def test_schmidt_dimensionality_thresholds(self):
        self.assertEqual([r["p_same_upper_bound"] for r in self.ent["Schmidt_number_thresholds"]],
                         [.04,.06,.08])
        self.assertEqual([r["certified_if_exceeded_at_least"]
                          for r in self.ent["Schmidt_number_thresholds"]],[2,3,4])

    def test_isotropic_noise_entanglement_threshold(self):
        r=self.ent["isotropic_scan"]
        self.assertAlmostEqual(next(x["p_same"]for x in r if x["visibility"]==.2),.04)
        self.assertAlmostEqual(next(x["p_same"]for x in r if x["visibility"]==1.),.10)

    def test_separable_coarse_counterexamples(self):
        for rec in self.ent["compressed_separable_counterexamples"]:
            self.assertGreater(rec["p_same_on_explicit_separable_product_state"],
                               rec["p_same_on_maximally_entangled_target"])

    def test_measure_reprepare_is_depolarizing(self):
        self.assertAlmostEqual(self.ent["measure_reprepare_depolarizing_shrinkage"],.2)
        self.assertLess(self.ent["max_tested_reprepare_identity_residual"],1e-10)

    def test_measure_reprepare_capacity_obstruction(self):
        self.assertTrue(self.ent["measure_reprepare_channel_is_entanglement_breaking"])
        self.assertAlmostEqual(self.ent["Choi_singlet_fraction"],.25)

    def test_illustrative_detection_budget_not_guarantee(self):
        r=self.ent["5sigma_illustrative_shots"]
        self.assertEqual([x["illustrative_5sigma_normal_approx_launches"] for x in r],
                          [108267,3008,423])
        self.assertIn("not a finite-shot statistical guarantee",self.ent["limits"])

    def test_verified_w33_four_cycle(self):
        self.assertEqual(self.gauge["W33_cycle"],[0,36,9,37])

    def test_exact_Gauss_constraint_dimension(self):
        self.assertEqual(self.gauge["total_unconstrained_dimension"],64)
        self.assertEqual(self.gauge["Gauss_positive_physical_dimension"],8)

    def test_background_charge_parity_obstruction(self):
        states,_,_,_,_=gauge.build()
        self.assertEqual(len(states),8)
        for m,b in states:self.assertEqual(gauge.gauss(m,b),(1,1,1,1))

    def test_static_AB_destructive_interference(self):
        for x in self.gauge["sweep"]:
            if x["electric_h"]==0:
                self.assertAlmostEqual(x["opposite_vertex_probability"],
                   math.sin(x["t"])**4 if x["initial_flux"]==1 else 0.,places=10)

    def test_electric_flux_nonconservation(self):
        self.assertTrue(self.gauge["electric_field_does_not_commute_with_W"])
        self.assertTrue(self.gauge["Gauss_constraints_preserved"])

    def test_negative_flux_becomes_transmissive_with_quantum_links(self):
        z=self.gauge["negative_flux_dynamic_t1p5_h0p3"]
        self.assertGreater(z["opposite_vertex_probability"],.59)
        self.assertGreater(z["Wilson_expectation"],.54)

    def test_distinguish_model_from_physical_experiment(self):
        self.assertIn("Not a real 2+1D",self.gauge["boundary"])
        self.assertIn("NOT Bell nonlocality",self.ent["limits"])


    def test_both_25bin_local_measurements_remain_informationally_complete(self):
        ranks=[x["single_ququart_Hermitian_POVM_span_rank"]for x in self.dual["layouts"]]
        self.assertEqual(ranks,[16,16,16])

    def test_full_joint_40ray_fidelity_exact_three_classes(self):
        c=self.dual["full_40_exact_minimum_norm_three_class_scores"]
        self.assertAlmostEqual(c["same_ray"],19/4)
        self.assertAlmostEqual(c["orthogonal_rays"],-3/2)
        self.assertAlmostEqual(c["distinct_nonorthogonal_rays"],7/12)

    def test_compressed_tomography_precision_penalty(self):
        x=self.dual["layouts"]
        std=[e["ideal_Phi_single_shot_estimator_SD"]for e in x]
        self.assertAlmostEqual(std[0],1.25,places=9)
        self.assertGreater(std[1],7)
        self.assertGreater(std[2],5)
        self.assertLess(std[2],std[1])

    def test_tomographic_dual_is_unbiased_for_maximally_entangled_target(self):
        for row in self.dual["layouts"]:
            self.assertLess(row["fidelity_reconstruction_residual"],1e-10)
            self.assertAlmostEqual(row["ideal_maximally_entangled_fidelity"],1.,places=9)


    def test_non_Witting_generic_MUB_control_is_exact_projective_two_design(self):
        self.assertEqual(self.mub["ray_outcomes"],20)
        self.assertEqual(self.mub["MUB_bases"],5)
        self.assertLess(self.mub["max_2design_error"],1e-10)
        self.assertLess(self.mub["max_same_label_identity_error"],1e-10)

    def test_generic_MUB_has_same_Schmidt_fidelity_witness_scaled(self):
        self.assertEqual(self.mub["Schmidt_k_same_label_bounds"],[.08,.12,.16])
        self.assertIn("cannot distinguish Witting",self.mub["interpretation"])

if __name__=="__main__":unittest.main()
