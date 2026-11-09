"""Regression: Q8/72 design gives tight mixed Schmidt number witnesses."""
import json
import sys
import unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'analysis'))
import w33_20261109_q8_schmidt_witness as mod

class TestQ8SchmidtWitness(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data=mod.checks()

    def test_exact_tight_bounds(self):
        vals=self.data['tight_schmidt_number_bounds']
        for k,row in enumerate(vals,start=1):
            self.assertEqual(row['schmidt_rank'],k)
            self.assertAlmostEqual(row['tight_bound'],10/9-2/(3*k),places=12)
            for x in row['observed_by_coset']:
                self.assertAlmostEqual(x,row['tight_bound'],places=11)

    def test_mixed_schmidt_bound(self):
        self.assertEqual(self.data['random_mixtures_tested'],112)
        self.assertLessEqual(self.data['largest_mixed_rank1_or_rank2_observed'][1],4/9+1e-10)
        self.assertLessEqual(self.data['largest_mixed_rank1_or_rank2_observed'][2],7/9+1e-10)

    def test_equal_means_unequal_variance(self):
        import math
        xs=sorted(self.data['coset_pair_collision_var_times_M'])
        for x,y in zip(xs,[56/81,104/81,104/81]):
            self.assertAlmostEqual(x,y,places=11)
        self.assertAlmostEqual(xs[-1]/xs[0],13/7,places=11)

    def test_loss_fakes_witness(self):
        loss=self.data['product_state_outcome_dependent_loss']
        self.assertTrue(loss['false_entanglement_if_uncalibrated'])
        self.assertGreater(min(loss['uncalibrated_F8_by_coset']),4/9)
        self.assertLess(loss['cross_coset_spread'],1e-10)
        for x in loss['calibrated_F8_by_coset']:
            self.assertAlmostEqual(x,4/9,places=11)

    def test_reference_power(self):
        powers=self.data['aligned_maxent_exact_binomial_power_95pct']
        self.assertEqual(powers['1']['pairs_per_basis'],116)
        self.assertEqual(powers['2']['pairs_per_basis'],1882)
        self.assertEqual(powers['2']['accepted_preparations_per_coset'],30112)
        self.assertGreaterEqual(powers['2']['reference_aligned_maxent_power'],.95)

    def test_frozen(self):
        freeze=ROOT/'data'/'w33_20261109_q8_schmidt_witness.json'
        if freeze.is_file():
            saved=json.loads(freeze.read_text(encoding='utf-8'))
            self.assertEqual(saved['status'],self.data['status'])
            self.assertEqual(saved['random_mixtures_tested'],112)

if __name__=='__main__':
    unittest.main()
