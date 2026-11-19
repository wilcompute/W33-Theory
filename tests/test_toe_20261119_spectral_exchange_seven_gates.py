"""Independent regression checks for eight causal/spectral physics gates."""
import pathlib,sys,unittest
import numpy as np
ROOT=pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"analysis"))
import toe_20261119_spectral_exchange_seven_gates as m

class EightSpectralPhysicsGates(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.output=m.run_all()
        cls.r=cls.output["gates"]

    def test_eight_independent_gates_are_complete(self):
        self.assertEqual(len(self.r),8)
        self.assertTrue(all(v["status"]=="PASS" for v in self.r.values()))

    def test_known_physical_completion_missing(self):
        self.assertFalse(self.output["TOE_solved"])
        self.assertFalse(self.output["derived_4D_GR_or_Born_rule"])
        self.assertFalse(self.output["derived_fermion_generations"])

    def test_two_dimensional_naive_four_doublers(self):
        f=self.r["spin_structure_and_2D_doubling"]
        self.assertEqual(f["four_spin_structures"][0]["naive_zero_components"],8)
        self.assertEqual(f["net_chirality"],0)

    def test_Wilson_fermion_lifts_doublers_but_breaks_chirality(self):
        f=self.r["spin_structure_and_2D_doubling"]["four_spin_structures"][0]
        self.assertEqual(f["wilson_zero_components"],2)
        self.assertGreater(f["max_wilson_chiral_anticommutator"],1.)

    def test_three_antiperiodic_spin_structures_lift_exact_zeros(self):
        rows=self.r["spin_structure_and_2D_doubling"]["four_spin_structures"]
        self.assertEqual(len(rows),4)
        self.assertTrue(all(row["naive_zero_components"]==0 for row in rows[1:]))

    def test_SU2_link_unitarity(self):
        for axis in range(3):
            for theta in [-.5,0,1.4]:
                U=m.U(theta,axis)
                np.testing.assert_allclose(U@U.conj().T,m.I,atol=1e-13)
                self.assertAlmostEqual(np.linalg.det(U),1,places=13)

    def test_nonabelian_constant_potentials_have_real_curvature(self):
        x=self.r["nonabelian_SU2_plaquette_curvature"]
        self.assertGreater(x["noncommuting_SU2_loop_action"],.0006)
        self.assertLess(x["commuting_loop_error"],1e-12)

    def test_plaquette_local_SU2_gauge_covariance(self):
        x=self.r["nonabelian_SU2_plaquette_curvature"]
        self.assertLess(x["local_gauge_transformation_error"],1e-12)

    def test_plaquette_small_area_continuum_limit(self):
        vals=self.r["nonabelian_SU2_plaquette_curvature"]["small_loop_ratios"]
        self.assertEqual(len(vals),4)
        self.assertLess(abs(vals[-1]-1/8),.001)
        self.assertLess(abs(vals[-1]-1/8),abs(vals[0]-1/8))

    def test_square_of_single_dirac_operator_forces_Pauli_curvature(self):
        x=self.r["single_Dirac_squared_Pauli_term"]
        self.assertLess(x["square_minus_laplacian_minus_Pauli_error"],1e-13)
        self.assertGreater(x["Pauli_curvature_omission_norm"],.6)

    def test_single_Dirac_operator_gauge_frame_covariance(self):
        x=self.r["single_Dirac_squared_Pauli_term"]
        self.assertLess(x["color_gauge_covariance_error"],1e-13)

    def test_Dirac_SU2_curvature_spectrum_is_paired(self):
        ev=self.r["single_Dirac_squared_Pauli_term"]["Fcurv_eigenvalues"]
        self.assertAlmostEqual(ev[0],-ev[1],places=13)
        self.assertGreater(ev[1],0)

    def test_SJ_quantum_two_point_state_PSD(self):
        x=self.r["causal_SJ_quantum_state_nonuniqueness"]
        self.assertGreater(x["positive_SJ_min_eigenvalue"],-1e-12)
        self.assertLess(x["SJ_commutator_residual"],1e-12)

    def test_half_commutator_is_not_a_positive_state(self):
        x=self.r["causal_SJ_quantum_state_nonuniqueness"]
        self.assertLess(x["naive_half_iDelta_negative_eigenvalue"],-.01)

    def test_SJ_positive_state_not_unique_at_fixed_commutator(self):
        x=self.r["causal_SJ_quantum_state_nonuniqueness"]
        self.assertGreater(x["second_state_positive_min_eigenvalue"],.14)
        self.assertEqual(x["second_state_added_noise"],.15)

    def test_SJ_respects_causal_event_relabeling(self):
        x=self.r["causal_SJ_quantum_state_nonuniqueness"]
        self.assertLess(x["relabel_invariance_error"],1e-12)

    def test_causal_order_conformally_invariant_and_volume_not(self):
        x=self.r["conformal_order_metric_ambiguity"]
        self.assertFalse(x["causal_order_changed"])
        self.assertGreater(x["volume_ratio"],1.3)

    def test_curved_metric_proper_time_changes_even_with_same_order(self):
        x=self.r["conformal_order_metric_ambiguity"]
        self.assertGreater(x["curved_proper_time"],x["flat_proper_time"])
        self.assertGreater(x["scalar_curvature_at_midpoint"],.2)

    def test_physical_volume_quadrature_versus_montecarlo(self):
        x=self.r["conformal_order_metric_ambiguity"]
        self.assertLess(abs(x["MC_volume_estimate"]-x["curved_volume"]),
                        4*x["MC_standard_error"]+.002)

    def test_locally_flat_global_winding_still_different(self):
        x=self.r["global_flat_holonomy_spectral_shift"]
        self.assertEqual(len(x["flat_winding_sectors"]),3)
        self.assertEqual(x["flat_winding_sectors"][0]["plaquette_curvature"],0.)
        self.assertEqual(x["flat_winding_sectors"][2]["plaquette_curvature"],0.)
        self.assertAlmostEqual(x["flat_winding_sectors"][-1]["winding_real_imag"][0],-1,places=12)

    def test_flat_holonomy_can_change_spectral_zero_modes(self):
        rows=self.r["global_flat_holonomy_spectral_shift"]["flat_winding_sectors"]
        self.assertLess(rows[0]["lowest_laplacian_eigenvalue"],1e-12)
        self.assertGreater(rows[2]["lowest_laplacian_eigenvalue"],.01)

    def test_flat_holonomy_changes_heat_traces_without_curvature(self):
        x=self.r["global_flat_holonomy_spectral_shift"]
        self.assertGreater(x["heat_trace_delta_theta0_minus_pi_at_t8"],.4)
        for t in ("1.0","3.0","8.0"):
            self.assertGreater(x["flat_winding_sectors"][0]["heat_traces"][t],
                               x["flat_winding_sectors"][-1]["heat_traces"][t])

    def test_4D_naive_species_doubling_has_sixteen_cones(self):
        x=self.r["four_dimensional_chiral_anomaly_gate"]
        self.assertEqual(x["Brillouin_cones"],16)
        self.assertEqual(x["naive_zero_spinor_components"],64)
        self.assertEqual(x["Wilson_zero_spinor_components"],4)

    def test_4D_cone_orientations_sum_to_zero(self):
        x=self.r["four_dimensional_chiral_anomaly_gate"]
        self.assertEqual(x["signed_chiralities"].count(1),8)
        self.assertEqual(x["signed_chiralities"].count(-1),8)
        self.assertEqual(x["net_cone_orientation"],0)

    def test_supplied_one_SM_generation_exact_anomaly_cancellation(self):
        x=self.r["four_dimensional_chiral_anomaly_gate"]
        self.assertTrue(all(int(k)==0 for k in x["exact_SM_one_family_anomaly_sums"].values()))
        self.assertEqual(x["SU2_left_doublet_count"]%2,0)

    def test_spin_antiperiodicity_and_charge_one_pi_holonomy_equivalent(self):
        z=self.r["spin_gauge_twist_compensation"]["four_spin_gauge_sectors"]
        np.testing.assert_allclose(z[1]["kx_sine_squared_sorted"],z[2]["kx_sine_squared_sorted"])

    def test_spin_and_gauge_minus_one_windings_compensate(self):
        z=self.r["spin_gauge_twist_compensation"]["four_spin_gauge_sectors"]
        self.assertEqual([v["naive_zero_spinor_components"] for v in z],[8,0,0,8])

    def test_fundamental_one_operator_remains_an_unproven_hypothesis(self):
        x=self.r["single_Dirac_squared_Pauli_term"]
        self.assertIn("NOT derived",x["scope"])
        self.assertFalse(self.output["selected_4D"])

if __name__=="__main__":
    unittest.main()
