#!/usr/bin/env python3
from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "analysis"))

import w33_temporal_merkle_gc as gc  # noqa: E402
import w33_async_schedule_replay as replay  # noqa: E402


class W33TemporalStorageReplayTests(unittest.TestCase):
    def test_gc_respects_strong_roots_but_not_hash_only_receipts(self):
        p = gc.verify()
        self.assertEqual(p["status"], "PASS")
        self.assertTrue(p["checks"]["strong_checkpoint_protects_old_snapshot"])
        self.assertTrue(p["checks"]["hash_only_receipt_does_not_prevent_sweep"])
        self.assertTrue(p["checks"]["live_root_survives_old_checkpoint_release"])
        self.assertTrue(p["checks"]["final_release_leaves_only_empty_reachable"])

    def test_async_schedule_is_replay_evidence(self):
        p = replay.verify()
        self.assertEqual(p["status"], "PASS")
        self.assertTrue(p["checks"]["fresh_runtime_replays_exact_schedule_root"])
        self.assertTrue(p["checks"]["canonical_schedule_delivers_two_messages"])
        self.assertTrue(p["checks"]["wake_order_is_committed"])
        self.assertTrue(p["checks"]["wrong_wake_order_changes_liveness_state"])


if __name__ == "__main__":
    unittest.main()
