"""Offline regression for six Witting physical falsifiers, including 4D/2D Petz
decoders, exact detector ambiguity, postselected two-ququart teleportation,
genuine finite Z2 gauge dynamics and anonymous-chart leakage."""
from __future__ import annotations
import math
import sys
import unittest
import json
from pathlib import Path
import numpy as np
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"analysis"))
import toe_20261121_five_physical_gates_decoder_blinding_z2 as f

class FivePhysicalGates(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.rays,cls.S,cls.decks,cls.A,cls.P,cls.O,cls.H,cls.P24,cls.K=f.setup()
        cls.cal=f.identifiability(cls.rays,cls.H,cls.P24)
        cls.rec=f.recovery(cls.rays)
        cls.tele=f.heralded_gate(cls.P,cls.S)
        cls.gauge=f.gauge_dynamics(cls.A)
        cls.leak=f.label_information(cls.S)
        cls.residual=f.check_model(cls.S,cls.A)

    def test_all_state_detector_chart_ambiguity(self):
        d=self.cal
        self.assertTrue(d["two_distinct_positive_chart_laws_and_detector_models_indistinguishable"])
        self.assertLess(d["maximum_probing_state_probability_difference"],1e-13)
        self.assertGreater(d["alternate_hidden_bias_distance"],1e-4)

    def test_24dim_local_detector_nuisance_kernel(self):
        d=self.cal
        self.assertTrue(d["local_24D_joint_Jacobian_nullspace"])
        self.assertLess(d["jacobian_cancellation_max_error"],1e-12)

    def test_known_reference_breaks_ambiguity(self):
        d=self.cal
        self.assertTrue(d["trusted_uniform_chart_reference_exactly_breaks_gauge"])
        self.assertLess(d["max_exact_reference_calibration_decoder_error"],1e-12)

    def test_finite_calibration_photon_budget_monotone_sample(self):
        d=self.cal["shot_simulations_with_reference_and_no_click"]
        self.assertLess(d["2000000"]["hidden_bias_l2_error"],
                        d["20000"]["hidden_bias_l2_error"])
        self.assertEqual(d["2000000"]["calibration_launches"],2000000)
        self.assertEqual(d["2000000"]["target_launches"],2000000)

    def test_full_ququart_explicit_petz(self):
        d=self.rec["full_ququart_recovery"]
        self.assertAlmostEqual(d["Fe"],.611089605158904,places=9)
        self.assertAlmostEqual(d["Fav"],(.611089605158904*4+1)/5,places=9)
        self.assertLess(d["recovery_tp_error"],1e-10)

    def test_subcode_petz_recovery_above_90pct_entanglement_fidelity(self):
        d=self.rec["best_two_dim_subcode_recovery"]
        self.assertGreater(d["Fe"],.903)
        self.assertGreater(d["Fav"],.935)
        self.assertEqual(d["output_support_rank"],9)
        self.assertLess(d["recovery_tp_error"],1e-10)

    def test_reconstruct_stored_four_by_two_subcode(self):
        d=self.rec
        V=np.array(d["best_subcode_4x2_isometry_real"])+1j*np.array(
            d["best_subcode_4x2_isometry_imag"])
        self.assertEqual(V.shape,(4,2))
        np.testing.assert_allclose(V.conj().T@V,np.eye(2),atol=1e-12)

    def test_postselected_two_ququart_teleportation_exact(self):
        d=self.tele
        self.assertEqual(d["chart_unitaries_tested"],45)
        self.assertEqual(d["outputs_tested"],135)
        self.assertAlmostEqual(d["ideal_single_postselected_outcome_probability"],1/256)
        self.assertLess(d["max_teleportation_unitary_residual"],1e-12)

    def test_gate_teleportation_is_not_free_hardware_compilation(self):
        d=self.tele
        self.assertEqual(d["resource_ancilla_ququarts"],4)
        self.assertEqual(d["additional_input_ququarts"],2)
        self.assertTrue(d["state_independent_ideal_herald_probability"])

    def test_gauge_gauss_constraints_exact(self):
        d=self.gauge
        self.assertEqual(d["Hilbert_total_dim"],256)
        self.assertEqual(d["independent_Z2_Gauss_constraints"],4)
        self.assertEqual(d["physical_Gauss_plus1_subspace_dim"],16)
        self.assertLess(d["max_exact_Gauss_commutation_error"],1e-12)

    def test_gauge_plaquette_loop_has_dynamic_response(self):
        d=self.gauge["plaquette_coupling_scan"]
        self.assertEqual(len(d),5)
        self.assertLess(d[0]["ground_Wilson_loop_mean"],
                        d[-1]["ground_Wilson_loop_mean"])
        self.assertGreater(d[-1]["ground_Wilson_loop_mean"]-.39,0)

    def test_imposed_24dim_internal_sector_has_lower_energy(self):
        d=self.gauge
        self.assertTrue(d["engineered_24D_is_lowest_of_three_internal_sectors"])
        self.assertLess(d["engineered_24D_sector_ground_energy"],
                        d["uncoupled_uniform_sector_ground_energy"])

    def test_chart_local_gauge_Wilson_defect_mixes_24dim_sector(self):
        d=self.gauge
        self.assertTrue(d["chart_local_defect_Wilson_mixes_spectral_sectors"])
        seq=d["chart_local_Wilson_coupling_scan"]
        self.assertEqual([x["chart_local_Wilson_coupling"] for x in seq],[0,.3,1.,2.])
        self.assertGreater(seq[2]["internal_sector_weights"]["sector24"],.44)
        self.assertLess(seq[0]["internal_sector_weights"]["sector24"],1e-8)
        self.assertGreater(seq[3]["internal_sector_weights"]["sector24"],.5)

    def test_single_photon_chart_ID_leakage(self):
        d=self.leak
        self.assertAlmostEqual(d["single_ray_information_leak_bits"],math.log2(5))
        self.assertEqual(d["single_ray_compatible_chart_count"],9)
        self.assertAlmostEqual(d["case_distribution"][0]["maximum_a_posteriori_guess_accuracy"],1/9)

    def test_two_repeated_photons_identify_chart_more_than_half(self):
        d=self.leak["case_distribution"]
        self.assertAlmostEqual(d[1]["maximum_a_posteriori_guess_accuracy"],5/9)
        self.assertGreater(d[2]["maximum_a_posteriori_guess_accuracy"],.86)
        self.assertGreater(d[3]["maximum_a_posteriori_guess_accuracy"],.96)

    def test_compressed_25bin_detector_leaks_less_chart_information(self):
        d=self.leak
        self.assertAlmostEqual(d["one_shot_25bin_compressed_chart_information_leak_bits"],
                               1.4359177277412059,places=10)
        self.assertGreater(d["25bin_compression_leak_reduction_bits"],.88)

    def test_chart_information_progressively_revealed(self):
        d=self.leak["case_distribution"]
        mis=[e["mutual_info_chart_to_rays_bits"] for e in d]
        self.assertTrue(all(mis[i+1]>mis[i] for i in range(3)))
        self.assertLess(mis[-1],math.log2(45))

    def test_15dim_anonymous_onephoton_statistical_falsifier(self):
        d=self.residual
        self.assertEqual(d["null_goodness_of_fit_constraints_dim"],15)
        self.assertEqual(d["uniform_model_asymptotic_reference_chi_square_degrees_of_freedom"],15)
        self.assertTrue(d["residual_orthogonal_projector_exact"])
        self.assertLess(abs(d["seeded_null_mean_chisquare"]-15),3)

    def test_blind_calibration_can_fail_even_when_model_test_passes(self):
        self.assertTrue(self.residual["undetectable_24D_calibration_modes_remain"])

    def test_frozen_json_six_falsifiers(self):
        data=json.loads((ROOT/"data/toe_20261121_decoder_calibration_teleport_gauge_falsifiers.json").read_text())
        self.assertEqual(data["status"],"PASS")
        self.assertEqual(len([x for x in data if x.startswith("front")]),6)
        self.assertEqual(data["front4_true_Z2_lattice_gauge_matter_Gauss_law"]["physical_Gauss_plus1_subspace_dim"],16)

if __name__=="__main__":unittest.main()
