#!/usr/bin/env python3
from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "analysis"))

import w33_history_time_reversible_vm as r  # noqa: E402


class W33HistoryJournalVMTests(unittest.TestCase):
    def test_verifier(self):
        payload = r.verify()
        self.assertEqual(payload["status"], "PASS")
        self.assertTrue(all(payload["checks"].values()))

    def test_one_step_round_trip(self):
        vm = r.make_sample()
        before = r.state_fingerprint(vm)
        self.assertIsNotNone(vm.forward())
        vm.backward()
        self.assertEqual(r.state_fingerprint(vm), before)
        self.assertEqual(vm.time_index, 0)

    def test_full_round_trip(self):
        vm = r.make_sample()
        before = r.state_fingerprint(vm)
        vm.run_forward()
        self.assertEqual(vm.base.state.counters(), [18, 0])
        self.assertEqual(vm.time_index, 24)
        vm.uncompute_all()
        self.assertEqual(r.state_fingerprint(vm), before)
        self.assertEqual(vm.time_index, 0)

    def test_journal_clear_blocks_round_trip(self):
        vm = r.make_sample()
        for _ in range(3):
            vm.forward()
        row = vm.discard_history()
        self.assertEqual(row["records_discarded"], 3)
        with self.assertRaises(RuntimeError):
            vm.backward()


if __name__ == "__main__":
    unittest.main()
