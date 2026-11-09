"""12-setting completion of eight Q8 Bell MUB correlation tomography."""
import json,sys,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'analysis'))
import w33_20261109_q8_12setting_completion as m

class TestQ8Completion(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.d=m.main()

    def test_complete_operator_rank(self):
        d=self.d
        self.assertEqual((d["bell_rank"],d["combined_rank"]),(64,80))
        self.assertEqual((d["bell_settings"],d["product_settings"]),(8,4))
        self.assertEqual(d["all_traceless_density_parameters"],80)
        self.assertEqual(d["local_generators_added"],16)

    def test_exact_condition(self):
        self.assertAlmostEqual(self.d["combined_condition_number"],2**.5,places=10)
        self.assertLess(self.d["product_MUB_overlap_error"],5e-12)

    def test_random_full_tomography(self):
        self.assertEqual(self.d["random_density_controls"],60)
        self.assertLess(self.d["max_reconstruction_error"],5e-12)
        self.assertLess(self.d["max_marginal_reconstruction_error"],5e-12)

    def test_purity_ambiguity_gone(self):
        self.assertLess(self.d["bell_only_indistinguishable_max_error"],1e-12)
        self.assertGreater(self.d["product_setting_discrimination_max_difference"],.1)

    def test_minimality_boundary(self):
        self.assertTrue(self.d["minimum_four_matched_product_settings_in_this_protocol"])
        self.assertTrue(self.d["not_global_minimum_number_of_arbitrary_projective_settings"])

    def test_frozen_json(self):
        p=ROOT/'data/w33_20261109_q8_12setting_completion.json'
        if p.exists():
            f=json.loads(p.read_text(encoding='utf8'))
            self.assertEqual(f['combined_rank'],80)
            self.assertEqual(f['status'],self.d['status'])

if __name__=='__main__':
    unittest.main()
