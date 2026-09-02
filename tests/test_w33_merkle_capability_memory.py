#!/usr/bin/env python3
from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "analysis"))

import w33_merkle_capability_memory as m  # noqa: E402
from w33_typed_universal_microvm import Carrier  # noqa: E402


class W33MerkleCapabilityMemoryTests(unittest.TestCase):
    def test_frozen_verifier(self):
        payload = m.verify()
        self.assertEqual(payload["status"], "PASS")
        self.assertTrue(all(payload["checks"].values()))

    def test_persistent_copy_on_write(self):
        store = m.ContentStore()
        cap = m.MemoryCapability(Carrier.CIRCUIT_ST81)
        a = m.PersistentMemory.empty(store, Carrier.CIRCUIT_ST81)
        b = a.write(cap, (1, 2, 3), "x")
        self.assertIsNone(a.read(cap, (1, 2, 3)))
        self.assertEqual(b.read(cap, (1, 2, 3)), "x")
        self.assertNotEqual(a.root, b.root)

    def test_rights_are_monotone_and_prefix_scoped(self):
        cap = m.MemoryCapability(Carrier.CIRCUIT_ST81)
        read_only = cap.derive((7, 8), {"read"})
        self.assertTrue(read_only.authorizes((7, 8, 9), "read"))
        self.assertFalse(read_only.authorizes((7, 9, 9), "read"))
        self.assertFalse(read_only.authorizes((7, 8, 9), "write"))
        with self.assertRaises(PermissionError):
            read_only.derive((9,), {"write"})

    def test_carrier_cannot_cross_memory_type(self):
        store = m.ContentStore()
        mem = m.PersistentMemory.empty(store, Carrier.CIRCUIT_ST81)
        wrong = m.MemoryCapability(Carrier.PAIR_ST64)
        with self.assertRaises(PermissionError):
            mem.read(wrong, (1,))

    def test_cartesian_w33_route_is_bounded_by_2d(self):
        source = (0, 1, 2, 3, 4)
        target = (39, 38, 37, 36, 35)
        events = m.route_address(source, target)
        self.assertLessEqual(len(events), 2 * len(source))
        self.assertEqual(tuple(events[-1]["to"]), target)


if __name__ == "__main__":
    unittest.main()
