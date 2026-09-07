"""Exact admission, independent recovery, stale quotes and deep shared GC."""
from copy import deepcopy
from dataclasses import replace
import json
from pathlib import Path
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "analysis"))
import w33_shared_counter_archive as shared
from w33_authenticated_counter_machine import BitStore, genesis, prove_step, verify_step
from w33_finite_control_unbounded_guest_hypervisor import FibreProductAddress
from w33_merkle_capability_memory import ContentStore, canonical_json
from w33_temporal_merkle_gc import RootRegistry, TemporalMerkleGC
from w33_typed_universal_microvm import Carrier, add_r1_into_r0_program


class SharedArchiveTests(unittest.TestCase):
    def test_frozen_population_and_exact_marginal_costs(self):
        expected = json.loads((Path(__file__).resolve().parents[1] / "analysis" /
                               "w33_shared_counter_archive_certificate.json").read_text())
        self.assertEqual(shared.verify(), expected)
        self.assertEqual(expected["status"], "PASS")

    def setUp(self):
        self.program = add_r1_into_r0_program()
        self.memory, self.archive, self.registry = BitStore(), ContentStore(), RootRegistry()
        self.state = genesis(self.program, self.memory, (7, 11), session="shared-archive-test")
        self.fibre = FibreProductAddress(5, 3, 4)

    def proposal(self, state=None, fibre=None):
        return shared.prepare(state or self.state, fibre or self.fibre, self.memory)

    def publish(self, proposal, owner="g", budget=10**9):
        return shared.publish(owner, proposal, self.archive, self.registry, max_payload_bytes=budget)

    def restore(self, handle):
        return shared.resume(handle, handle.root, self.archive, self.registry)

    def test_exact_budget_rejection_is_atomic_and_boundary_admits(self):
        p = self.proposal()
        q = shared.quote(p, self.archive, self.registry)
        before = (deepcopy(self.archive.blobs), dict(self.registry.references))
        with self.assertRaises(MemoryError):
            self.publish(p, budget=q["prospective_payload_bytes"] - 1)
        self.assertEqual((self.archive.blobs, self.registry.references), before)
        h = self.publish(p, budget=q["prospective_payload_bytes"])
        self.assertEqual(sum(len(canonical_json(r)) for r in self.archive.blobs.values()),
                         q["prospective_payload_bytes"])
        self.assertEqual(self.restore(h)[:2], (self.state, self.fibre))

    def test_forks_share_data_but_releasing_one_preserves_the_other(self):
        a = self.publish(self.proposal(), "a")
        other = replace(self.state, carrier=Carrier.PAIR_ST64.value)
        p = self.proposal(other, FibreProductAddress(5, 3, 1))
        q = shared.quote(p, self.archive, self.registry)
        self.assertEqual(q["prospective_blobs"], len(self.archive.blobs) + 1)
        b = self.publish(p, "b")
        self.registry.pin("AUDIT", "a", a.root, "HASH_ONLY")
        self.registry.release(a.reference_id)
        TemporalMerkleGC(self.archive, self.registry).collect()
        self.assertNotIn(a.root, self.archive.blobs)
        self.memory.nodes.clear()
        state, fibre, memory = self.restore(b)
        self.assertEqual((state, fibre), (other, FibreProductAddress(5, 3, 1)))
        while not state.halted:
            receipt = prove_step(self.program, state, memory)
            state, _ = verify_step(self.program, state, receipt)
        self.assertEqual([memory.decode(r) for r in state.roots], [18, 0])
        with self.assertRaises(PermissionError):
            self.restore(a)
        self.registry.release(b.reference_id)
        TemporalMerkleGC(self.archive, self.registry).collect()
        self.assertEqual(set(self.archive.blobs), {self.archive.empty})

    def test_stale_quote_cannot_overcommit_after_another_guest_is_pinned(self):
        a = self.proposal()
        b = self.proposal(fibre=FibreProductAddress(5, 3, 2))
        stale = shared.quote(b, self.archive, self.registry)
        self.publish(a, "a")
        before = (deepcopy(self.archive.blobs), dict(self.registry.references))
        with self.assertRaises(MemoryError):
            self.publish(b, "b", stale["prospective_payload_bytes"])
        self.assertEqual((self.archive.blobs, self.registry.references), before)

    def test_deep_shared_chain_gc_resume_and_missing_child_fail_before_sweep(self):
        self.state = genesis(self.program, self.memory, ((1 << 4096) - 1, 0), session="deep")
        h = self.publish(self.proposal())
        TemporalMerkleGC(self.archive, self.registry).collect()
        state, _, memory = self.restore(h)
        self.assertEqual(memory.decode(state.roots[0]), (1 << 4096) - 1)
        child = self.archive.blobs[h.root]["children"][0][1]
        self.archive.blobs.pop(child)
        before = deepcopy(self.archive.blobs)
        with self.assertRaises(KeyError):
            TemporalMerkleGC(self.archive, self.registry).collect()
        self.assertEqual(self.archive.blobs, before)

    def test_serialized_proposal_and_archive_preserve_identity(self):
        p = self.proposal()
        h = self.publish(p)
        self.archive.blobs = json.loads(json.dumps(self.archive.blobs))
        p2 = shared.PreparedSnapshot(p.root, tuple(tuple(x) for x in json.loads(json.dumps(p.blobs))))
        self.assertEqual(shared.quote(p2, self.archive, self.registry)["marginal_payload_bytes"], 0)
        self.assertEqual(self.publish(p2), h)
        self.assertEqual(self.restore(h)[:2], (self.state, self.fibre))

    def test_bad_proposals_corruption_and_limits_do_not_change_retention(self):
        p = self.proposal()
        malformed = [shared.PreparedSnapshot(p.root, p.blobs + (p.blobs[0],)),
                     shared.PreparedSnapshot(p.root, p.blobs[:-1]),
                     shared.PreparedSnapshot(p.root, ((p.blobs[0][0], '{}'),) + p.blobs[1:])]
        for bad in malformed:
            before = (deepcopy(self.archive.blobs), dict(self.registry.references))
            with self.assertRaises((KeyError, ValueError)):
                self.publish(bad)
            self.assertEqual((self.archive.blobs, self.registry.references), before)
        with self.assertRaises(TimeoutError):
            shared.prepare(self.state, self.fibre, self.memory, max_nodes=0)
        h = self.publish(p)
        with self.assertRaises(ValueError):
            shared.resume(h, self.archive.empty, self.archive, self.registry)
        self.archive.blobs[h.root]["value"]["fibre"]["pair_tag"] = 0
        with self.assertRaises(ValueError):
            self.restore(h)

    def test_existing_foreign_strong_root_is_included_in_budget(self):
        foreign = self.archive.put({"kind": "opaque-existing-resource", "data": "x" * 10000})
        self.registry.pin("LIVE_VM", "foreign", foreign)
        p = self.proposal()
        q = shared.quote(p, self.archive, self.registry)
        self.assertGreater(q["current_payload_bytes"], 10000)
        h = self.publish(p, budget=q["prospective_payload_bytes"])
        self.assertIn(foreign, self.archive.blobs)
        self.assertEqual(self.restore(h)[0], self.state)


if __name__ == "__main__":
    unittest.main()
