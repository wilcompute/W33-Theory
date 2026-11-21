"""Fully offline regression for Witting physical gate / 24D collision certificate.

Uses the 2026-11-21 committed Witting ray and fivefront geometry producers.
Does not crawl websites, modify existing data, or run any hardware.
"""
from __future__ import annotations
import json, math, sys, unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"analysis"))
import toe_20261121_fivefront_physical_falsifiers as a

class TestFivefrontPhysicalFalsifiers(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.rays,_,cls.iso,cls.supports,cls.schedules,cls.graph,cls.mapping=a.geometry()
        cls.opt=a.optical_noise(cls.rays,cls.supports,cls.schedules)
        cls.sched=a.scheduler(cls.supports,cls.schedules,cls.graph)
        cls.channel=a.channel(cls.rays,cls.mapping)
        cls.selector=a.selector(cls.rays,cls.supports,cls.schedules,cls.graph)
        cls.memory=a.causal_memory(cls.iso,cls.graph)
    def test_universal_port_counts_and_shot_survival(self):
        x=self.opt
        self.assertEqual((x["universal_4mode_MZI_count"],x["universal_8mode_MZI_count"]),(6,28))
        self.assertEqual((x["four_mode_PVM_settings"],x["eight_mode_doubleSIC_settings_per_deck"]),(40,5))
        self.assertEqual(len(x["loss_sensitivity_benchmark"]),8)
        self.assertTrue(all(0<b["pvm_40setting_survival"]<1 for b in x["loss_sensitivity_benchmark"]))
    def test_adversarial_detector_loss_mimics_entanglement(self):
        self.assertAlmostEqual(self.opt["biased_postselected_separable_match"],.28)
        self.assertAlmostEqual(self.opt["unfiltered_separable_match_bound"],.2)
        self.assertGreater(self.opt["biased_postselected_separable_match"],.2)
    def test_27_optimal_five_chart_covers(self):
        self.assertEqual(self.sched["all_minimal_exact_disjoint_covers"],27)
        self.assertEqual(self.sched["cost_visible_rank"],21)
        self.assertEqual(self.sched["cost_invisible_nullity"],24)
    def test_24dim_deck_cost_nullspace(self):
        self.assertLess(self.sched["max_27_schedule_cost_deviation_for_nonuniform_invisible_cost"],1e-12)
        self.assertLess(self.sched["random_cost_min_total"],self.sched["random_cost_mean_total"])
        self.assertGreater(self.sched["random_cost_max_total"],self.sched["random_cost_mean_total"])
    def test_fullrank_entanglement_breaking_Choi(self):
        self.assertEqual(self.channel["Choi_normalized_rank"],36)
        self.assertGreater(self.channel["Choi_normalized_min_eigen"],0)
        self.assertGreater(self.channel["Choi_PPT_min_eigen"],0)
        self.assertEqual(self.channel["explicit_separable_Choi_terms"],40)
        self.assertEqual(self.channel["quantum_capacity"],0)
    def test_entanglement_fidelity_and_diamond_no_go(self):
        self.assertEqual(self.channel["universal_entanglement_fidelity_upper_bound_for_every_isometry"],.25)
        self.assertEqual(self.channel["diamond_norm_distance_lower_bound_from_any_ideal_isometry"],1.5)
        self.assertTrue(all(f<.25+1e-12 for f in
            self.channel["isometry_reference_entanglement_fidelity_10samples"]))
    def test_complete_780pair_collision_sector_exact_GF7_rank(self):
        d=self.selector
        self.assertEqual(d["all_780_centered_pair_collision_vectors_span_rank"],24)
        self.assertEqual(d["exact_centered_collision_rank_over_GF7"],24)
        self.assertTrue(d["exact_integer_kernel_residual_zero"])
        self.assertLess(d["centered_collision_deck_null_residual"],1e-10)
        self.assertLess(d["centered_collision_minus3_eigenspace_residual"],1e-10)
    def test_all_nonorthogonal_pairs_unique_three_level_selector(self):
        d=self.selector
        self.assertEqual(d["two_copy_joint_collision_max_degeneracy_histograms"]["nonorthogonal"],{1:540})
        self.assertEqual(d["quartic_collision_unique_max_matches_incidence_chart"]["nonorthogonal"],540)
        self.assertEqual(d["two_copy_joint_collision_max_degeneracy_histograms"]["orthogonal"],{3:240})
        self.assertAlmostEqual(d["minimum_nonorthogonal_score_maximum_margin"],1/3)
        self.assertEqual(d["exact_nonorthogonal_chart_score_histogram_times9"],{4:12,5:32,8:1})
        self.assertEqual(d["exact_orthogonal_chart_score_histogram_times9"],{0:3,3:12,4:27,6:3})
    def test_two_copy_physical_limit_and_shot_bound(self):
        d=self.selector
        self.assertAlmostEqual(d["nonorthogonal_ray_projector_commutator_norm"],math.sqrt(2)/3)
        self.assertTrue(d["total_chart_intensity_selector_is_impossible"])
        self.assertAlmostEqual(d["matched_doubleSIC_nonorthogonal_probability_margin"],1/12)
        self.assertGreater(d["assumed_total_45chart_trials"],100_000)
        self.assertGreater(d["min_random_ground_gap_with_norm0p4_perturbation"],.2)
    def test_full_symmetry_reverses_all_causal_edges(self):
        d=self.memory
        self.assertEqual(d["all_ordered_incident_pairs_single_orbit"],540)
        self.assertTrue(d["one_element_reverses_any_given_edge"])
        self.assertEqual(d["two_ticks_accessible_spatial_vertices"],45)
        self.assertAlmostEqual(d["two_tick_markov_probability_any_other_vertex"],1/48)
    def test_qutrit_quantum_memory_dimension_threshold(self):
        d=self.memory
        self.assertEqual(d["qutrit_two_design_probes"],12)
        self.assertEqual(d["qutrit_EB_memory_fidelity_upper_bound"],.5)
        self.assertEqual(d["qutrit_intermediate_quantum_memory_dim_le_2_fidelity_upper_bound"],.75)
    def test_frozen_commit_certificate(self):
        obj=json.loads((ROOT/"data/toe_20261121_device_scheduler_channel_causal_audit.json").read_text(encoding="utf8"))
        self.assertEqual(obj["status"],"PASS")
        self.assertEqual(len([x for x in obj if x.startswith("front_")]),5)

if __name__=="__main__":unittest.main()
