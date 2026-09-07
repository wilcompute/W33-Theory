"""Executable tests for the content-addressed HoloVM process kernel."""
from copy import deepcopy
import json
from pathlib import Path
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "analysis"))

import w33_holovm_process_kernel as kernel
from w33_authenticated_counter_machine import BitStore, genesis
from w33_finite_control_unbounded_guest_hypervisor import FibreProductAddress
from w33_merkle_capability_memory import ContentStore, digest
from w33_temporal_merkle_gc import RootRegistry
from w33_typed_universal_microvm import add_r1_into_r0_program


class HoloVMProcessKernelTests(unittest.TestCase):
    def setUp(self):
        self.program = add_r1_into_r0_program()
        self.memory = BitStore()
        self.state = genesis(
            self.program, self.memory, (255, 0), session="process-test"
        )
        self.fibre = FibreProductAddress(7, 2, 5)
        self.passport = digest({"passport": "test", "image": self.program.image_id})
        self.root = kernel.spawn(self.state, self.fibre, self.passport)
        self.left = kernel.fork(self.root, "left")
        self.right = kernel.fork(self.root, "right")

    def test_full_certificate(self):
        result = kernel.verify()
        self.assertEqual(result["status"], "PASS")
        self.assertTrue(all(result["checks"].values()))

    def test_value_identity_and_process_identity_are_separate(self):
        a = kernel.prepare_process(self.left, self.memory)
        b = kernel.prepare_process(self.right, self.memory)
        self.assertEqual(a.snapshot_root, b.snapshot_root)
        self.assertNotEqual(a.root, b.root)
        self.assertNotEqual(self.left.process_id, self.right.process_id)
        self.assertEqual(self.left.state, self.right.state)

    def test_step_is_deterministic_and_preserves_process_id(self):
        first, receipt = kernel.advance(self.program, self.left, self.memory)
        replay_store = BitStore(self.memory.nodes.values())
        second, receipt2 = kernel.advance(self.program, self.left, replay_store)
        self.assertEqual(first, second)
        self.assertEqual(receipt.receipt_id, receipt2.receipt_id)
        self.assertEqual(first.process_id, self.left.process_id)
        self.assertEqual(first.parent, self.left.continuation_id)
        self.assertLessEqual(len(receipt.route) - 1, 2)

    def test_process_root_transitively_pins_shared_snapshot(self):
        archive, registry = ContentStore(), RootRegistry()
        proposal = kernel.prepare_process(self.left, self.memory)
        handle = kernel.install(
            "left", proposal, archive, registry, max_payload_bytes=10**9
        )
        process, memory = kernel.resume_process(
            handle, handle.root, archive, registry
        )
        self.assertEqual(process, self.left)
        self.assertEqual(memory.decode(process.state.roots[0]), 255)
        self.assertIn(proposal.snapshot_root, archive.blobs)

    def test_budget_failure_is_atomic(self):
        archive, registry = ContentStore(), RootRegistry()
        proposal = kernel.prepare_process(self.left, self.memory)
        before = (deepcopy(archive.blobs), dict(registry.references))
        with self.assertRaises(MemoryError):
            kernel.install(
                "left", proposal, archive, registry, max_payload_bytes=0
            )
        self.assertEqual(archive.blobs, before[0])
        self.assertEqual(registry.references, before[1])

    def test_corrupt_outer_descriptor_fails_closed(self):
        archive, registry = ContentStore(), RootRegistry()
        proposal = kernel.prepare_process(self.left, self.memory)
        blobs = list(proposal.blobs)
        root_index = next(i for i, (key, _) in enumerate(blobs) if key == proposal.root)
        key, wire = blobs[root_index]
        row = json.loads(wire)
        row["value"]["process"]["branch"] = "forged"
        blobs[root_index] = (
            key, json.dumps(row, sort_keys=True, separators=(",", ":"))
        )
        forged = kernel.PreparedProcess(
            proposal.root, proposal.snapshot_root, tuple(blobs)
        )
        with self.assertRaises(ValueError):
            kernel.install(
                "left", forged, archive, registry, max_payload_bytes=10**9
            )
        self.assertEqual(registry.references, {})

    def test_same_process_root_can_have_multiple_retention_owners(self):
        archive, registry = ContentStore(), RootRegistry()
        proposal = kernel.prepare_process(self.left, self.memory)
        one = kernel.install(
            "owner-a", proposal, archive, registry, max_payload_bytes=10**9
        )
        two = kernel.install(
            "owner-b", proposal, archive, registry, max_payload_bytes=10**9
        )
        self.assertNotEqual(one.reference_id, two.reference_id)
        self.assertEqual(one.root, two.root)
        registry.release(one.reference_id)
        process, _ = kernel.resume_process(two, two.root, archive, registry)
        self.assertEqual(process, self.left)


if __name__ == "__main__":
    unittest.main()
