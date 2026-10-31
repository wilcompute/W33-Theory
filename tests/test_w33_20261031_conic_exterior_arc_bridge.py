"""Check the coordinate dictionary and its coding interpretation independently."""
import importlib.util
from pathlib import Path
import unittest

PATH = Path(__file__).resolve().parents[1] / "analysis/w33_20261031_conic_exterior_arc_bridge.py"
SPEC = importlib.util.spec_from_file_location("conic_bridge", PATH)
bridge = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(bridge)


class ConicBridgeTests(unittest.TestCase):
    def test_pole_polar_recovers_chord_including_infinity(self):
        for q in (3, 5, 7, 11, 13):
            for a, b in bridge.combinations([bridge.INF] + list(range(q)), 2):
                x, y, z = bridge.pole((a, b), q)
                polar = bridge.normalize((-z, 2*y, -x), q)
                self.assertEqual(polar, bridge.normalize(bridge.chord((a, b), q), q))

    def test_second_projective_chart_preserves_the_predicates(self):
        # t -> (t+1)/t, including its pole and infinity. This is not an
        # affine relabeling: it exercises the chart boundary explicitly.
        for q, m in ((7, (("inf", 0), (1, 3), (2, 6), (4, 5))),
                     (11, (("inf", 0), (1, 2), (3, 6), (4, 8), (5, 10), (7, 9)))):
            def transform(t):
                return 1 if t == "inf" else ("inf" if t == 0 else (t+1)*pow(t, -1, q) % q)
            moved = tuple(tuple(transform(t) for t in p) for p in m)
            self.assertTrue(bridge.exterior_arc(moved, q))
            self.assertEqual(bridge.stopping_set_audit(moved, q), bridge.stopping_set_audit(m, q))

    def test_pairwise_external_does_not_imply_arc(self):
        # All three external points on one external line at q=5: pairwise
        # exterior is true, but the forbidden concurrent-chord triple remains.
        m = (("inf", 0), (1, 2), (3, 4))
        self.assertTrue(all(bridge.exterior_compatible(a, b, 5) for a, b in bridge.combinations(m, 2)))
        self.assertTrue(bridge.collinear(m, 5))
        self.assertFalse(bridge.exterior_arc(m, 5))

    def test_stopping_set_is_not_promoted_to_codeword(self):
        r = bridge.stopping_set_audit((("inf", 0), (1, 3), (2, 6), (4, 5)), 7)
        self.assertEqual(r["line_intersection_histogram"], {"0": 15, "2": 30, "3": 12})
        self.assertTrue(r["stopping_set"])
        self.assertFalse(r["binary_even_codeword"])


if __name__ == "__main__":
    unittest.main()
