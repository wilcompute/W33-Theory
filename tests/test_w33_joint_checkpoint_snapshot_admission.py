"""Regression tests for continuation-bound joint checkpoint/snapshot admission."""
from pathlib import Path
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "analysis"))

import w33_joint_checkpoint_snapshot_admission as joint
from w33_merkle_capability_memory import ContentStore, digest
from w33_snapshot_admission_scheduler import witness_requests
from w33_temporal_merkle_gc import RootRegistry


class JointCheckpointSnapshotAdmissionTests(unittest.TestCase):
    def test_frozen_verify_workload(self):
        out = joint.verify()
        self.assertEqual(out["status"], "PASS")
        self.assertTrue(all(out["checks"].values()))
        self.assertEqual(out["installed_snapshot_ids"], ["254", "255"])
        self.assertLessEqual(out["joint_plan"]["placement"]["peak_live_boundary"], 100)

    def test_continuation_and_policy_identity_are_committed(self):
        requests = witness_requests()
        process = digest({"test": "process"})
        c1 = digest({"test": "continuation-1"})
        c2 = digest({"test": "continuation-2"})
        # Large capacity keeps the identity test independent of a particular
        # frontier byte count.
        kw = dict(generation=3, steps=256, capacity_bytes=10**9)
        p1 = joint.plan_joint(requests, ContentStore(), RootRegistry(),
                              continuation_root=c1, process_id=process, **kw)
        p2 = joint.plan_joint(requests, ContentStore(), RootRegistry(),
                              continuation_root=c2, process_id=process, **kw)
        self.assertNotEqual(p1.problem_root, p2.problem_root)
        self.assertEqual(p1.strategy_digest, p2.strategy_digest)

    def test_no_joint_candidate_can_exceed_capacity(self):
        requests = witness_requests()
        p = joint.plan_joint(
            requests, ContentStore(), RootRegistry(),
            continuation_root=digest({"test": "continuation"}),
            process_id=digest({"test": "process"}),
            generation=0, steps=512, capacity_bytes=10**9,
        )
        self.assertLessEqual(p.combined_bytes, p.capacity_bytes)
        self.assertEqual(dict(p.strategy_descriptor)["logical_irreversible_erasures"], 0)


if __name__ == "__main__":
    unittest.main()
