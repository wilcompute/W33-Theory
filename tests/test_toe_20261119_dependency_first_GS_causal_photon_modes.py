"""Tests for causal, GS-center, localized flavor, orbifold and photonic dependency gates."""
import unittest,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"analysis"))
import toe_20261119_dependency_first_GS_causal_photon_modes as m
class DependencyFirstGates(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.a=m.e8_GS_Higgs_center_bridge()
        cls.c=m.causal_wave_operator_failure()
        cls.y=m.Yukawa_geometry_action_target()
        cls.g=m.orbifold_reps_and_boundary_mass()
        cls.p=m.one_photon_information_capacity()
        cls.e=m.photon_falsifier_resource_budget()
        cls.d=m.dependency_DAG()
    def test_E8_Higgs_integral_character_index(self):
        self.assertEqual(self.a["Higgs_Smith_invariants"],[1,1,4])
        self.assertEqual(self.a["combined_Higgs_plus_GS_Smith_invariants"],[1,1,4])
    def test_both_GS_directions_exist_in_existing_higgs_phase_lattice(self):
        self.assertEqual(self.a["two_GS_shift_charge_vectors"],[[2,1,1],[0,1,-5]])
        self.assertIn("theta_D",self.a["GS_shift1_exact_Higgs_phase"])
        self.assertIn("-2 theta_A",self.a["GS_shift2_exact_Higgs_phase"])
    def test_Spin10_center_character_congruence(self):
        r=self.a["representation_residues"]
        self.assertEqual([r[str(k)]["sum_charge_mod4"] for k in (16,10,1)],[1,2,0])
    def test_center_is_not_new_R_symmetry(self):
        self.assertIn("NOT automatically",self.a["center_interpretation"])
        self.assertIn("not derived",self.a["physical_remaining"])
    def test_causal_scalar_constant_limit(self):
        self.assertEqual(self.c["constant_limit"],3)
        self.assertLess(abs(self.c["numerical"][-1]["weighted_constant"]-3),.004)
    def test_causal_ordinary_wave_operator_known_nonzero(self):
        self.assertEqual(self.c["continuum_Box_on_probe"],-8)
        self.assertAlmostEqual(self.c["numerical"][-1]["weighted_s_t2_minus_r2"],-.0993042632,places=7)
        self.assertEqual(self.c["s_probe_limit"],0)
    def test_causal_counterexample_is_narrow(self):
        self.assertIn("DOES NOT",self.c["negative_result"])
        self.assertIn("only invalidates",self.c["not_a_no_go"].lower())
    def test_M2_action_hierarchy_target(self):
        from math import log
        self.assertAlmostEqual(self.y["dimensionless_Euclidean_M2_action_difference_if_equal_prefactors"],
                               log(self.y["minimum_unknown_overlap_times_Higgs_projection_ratio"]),places=12)
        self.assertGreater(self.y["minimum_unknown_overlap_times_Higgs_projection_ratio"],69000)
    def test_Gaussian_overlap_width_ratio(self):
        from math import exp
        x=self.y["Gaussian_triple_overlap_required_displacement_in_widths"]
        R=self.y["minimum_unknown_overlap_times_Higgs_projection_ratio"]
        self.assertAlmostEqual(exp(-x*x/3),1/R,places=12)
        self.assertGreater(x,5.)
    def test_hierarchy_still_requires_physical_geometry(self):
        self.assertIn("neither",self.y["critical_caveat"].lower())
        self.assertIn("instanton actions",self.y["minimal_geometric_task"])
    def test_SU5_parity_triplet_octet_equal(self):
        self.assertEqual(self.g["shared_flavor_parity_example"]["common_plusplus_dim"],1)
        self.assertIn("identical",self.g["exact_same_count_theorem"])
    def test_SU5_boundary_mass_escape_is_assumption(self):
        self.assertTrue(self.g["one_octet_two_triplets_example"])
        self.assertEqual(len(self.g["low_energy_octet_boundary_mass_example_GeV"]),2)
        self.assertIn("no 5D",self.g["important_limit"])
    def test_photon_40_and_240_mode_dimensions(self):
        self.assertEqual(self.p["40_mode_qubit_upper_bound"],5)
        self.assertEqual(self.p["240_mode_qubit_upper_bound"],7)
        for r in self.p["mode_table"]:
            self.assertLessEqual(2**r["qubits_max_by_subspace_dimension"],r["dimension"])
    def test_single_photon_passive_linear_optics_norm(self):
        self.assertAlmostEqual(self.p["240_mode_600_passive_gate_simulator_final_norm"],1.,places=12)
        self.assertIn("complex amplitude",self.p["classical_simulation"])
    def test_event_ready_experiment_detects_hypothetical_one_percent_shift(self):
        self.assertEqual(self.e["detected_successful_events_in_preregistered_fixed_setting"],55000)
        self.assertGreater(self.e["upper_alternative_power"],.90)
        self.assertLess(self.e["two_sided_null_tail_for_symmetric_p0"],.001)

    def test_event_ready_experiment_is_not_a_TOE_prediction(self):
        self.assertAlmostEqual(self.e["ideal_event_ready_heralded_acceptance_with_two_photons"],.1568)
        self.assertGreater(self.e["expected_emitted_photon_pairs_at_assumed_acceptance"],350000)
        self.assertIn("NOT a prediction",self.e["important"])

    def test_dependency_DAG_has_no_cycles_and_parallel_stems(self):
        self.assertGreaterEqual(self.d["descendant_counts"]["compact_G2_geometry"],5)
        self.assertGreaterEqual(self.d["descendant_counts"]["UV_causal_action"],5)
        self.assertIn("unbuilt",set(self.d["nodes"].values()))
        self.assertIn("first_gravity_gate",self.d)
        self.assertIn("first_particle_gate",self.d)
    def test_source_chirality_is_conditional_not_TOE(self):
        self.assertEqual(self.d["nodes"]["source_chiral_index"],"conditional_verified")
        self.assertEqual(self.d["nodes"]["physical_TOE_completion"],"unbuilt")
if __name__=="__main__":unittest.main()
