"""Regression and independent positive-state falsifiers for the Witting-origin bridge."""
from __future__ import annotations
import sys, unittest
from pathlib import Path
import numpy as np
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/"analysis"))
import toe_20261120_witting_transvection_parity as T

class WittingOriginBridge(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.out=T.run(write=False)
        cls.a=cls.out["q3_n2"]
        cls.b=cls.out["q5_n2"]

    def test_all_40_reflection_gates_and_80_Weyl_labels(self):
        self.assertEqual(self.a["Weyl_conjugation_cases"],3200)
        self.assertLess(self.a["max_exact_Weyl_covariance_error"],1e-11)

    def test_all_40_ray_permutations(self):
        self.assertEqual(self.a["Witting_odd_action_cases"],1600)
        self.assertLess(self.a["max_Witting_projector_action_error"],1e-11)

    def test_all_full_gates_are_order_three_unitary(self):
        self.assertLess(self.a["max_unitarity_error"],1e-11)

    def test_all_40_actual_Witting_rays_match_preexisting_dictionary(self):
        self.assertLess(self.a["prior_Witting_ray_projector_match_error"],1e-11)

    def test_rank_one_Witting_gram_and_tightness(self):
        self.assertLess(self.a["odd_Gram_error"],1e-11)
        self.assertLess(self.a["odd_tight_error"],1e-11)

    def test_rank_two_even_sector_gram_and_tightness(self):
        self.assertLess(self.a["even_Gram_error"],1e-11)
        self.assertLess(self.a["even_tight_error"],1e-11)

    def test_exact_operator_parity_sum(self):
        self.assertLess(self.a["parity_sum_residual"],1e-11)

    def test_full_and_both_sector_trace_contrasts(self):
        self.assertEqual(self.a["trace_contrasts_squared"],
                         {"full9":1/3,"odd4":7/16,"even5":7/25})
        self.assertLess(self.a["trace_contrast_numerical_error"],1e-11)

    def test_randomized_measurement_parity_statistics(self):
        self.assertEqual(self.a["zero_outcome_probability"],
                         {"odd":1/4,"even":2/5,"max_mixed":1/3})

    def test_independent_random_positive_mixed_states(self):
        P=T.parity()
        ps=[T.zero_projector(v,3) for v in T.projective_points(3,2)]
        Q=sum(ps)/40
        rng=np.random.default_rng(20261120)
        for _ in range(30):
            G=rng.normal(size=(9,9))+1j*rng.normal(size=(9,9))
            rho=G@G.conj().T
            rho/=np.trace(rho).real
            direct=float(np.trace(Q@rho).real)
            expected=(13+3*np.trace(P@rho).real)/40
            self.assertAlmostEqual(direct,expected,places=12)

    def test_ququint_5D_control_no_rank_one_odd_rays(self):
        self.assertEqual(self.b["p"],5)
        self.assertEqual(self.b["projective_directions"],156)
        self.assertEqual(self.b["zero_eigen_ranks_even_odd"],[3,2])
        self.assertLess(self.b["identity_residual"],1e-9)

    def test_ququint_general_operator_sum(self):
        self.assertEqual(self.b["sum_projectors_even_eigenvalue"],36)
        self.assertEqual(self.b["sum_projectors_odd_eigenvalue"],26)

    def test_rank_one_odd_only_for_two_qutrits_among_small_primes(self):
        survivors=[(p,n) for p in (3,5,7,11) for n in range(2,5)
                   if (p**(n-1)-1)//2==1]
        self.assertEqual(survivors,[(3,2)])

    def test_all_forty_wigner_histograms_are_identical(self):
        w=self.out["wigner_magic"]
        self.assertEqual(w["tested_ray_phase_points"],3240)
        self.assertEqual((w["negative_cells_per_ray"],w["positive_cells_per_ray"],
                          w["zero_cells_per_ray"]),(3,24,54))
        self.assertLess(w["max_formula_residual"],1e-11)

    def test_negative_phase_line_and_orthogonal_hyperplane(self):
        w=self.out["wigner_magic"]
        self.assertIn("span_F3(v)",w["negative_support"])
        self.assertIn("hyperplane",w["positive_support"])
        self.assertEqual(w["negative_value"],-1/9)
        self.assertEqual(w["positive_value"],1/18)

    def test_commutation_admission_equals_Wigner_negativity_threshold(self):
        self.assertEqual(self.a["projective_compatibility_rate_self_plus_commuting"],13/40)
        self.assertEqual(self.b["projective_neighbors_plus_self"],31)
        self.assertAlmostEqual(self.b["uniform_projective_compatibility_rate"],31/156)
        self.assertAlmostEqual(self.b["same_as_centered_Wigner_negativity_threshold"],31/156)
        for p in (3,5,7,11):
            N=(p**4-1)//(p-1)
            self.assertEqual((N-1)//p,p*(p+1)+1)

    def test_full_Witting_Gram_is_recovered_from_Wigner_support(self):
        w=self.out["wigner_magic"]
        self.assertLess(w["Wigner_reconstructed_Gram_max_error"],1e-10)
        self.assertEqual(w["Wigner_40_by_81_matrix_rank"],16)

    def test_mana_and_explicit_strange_tensor_stabilizer_state(self):
        w=self.out["wigner_magic"]
        self.assertAlmostEqual(w["Wigner_L1_norm"],5/3,places=13)
        self.assertAlmostEqual(w["mana_natural_log"],np.log(5/3),places=13)
        self.assertLess(w["explicit_reference_density_residual"],1e-11)

if __name__=="__main__":
    unittest.main()
