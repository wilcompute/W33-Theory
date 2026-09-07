#!/usr/bin/env python3
from __future__ import annotations

import math
import os
import sys
import unittest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ANALYSIS = os.path.join(ROOT, "analysis")
if ANALYSIS not in sys.path:
    sys.path.insert(0, ANALYSIS)

from w33_holovm_thermodynamic_ledger import (  # noqa: E402
    DEFAULT_TEMPERATURE_K,
    K_B,
    conditional_landauer,
    run_policy,
    verify,
)


class TestHoloVMThermodynamicLedger(unittest.TestCase):
    def test_certificate_passes(self):
        out = verify()
        self.assertEqual(out["status"], "PASS")
        self.assertTrue(all(out["checks"].values()))

    def test_interval_one_needs_no_recomputation(self):
        row = run_policy(1, steps=8)
        self.assertEqual(row.recomputation_steps_total, 0)
        self.assertEqual(row.recomputation_replays_verified, 8)

    def test_sparser_checkpoints_require_more_replay(self):
        dense = run_policy(2, steps=8)
        sparse = run_policy(4, steps=8)
        self.assertLessEqual(dense.recomputation_steps_total, sparse.recomputation_steps_total)
        self.assertGreaterEqual(dense.retained_byte_ticks, sparse.retained_byte_ticks)

    def test_landauer_number_is_only_formula_multiplication(self):
        bits = 1234
        expected = bits * K_B * DEFAULT_TEMPERATURE_K * math.log(2.0)
        self.assertAlmostEqual(conditional_landauer(bits), expected, places=30)

    def test_bad_physical_parameters_rejected(self):
        with self.assertRaises(ValueError):
            conditional_landauer(-1)
        with self.assertRaises(ValueError):
            conditional_landauer(1, 0)


if __name__ == "__main__":
    unittest.main()
