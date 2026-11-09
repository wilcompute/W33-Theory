"""Standard-library regression tests for the independent five-front pass."""
import importlib.util
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / 'analysis' / 'w33_20261109_five_fronts.py'
spec = importlib.util.spec_from_file_location('w33_five_fronts_20261109', SRC)
mod = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = mod
spec.loader.exec_module(mod)


class TestFiveFronts(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.r = mod.main()

    def test_pentad_S5_singlets(self):
        self.assertEqual(self.r['pentad']['high_M_S5_singlets'], 9)
        self.assertEqual(self.r['pentad']['star_eigenvalues'], [-1,4,4,4,4])

    def test_photonic_exact_variance_and_shot_cost(self):
        p = self.r['photonic']
        self.assertLess(p['exact_N3_variance_error'], 1e-12)
        self.assertEqual(p['Hoeffding_95pct_epsilon_0_1_total_preparations_per_coset'], 53120)
        self.assertLess(abs(p['Monte_Carlo_variance_ratio']-1), .13)

    def test_photonic_loss_common_mode_is_undetected(self):
        p = self.r['photonic']['input_cases']['product']
        self.assertLess(p['efficiency_distorted_max_minus_min'], 1e-12)
        self.assertGreater(p['apparent_entropy_if_loss_ignored'], .02)
        self.assertLess(p['max_calibrated_loss_correction_error'], 1e-12)

    def test_shortest_W33_loops_span_cycle_space(self):
        g = self.r['gauge_dynamics']
        self.assertEqual((g['incidence_graph_vertices'], g['incidence_edges']), (80,160))
        self.assertEqual((g['distinct_eight_cycles'], g['binary_cycle_rank']), (1620,81))
        self.assertEqual(g['cycle_dependencies'], 1539)
        self.assertLess(g['relative_gauge_action_error'], 1e-12)
        self.assertLess(g['laplacian_covariance_error'], 1e-12)

    def test_chirality_no_uniqueness_from_anomalies(self):
        c = self.r['chirality']
        self.assertTrue(c['all_family_counts_from_1_to_10_anomaly_free'])
        self.assertEqual(c['finite_parity_symmetric_double_well_minima']['1'],
                         c['finite_parity_symmetric_double_well_minima']['-1'])

    def test_cosmology_stale_shear_held_out(self):
        c = self.r['cosmology']
        self.assertTrue(c['reuses_repository_numbers_not_new_likelihood'])
        self.assertEqual(c['frozen_date'], '2026-11-08')
        for v in c['controls'].values():
            self.assertGreater(v['margin_to_predicted_2_gap'], 0)
            self.assertGreater(v['margin_to_predicted_4_LCDM'], 0)


if __name__ == '__main__':
    unittest.main()
