#!/usr/bin/env python3
from __future__ import annotations

import os
import sys
import unittest
from math import sqrt

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ANALYSIS = os.path.join(ROOT, "analysis")
if ANALYSIS not in sys.path:
    sys.path.insert(0, ANALYSIS)

from w33_continuation_superposition_semantics import (  # noqa: E402
    ContinuationSelector,
    DIMENSION,
    ZERO_SLOT,
    slot_permutation,
    uniform_selector,
    verify,
)


class TestContinuationSuperpositionSemantics(unittest.TestCase):
    def test_certificate_passes(self):
        out = verify()
        self.assertEqual(out["status"], "PASS")
        self.assertTrue(all(out["checks"].values()))

    def test_every_transvection_fixes_zero_slot(self):
        for axis in range(40):
            for lam in (1, 2):
                self.assertEqual(slot_permutation(axis, lam)[ZERO_SLOT], ZERO_SLOT)

    def test_uniform_selector_remains_normalized(self):
        state = uniform_selector().apply_transvection(5, 1)
        self.assertAlmostEqual(sum(abs(z) ** 2 for z in state.amplitudes), 1.0, places=12)

    def test_measurement_returns_root_not_amplitude_payload(self):
        state = uniform_selector()
        root = state.measure_by_quantile(0.5)
        self.assertIn(root, state.roots)
        self.assertIsInstance(root, str)
        self.assertTrue(root.startswith("sha256:"))

    def test_relative_phase_changes_selector_but_not_root_table_or_probabilities(self):
        state = uniform_selector()
        amps = [0j] * DIMENSION
        amps[2] = complex(1 / sqrt(2), 0)
        amps[9] = complex(1 / sqrt(2), 0)
        a = ContinuationSelector(state.roots, tuple(amps))
        amps[9] *= -1
        b = ContinuationSelector(state.roots, tuple(amps))
        self.assertNotEqual(a.selector_id, b.selector_id)
        self.assertEqual(a.root_table_id, b.root_table_id)
        self.assertEqual(a.probabilities(), b.probabilities())

    def test_bad_dimension_rejected(self):
        state = uniform_selector()
        with self.assertRaises(ValueError):
            ContinuationSelector(state.roots[:-1], state.amplitudes[:-1])

    def test_non_normalized_state_rejected(self):
        state = uniform_selector()
        amps = list(state.amplitudes)
        amps[0] = complex(2 / sqrt(DIMENSION), 0)
        with self.assertRaises(ValueError):
            ContinuationSelector(state.roots, tuple(amps))


if __name__ == "__main__":
    unittest.main()
