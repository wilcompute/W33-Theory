#!/usr/bin/env python3
from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "analysis"))

import w33_capability_epoch_revocation as revocation  # noqa: E402
import w33_async_deadlock_detector as deadlock  # noqa: E402


class W33FailureControlPlaneTests(unittest.TestCase):
    def test_selective_revocation_and_epoch_rotation(self):
        p = revocation.verify()
        self.assertEqual(p["status"], "PASS")
        self.assertTrue(p["checks"]["ancestor_revocation_kills_descendant"])
        self.assertTrue(p["checks"]["unrelated_sibling_survives_selective_revocation"])
        self.assertTrue(p["checks"]["epoch_rotation_invalidates_all_old_tokens"])
        self.assertTrue(p["checks"]["revocation_layer_does_not_enable_rights_escalation"])

    def test_async_deadlock_is_detected_and_breakable_only_with_authority(self):
        p = deadlock.verify()
        self.assertEqual(p["status"], "PASS")
        self.assertTrue(p["checks"]["three_component_cycle_detected"])
        self.assertTrue(p["checks"]["unauthorized_cancellation_blocked"])
        self.assertTrue(p["checks"]["narrow_capability_breaks_cycle"])
        self.assertTrue(p["checks"]["ordinary_wait_chain_not_deadlock"])


if __name__ == "__main__":
    unittest.main()
