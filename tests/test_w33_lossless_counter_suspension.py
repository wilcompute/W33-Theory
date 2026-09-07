"""Recovery, garbage collection, malformed archives and retention admission."""
from copy import deepcopy
from dataclasses import replace
from pathlib import Path
import json
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "analysis"))
from w33_authenticated_counter_machine import BitStore, genesis, prove_step, verify_step
from w33_finite_control_unbounded_guest_hypervisor import FibreProductAddress
from w33_lossless_counter_suspension import (
    KIND, SuspensionHandle, checkpoint_retention_audit, resume, suspend,
)
from w33_merkle_capability_memory import ContentStore, digest
from w33_temporal_merkle_gc import RootRegistry, TemporalMerkleGC
from w33_typed_universal_microvm import Carrier, add_r1_into_r0_program


class SuspensionTests(unittest.TestCase):
    def setUp(self):
        self.program = add_r1_into_r0_program()
        self.memory = BitStore()
        self.state = genesis(self.program, self.memory, (7, 11), session="suspend-test")
        self.address = FibreProductAddress(17, 2, 5)
        self.archive, self.registry = ContentStore(), RootRegistry()

    def save(self, **kwargs):
        return suspend("guest", self.state, self.address, self.memory,
                       self.archive, self.registry, **kwargs)

    def restore(self, handle, **kwargs):
        return resume(handle, handle.root, self.archive, self.registry, **kwargs)

    def test_resume_and_execute_after_worker_memory_is_discarded(self):
        for carrier in Carrier:
            self.state = replace(self.state, carrier=carrier.value)
            for _ in range(7):
                receipt = prove_step(self.program, self.state, self.memory)
                self.state, _ = verify_step(self.program, self.state, receipt)
            handle = self.save()
            self.memory.nodes.clear()
            TemporalMerkleGC(self.archive, self.registry).collect()
            state, address, memory = self.restore(handle)
            self.assertEqual((state, address), (self.state, self.address))
            for _ in range(100):
                if state.halted:
                    break
                receipt = prove_step(self.program, state, memory)
                state, _ = verify_step(self.program, state, receipt)
            self.assertTrue(state.halted)
            self.assertEqual(tuple(memory.decode(r) for r in state.roots), (18, 0))
            self.memory = BitStore()
            self.state = genesis(self.program, self.memory, (7, 11), session="suspend-test")

    def test_all_fibre_addresses_survive_and_base_only_is_not_injective(self):
        live_projection_buckets = {}
        handles = set()
        for packed in range(1296):
            self.address = FibreProductAddress.unpack(packed)
            handle = self.save()
            _, restored, _ = self.restore(handle)
            self.assertEqual(restored.packed, packed)
            handles.add(handle.root)
            live_projection_buckets.setdefault(restored.circuit216, set()).add(restored.pair_tag)
        self.assertEqual(len(handles), 1296)
        self.assertEqual(len(live_projection_buckets), 216)
        self.assertEqual({len(x) for x in live_projection_buckets.values()}, {6})

    def test_audit_hash_survives_but_cannot_resume_after_collection(self):
        handle = self.save()
        self.registry.pin("RECEIPT", "guest", handle.root, "HASH_ONLY")
        self.registry.release(handle.reference_id)
        TemporalMerkleGC(self.archive, self.registry).collect()
        self.assertIn(handle.root, self.registry.audit_roots())
        self.assertNotIn(handle.root, self.archive.blobs)
        with self.assertRaises(PermissionError):
            self.restore(handle)

    def test_archive_json_round_trip_is_idempotent(self):
        handle = self.save()
        self.archive.blobs = json.loads(json.dumps(self.archive.blobs))
        self.assertEqual(self.restore(handle)[:2], (self.state, self.address))
        self.assertEqual(self.save(), handle)

    def test_frozen_recovery_certificate_reproduces(self):
        from w33_lossless_counter_suspension import verify
        path = Path(__file__).resolve().parents[1] / "analysis" / "w33_lossless_counter_suspension_certificate.json"
        self.assertEqual(verify(), json.loads(path.read_text()))

    def test_wrong_root_corruption_and_budget_fail_without_registry_changes(self):
        before = (deepcopy(self.archive.blobs), dict(self.registry.references))
        with self.assertRaises(TimeoutError):
            self.save(max_nodes=0)
        self.assertEqual((self.archive.blobs, self.registry.references), before)
        handle = self.save()
        with self.assertRaises(ValueError):
            resume(handle, digest("different snapshot"), self.archive, self.registry)
        with self.assertRaises(TimeoutError):
            self.restore(handle, max_nodes=0)
        self.archive.blobs[handle.root]["fibre"]["pair_tag"] = 0
        with self.assertRaises(ValueError):
            self.restore(handle)

    def test_structural_validation_even_for_a_trusted_content_hash(self):
        handle = self.save()
        original = deepcopy(self.archive.get(handle.root))
        malformed = []
        row = deepcopy(original); row["fibre"]["pair_tag"] = True; malformed.append(row)
        row = deepcopy(original); row["state"]["roots"] = "bad"; malformed.append(row)
        row = deepcopy(original); row["nodes"].pop(); malformed.append(row)
        row = deepcopy(original); row["nodes"].append(row["nodes"][0]); malformed.append(row)
        row = deepcopy(original); row["nodes"][0]["bit"] = True; malformed.append(row)
        for row in malformed:
            root = self.archive.put(row)
            ref = self.registry.pin(KIND, "malformed", root, "STRONG")
            with self.assertRaises((ValueError, KeyError)):
                self.restore(SuspensionHandle(ref.reference_id, root))

    def test_ladder_overflow_does_not_satisfy_strong_retention_demand(self):
        from w33_ladder_checkpoint_placement import LadderCheckpointPlacer
        # Use real feasible scheduler frontier objects, not synthetic assignments.
        from w33_adaptive_reversible_scheduler import AdaptiveReversibleScheduler
        plans = [LadderCheckpointPlacer().place(p)
                 for p in AdaptiveReversibleScheduler(4096, address_depth=5).frontier]
        self.assertTrue(any(p.strong_checkpoints > 10 for p in plans))
        for plan in plans:
            audit = checkpoint_retention_audit(plan)
            self.assertEqual(audit["retention_demand_met"], plan.strong_checkpoints <= 10)
            self.assertFalse(audit["runtime_dispatch_certified"])


if __name__ == "__main__":
    unittest.main()
