"""Falsifiable checks: topology, Spin^c representations, exact lattice chirality,
pure-state ambiguity, dimensional gravity gate, and variational Yang Mills."""
import math,pathlib,sys,unittest
import numpy as np
ROOT=pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"analysis"))
import toe_20261119_spinc_overlap_6_homerun_gates as m


class SixHighUpsideTOEGates(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.o=m.produce()
        cls.f=cls.o["fronts"]

    def test_all_six_physics_fronts_executed(self):
        self.assertEqual(len(self.f),6)
        self.assertTrue(all(v["status"]=="PASS" for v in self.f.values()))

    def test_not_a_TOE_and_input_backgrounds_identified(self):
        self.assertFalse(self.o["TOE_solved"])
        self.assertFalse(self.o["quantum_gravity_derived"])
        self.assertFalse(self.o["SM_generation_or_constants_derived"])
        self.assertTrue(self.o["lattice_metric_spin_gauge_as_inputs"])

    def test_torus_euler_and_Gf2_betti_exact(self):
        x=self.f["I_intrinsic_torus_cohomology_and_spin_torsor"]
        self.assertEqual(x["cell_counts"],{"V":9,"E":18,"F":9,"Euler_characteristic":0})
        self.assertEqual(x["GF2_betti_numbers"],[1,2,1])
        self.assertEqual(x["GF2_boundary_ranks"],[8,8])

    def test_torus_boundary_of_boundary_and_spin_count(self):
        x=self.f["I_intrinsic_torus_cohomology_and_spin_torsor"]
        self.assertEqual(x["boundary_of_boundary_nonzero_entries"],0)
        self.assertEqual(x["number_of_H1_Z2_spin_torsor_classes"],4)

    def test_GF2_rank_against_singular_example(self):
        b=np.array([[1,1,0],[0,1,1],[1,0,1]],int)
        self.assertEqual(m.rank2(b),2)

    def test_u1_quantized_torus_plaquette_flux(self):
        for q in (-2,-1,0,1,2):
            ux,uy=m.links(6,q)
            p=m.plaquette_phases(ux,uy)
            np.testing.assert_allclose(p,np.exp(2j*np.pi*q/36),atol=1e-12)
            self.assertEqual(int(round(np.angle(p).sum()/(2*np.pi))),q)

    def test_overlap_index_matches_flux_for_all_seven_sectors(self):
        rows=self.f["II_overlap_Dirac_GW_flux_index_and_gauge_covariance"]["sectors"]
        self.assertEqual(len(rows),7)
        for r in rows:
            self.assertEqual(r["overlap_index_in_our_gamma_convention"],
                             -r["inserted_U1_flux_Q"])
            self.assertEqual(r["measured_plaquette_winding"],r["inserted_U1_flux_Q"])

    def test_overlap_Ginsparg_Wilson_residuals(self):
        rows=self.f["II_overlap_Dirac_GW_flux_index_and_gauge_covariance"]["sectors"]
        self.assertLess(max(r["Ginsparg_Wilson_Frobenius_residual"] for r in rows),3e-11)

    def test_overlap_kernel_gap_nonzero_for_all_smooth_sectors(self):
        rows=self.f["II_overlap_Dirac_GW_flux_index_and_gauge_covariance"]["sectors"]
        self.assertGreater(min(r["H_W_spectral_gap"] for r in rows),.5)

    def test_overlap_zero_modes_are_topologically_protected(self):
        rows=self.f["II_overlap_Dirac_GW_flux_index_and_gauge_covariance"]["sectors"]
        for r in rows:
            self.assertGreaterEqual(r["overlap_zero_modes"],abs(r["inserted_U1_flux_Q"]))

    def test_overlap_covariant_under_local_U1_rephasing(self):
        x=self.f["II_overlap_Dirac_GW_flux_index_and_gauge_covariance"]
        self.assertLess(x["local_U1_gauge_covariance_error"],1e-10)

    def test_global_spin_twist_reshuffles_zero_modes_without_flux(self):
        x=self.f["II_overlap_Dirac_GW_flux_index_and_gauge_covariance"]
        self.assertEqual(x["flat_periodic_zero_modes"],2)
        self.assertEqual(x["flat_antiperiodic_zero_modes"],0)

    def test_nonzero_background_twist_preserves_flux_index(self):
        a=m.overlap_operator(*m.links(5,1,twist_x=0))
        b=m.overlap_operator(*m.links(5,1,twist_x=np.pi))
        self.assertEqual(a["index"],-1)
        self.assertEqual(b["index"],-1)

    def test_SpinC_representation_descends_exactly_for_charge_spin_parity(self):
        rows=self.f["V_global_SpinC_charge_and_chiral_anomaly_constraints"]["representation_center_constraints"]
        for r in rows:
            expected=(r["integer_U1_character_weight"] %2)==int(r["spinor"])
            self.assertEqual(r["SpinC_quotient_representation_well_defined"],expected)

    def test_odd_charge_square_congruence_mod8_with_signs(self):
        for q in range(-31,32,2):
            self.assertEqual(q*q %8,1)

    def test_2D_anomaly_free_but_nonvectorlike_odd_charge_spectrum(self):
        c=self.f["V_global_SpinC_charge_and_chiral_anomaly_constraints"]["sample_nonvectorlike_2D_chiral_anomaly_free_charges"]
        self.assertEqual(c["left"],[1,7])
        self.assertEqual(c["right"],[5,5])
        self.assertEqual(sum(x*x for x in c["left"]),
                         sum(y*y for y in c["right"]))
        self.assertNotEqual(sorted(c["left"]),sorted(c["right"]))

    def test_2D_odd_charge_number_mismatch_must_be_multiple_of8(self):
        # Necessary not sufficient! Check exact congruence for sampled odd lists.
        left=[1,1,1]
        right=[3]
        delta=sum(q*q for q in left)-sum(q*q for q in right)
        self.assertEqual(delta %8,(len(left)-len(right))%8)
        self.assertNotEqual(delta,0)

    def test_multiple_pure_Gaussian_states_have_same_commutator(self):
        rows=self.f["III_pure_quantum_state_selection_nonuniqueness"]["pure_Gaussian_two_point_options"]
        self.assertEqual(len(rows),3)
        for r in rows:
            self.assertAlmostEqual(r["symplectic_purity_det_V"],.25,places=12)
            self.assertLess(r["fixed_commutator_error"],1e-12)
            self.assertGreater(r["min_W_eigenvalue"],-1e-11)

    def test_pure_squeezed_vacua_have_distinct_q_variances(self):
        rows=self.f["III_pure_quantum_state_selection_nonuniqueness"]["pure_Gaussian_two_point_options"]
        self.assertLess(rows[0]["q_variance"],rows[-1]["q_variance"])
        self.assertGreater(rows[0]["p_variance"],rows[-1]["p_variance"])
        self.assertGreater(rows[-1]["H_oscillator_frequency_1_energy"],1.8)

    def test_Hamiltonian_selection_depends_on_frequency(self):
        r=self.f["III_pure_quantum_state_selection_nonuniqueness"]
        self.assertAlmostEqual(r["frequency_4_ground_energy"],2)
        self.assertGreater(r["frequency_4_energy_in_frequency_1_vacuum"],2)

    def test_regge_2D_Gauss_Bonnet_torus_action_vanishes(self):
        r=self.f["IV_dimension_gravity_topological_action_and_growth"]
        self.assertEqual(r["torus_cell_complex"]["chi"],0)
        self.assertLess(abs(r["torus_regge_total_deficit_radians"]),1e-11)

    def test_regge_nontrivial_local_curvature_can_have_zero_total(self):
        r=self.f["IV_dimension_gravity_topological_action_and_growth"]
        self.assertGreater(r["local_regge_deficit_L2_norm"],.01)
        self.assertLess(r["local_deficit_min_max"][0],0)
        self.assertGreater(r["local_deficit_min_max"][1],0)

    def test_spherical_2D_regge_Gauss_Bonnet_four_pi(self):
        r=self.f["IV_dimension_gravity_topological_action_and_growth"]
        self.assertAlmostEqual(r["sphere_tetrahedron_total_deficit_radians"],4*np.pi)

    def test_sampled_unembedded_causal_growth_does_not_universally_select4D(self):
        r=self.f["IV_dimension_gravity_topological_action_and_growth"]
        dims=[x for x in r["median_intrinsic_dimension_estimates"] if x is not None]
        self.assertGreaterEqual(len(dims),2)
        self.assertTrue(all(abs(d-4)>.75 for d in dims))
        self.assertGreater(max(dims)-min(dims),.3)

    def test_SU2_Yang_Mills_action_invariant_under_9_local_frames(self):
        r=self.f["VI_extra_dynamic_SU2_Yang_Mills_variational_force"]
        self.assertLess(r["local_frame_gauge_action_error"],1e-11)

    def test_SU2_Yang_Mills_has_a_nonzero_field_force(self):
        r=self.f["VI_extra_dynamic_SU2_Yang_Mills_variational_force"]
        self.assertGreater(r["force_norm"],.1)
        self.assertAlmostEqual(np.linalg.norm(r["one_link_gauge_force_vector"]),
                               r["force_norm"],places=11)

    def test_variational_link_update_actually_decreases_Yang_Mills_action(self):
        r=self.f["VI_extra_dynamic_SU2_Yang_Mills_variational_force"]
        self.assertGreater(r["energy_decrease"],.01)
        self.assertLess(r["after_one_negative_gradient_step"],r["initial_wilson_action"])

    def test_charge_multiplication_and_flux_match_lattice_index(self):
        rows=self.f["II_overlap_Dirac_GW_flux_index_and_gauge_covariance"]["sectors"]
        for q in (1,3,5):
            r=next(x for x in rows if x["inserted_U1_flux_Q"]==q)
            # Equivalent to a charge-q fermion in background flux +1.
            self.assertEqual(r["overlap_index_in_our_gamma_convention"],-q)

    def test_causal_GUT_or_SM_not_claimed(self):
        self.assertIn("NO TOE",self.o["status"])
        self.assertFalse(self.o["SM_generation_or_constants_derived"])
        self.assertTrue(self.o["lattice_metric_spin_gauge_as_inputs"])

if __name__=="__main__":unittest.main()
