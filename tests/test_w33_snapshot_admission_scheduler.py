"""Joint admission against materialized archives, stale input and failure paths."""
from copy import deepcopy
from dataclasses import replace
from itertools import combinations
import json
from pathlib import Path
import sys
import unittest
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "analysis"))
import w33_snapshot_admission_scheduler as scheduler
from w33_authenticated_counter_machine import BitStore, genesis
from w33_finite_control_unbounded_guest_hypervisor import FibreProductAddress
from w33_merkle_capability_memory import ContentStore, canonical_json
from w33_shared_counter_archive import PreparedSnapshot, prepare, publish, resume
from w33_temporal_merkle_gc import RootRegistry, TemporalMerkleGC
from w33_typed_universal_microvm import add_r1_into_r0_program


class AdmissionTests(unittest.TestCase):
    def setUp(self):
        self.requests = scheduler.witness_requests()
        self.archive, self.registry = ContentStore(), RootRegistry()
        self.budget = 3850

    def plan(self, requests=None, budget=None):
        return scheduler.plan(self.requests if requests is None else requests,
                              self.archive, self.registry,
                              max_payload_bytes=self.budget if budget is None else budget)

    def admit(self, p, requests=None, budget=None):
        return scheduler.admit(p, self.requests if requests is None else requests,
                               self.archive, self.registry,
                               max_payload_bytes=self.budget if budget is None else budget)

    def before(self):
        return deepcopy(self.archive.blobs), dict(self.registry.references)

    def test_frozen_witness(self):
        certificate = Path(__file__).resolve().parents[1] / "analysis" / "w33_snapshot_admission_certificate.json"
        self.assertEqual(scheduler.verify(), json.loads(certificate.read_text()))

    def test_joint_optimum_and_input_order_are_deterministic(self):
        p = self.plan()
        self.assertEqual((p.selected, p.utility, p.payload_bytes), (("254", "255"), 2, 3850))
        self.assertEqual(p, self.plan(list(reversed(self.requests))))
        handles = self.admit(p)
        TemporalMerkleGC(self.archive, self.registry).collect()
        for key, handle in handles.items():
            state, _, memory = resume(handle, handle.root, self.archive, self.registry)
            self.assertEqual(memory.decode(state.roots[0]), int(key))
        self.assertNotIn(self.requests[0].snapshot.root, self.archive.blobs)

    def test_exact_costs_match_independent_materialized_subset_oracle(self):
        # Actual publication and GC price each subset; no scheduler cost helper.
        memory, program = BitStore(), add_r1_into_r0_program()
        extra = tuple(scheduler.Request(str(n), n % 3 + 1, prepare(
            genesis(program, memory, (n, 0), session="oracle"),
            FibreProductAddress(1, 2, 3), memory)) for n in (7, 8))
        requests = tuple(sorted(self.requests + extra, key=lambda r: r.request_id))
        foreign = self.archive.put({"kind": "foreign-live", "bytes": "x" * 73})
        self.registry.pin("LIVE_VM", "outside", foreign)
        self.archive.put({"kind": "unretained-garbage", "bytes": "z" * 1000})
        oracle = []
        for count in range(len(requests) + 1):
            for group in combinations(requests, count):
                a, r = ContentStore(), RootRegistry()
                a.blobs = deepcopy(self.archive.blobs)
                r.references = dict(self.registry.references)
                for request in group:
                    publish(request.request_id, request.snapshot, a, r, max_payload_bytes=10**9)
                TemporalMerkleGC(a, r).collect()
                cost = sum(len(canonical_json(row)) for row in a.blobs.values())
                oracle.append((-sum(x.utility for x in group), cost,
                               tuple(x.request_id for x in group)))
        for budget in sorted({row[1] for row in oracle}):
            best = min(row for row in oracle if row[1] <= budget)
            p = self.plan(requests, budget)
            self.assertEqual((-p.utility, p.payload_bytes, p.selected), best)
            self.assertEqual(p.subsets_examined, 32)

    def test_utility_and_ties_have_explicit_meaning(self):
        requests = (replace(self.requests[0], utility=3),) + self.requests[1:]
        self.assertEqual(self.plan(requests).selected, ("128",))
        self.assertEqual(self.plan(budget=2821).selected, ("128",))
        zeros = tuple(replace(r, utility=0) for r in self.requests)
        p = self.plan(zeros)
        self.assertEqual((p.selected, p.utility), ((), 0))
        before = self.before()
        self.assertEqual(self.admit(p, zeros), {})
        self.assertEqual(self.before(), before)

    def test_stale_registry_and_altered_plan_reject_without_changes(self):
        p = self.plan()
        for altered in (replace(p, selected=("128",)), replace(p, utility=999),
                        replace(p, payload_bytes=0), replace(p, problem_root="forged")):
            before = self.before()
            with self.assertRaises(ValueError):
                self.admit(altered)
            self.assertEqual(self.before(), before)
        # Even a HASH_ONLY change invalidates the registry binding; it costs no
        # payload but changes the plan's audited context.
        self.registry.pin("AUDIT", "outside", self.archive.empty, "HASH_ONLY")
        before = self.before()
        with self.assertRaises(ValueError):
            self.admit(p)
        self.assertEqual(self.before(), before)

    def test_changed_request_or_external_budget_cannot_reuse_a_plan(self):
        p = self.plan()
        changed = (replace(self.requests[0], utility=9),) + self.requests[1:]
        with self.assertRaises(ValueError):
            self.admit(p, changed)
        with self.assertRaises(ValueError):
            self.admit(p, budget=3851)
        self.assertEqual(self.registry.references, {})

    def test_corruption_and_malformed_excluded_request_fail_closed(self):
        first = self.requests[0]
        broken = replace(first, utility=0, snapshot=PreparedSnapshot(
            first.snapshot.root, first.snapshot.blobs[:-1]))
        before = self.before()
        with self.assertRaises((KeyError, ValueError)):
            self.plan((broken,) + self.requests[1:])
        self.assertEqual(self.before(), before)
        self.archive.blobs[self.archive.empty]["value"] = "corrupt"
        with self.assertRaises(ValueError):
            self.plan()

    def test_staging_failure_never_partially_admits_the_batch(self):
        p = self.plan()
        before = self.before()
        calls = []
        def fail_second(*args, **kwargs):
            calls.append(args[0])
            if len(calls) == 2:
                raise OSError("injected staging failure")
            return publish(*args, **kwargs)
        with patch.object(scheduler, "publish", side_effect=fail_second):
            with self.assertRaises(OSError):
                self.admit(p)
        self.assertEqual(calls, ["254", "255"])
        self.assertEqual(self.before(), before)

    def test_mandatory_roots_over_budget_are_never_evicted(self):
        root = self.archive.put({"kind": "foreign-live", "bytes": "x" * 5000})
        self.registry.pin("LIVE_VM", "outside", root)
        before = self.before()
        p = self.plan()
        self.assertFalse(p.feasible)
        self.assertEqual(p.feasible_subsets, 0)
        with self.assertRaises(MemoryError):
            self.admit(p)
        self.assertEqual(self.before(), before)

    def test_limits_duplicates_empty_requests_and_shared_roots(self):
        with self.assertRaises(ValueError):
            self.plan([self.requests[0]] * 2)
        for utility in (-1, True, 1.5):
            with self.assertRaises(ValueError):
                self.plan([replace(self.requests[0], utility=utility)])
        clones = [replace(self.requests[0], request_id=f"fork{i:02d}") for i in range(17)]
        with self.assertRaises(ValueError):
            self.plan(clones)
        # Identical roots may be distinct caller-designated fork requests;
        # no per-reference overhead is included in the payload metric.
        p = self.plan(clones[:16], budget=2821)
        self.assertEqual((p.utility, p.payload_bytes, p.subsets_examined), (16, 2821, 65536))
        self.assertEqual(len(self.admit(p, clones[:16], budget=2821)), 16)
        empty = self.plan([], budget=2821)
        self.assertTrue(empty.feasible)
        self.assertEqual(empty.subsets_examined, 1)


if __name__ == "__main__":
    unittest.main()
