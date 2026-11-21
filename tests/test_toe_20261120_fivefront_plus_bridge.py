"""Reproducible numerical and algebraic falsifiers for five-front TOE packet."""
from __future__ import annotations
import sys, math, unittest
from pathlib import Path
import numpy as np
sys.path.insert(0, str(Path(__file__).resolve().parents[1]/'analysis'))
from toe_20261120_fivefront_plus_bridge import (
    main, E, OMEGA, optical_switch, weyl, symp, shear,
    anomaly_index_lattice, calibrated_center, clopper_pearson_bounds,
    make_switch_process, physical_prediction_gate
)

class FiveFrontTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.result=main(write=False)

    def test_photonic_is_18_mode_unitary(self):
        V,_,_=optical_switch(tuple(E[:,0]),tuple(E[:,2]),0)
        self.assertEqual(V.shape,(18,18))
        self.assertLess(np.max(abs(V.conj().T@V-np.eye(18))),1e-12)

    def test_two_complementary_quadratures(self):
        u,v=tuple(E[:,0]),tuple(E[:,2])
        vx,_,_=optical_switch(u,v,0)
        vy,_,_=optical_switch(u,v,np.pi/2)
        z=np.zeros(18);z[0]=1
        self.assertAlmostEqual(float(np.linalg.norm((vx@z)[:9])**2),.25)
        self.assertAlmostEqual(float(np.linalg.norm((vy@z)[:9])**2),
                               (1+math.sqrt(3)/2)/2)

    def test_branch_permutation_and_phases(self):
        layout=self.result['front_1_optical_compilation']['layout']
        self.assertEqual(len(layout),7)
        for r in layout:
            for branch in ('phase0_branch','phase1_branch'):
                self.assertEqual(sorted(r[branch]['output_mode_for_each_input_mode']),list(range(9)))
                self.assertEqual(len(r[branch]['phase_radians_per_input_mode']),9)

    def test_noisy_heralding_and_address_falsification(self):
        r=self.result['front_1_optical_compilation']
        self.assertEqual(r['accepted_photon_trials_per_7setting_run'],2240)
        self.assertEqual(r['honest_correct'],r['runs'])
        self.assertEqual(r['nonlinear_basis_pass_and_holdout_reject'],r['runs'])
        self.assertGreater(r['average_attempted_photon_trials_per_7setting_run'],5500)
        self.assertLess(r['average_attempted_photon_trials_per_7setting_run'],5720)

    def test_exact_shear_gate_bijection(self):
        from itertools import product
        addresses=list(product(range(3), repeat=4))
        self.assertEqual(len({shear(u) for u in addresses}),81)
        self.assertNotEqual(symp((0,1,0,1),(0,0,1,0)),
                            symp(shear((0,1,0,1)),shear((0,0,1,0))))

    def test_flux_anomaly_kernel_only_complete_27(self):
        r=self.result['front_2_anomaly_kernel']
        A=np.asarray(r['anomaly_matrix'])
        self.assertEqual(np.linalg.matrix_rank(A),2)
        self.assertEqual((A@np.ones(3,dtype=int)).tolist(),[0,0,0])
        self.assertEqual(r['integer_kernel_generator'],[1,1,1])

    def test_flux_compensation_needed(self):
        r=self.result['front_2_anomaly_kernel']
        self.assertEqual(r['isolated_flux_anomalies'],[0,2160,-18])
        self.assertEqual(r['required_net_additional_chirality_indices'],[0,-9,-45])
        self.assertEqual(r['compensating_sector_anomalies'],[0,-2160,18])

    def test_exact_binomial_bound_nonzero_errors(self):
        low,up=clopper_pearson_bounds(23500,25000,.01)
        self.assertTrue(0<low<23500/25000<up<1)
        self.assertEqual(clopper_pearson_bounds(0,5,.01)[0],0)
        self.assertEqual(clopper_pearson_bounds(5,5,.01)[1],1)

    def test_calibrated_center_nonzero_errors(self):
        r=self.result['front_3_noise_calibrated_center']
        self.assertGreater(r['central_datasets_certified_at_norm_0p25'],100)
        self.assertEqual(r['noncentral_datasets_certified_at_norm_0p25'],0)
        self.assertGreater(r['noncentral_Re_c_0p96_median_upper_Frobenius_squared'],.7)

    def test_identical_CPTP_marginals_any_path_coherence(self):
        r=self.result['front_3_noise_calibrated_center']
        m=r['branch_environment_indistinguishability']
        self.assertEqual([x['environment_overlap'] for x in m],[0.,.4,1.])
        self.assertTrue(all(x['target_channel_both_arms']=='identity CPTP' for x in m))

    def test_causal_process_validity(self):
        r=self.result['front_4_ideal_process_certificate']
        self.assertEqual(r['raw_process_rank'],1)
        self.assertEqual(r['raw_process_trace'],4)
        self.assertEqual(r['independent_random_local_general_CPTP_normalization_checks'],32)

    def test_bidirectional_signaling(self):
        r=self.result['front_4_ideal_process_certificate']
        self.assertTrue(np.allclose(r['A_to_B_signaling_measurement_probability_preparer_0_then_1'],[0,.5]))
        self.assertTrue(np.allclose(r['B_to_A_signaling_measurement_probability_preparer_0_then_1'],[0,.5]))

    def test_process_coherence_not_automatically_a_linear_witness(self):
        r=self.result['front_4_ideal_process_certificate']
        self.assertTrue(np.allclose(r['process_state_purities_coherent_and_dephased'],[1,.5]))
        self.assertAlmostEqual(r['normalized_process_trace_distance_coherent_vs_dephased'],.5)
        self.assertIn('not a robust linear',r['not_a_linear_noisy_witness'])

    def test_heisenberg_associativity_falsifier(self):
        r=self.result['front_5_new_physics_gate']
        self.assertEqual(r['random_exact_cocycle_associativity_tests'],30000)
        self.assertEqual(r['mismatches'],0)
        self.assertTrue(r['example_phase_is_phenomenological_input_not_derived'])

    def test_parameter_free_prediction_not_fabricated(self):
        r=self.result['front_5_new_physics_gate']
        self.assertIn('not a parameter-free',r['no_new_physics_claim'])
        self.assertGreater(r['absolute_gap'],.1)
        self.assertLess(r['conditional_99pct_conservative_shots_per_hypothesis'],1000)

    def test_data_schema_and_scope(self):
        self.assertEqual(self.result['status'],'PASS_FIVE_FORMAL_FRONTS_WITH_OPEN_PHYSICAL_GATES')
        self.assertIn('no real optics',self.result['source_boundary'])

if __name__=='__main__': unittest.main()
